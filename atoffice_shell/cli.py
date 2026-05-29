from __future__ import annotations

import shlex
import sys
import typer

from . import __version__
from .project import run_interactive_shell
from .pyfunny import joke, joke_trex
from .settings import launch_settings
from .todocli import addtask, completetask, deletetask, showtask, updatetask
from .chronoterm.shell import app as chronoterm_app

app = typer.Typer(name="atoffice-shell", help="AtOffice Shell: jokes, todos, time, and more.")

def app_with_lower() -> None:
    """Entry point that normalizes command name to lowercase for case-insensitive invocation."""
    # Normalize the command name to lowercase for case-insensitive behavior
    if len(sys.argv) > 0:
        sys.argv[0] = sys.argv[0].lower()
    # Invoke the main Typer app
    app()

def _invoke_chronoterm_command(command: str) -> None:
    try:
        chronoterm_app(shlex.split(command))
    except SystemExit:
        return
    except Exception as error:
        typer.secho(f"Error running ChronoTerm command: {error}", fg=typer.colors.RED)


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context) -> None:
    """Launch the AtOffice Shell interactive REPL when no command is provided."""
    if ctx.invoked_subcommand is None:
        run_interactive_shell()


@app.command("version")
def version() -> None:
    """Show the installed AtOffice Shell version."""
    typer.echo(__version__)


@app.command("joke")
def cli_joke() -> None:
    """Tell a random joke with ASCII art."""
    typer.echo(joke())


@app.command("joke-trex")
def cli_joke_trex() -> None:
    """Tell a T-Rex joke with sound."""
    typer.echo(joke_trex())


@app.command("addtask")
def cli_addtask(task: str, category: str) -> None:
    """Add a todo task."""
    addtask(task, category)


@app.command("deletetask")
def cli_deletetask(position: int) -> None:
    """Delete a todo task by position."""
    deletetask(position)


@app.command("updatetask")
def cli_updatetask(position: int, task: str | None = None, category: str | None = None) -> None:
    """Update the text or category of a todo task."""
    updatetask(position, task, category)


@app.command("completetask")
def cli_completetask(position: int) -> None:
    """Mark a todo task as complete."""
    completetask(position)


@app.command("showtasks")
def cli_showtasks() -> None:
    """Show all todo tasks."""
    showtask()


@app.command("settings")
def cli_settings() -> None:
    """Open the interactive settings manager."""
    launch_settings()


@app.command("now")
def cli_now() -> None:
    """Show the current local time."""
    _invoke_chronoterm_command("now")


@app.command("time")
def cli_time() -> None:
    """Show the current time in an ASCII clock."""
    _invoke_chronoterm_command("time")


@app.command("world")
def cli_world() -> None:
    """Show world time for favorite timezones."""
    _invoke_chronoterm_command("world")


@app.command("tz")
def cli_tz(action: str = typer.Argument("list", help="list | add | remove"), name: str | None = typer.Argument(None, help="IANA timezone name, e.g. Europe/London")) -> None:
    """Manage favorite timezones."""
    command = "tz"
    if name:
        command += f" {action} {name}"
    else:
        command += f" {action}"
    _invoke_chronoterm_command(command)


@app.command("alarm")
def cli_alarm(action: str = typer.Argument("list", help="list | add | remove"), time: str | None = typer.Argument(None, help="Time as HH:MM or YYYY-MM-DD HH:MM"), tz: str | None = typer.Option(None, "--tz", help="Timezone name"), label: str | None = typer.Option(None, "--label", help="Alarm label")) -> None:
    """Manage alarms."""
    command = "alarm " + action
    if time:
        command += f" {time}"
    if tz:
        command += f" --tz {tz}"
    if label:
        command += f" --label {label}"
    _invoke_chronoterm_command(command)


@app.command("sw")
def cli_sw(action: str = typer.Argument("show", help="start | pause | lap | reset | show")) -> None:
    """Control the stopwatch."""
    _invoke_chronoterm_command(f"sw {action}")
