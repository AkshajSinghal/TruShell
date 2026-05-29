import os
from types import SimpleNamespace

from typer.testing import CliRunner

from trushell.cli import app
from trushell.project import TruShellEditor, _handle_cd_command, _handle_edit_command, _handle_local_command, _handle_os_fallback


runner = CliRunner()


def test_version_command() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert "0.1.0" in result.stdout


def test_help_shows_usage() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.stdout


def test_unknown_command_uses_os_fallback(monkeypatch) -> None:
    calls = {}

    def fake_run(command: str, shell: bool, check: bool, cwd: str) -> SimpleNamespace:
        calls["command"] = command
        calls["shell"] = shell
        calls["check"] = check
        calls["cwd"] = cwd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr("trushell.project.subprocess.run", fake_run)

    assert _handle_os_fallback("pwd") is True
    assert calls == {"command": "pwd", "shell": True, "check": False, "cwd": os.getcwd()}


def test_cd_command_changes_directory_and_runs_ls(monkeypatch) -> None:
    calls = {}

    def fake_chdir(path: str) -> None:
        calls["chdir"] = path

    def fake_run(command: str, shell: bool, check: bool, cwd: str) -> SimpleNamespace:
        calls["ls_command"] = command
        calls["ls_shell"] = shell
        calls["ls_check"] = check
        calls["ls_cwd"] = cwd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr("trushell.project.os.chdir", fake_chdir)
    monkeypatch.setattr("trushell.project.subprocess.run", fake_run)

    assert _handle_cd_command("cd /tmp") is True
    assert calls == {"chdir": "/tmp", "ls_command": "ls", "ls_shell": True, "ls_check": False, "ls_cwd": os.getcwd()}


def test_cd_without_target_prints_syntax_hint(monkeypatch) -> None:
    calls = {}

    def fake_chdir(path: str) -> None:
        calls["chdir"] = path

    def fake_run(command: str, shell: bool, check: bool, cwd: str) -> SimpleNamespace:
        calls["ls_command"] = command
        calls["ls_cwd"] = cwd
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr("trushell.project.os.path.expanduser", lambda path: "/home/test")
    monkeypatch.setattr("trushell.project.os.chdir", fake_chdir)
    monkeypatch.setattr("trushell.project.subprocess.run", fake_run)

    assert _handle_cd_command("cd") is True
    assert calls == {}


def test_addtask_missing_arguments_is_blocked(monkeypatch) -> None:
    messages = []

    monkeypatch.setattr(
        "trushell.project.typer.secho",
        lambda message, fg=None: messages.append((message, fg)),
    )

    assert _handle_local_command("addtask", "") == "handled"


def test_edit_requires_filename(monkeypatch) -> None:
    messages = []

    monkeypatch.setattr(
        "trushell.project.typer.secho",
        lambda message, fg=None: messages.append((message, fg)),
    )

    assert _handle_edit_command("edit") is True
    assert messages and "Syntax: edit <filename>" in messages[0][0]


def test_edit_launches_editor_for_existing_file(monkeypatch, tmp_path) -> None:
    file_path = tmp_path / "note.txt"
    file_path.write_text("hello", encoding="utf-8")

    calls = {}

    class FakeEditor:
        def __init__(self, filename: str, initial_text: str) -> None:
            calls["filename"] = filename
            calls["initial_text"] = initial_text

        def run(self) -> None:
            calls["ran"] = True

    monkeypatch.setattr("trushell.project.TruShellEditor", FakeEditor)

    assert _handle_edit_command(f"edit {file_path}") is True
    assert calls == {"filename": str(file_path), "initial_text": "hello", "ran": True}


def test_trushell_editor_uses_initial_text_without_re_reading_file(tmp_path) -> None:
    file_path = tmp_path / "note.txt"
    file_path.write_text("from-disk", encoding="utf-8")

    editor = TruShellEditor(str(file_path), initial_text="from-arg")

    assert editor.file_content == "from-arg"


def test_action_save_file_notifies_on_permission_error(monkeypatch, tmp_path) -> None:
    file_path = tmp_path / "readonly.txt"
    editor = TruShellEditor(str(file_path), initial_text="draft")

    notifications = []

    class FakeTextArea:
        text = "draft"

    monkeypatch.setattr(editor, "query_one", lambda *_args, **_kwargs: FakeTextArea())
    monkeypatch.setattr(editor, "notify", lambda message, severity=None: notifications.append((message, severity)))

    def fail_open(*_args, **_kwargs):
        raise PermissionError("read-only")

    monkeypatch.setattr("builtins.open", fail_open)

    editor.action_save_file()

    assert notifications and "Failed to save file" in notifications[0][0]
