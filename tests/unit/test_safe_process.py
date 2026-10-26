import os
import subprocess
from types import SimpleNamespace

import pytest

from hermes_feishu_card import process


@pytest.mark.parametrize(
    ("output", "returncode", "expected"),
    [
        ('"python.exe","1234","Console","1","20 K"\n', 0, True),
        ('"python.exe","2345","Console","1","20 K"\n', 0, False),
        ("", 0, True),
        ("unrecognized output", 0, True),
        ('"python.exe","2345"\n', 1, True),
    ],
)
def test_windows_pid_probe_only_reads_task_list(monkeypatch, output, returncode, expected):
    observed = []
    monkeypatch.setenv("SYSTEMROOT", r"C:\Windows")

    def forbidden_signal(*_args):
        pytest.fail("a PID query must not send a process-control signal")

    def tasklist(args, **kwargs):
        observed.append((args, kwargs))
        return SimpleNamespace(returncode=returncode, stdout=output)

    monkeypatch.setattr(process.os, "kill", forbidden_signal)
    monkeypatch.setattr(process.subprocess, "run", tasklist)
    assert process._pid_is_running_windows(1234) is expected
    assert observed[0][0][-3:] == ["/FO", "CSV", "/NH"]
    assert observed[0][1]["timeout"] == 5


def test_windows_pid_probe_treats_timeout_as_unknown(monkeypatch):
    monkeypatch.setenv("SYSTEMROOT", r"C:\Windows")

    def timeout(*_args, **_kwargs):
        raise subprocess.TimeoutExpired("tasklist", 5)

    monkeypatch.setattr(process.subprocess, "run", timeout)
    assert process._pid_is_running_windows(1234)


@pytest.mark.skipif(os.name != "nt", reason="requires real Windows tasklist")
def test_windows_pid_probe_checks_real_task_list_without_signalling():
    assert process._pid_is_running_windows(os.getpid())
    assert not process._pid_is_running_windows(2**64)
