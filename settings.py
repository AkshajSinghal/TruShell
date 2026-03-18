import os
import msvcrt
import typer

from chronoterm.state import StateStore


COMMANDS = [
    "joke",
    "joke_trex",
    "addtask",
    "deletetask",
    "updatetask",
    "completetask",
    "showtasks",
    "now",
    "time",
    "world",
    "tz",
    "alarm",
    "sw",
]

TIME_TEMPLATES = [
    ("lcd", "LCD Display"),
    ("wrist_watch", "Wrist Watch"),
    ("desktop", "Desktop Clock"),
]


def _clear_screen() -> None:
    os.system("cls")


def _select_from_menu(title: str, options: list[str]) -> str | None:
    index = 0

    while True:
        _clear_screen()
        typer.secho(f"? {title}", fg=typer.colors.CYAN)
        typer.secho("  Use arrow keys. Press Enter to select. Press Esc to go back.", fg=typer.colors.BRIGHT_BLACK)
        typer.echo("")

        for current_index, option in enumerate(options):
            prefix = ">" if current_index == index else " "
            color = typer.colors.GREEN if current_index == index else typer.colors.WHITE
            typer.secho(f"{prefix} {option}", fg=color)

        key = msvcrt.getwch()
        if key in ("\x00", "\xe0"):
            arrow = msvcrt.getwch()
            if arrow == "H":
                index = (index - 1) % len(options)
            elif arrow == "P":
                index = (index + 1) % len(options)
        elif key == "\r":
            return options[index]
        elif key == "\x1b":
            return None


def _command_settings(command_name: str) -> None:
    if command_name != "time":
        typer.secho(f"No editable settings are available yet for '{command_name}'.", fg=typer.colors.YELLOW)
        return

    selected_label = _select_from_menu(
        "Select a template for the time command:",
        [label for _, label in TIME_TEMPLATES],
    )
    if selected_label is None:
        typer.secho("Settings cancelled.", fg=typer.colors.YELLOW)
        return

    template_lookup = {label: key for key, label in TIME_TEMPLATES}
    store = StateStore()
    state = store.load()
    state.time_template = template_lookup[selected_label]
    store.save(state)

    typer.secho(f"Time template updated to {selected_label}.", fg=typer.colors.GREEN)


def launch_settings() -> None:
    selected_command = _select_from_menu("Select a command to configure:", COMMANDS)
    _clear_screen()

    if selected_command is None:
        typer.secho("Settings closed.", fg=typer.colors.YELLOW)
        return

    _command_settings(selected_command)
