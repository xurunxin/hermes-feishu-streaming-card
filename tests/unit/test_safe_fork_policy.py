from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "hermes_feishu_card"
CLI = PACKAGE / "cli.py"


def test_safe_cli_removes_remote_installer_and_windows_api_surface():
    for source_path in (CLI,):
        lowered = source_path.read_text(encoding="utf-8").lower()
        assert "ctypes" not in lowered
        assert "windll" not in lowered
        assert "createfilew" not in lowered
        assert "curl -fssl" not in lowered
        assert "official_installer_command" not in lowered
        assert "maintenance" not in lowered


def test_safe_runtime_has_no_windows_ctypes_process_control():
    text = (PACKAGE / "process.py").read_text(encoding="utf-8")
    assert "ctypes" not in text.lower()
    assert "windll" not in text.lower()
    assert "kernel32" not in text.lower()
    assert "openprocess" not in text.lower()






def test_safe_fork_has_explicit_local_version():
    init_text = (PACKAGE / "__init__.py").read_text(encoding="utf-8")
    project_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '__version__ = "5.0.9+safe.1"' in init_text
    assert 'version = "5.0.9+safe.1"' in project_text


def test_safe_package_excludes_remote_updater_and_native_handle_helpers():
    forbidden_files = {"maintenance_card.py", "maintenance_process.py", "maintenance_runner.py",
                       "maintenance_store.py", "maintenance_update.py", "maintenance_evidence.py"}
    assert not forbidden_files.intersection(p.name for p in PACKAGE.iterdir())
    for source in PACKAGE.rglob("*.py"):
        text = source.read_text(encoding="utf-8").lower()
        assert "maintenance" not in text, source
        assert "ctypes" not in text, source
        assert "windll" not in text, source
        assert "createfilew" not in text, source
        assert "official_installer_command" not in text, source


def test_safe_package_has_no_private_updater_hook():
    from hermes_feishu_card import hook_runtime
    from hermes_feishu_card.operations import OperationStore
    assert not hasattr(hook_runtime, "_hfc_install_update_command_handler")
    assert not hasattr(hook_runtime, "maintenance_admission_from_hermes_locals")
    assert not hasattr(OperationStore, "prepare_update")
