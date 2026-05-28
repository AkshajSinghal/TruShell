from __future__ import annotations

import os
import re
import shlex
import subprocess

import typer

from .pyfunny import joke, joke_trex
from .settings import launch_settings
from .todocli import addtask, delete_todo, update_todo, complete_todo, showtask
from .chronoterm.shell import app as chronoterm_app

HELP_TEXT = (
    "Available commands: joke, joke_trex, "
    "addtask, deletetask, updatetask, completetask, showtask, "
    "now, time, world, tz, alarm, sw, settings, exit, help"
)


def _prompt_command() -> tuple[str, str]:
    raw_command = typer.prompt("atoffice-shell").strip()
    normalized_command = raw_command.lower()
    return raw_command, normalized_command


def _handle_joke_command(command: str) -> bool:
    if command in {"joke", "joke_trex", "joke-trex"}:
        if command == "joke":
            typer.echo(joke())
        else:
            typer.echo(joke_trex())
        return True
    return False


def _handle_todo_command(command: str) -> bool:
    delete_match = re.match(r"deletetask\s+(\d+)", command)
    if delete_match:
        delete_todo(int(delete_match.group(1)))
        return True

    add_match = re.match(r'addtask\s+"([^"]+)"\s+"([^"]+)"', command)
    if add_match:
        addtask(add_match.group(1), add_match.group(2))
        return True

    update_match = re.match(r'updatetask\s+(\d+)\s+"([^"]+)"\s+"([^"]+)"', command)
    if update_match:
        update_todo(int(update_match.group(1)), update_match.group(2), update_match.group(3))
        return True

    complete_match = re.match(r'completetask\s+(\d+)', command)
    if complete_match:
        complete_todo(int(complete_match.group(1)))
        return True

    if command == "showtasks":
        showtask()
        return True

    return False


def _handle_local_command(command: str) -> str:
    if command in {"exit", "quit"}:
        return "exit"
    if _handle_joke_command(command):
        return "handled"
    if _handle_todo_command(command):
        return "handled"
    if command == "settings":
        launch_settings()
        return "handled"
    if command == "help":
        typer.echo(HELP_TEXT)
        return "handled"
    return "unhandled"


def _handle_chronoterm_command(raw_command: str, normalized_command: str) -> bool:
    if not re.match(r"^(now|time|world|tz|alarm|sw)\b", normalized_command):
        return False

    try:
        chronoterm_app(shlex.split(raw_command))
    except SystemExit:
        pass
    return True


def _handle_cd_command(raw_command: str) -> bool:
    """Handle cd natively so the shell's working directory changes permanently."""
    command = raw_command.strip()
    if not command.startswith("cd "):
        return False

    target_path = command[3:].strip() or "~"
    expanded_target = os.path.expanduser(target_path)

    try:
        os.chdir(expanded_target)
    except (FileNotFoundError, NotADirectoryError) as error:
        typer.secho(f"cd: {target_path}: {error}", fg=typer.colors.RED)
        return True
    except OSError as error:
        typer.secho(f"cd: {target_path}: {error}", fg=typer.colors.RED)
        return True

    try:
        subprocess.run("ls", shell=True, check=False)
    except OSError as error:
        typer.secho(f"ls fallback error: {error}", fg=typer.colors.RED)

    return True


def _handle_os_fallback(raw_command: str) -> bool:
    """Pass unrecognized commands to the host OS shell."""
    command = raw_command.strip()
    if not command:
        return False

    try:
        completed = subprocess.run(command, shell=True, check=False)
    except OSError as error:
        typer.secho(f"OS fallback error: {error}", fg=typer.colors.RED)
        return True

    if completed.returncode != 0:
        typer.secho(
            f"OS fallback returned exit code {completed.returncode}",
            fg=typer.colors.YELLOW,
        )
    return True


def run_interactive_shell() -> None:
    """Persistent REPL loop for the AtOffice shell core."""
    typer.secho("Entering AtOffice Shell. Type 'exit' to quit.", fg=typer.colors.CYAN)

    while True:
        try:
            raw_command, command = _prompt_command()
        except (KeyboardInterrupt, EOFError):
            typer.echo("")
            break

        local_result = _handle_local_command(command)
        if local_result == "exit":
            break
        if local_result == "handled":
            continue
        if _handle_chronoterm_command(raw_command, command):
            continue
        if _handle_cd_command(raw_command):
            continue
        if _handle_os_fallback(raw_command):
            continue

        typer.secho(f"Unknown command: {command}", fg=typer.colors.RED)
