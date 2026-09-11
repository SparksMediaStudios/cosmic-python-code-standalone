from tests import conftest


def test_prefers_docker_compose_binary(monkeypatch):
    monkeypatch.setattr(
        conftest.shutil,
        "which",
        lambda command: "/usr/bin/docker-compose" if command == "docker-compose" else None,
    )

    assert conftest.get_docker_compose_command() == ["docker-compose"]


def test_falls_back_to_docker_compose_plugin(monkeypatch):
    monkeypatch.setattr(
        conftest.shutil,
        "which",
        lambda command: "/usr/bin/docker" if command == "docker" else None,
    )
    seen_commands = []

    def fake_run(command, **kwargs):
        seen_commands.append((command, kwargs))

        class Result:
            returncode = 0

        return Result()

    monkeypatch.setattr(conftest.subprocess, "run", fake_run)

    assert conftest.get_docker_compose_command() == ["docker", "compose"]
    assert seen_commands[0][0] == ["docker", "compose", "version"]


def test_returns_none_when_docker_compose_is_unavailable(monkeypatch):
    monkeypatch.setattr(conftest.shutil, "which", lambda command: None)

    assert conftest.get_docker_compose_command() is None
