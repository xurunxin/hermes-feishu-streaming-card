# v4.2.6 Safe Fork Release

2026-08-04

The first formally installable Safe Fork release, derived from upstream `v4.2.5`, with package version `4.2.6`.

## Installer fixes

- Bash, PowerShell, and Docker installers now default to `xurunxin/hermes-feishu-streaming-card`.
- `HFC_VERSION=latest` queries the user's fork GitHub Releases API and pins the verified `v4.2.6` tag.
- Explicit `HFC_REPO` overrides remain supported for users maintaining another mirror or fork.
- Release packages include macOS/Linux/Windows installer entry points, the Docker installer, Compose example, config template, and SHA-256 checksums.
- The release workflow verifies the annotated tag, package/config/Compose/CI version markers, and that the release commit belongs to the `safe-v4.2.5` branch.

## Safe Fork boundary

- The independent maintenance self-update chain, remote installer guidance, and Windows ctypes/Win32 helper paths were removed.
- The Safe Fork manages the plugin and sidecar only; it does not download or install a new Hermes runtime by itself.
- This is a user-maintained fork release, not an upstream official release. Review Windows Security/Defender after installation.

## Recommended installation

Linux/macOS:

```bash
curl -fsSL https://raw.githubusercontent.com/xurunxin/hermes-feishu-streaming-card/v4.2.6/install.sh | bash
```

Windows PowerShell:

```powershell
irm https://raw.githubusercontent.com/xurunxin/hermes-feishu-streaming-card/v4.2.6/install.ps1 | iex
```

Docker/source-stripped Hermes:

```bash
export HFC_VERSION=v4.2.6
bash install-docker.sh
```

For an explicit fixed install, set `HFC_REPO=xurunxin/hermes-feishu-streaming-card` and `HFC_VERSION=v4.2.6`.
