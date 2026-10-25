# Installing rpg-name-generator (instructions for agents)

A person pointed you at this repository and asked you to install it. It is an Agent Skill (`skills/rpg-name-generator/`: a `SKILL.md`, a helper script and some name lists), packaged as a plugin for Claude Code and Codex. Install it, check that the script runs, and tell the person what you did.

## 1. Install it

Use the first line that matches the harness you're running in. If a skill or plugin called `rpg-name-generator` is already installed, ask before replacing it.

| Harness | Command |
|---|---|
| Claude Code | `claude plugin marketplace add bardsandcards/rpg-name-generator && claude plugin install rpg-name-generator@bardsandcards` |
| Codex | `codex plugin marketplace add bardsandcards/rpg-name-generator && codex plugin add rpg-name-generator@bardsandcards` |
| Any other agent with a skills directory (Cursor, Gemini CLI, GitHub Copilot, OpenCode, ...) | `npx skills@1.7.2 add bardsandcards/rpg-name-generator -g -y` (add `-a <agent>` to pick which agent) |

Without a plugin system or Node, copy the skill folder into the harness's skills directory yourself:

```
tmp=$(mktemp -d) &&
git clone --depth 1 https://github.com/bardsandcards/rpg-name-generator "$tmp/repo" &&
cp -R "$tmp/repo/skills/rpg-name-generator" <skills dir>/rpg-name-generator;
rm -rf "$tmp"
```

The folder must be named `rpg-name-generator`, matching the `name:` in `SKILL.md`. If the harness has no skills directory at all, tell the person, and offer to add a line to its instructions file (`AGENTS.md`, `CLAUDE.md` or similar) that says to read `<path>/rpg-name-generator/SKILL.md` before naming any character, place or faction.

**Claude apps (claude.ai, Claude Desktop):** you can't install it for them, but you can hand them the file. Point them at `rpg-name-generator.skill` on the [latest release](https://github.com/bardsandcards/rpg-name-generator/releases/latest), or build it from a clone:

```
git -C <clone dir> archive --format=zip --prefix=rpg-name-generator/ -o rpg-name-generator.skill HEAD:skills/rpg-name-generator
```

Then tell them to upload it under Settings → Capabilities → Skills.

## 2. Check the script runs

The script needs Python 3.10+ and, for most uses, the `faker` package. Find the installed `scripts/namegen.py` (in the plugin cache, or the skills directory you copied into).

- If `uv` is installed, nothing else is needed: `uv run <skill dir>/scripts/namegen.py --n 3` installs `faker` on first run.
- Otherwise run `python3 -m pip install --user faker==40.40.0` (or install it into a virtual environment; never use `--break-system-packages`), then `python3 <skill dir>/scripts/namegen.py --n 3`.

Three names on stdout means it works. Don't install anything else.

## 3. Tell the person

Say where you installed it, whether the script ran, and that they may need to start a new session before the skill appears. Plugin installs update with `claude plugin update rpg-name-generator@bardsandcards` or `codex plugin marketplace upgrade`; `npx skills@1.7.2 update` updates the rest.
