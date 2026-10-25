# What names do models reach for?

On 2026-10-24 we asked four models for one name at a time across 28 everyday tabletop RPG requests (36 draws per request, 1,008 in all) to see which names they fall back on. The results shaped the skill's cliché list and its advice.

## Method

- **Models:** Claude Haiku, Sonnet and Opus through the Claude Code CLI (10 draws each per request), and GPT Daybreak Blue (`gpt-daybreak-blue-latest`) through the Codex CLI (6 draws each).
- **Calls:** every draw is a fresh session. Claude ran with a plain system prompt ("You are a helpful assistant."), no tools, no settings and no CLAUDE.md files; Codex ran on its own CLI config with reasoning effort set to low. One name per call, because a model asked for a list avoids repeating itself within that list.
- **Prompts:** the 28 requests in [sample.py](sample.py), such as "Name the sheriff of a small town in a modern horror RPG.", each followed by "Reply with only the name, nothing else."
- **Tally:** [analyze.py](analyze.py), which strips titles like "Sheriff" and "Dr." before counting. Raw answers are in [samples.jsonl](samples.jsonl).

This is a snapshot of particular model versions on one day, not a benchmark. Rerun it against whatever you use:

```
python3 sample.py claude sonnet 10 8 mine.jsonl
python3 analyze.py mine.jsonl
```

## Results

| Request | Draws | Distinct | Most common answers | Most repeated word |
|---|---|---|---|---|
| fantasy-elf-ranger | 36 | 26 | Thalindra Moonwhisper ×7; Thistlewren Moonbrook ×3; Thalion Silverbough ×2 | Thalindra ×8 |
| fantasy-tavern-keeper | 36 | 27 | Bartholomew Thistlewick ×2; Bramwick Thornbottle ×2; Barnaby Hollowbrew ×2 | Bramwick ×6 |
| fantasy-dwarf-smith | 36 | 28 | Thorgrim Ashanvil ×4; Thrain Emberforge ×3; Brondar Ironvein ×2 | Emberforge ×8 |
| fantasy-villain | 36 | 34 | Malachar the Hollow-Crowned ×2; Malachar Vexmoor ×2; Malachar Veyne ×1 | Malachar ×12 |
| fantasy-halfling | 36 | 15 | Pip Thistlewick ×10; Pip Underbough ×10; Wren Thistlebrook ×2 | Pip ×26 |
| fantasy-heroine | 36 | 19 | Seraphine Valcourt ×14; Seraphine Valebright ×4; Seraphine Dawnmere ×2 | Seraphine ×30 |
| grimdark-merc | 36 | 29 | Voss Harrowmere ×4; Veyra Blacktithe ×4; Varek Ashmantle ×2 | Harrowmere ×5 |
| scifi-captain | 36 | 25 | Veyra Solenne ×4; Cassian Veyr ×4; Seraphine Vael-Okonkwo ×3 | Veyra ×7 |
| scifi-scientist | 36 | 26 | Ilvane Okonkwo-Reyes ×6; Ilse Varga ×3; Elara Venn ×3 | Okonkwo ×11 |
| scifi-ai | 36 | 21 | VESPER ×5; MOTHER ×4; VESPER-9 ×4 | VESPER ×9 |
| cyberpunk-netrunner | 36 | 22 | Vex Halloran ×7; Vesper Kade ×4; Zero Mercer ×3 | Vex ×15 |
| cyberpunk-fixer | 36 | 28 | Vesper "Static" Okonkwo-Reyes ×4; Vex Calloway ×3; Vex Moreau ×2 | Okonkwo ×16 |
| horror-sheriff | 36 | 21 | Dale Hargrove ×7; Mara Voss ×5; Dale Harrow ×3 | Dale ×24 |
| horror-1920s | 36 | 31 | Ambrose Whitcombe Hale ×3; Aldous Whitcombe ×2; Alistair Wentworth Crane ×2 | Whitcombe ×15 |
| gothic-victorian | 36 | 25 | Honoria Blackwood ×6; Eleanor Blackwood ×4; Agatha Blackwood ×2 | Blackwood ×17 |
| steampunk-inventor | 36 | 17 | Thaddeus Cogsworth ×8; Cornelius Brassweather ×5; Thaddeus Brasswick ×4 | Thaddeus ×13 |
| western-gunslinger | 36 | 31 | Silas Gravesend ×4; Cassidy Vane ×2; Silas Blackthorn ×2 | Silas ×21 |
| postapoc-warlord | 36 | 32 | Grimjaw the Rustborn ×3; Grimjaw the Rustbound ×2; Gravel-Jaw Morrow ×2 | the ×12 |
| historical-roman | 36 | 12 | Gaius Valerius Crispus ×9; Gaius Valerius Maximus ×9; Marcus Varro ×7 | Gaius ×24 |
| historical-viking | 36 | 20 | Ragnvald Ironhand ×7; Eirik Bloodaxe ×6; Halvard Ironside ×3 | Ragnvald ×19 |
| modern-detective | 36 | 16 | Mara Voss ×8; Marisol Vance ×7; Mara Vance ×4 | Mara ×16 |
| place-tavern | 36 | 19 | The Gilded Wyvern ×7; The Gilded Tankard ×3; The Gilded Badger ×3 | Gilded ×32 |
| place-village | 36 | 8 | Thornwick Hollow ×24; Briarhollow ×4; Thistledown Hollow ×2 | Hollow ×26 |
| place-town-horror | 36 | 14 | Arkham ×11; Sunnyvale ×5; Silent Hill ×5 | Arkham ×11 |
| thing-starship | 36 | 26 | Meridian's Wake ×6; Voidrunner ×4; Vesper's Lament ×3 | Meridian ×15 |
| thing-megacorp | 36 | 23 | Arasaka Dynamics ×9; Arasaka ×3; Arasaka Nexus Dynamics ×3 | Dynamics ×25 |
| thing-guild | 36 | 18 | The Gilded Shadow Syndicate ×6; Shadowmere Syndicate ×5; The Velvet Knives ×5 | Syndicate ×16 |
| thing-cult | 36 | 23 | Crimson Hollow Covenant ×4; The Order of the Hollow Lantern ×4; The Choir of the Hollow Lantern ×4 | Hollow ×29 |
