# AtOffice Shell

AtOffice Shell is a polished open-source Python CLI that combines jokes, todos, alarms, world clocks, and a productivity-focused terminal shell.

# Hello!
## Key Features

- Unified CLI: `atoffice-shell` starts a single interactive shell for jokes, todos, and ChronoTerm.
- Todo manager: add, update, complete, and list tasks with an SQLite-backed store.
- ChronoTerm utilities: current time, world clock, timezones, alarms, and stopwatch.
- Configurable settings: change clock style, time template, joke character, and sound.
- Platform-safe storage: app data and state are stored in user-specific directories.
- UV-first install: `uv tool install git+https://github.com/AkshajSinghal/at-office-shell`

## Installation

### Install with uv

```bash
uv tool install git+https://github.com/AkshajSinghal/at-office-shell
```

### Install with pip

```bash
python -m pip install git+https://github.com/AkshajSinghal/at-office-shell
```

## Quick Start

```bash
atoffice-shell
```

Inside the app, try:

```text
joke
showtasks
addtask "Review PR" "Work"
time
world
settings
edit
```

## CLI Commands

- `atoffice-shell` — start the interactive shell
- `atoffice-shell version` — show the installed version
- `atoffice-shell joke` — tell a joke with ASCII art
- `atoffice-shell joke-trex` — tell a T-Rex joke
- `atoffice-shell addtask <task> <category>` — add a todo
- `atoffice-shell deletetask <position>` — delete a todo
- `atoffice-shell updatetask <position> [task] [category]` — update a todo
- `atoffice-shell completetask <position>` — mark a todo done
- `atoffice-shell showtasks` — list all todos
- `atoffice-shell settings` — configure clock and joke preferences
- `atoffice-shell now` — show the current local time
- `atoffice-shell time` — show ASCII clock output
- `atoffice-shell world` — show favorite world timezones
- `atoffice-shell tz list|add|remove` — manage saved zones
- `atoffice-shell alarm list|add|remove` — manage alarms
- `atoffice-shell sw show|start|pause|lap|reset` — control stopwatch

## Example Usage

```bash
atoffice-shell addtask "Finish README" "Documentation"
atoffice-shell showtasks
atoffice-shell tz add Europe/London
atoffice-shell alarm add "07:30" --label "Morning"
```

## Architecture Overview

The package is organized into a single installable Python package:

- `atoffice_shell/cli.py` — CLI entrypoint and command routing
- `atoffice_shell/project.py` — interactive shell logic
- `atoffice_shell/pyfunny.py` — joke commands and sound handling
- `atoffice_shell/todocli.py` — todo command implementations
- `atoffice_shell/database.py` — SQLite storage in the user data directory
- `atoffice_shell/settings.py` — platform-safe settings manager
- `atoffice_shell/chronoterm/` — time, timezone, alarm, and stopwatch features

## Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening an issue or pull request.

## Roadmap

- Add more sound and joke options
- Improve shell prompts and command history
- Add serialization tests for state and data storage
- Expand support for cross-platform audio playback

## License

Apache 2.0. See [LICENSE](LICENSE) for details.
