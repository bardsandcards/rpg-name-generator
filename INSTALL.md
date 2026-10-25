# Installing rpg-name-generator (instructions for agents)

A person pointed you at this repository and asked you to install it. It is an Agent Skill: a folder with a `SKILL.md` and a helper script. Install it, check that the script runs, and tell the person what you did.

## 1. Put the skill where your harness loads skills

The folder must be named `rpg-name-generator`, matching the `name:` in `SKILL.md`. Clone it straight into place:

| Harness | Command |
|---|---|
| Claude Code (all projects) | `git clone https://github.com/bardsandcards/rpg-name-generator ~/.claude/skills/rpg-name-generator` |
| Claude Code (one project) | `git clone https://github.com/bardsandcards/rpg-name-generator .claude/skills/rpg-name-generator` |
| Codex | `git clone https://github.com/bardsandcards/rpg-name-generator ~/.codex/skills/rpg-name-generator` |
| A harness that reads `~/.agents/skills` | `git clone https://github.com/bardsandcards/rpg-name-generator ~/.agents/skills/rpg-name-generator` |

For any other harness, use its documented skills directory. If it has none, tell the person, and offer to add a line to its instructions file (`AGENTS.md`, `CLAUDE.md` or similar) that says to read `rpg-name-generator/SKILL.md` before naming any character, place or faction.

If a `rpg-name-generator` skill is already installed there, ask before replacing it.

**Claude apps (claude.ai, Claude Desktop):** you can't install it for them, but you can hand them the file. Point them at `rpg-name-generator.skill` on the [latest release](https://github.com/bardsandcards/rpg-name-generator/releases/latest), or build it from a clone:

```
git -C <clone dir> archive --format=zip --prefix=rpg-name-generator/ -o rpg-name-generator.skill HEAD SKILL.md LICENSE scripts
```

Then tell them to upload it under Settings → Capabilities → Skills.

## 2. Check the script runs

The script needs Python 3.9+ and the `faker` package.

- If `uv` is installed, nothing else is needed: `uv run <skill dir>/scripts/namegen.py --n 3` installs `faker` on first run.
- Otherwise run `python3 -m pip install faker` (add `--user`, or `--break-system-packages` where pip refuses), then `python3 <skill dir>/scripts/namegen.py --n 3`.

Three names on stdout means it works. Don't install anything else.

## 3. Tell the person

Say where you installed it, whether the script ran, and that they may need to start a new session before the skill appears. To update later: `git -C <skill dir> pull`.
