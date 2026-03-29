import os
import msvcrt
import typer
from pathlib import Path

from chronoterm.state import StateStore

#CS50.DEV

COMMANDS = [
    "joke",
    "time",
    "world",
]

TIME_TEMPLATES = [
    ("lcd", "LCD Display"),
    ("wrist_watch", "Wrist Watch"),
    ("desktop", "Desktop Clock"),
]

CLOCK_FORMATS = [
    ("24h", "24 Hour (Military)"),
    ("12h", "12 Hour (AM/PM)"),
]

JOKE_CHARACTERS = [
    "cow",
    "trex",
    "dragon",
    "tux",
    "kitty",
    "turkey",
    "stegosaurus",
    "ghostbusters",
    "pig",
    "daemon",
]


def _clear_screen():
    os.system("cls")


def _show_cancelled_message():
    typer.secho("Settings cancelled.", fg=typer.colors.YELLOW)


def _show_selection_screen(title, options, selected_index):
    _clear_screen()
    typer.secho(f"? {title}", fg=typer.colors.CYAN)
    typer.secho("  Use arrow keys. Press Enter to select. Press Esc to go back.", fg=typer.colors.BRIGHT_BLACK)
    typer.echo("")

    current_index = 0
    while current_index < len(options):
        current_option = options[current_index]
        prefix_text = " "
        color_name = typer.colors.WHITE

        if current_index == selected_index:
            prefix_text = ">"
            color_name = typer.colors.GREEN

        typer.secho(f"{prefix_text} {current_option}", fg=color_name)
        current_index = current_index + 1


def _read_menu_key(selected_index, option_count):
    key_pressed = msvcrt.getwch()

    if key_pressed in ("\x00", "\xe0"):
        arrow_key = msvcrt.getwch()
        if arrow_key == "H":
            selected_index = (selected_index - 1) % option_count
        elif arrow_key == "P":
            selected_index = (selected_index + 1) % option_count
        return selected_index, False, False

    if key_pressed == "\r":
        return selected_index, True, False

    if key_pressed == "\x1b":
        return selected_index, False, True

    return selected_index, False, False


def _select_from_menu(title, options):
    selected_index = 0

    while True:
        _show_selection_screen(title, options, selected_index)
        selected_index, did_submit, did_escape = _read_menu_key(selected_index, len(options))

        if did_submit:
            return options[selected_index]

        if did_escape:
            return None


def _build_template_labels():
    template_label_list = []
    current_index = 0

    while current_index < len(TIME_TEMPLATES):
        current_template = TIME_TEMPLATES[current_index]
        template_label_list.append(current_template[1])
        current_index = current_index + 1

    return template_label_list


def _build_clock_format_labels():
    clock_format_label_list = []
    current_index = 0

    while current_index < len(CLOCK_FORMATS):
        current_format = CLOCK_FORMATS[current_index]
        clock_format_label_list.append(current_format[1])
        current_index = current_index + 1

    return clock_format_label_list


def _find_template_key(selected_label):
    current_index = 0

    while current_index < len(TIME_TEMPLATES):
        current_template = TIME_TEMPLATES[current_index]
        template_key = current_template[0]
        template_label = current_template[1]
        if template_label == selected_label:
            return template_key
        current_index = current_index + 1

    return None


def _find_clock_format_key(selected_label):
    current_index = 0

    while current_index < len(CLOCK_FORMATS):
        current_format = CLOCK_FORMATS[current_index]
        format_key = current_format[0]
        format_label = current_format[1]
        if format_label == selected_label:
            return format_key
        current_index = current_index + 1

    return None


def _available_sound_files():
    sound_file_list = []
    sounds_folder = Path(__file__).resolve().parent / "chronoterm" / "sounds"

    if not sounds_folder.exists():
        return sound_file_list

    for current_path in sounds_folder.iterdir():
        if current_path.is_file():
            sound_file_list.append(current_path.name)

    sound_file_list.sort()
    return sound_file_list


def _edit_time_template():
    template_label_list = _build_template_labels()
    selected_label = _select_from_menu("Select a template for the time command:", template_label_list)

    if selected_label is None:
        _show_cancelled_message()
        return

    selected_template_key = _find_template_key(selected_label)
    if selected_template_key is None:
        typer.secho("That template could not be found.", fg=typer.colors.RED)
        return

    state_store = StateStore()
    current_state = state_store.load()
    current_state.time_template = selected_template_key

    # I need to save the file here so I don't lose the new template choice.
    state_store.save(current_state)
    typer.secho(f"Time template updated to {selected_label}.", fg=typer.colors.GREEN)


def _edit_clock_format(command_name):
    clock_format_label_list = _build_clock_format_labels()
    selected_label = _select_from_menu(
        f"Select a clock format for the {command_name} command:",
        clock_format_label_list,
    )

    if selected_label is None:
        _show_cancelled_message()
        return

    selected_format_key = _find_clock_format_key(selected_label)
    if selected_format_key is None:
        typer.secho("That clock format could not be found.", fg=typer.colors.RED)
        return

    state_store = StateStore()
    current_state = state_store.load()
    current_state.clock_format = selected_format_key

    # I save right after changing the format so the next command uses it.
    state_store.save(current_state)
    typer.secho(f"Clock format updated to {selected_label}.", fg=typer.colors.GREEN)


def _edit_time_settings():
    setting_choices = ["Template", "Clock Format"]
    selected_setting = _select_from_menu("Select a time setting to edit:", setting_choices)

    if selected_setting is None:
        _show_cancelled_message()
        return

    if selected_setting == "Template":
        _edit_time_template()
        return

    _edit_clock_format("time")


def _edit_joke_character():
    selected_character = _select_from_menu("Select a character for the joke command:", JOKE_CHARACTERS)

    if selected_character is None:
        _show_cancelled_message()
        return

    state_store = StateStore()
    current_state = state_store.load()
    current_state.joke_character = selected_character

    # I save here so the joke command can remember the new character later.
    state_store.save(current_state)
    typer.secho(f"Joke character updated to {selected_character}.", fg=typer.colors.GREEN)


def _edit_joke_sound():
    sound_file_list = _available_sound_files()

    if len(sound_file_list) == 0:
        typer.secho("No sound files were found in chronoterm/sounds.", fg=typer.colors.RED)
        return

    selected_sound = _select_from_menu("Select a sound for the joke command:", sound_file_list)

    if selected_sound is None:
        _show_cancelled_message()
        return

    state_store = StateStore()
    current_state = state_store.load()
    current_state.joke_sound = selected_sound

    # I save after picking the sound so the next joke uses the same file.
    state_store.save(current_state)
    typer.secho(f"Joke sound updated to {selected_sound}.", fg=typer.colors.GREEN)


def _edit_joke_settings():
    joke_setting_choices = ["Character", "Sound"]
    selected_setting = _select_from_menu("Select a joke setting to edit:", joke_setting_choices)

    if selected_setting is None:
        _show_cancelled_message()
        return

    if selected_setting == "Character":
        _edit_joke_character()
        return

    _edit_joke_sound()


def _command_settings(command_name):
    if command_name == "time":
        _edit_time_settings()
        return

    if command_name == "world":
        _edit_clock_format("world")
        return

    if command_name == "joke":
        _edit_joke_settings()
        return

    typer.secho(f"No editable settings are available yet for '{command_name}'.", fg=typer.colors.YELLOW)


def launch_settings():
    selected_command = _select_from_menu("Select a command to configure:", COMMANDS)
    _clear_screen()

    if selected_command is None:
        typer.secho("Settings closed.", fg=typer.colors.YELLOW)
        return

    _command_settings(selected_command)
