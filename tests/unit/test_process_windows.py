from __future__ import annotations

from types import SimpleNamespace

import pytest

from hermes_feishu_card import process


pytestmark = pytest.mark.windows_only


def test_process_token_hash_is_stable_and_empty_safe():
    assert process.process_token_hash("") == ""
    assert process.process_token_hash(None) == ""
    assert process.process_token_hash("sidecar-token")
    assert process.process_token_hash("sidecar-token") == process.process_token_hash(
        "sidecar-token"
    )
    assert process.process_token_hash("sidecar-token") != process.process_token_hash(
        "other-token"
    )


def test_windows_pid_probe_falls_back_to_tasklist(monkeypatch):
    calls = []

    def raise_system_error(_pid, _signal):
        raise SystemError("translated native pid")

    def fake_tasklist(command, **_kwargs):
        calls.append(command)
        return SimpleNamespace(
            returncode=0,
            stdout='"python.exe","4321","Console","1","10,000 K"\n',
        )

    monkeypatch.setattr(process.os, "kill", raise_system_error)
    monkeypatch.setattr(process.subprocess, "run", fake_tasklist)

    assert process._pid_is_running_windows(4321) is True
    assert calls and calls[0][:2] == ["tasklist", "/FI"]
