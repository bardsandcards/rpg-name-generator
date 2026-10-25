# rpg-name-generator

Ask an AI to name a small-town sheriff and you'll probably meet Sheriff Dale. Ask for a paladin and you get Seraphine; ask for a village and you get Thornwick Hollow. Ask again and you get them again.

rpg-name-generator is a skill for AI agents (Claude, Codex and others) that fixes this for tabletop RPGs and fiction. When your agent needs a name, for an NPC, a town, a tavern, a ship or a cult, the skill has it start from real-world name data, check the result against the people and places already in your campaign, and reshape it by hand, so the name fits your setting instead of every setting. It works for any genre: fantasy, sci-fi, cyberpunk, horror, steampunk, historical, western, post-apocalyptic and modern.

## Install

Tell your agent:

> Install the skill at https://github.com/bardsandcards/rpg-name-generator

It reads [INSTALL.md](INSTALL.md) and handles the rest. Or do it yourself:

- **Claude Code:** `/plugin install rpg-name-generator --marketplace bardsandcards/rpg-name-generator`
- **Codex:** `codex plugin marketplace add bardsandcards/rpg-name-generator`, then `codex plugin add rpg-name-generator@bardsandcards`
- **Cursor, Gemini CLI, GitHub Copilot and other agents:** `npx skills add bardsandcards/rpg-name-generator`
- **claude.ai or Claude Desktop:** download `rpg-name-generator.skill` from the [latest release](https://github.com/bardsandcards/rpg-name-generator/releases/latest) and upload it under Settings → Capabilities → Skills.

## Examples

**At the table.** A player asks the gate guard's name. You ask your agent, and it answers with one name straight away (say, *Raf*) and, if it keeps your campaign notes, jots down who Raf is, ready for next session.

**Prepping an adventure.** "Write up the river town of Fenmarch: the reeve, the ferryman, the smuggler and the priest." The agent gathers the names your campaign already has, picks a sound for the town, generates candidates, reshapes them, and checks them against your cast and each other. You get a short table with a note on where each name came from ("from Czech 'Rajhrad', cut to two syllables"), and none of them start like Captain Ilse Marten or the Widow Grieve.

**Any genre.** A Weird West gunslinger's name comes from what Americans were actually naming their children in the 1850s. A 1920s Call of Cthulhu professor gets a name from the decade they were born in, not the decade of the game. A cyberpunk fixer gets a real name from the mix of places the city draws on.

**The script on its own.** The skill's helper script also works by hand, from `skills/rpg-name-generator/`:

```
$ uv run scripts/namegen.py --locales pt_BR,vi_VN,pl_PL,zu_ZA --part full --n 4
Khanyisile Balawender
Minenhle Đặng
Antonella Trần
Klara Mdlalose

$ uv run scripts/namegen.py --locales de_DE,cs_CZ --part place --blend --n 4
Rýdlinge
Oslavon
Regeld
Chatz

$ uv run scripts/namegen.py --compound --n 3
Ronald Rattlefoot
Wendy Whistleskip
Martin Mudbottom

$ uv run scripts/namegen.py --avoid cast.txt --check "Hollis Brandt" "Ilsa Moor" "Mara Voss"
Hollis Brandt: ok
Ilsa Moor: clashes with ilsa~ilse
Mara Voss: clashes with mara, voss, mara~marten
```

The script's output is raw material. The skill has the agent reshape it before you see it. Run `uv run scripts/namegen.py --help` for every option.

## How it works

Language models have favorite names. We asked four models (Claude Haiku, Sonnet and Opus, and GPT Daybreak Blue through Codex) for one name at a time, 1,008 times, across 28 everyday RPG requests, each in a fresh session with no other context ([method and data](research/README.md)). The same few answers kept coming back:

| Asked for | What came back, out of 36 |
|---|---|
| A small-town sheriff | **Dale**, 24 times (Dale Hargrove, Dale Harrow…), including every Sonnet and Opus draw |
| A homicide detective | **Mara**, 16 times; **Voss** or **Vance**, 21 (Mara Voss ×8, Marisol Vance ×7) |
| A paladin heroine | **Seraphine**, 34 times (Seraphine Valcourt ×14) |
| A halfling rogue | a name starting with **Pip**, 33 times (Pip Thistlewick ×10, Pip Underbough ×10) |
| A steampunk inventor | **Thaddeus** or **Cornelius**, 26 times (Thaddeus Cogsworth ×8) |
| A Weird West gunslinger | **Silas**, 21 times |
| A Victorian widow | **Blackwood**, 17 times |
| A Roman legionary | **Gaius** or **Marcus**, all 36 (Gaius Valerius Crispus ×9) |
| A Viking raider | **Ragnvald**, **Eirik** or **Bjorn**, 27 times (Eirik Bloodaxe ×6) |
| A fantasy village | **Thornwick Hollow**, 24 times |
| A fantasy tavern | **The Gilded** something, 32 times |
| A secret cult | something **Hollow**, 29 times |
| A cyberpunk megacorp | something **Dynamics**, 25 times; **Arasaka**, 15 |
| A horror town | a town from someone else's story, 28 times: Arkham, Silent Hill, Hawkins, Sunnydale |

Each of these shows up in at least two of the four models; the [full results](research/README.md) cover all 28 requests.

They also reach for names that already belong to someone (Malcolm Reynolds, MOTHER, Arasaka, Nostromo, Silent Hill), and stack the same words on everything: Gilded, Hollow, Ember, Iron, Thorn, Black, Vesper, Meridian, Syndicate. Even where the names are real, like Gaius and Marcus, every legionary at your table ends up with one.

The skill tells the agent to work differently:

1. **Work out the situation.** A quick name at the table should be fast: one name, no list, no explanation. Prep for an adventure gets two or three options for important characters and a short table for the rest.
2. **Gather the cast.** If the agent knows your campaign, from the conversation, your notes or the adventure you're running, it lists every name already in play, plus the genre's famous ones, so new names don't sound like old ones. Players confuse names that start the same way.
3. **Pick a source for the sound.** Each genre and culture gets a source of real names: a country's names, a period's records for historical games, or the setting's own names for its peoples. The skill has a table for this.
4. **Generate candidates.** The script returns 15 or 20 real names from that source, or new names blended from it, dropping the clichés above and anything too close to your cast or to the rest of the batch.
5. **Reshape.** The agent changes a syllable, shortens, or swaps an ending to fit the culture, then checks the finished name against your cast again.

Taverns, ships, guilds and companies don't come from the script. The skill has the agent name them after something specific in your setting (a former owner, a local event, a trade) instead of the stock words.

## What's included, and why

Everything the skill needs lives in [skills/rpg-name-generator/](skills/rpg-name-generator/):

- **[SKILL.md](skills/rpg-name-generator/SKILL.md)**: the instructions your agent follows. This is the skill itself.
- **[scripts/namegen.py](skills/rpg-name-generator/scripts/namegen.py)**: a single Python script with one dependency. Agents invent names from habit (see the table above); the script gives them a source to work from instead. It:
  - draws real first names, surnames and town names from [Faker](https://faker.readthedocs.io/), a widely used library of locale data for dozens of countries, or from a name list;
  - can blend those names into new ones with a small Markov chain, which strings letters together the way the source does, so invented names keep its sound;
  - filters out a list of names models overuse, and anything too similar to your cast or to the rest of the batch;
  - checks finished names against your cast with `--check`.
- **Faker**: the only third-party library. It's here for its data (people's names and towns by locale), not its fake-data features. `uv run` installs it automatically; otherwise it's `pip install faker`. Name lists used with `--seed-file` don't need it.
- **[seeds/](skills/rpg-name-generator/seeds/)**: real name lists for eras Faker doesn't cover: US first names by birth decade (1880s–1920s), US surnames, England and Wales in 1904, Roman names and Old Norse names. [SOURCES.md](skills/rpg-name-generator/seeds/SOURCES.md) says where each one comes from.

The rest of the repo is packaging and upkeep:

- **[INSTALL.md](INSTALL.md)**: install steps for your agent.
- **`.claude-plugin/`, `.codex-plugin/`, `.agents/plugins/`**: the plugin manifests that let Claude Code and Codex install the skill in one command.
- **[tests/](tests/)** and **[.github/workflows/](.github/workflows/)**: tests of the script's behavior, run on every push alongside Claude Code's plugin validator; each release attaches a ready-to-upload `.skill` file.
- **[research/](research/)**: the script that sampled the models for the table above, and its raw results, so you can check the numbers or rerun them against newer models.

## License

The code and instructions are [MIT No Attribution](LICENSE): use, copy, change and share them however you like, no credit required. © Bards & Cards LLC.

The name lists in `seeds/` keep their sources' terms: US government data (public domain), ONS data (Open Government Licence v3.0) and lists drawn from Wikipedia and Wiktionary (CC BY-SA 4.0). [SOURCES.md](skills/rpg-name-generator/seeds/SOURCES.md) gives the attribution each one asks for.
