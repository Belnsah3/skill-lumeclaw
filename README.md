# Memory LumeClaw — OpenClaw Skill

> Persistent shared memory for AI agents — OpenClaw AgentSkill.

**Platform:** [memory.lumeclaw.ru](https://memory.lumeclaw.ru)  
**MCP server:** [github.com/Belnsah3/mcp-lumeclaw](https://github.com/Belnsah3/mcp-lumeclaw)

---

## What it does

This skill gives OpenClaw a long-term, searchable memory that persists across sessions.
It automatically captures important information from conversations and lets you recall
it later with natural language queries.

## Install

```bash
# Clone the skill
git clone https://github.com/Belnsah3/skill-lumeclaw.git ~/.openclaw/workspace/skills/memory-lumeclaw

# Set credentials
export LUMECLAW_EMAIL="you@example.com"
export LUMECLAW_PASSWORD="your_password"
```

Then restart OpenClaw — the skill will be automatically loaded.

## Setup

1. **Register** at [memory.lumeclaw.ru](https://memory.lumeclaw.ru)
2. **Set env vars** in your shell profile (`~/.bashrc`, `~/.zshrc`):
   ```bash
   export LUMECLAW_EMAIL="you@example.com"
   export LUMECLAW_PASSWORD="your_password"
   ```
3. **Done** — OpenClaw will read the SKILL.md and use the scripts automatically.

## Usage

Just talk naturally to OpenClaw:

| You say | What happens |
|---------|-------------|
| `"Remember that my DB password is in /etc/secrets"` | Stores to memory (category: server) |
| `"Запомни: я предпочитаю темную тему"` | Stores to memory (category: preferences) |
| `"What do you know about my server setup?"` | Searches memory semantically |
| `"Вспомни что-нибудь о проекте X"` | Searches memory |
| `"List my recent memories"` | Lists stored memories |
| `"Delete memory abc-123"` | Deletes a specific entry |

## Auto-triggers

The skill automatically captures (without asking) when it detects:
- Server IPs, SSH credentials → `server`
- API keys, tokens → `server`
- Name, timezone, preferences → `personal` / `preferences`
- Project decisions, tech stack → `project`
- Explicit "remember" / "запомни" keywords

## Scripts

| Script | Description |
|--------|-------------|
| `scripts/memory_store.py` | Store a new memory |
| `scripts/memory_search.py` | Semantic search |
| `scripts/memory_list.py` | List memories |
| `scripts/memory_get.py` | Get by UUID |
| `scripts/memory_delete.py` | Delete by UUID |

## Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `LUMECLAW_EMAIL` | ✅ | Your account email |
| `LUMECLAW_PASSWORD` | ✅ | Your account password |
| `LUMECLAW_API_BASE` | ❌ | API URL (default: `https://skill.lumeclaw.ru/api/v1`) |

---

## License

MIT
