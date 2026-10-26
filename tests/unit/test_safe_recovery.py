import pytest

from hermes_feishu_card.install import file_transaction, recovery


def test_safe_fork_refuses_portable_evidence_deletion_without_mutation(tmp_path):
    root = tmp_path / "hermes"
    root.mkdir()
    first, second = root / "backup", root / "manifest"
    before = {first: b"source backup\r\n", second: b"manifest\r\n"}
    for path, data in before.items():
        path.write_bytes(data)
    identities, directories = file_transaction._snapshot_restore_evidence(
        root, {path.name: path for path in before}
    )
    assert not recovery._portable_restore_supported()
    with pytest.raises(ValueError, match="original files preserved"):
        file_transaction._remove_targets_portably(
            list(before), expected_identities=identities,
            expected_directories=directories,
        )
    assert {path: path.read_bytes() for path in before} == before
