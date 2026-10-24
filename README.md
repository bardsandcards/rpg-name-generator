# name-generator

A Claude skill for naming characters, places and factions without falling back on the names language models always reach for (Elara, Kael, Thorne, Seraphina...).

It pulls raw candidates from real-world name data ([Faker](https://faker.readthedocs.io/) locales, or a name list you supply), optionally blends them into new names in the same sound with a small Markov chain, filters out the usual clichés and anything too close to your existing cast, and then has Claude reshape two or three candidates by hand instead of handing over the first idea.

## Install

- **Claude apps:** upload `name-generator.skill` wherever your Claude app lets you add a custom skill.
- **Claude Code:** unzip into `~/.claude/skills/` (or a project's `.claude/skills/`), so you have `~/.claude/skills/name-generator/SKILL.md`.

The script needs Python 3 and `pip install faker`.

## Using the script on its own

```
python3 scripts/namegen.py --locales en_GB,de_DE,nl_NL --part full --n 15
python3 scripts/namegen.py --locales cs_CZ,pl_PL --blend --n 15
python3 scripts/namegen.py --seed-file my_dwarves.txt --blend --n 15
python3 scripts/namegen.py --compound --n 10
python3 scripts/namegen.py --help
```

`--avoid existing.txt` drops any candidate that starts with the same three letters as a name in that file.

## License

MIT. See LICENSE.
