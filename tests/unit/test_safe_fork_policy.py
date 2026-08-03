from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PACKAGE = ROOT / "hermes_feishu_card"
CLI = PACKAGE / "cli.py"


def test_safe_cli_removes_remote_installer_and_windows_api_surface():
    for source_path in (CLI, PACKAGE / "cli_core.py"):
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


def test_safe_runtime_has_no_removed_update_dependency_chain():
    forbidden = (
        "maintenance",
        "updateinspection",
        "inspect_update",
        "launch_job",
        "maintenance_paths",
        "maintenance_refused",
    )
    for source_path in PACKAGE.rglob("*.py"):
        lowered = source_path.read_text(encoding="utf-8").lower()
        assert not any(token in lowered for token in forbidden), source_path


def test_safe_fork_removes_maintenance_runtime_and_hook_admission():
    for name in (
        "maintenance_card.py",
        "maintenance_process.py",
        "maintenance_runner.py",
        "maintenance_store.py",
        "maintenance_update.py",
    ):
        assert not (PACKAGE / name).exists(), name
    assert "maintenance_admission" not in (
        PACKAGE / "hook_runtime.py"
    ).read_text(encoding="utf-8")
    assert "maintenance_admission" not in (
        PACKAGE / "install" / "patcher.py"
    ).read_text(encoding="utf-8")
    hook_text = (PACKAGE / "hook_runtime.py").read_text(encoding="utf-8")
    assert "_hfc_request_update_command" not in hook_text
    assert "_hfc_install_update_command_handler" not in hook_text


def test_safe_fork_has_explicit_local_version():
    init_text = (PACKAGE / "__init__.py").read_text(encoding="utf-8")
    project_text = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    assert '__version__ = "4.2.5.post1"' in init_text
    assert 'version = "4.2.5.post1"' in project_text
