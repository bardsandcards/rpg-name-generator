---
name: name-generator
description: Use whenever naming a character, NPC, place, ship, tavern, guild or faction, in fantasy, sci-fi, historical or modern settings. Generates candidates from real-world name data, then reshapes them by hand, instead of inventing names from habit.
---

# Name generator

Language models name things from habit. Ask for a fantasy character and you get Elara, Kael, Thorne, Seraphina or Aldric, over and over. This skill gets raw candidates from real-world name data, then reshapes the best of them by hand. The generator supplies ideas; the name you hand over is a modification, not a pick.

## 1. Decide whether it needs a name at all

- **A one-scene character** (a shopkeeper, a guard, a passer-by) usually shouldn't get a prominent name. Give them a quirk and a voice instead. A first name dropped in someone's dialogue is fine. Readers and players remember names and expect named characters to matter.
- **Recurring characters, places and factions** get a real name. Unless the user asked for exactly one, offer **two or three** finished options.

## 2. Pick where the sound comes from

Decide the culture or feel first, then the source:

| Feel | Source |
|---|---|
| Anglo, Germanic, Low Countries (classic "knightly" fantasy) | `--locales en_GB,de_DE,nl_NL` |
| Romance-language, Mediterranean | `--locales fr_FR,it_IT` or `es_ES,pt_PT` |
| Central and Eastern European | `--locales cs_CZ,pl_PL` (blend these for anything "old-world") |
| Nordic | `--locales sv_SE,no_NO,fi_FI` |
| Japanese | `--locales ja_JP` (Faker's romanized names) |
| Any culture Faker doesn't cover in Latin script | find a real name list (web search, a reference book, the setting's own sources) and use `--seed-file` |
| A fictional people who already exist in the setting (its dwarves, elves, aliens) | `--seed-file` of the setting's existing names for them, with `--blend`, so new names sound like they belong |
| Whimsical small folk (halflings, kender, gnomes) | `--compound` for surnames like Copperbottom, then fix the first name |
| Modern or sci-fi characters | real names from wherever the character is from, no blend |

`--blend` runs a character-level Markov chain over the source, so you get new names that keep its sound. Without it you get real names. A seed file needs at least 15–20 names; fewer gives thin, repetitive output.

If the setting already has a cast, put their names in an avoid file (one per line) so nothing new starts with the same three letters as someone people already know.

## 3. Run the generator

The script is `scripts/namegen.py` in this skill's folder. It needs `faker` (`pip install faker`, adding `--break-system-packages` where pip requires it); seed-file runs without `--compound` don't. Ask for **15–20 candidates**:

```
python3 scripts/namegen.py --locales en_GB,de_DE,nl_NL --part full --n 20 --avoid existing.txt
python3 scripts/namegen.py --locales cs_CZ,de_DE --blend --n 20      # new names in that sound
python3 scripts/namegen.py --seed-file dwarves.txt --blend --n 20     # new names in the setting's own sound
python3 scripts/namegen.py --compound --n 15
```

The script drops a built-in list of overused fantasy names. Some locales quietly return English names; if the output doesn't match the locale, switch to a seed file.

## 4. Modify

Take two or three candidates you like and reshape each one:
- Change a syllable, or swap the ending to fit the culture (soft vowel endings for one people, hard consonants for another).
- Shorten until it's easy to say aloud on the first try. Minor characters get one or two syllables.
- Change the first sound if someone already in the cast shares it. People confuse names that start the same.
- No apostrophes, doubled vowels or stray Ys unless the culture really uses them.
- Don't hand over the generator's raw output, and don't take the first candidate.

## 5. Present

Give the finished names, each with a one-line note on where it came from ("from 'Rehorst', Dutch, cut down to two syllables"), so the user can see the reasoning and ask for another pass in a different direction.
