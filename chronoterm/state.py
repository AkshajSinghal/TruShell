import json
import os
from datetime import datetime
from pathlib import Path

#CS50.DEV

def _app_state_dir():
    appdata = os.environ.get("APPDATA")
    if appdata:
        return Path(appdata) / "ChronoTerm"
    return Path.home() / ".chronoterm"


def default_state_path():
    return _app_state_dir() / "state.json"


class AppState:
    def __init__(self):
        self.timezones = []
        self.alarms = []
        self.time_template = "lcd"
        self.clock_format = "24h"
        self.joke_character = "cow"
        self.joke_sound = "cow-sound.mp3"
        self.version = 1
        self.updated_at_iso = None

    def touch(self):
        self.updated_at_iso = datetime.now().astimezone().isoformat(timespec="seconds")


class StateStore:
    def __init__(self, path=None):
        self.path = path or default_state_path()

    def _new_state(self):
        return AppState()

    def load(self):
        current_state = self._new_state()

        try:
            with open(self.path, "r", encoding="utf-8") as state_file:
                file_data = json.load(state_file)

            current_state.timezones = file_data.get("timezones", [])
            current_state.alarms = file_data.get("alarms", [])
            current_state.time_template = file_data.get("time_template", "lcd")
            current_state.clock_format = file_data.get("clock_format", "24h")
            current_state.joke_character = file_data.get("joke_character", "cow")
            current_state.joke_sound = file_data.get("joke_sound", "cow-sound.mp3")
            current_state.version = file_data.get("version", 1)
            current_state.updated_at_iso = file_data.get("updated_at_iso")
        except FileNotFoundError:
            return current_state
        except Exception:
            print("Error loading file")
            return current_state

        return current_state

    def save(self, state):
        state.touch()

        save_data = {}
        save_data["version"] = state.version
        save_data["updated_at_iso"] = state.updated_at_iso
        save_data["timezones"] = state.timezones
        save_data["alarms"] = state.alarms
        save_data["time_template"] = state.time_template
        save_data["clock_format"] = state.clock_format
        save_data["joke_character"] = state.joke_character
        save_data["joke_sound"] = state.joke_sound

        # I need the folder to exist first, or Python cannot create the file there.
        self.path.parent.mkdir(parents=True, exist_ok=True)

        # I write the whole JSON here so the newest settings stay on disk.
        with open(self.path, "w", encoding="utf-8") as state_file:
            json.dump(save_data, state_file, indent=2, ensure_ascii=False)
