from types import SimpleNamespace

from typer.testing import CliRunner

from atoffice_shell.cli import app
from atoffice_shell.project import _handle_os_fallback


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

    def fake_run(command: str, shell: bool, check: bool) -> SimpleNamespace:
        calls["command"] = command
        calls["shell"] = shell
        calls["check"] = check
        return SimpleNamespace(returncode=0)

    monkeypatch.setattr("atoffice_shell.project.subprocess.run", fake_run)

    assert _handle_os_fallback("pwd") is True
    assert calls == {"command": "pwd", "shell": True, "check": False}
