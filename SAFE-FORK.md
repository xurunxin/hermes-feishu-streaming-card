# Safe fork of Hermes Feishu Streaming Card

This fork is based on upstream 5.0.9 and identifies its distribution as
`5.0.9+safe.1`. It preserves the upstream project's history and attribution.
Install the fork from its `main` or `safe-v4.2.5` branch. The upstream release
packages and the upstream install commands in the historical documentation do
not contain these fork changes.

The private-chat remote update command, update cards, and associated maintenance
modules and CLI have been removed. Windows process checks and portable file
operations use standard Python interfaces rather than direct native-handle
calls. A standard file open does not provide the same exclusive handle and
path-race guarantees as upstream's Windows implementation. Source identity,
content and directory checks remain in place.

Windows PID checks use a read-only task listing and treat a failed or
unparseable listing as still running. The earlier local `5.0.5+safe.4` build
used `os.kill(pid, 0)` on Windows; that can send a control event and should not
be used as a process-existence probe.

Windows cleanup of the legacy decomposed-patch recovery evidence requires the
upstream native-handle deletion mechanism; this fork refuses that recovery
before mutation rather than deleting evidence without it. This limitation does
not apply to the Hermes plugin-manager installation path. Preserve the existing
files and seek a separately reviewed recovery if this legacy path is needed.

The source changes are intended to avoid the previously reported antivirus
trigger. They do not constitute a guarantee about any antivirus product.
