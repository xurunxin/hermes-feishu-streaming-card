import os
from pathlib import Path
import subprocess
from types import SimpleNamespace

from hermes_feishu_card.install import plugin
from hermes_feishu_card.install.plugin_config_bytes import isolated_child_env


def test_isolated_child_environment_excludes_credentials_and_keeps_home(monkeypatch, tmp_path):
    monkeypatch.setenv("FEISHU_APP_SECRET", "SYNTHETIC-SECRET")
    monkeypatch.setenv("PYTHONPATH", "untrusted")
    home = tmp_path / "hermes home"
    root = tmp_path / "checkout"
    result = isolated_child_env(home, install_root=root, include_path=True)
    assert result["HOME"] == result["HERMES_HOME"] == str(home)
    assert result["HERMES_INSTALL_ROOT"] == str(root)
    assert "FEISHU_APP_SECRET" not in result
    assert "PYTHONPATH" not in result
    if os.name == "nt":
        assert result["USERPROFILE"] == str(home)
        assert result["SYSTEMROOT"] == os.environ.get("SYSTEMROOT", os.environ.get("WINDIR"))


def test_official_enable_uses_verified_source_and_bounded_timeout(monkeypatch, tmp_path):
    home = tmp_path / "home"
    root = tmp_path / "source"
    binding = SimpleNamespace(runtime_python=Path("python.exe"), checkout_root=root, hermes_home=home)
    verified = []
    observed = {}
    monkeypatch.setattr(plugin, "_verify_official_enable_source", verified.append)

    def fake_run(args, **kwargs):
        observed.update(kwargs)
        assert args[-1] == "--no-allow-tool-override"
        return subprocess.CompletedProcess(args, 0)

    monkeypatch.setattr(plugin.subprocess, "run", fake_run)
    assert plugin._run_official_enable(binding) == 0
    assert verified == [root]
    assert observed["timeout"] == (600 if os.name == "nt" else 30)
    assert observed["env"] == isolated_child_env(home, install_root=root, include_path=True)
