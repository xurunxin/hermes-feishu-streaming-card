# v4.2.6 Safe Fork Release

2026-08-04

这是 Safe Fork 的第一个正式可安装版本，基于上游 `v4.2.5`，包版本为 `4.2.6`。

## 安装修复

- Bash、PowerShell 和 Docker 安装器默认从 `xurunxin/hermes-feishu-streaming-card` 获取代码。
- `HFC_VERSION=latest` 查询用户 fork 的 GitHub Release，并固定到经过校验的 `v4.2.6` tag。
- 保留 `HFC_REPO` 显式覆盖能力，方便用户自行维护镜像或 fork。
- 发布包包含 macOS/Linux/Windows 安装入口、Docker 安装器、Compose 示例、配置模板和 SHA-256 checksums。
- Release workflow 会验证 annotated tag、包版本 marker、配置/Compose/CI 版本 marker，以及 release commit 所属的 `safe-v4.2.5` 分支。

## Safe Fork 边界

- 移除了独立 maintenance 自更新链、远程安装引导和 Windows ctypes/Win32 辅助路径。
- Safe Fork 只负责插件和 sidecar；不会自行下载或安装新的 Hermes runtime。
- 这是用户 fork 的安全维护版本，不是上游官方 release。安装后仍应检查 Windows Security/Defender 状态。

## 推荐安装

Linux/macOS：

```bash
curl -fsSL https://raw.githubusercontent.com/xurunxin/hermes-feishu-streaming-card/v4.2.6/install.sh | bash
```

Windows PowerShell：

```powershell
irm https://raw.githubusercontent.com/xurunxin/hermes-feishu-streaming-card/v4.2.6/install.ps1 | iex
```

Docker/source-stripped Hermes：

```bash
export HFC_VERSION=v4.2.6
bash install-docker.sh
```

显式安装固定版本时，也可以设置 `HFC_REPO=xurunxin/hermes-feishu-streaming-card` 和 `HFC_VERSION=v4.2.6`。
