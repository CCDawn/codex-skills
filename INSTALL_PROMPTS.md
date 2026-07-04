# Codex 一键安装提示词

把下面任意一版提示词复制到新的 Codex 会话里，就可以让 Codex 从 GitHub 安装 CCDawn skill 包。

大多数情况用“普通版”即可。如果你希望 Codex 严格限制操作范围，只做安装相关动作，就用“强约束版”。

## 普通版

```text
请帮我一键安装 CCDawn 的 Codex skills 技能包。

仓库地址：https://github.com/CCDawn/codex-skills.git

要求：
1. 如果本机已有这个仓库，就进入仓库并更新到最新 main；如果没有，就 clone 到一个合适的本地目录。
2. 只安装到当前用户的 Codex live skills 目录：~/.codex/skills。
3. 不要安装到 ~/.agents/skills，避免重复 slash-command。
4. 先运行安装演练，再执行正式安装。
5. 安装后验证 live skills 是否可用。
6. 最后用中文汇报：仓库位置、安装目录、安装了哪些 skills、验证是否通过、是否需要重启 Codex。
7. 重点提醒我：最重要入口是 /brt（ccdawn-brt）；日常使用优先从 /brt 开始，其它 skill 通常由它自动路由。

如果遇到 Git、Python、网络、权限问题，只问我一个最关键的阻塞问题。
```

## 强约束版

```text
你现在负责一键安装 CCDawn Codex skills 技能包。

Repo:
https://github.com/CCDawn/codex-skills.git

目标:
- 安装整个 skill 包，不是只安装 ccdawn-brt。
- 只安装到当前用户的 Codex live skills 目录：~/.codex/skills。
- 不要安装到 ~/.agents/skills、~/.claude/skills，除非我明确要求。
- 不要修改任何用户项目代码。
- 只允许创建/更新本地 codex-skills 仓库，以及写入 ~/.codex/skills 下的 skill 安装目录。
- 安装完成后明确告诉我：/brt（ccdawn-brt）是最重要入口，其它 skill 通常由 BRT 自动路由。

执行步骤:
1. 识别当前系统、shell、Git、Python 是否可用。
2. 找一个合适的本地工作目录保存仓库；如果已有 codex-skills 仓库，进入后 git pull；如果没有，从 GitHub clone。
3. 进入仓库根目录。
4. 先运行安装演练：
   - Windows 优先用：powershell -ExecutionPolicy Bypass -File .\install.ps1 -DryRun
   - 如果不适用，用：python scripts/install_codex_library.py --dry-run
5. 正式安装到 Codex：
   - Windows 优先用：powershell -ExecutionPolicy Bypass -File .\install.ps1
   - 如果不适用，用：python scripts/install_codex_library.py --agent codex
6. 安装后验证：
   - 优先用：python scripts/install_codex_library.py --verify-only
   - 如果验证器缺失，要明确说明验证器缺失，但仍检查 ~/.codex/skills 下是否存在已安装 skill。
7. 最后中文汇报：
   - 仓库路径
   - 安装目标路径
   - 安装/验证命令
   - 已安装 skill 数量和关键 skill，例如 ccdawn-brt
   - 最重要入口：/brt（ccdawn-brt），其它 skill 是下游能力，通常由 BRT 自动路由
   - 验证结果
   - 是否需要重启 Codex 或新开会话

失败处理:
- 不要猜测成功。
- 不要跳过验证。
- 不要反复问多个问题。
- 如果 Git、Python、网络、权限或路径阻塞，只问我一个最关键的问题。
```

## 手动安装

如果你想自己执行命令，可以使用：

```powershell
git clone https://github.com/CCDawn/codex-skills.git
cd codex-skills
powershell -ExecutionPolicy Bypass -File .\install.ps1 -DryRun
powershell -ExecutionPolicy Bypass -File .\install.ps1
python scripts/install_codex_library.py --verify-only
```

安装后重启 Codex 或新开会话，让客户端重新加载本地 skills。日常使用优先从 `/brt`（`ccdawn-brt`）开始，让它自动判断是否需要路由到其它 skill。
