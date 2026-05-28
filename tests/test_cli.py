import os
from types import SimpleNamespace

from typer.testing import CliRunner

from atoffice_shell.cli import app
from atoffice_shell.project import _handle_cd_command, _handle_local_command, _handle_os_fallback


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

    monkeypatch.setattr("atoffice_shell.project.subprocess.run", fake_run)

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

    monkeypatch.setattr("atoffice_shell.project.os.chdir", fake_chdir)
    monkeypatch.setattr("atoffice_shell.project.subprocess.run", fake_run)

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

    monkeypatch.setattr("atoffice_shell.project.os.path.expanduser", lambda path: "/home/test")
    monkeypatch.setattr("atoffice_shell.project.os.chdir", fake_chdir)
    monkeypatch.setattr("atoffice_shell.project.subprocess.run", fake_run)

    assert _handle_cd_command("cd") is True
    assert calls == {}


def test_addtask_missing_arguments_is_blocked(monkeypatch) -> None:
    messages = []

    monkeypatch.setattr(
        "atoffice_shell.project.typer.secho",
        lambda message, fg=None: messages.append((message, fg)),
    )

    assert _handle_local_command("addtask", "") == "handled"
    assert messages and "Missing arguments" in messages[0][0]
