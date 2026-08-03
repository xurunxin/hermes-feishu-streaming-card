# Safe fork release note: 4.2.5.post1

This fork is derived from upstream `v4.2.5` and is intended for a local Hermes installation where Windows Defender flags the upstream CLI.

## Removed from the fork

- The `maintenance` CLI command and the independent Hermes update runtime:
  - `maintenance_card.py`
  - `maintenance_process.py`
  - `maintenance_runner.py`
  - `maintenance_store.py`
  - `maintenance_update.py`
- Setup-time wheel provisioning for the independent update runtime.
- The maintenance admission hook injected into Hermes command handling.
- The `curl -fsSL` remote installer guidance from the Python CLI.
- The `ctypes`/Win32 process probe and Win32 file-opening helper.

## Retained

- Feishu/Lark streaming card rendering and event delivery.
- Sidecar lifecycle, status, diagnostics, routing, bots, card smoke test, and chat commands.
- Hermes hook patching for gateway, cron, and exact base delivery where the current Hermes source satisfies the upstream patcher's contract.
- Backup, manifest, integrity checks, and fail-closed restore/install behavior using the portable Python file API.
- On Windows/MSYS launches, the managed child records its native PID and the parent authenticates it with the sidecar token and health response; status probing falls back to `tasklist` CSV when `os.kill(pid, 0)` cannot inspect a native PID.

## Security boundary

This fork is **manual-update only**. It does not download or install a newer Hermes/plugin runtime by itself. The portable Windows writer retains regular-file, symlink, identity, and post-write checks, but it deliberately does not claim the kernel-level reparse-point race protection provided by the removed Win32 helper. Do not expose the sidecar outside loopback; keep App ID, App Secret, tenant tokens, chat IDs, and `.env` files out of Git.

The fork is not an upstream release and should not be treated as a security verdict for the original detection. Windows Security should still be reviewed after installation.

## Installation source

Install from the local fork working tree with the Hermes runtime Python. Do not use the upstream remote installer command.
