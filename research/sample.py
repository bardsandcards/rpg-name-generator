#!/usr/bin/env python3
"""Ask models for one name per call, many times, to see what names they default to.

Usage: sample.py claude|codex MODEL DRAWS_PER_PROMPT WORKERS OUT.jsonl
  sample.py claude haiku 10 8 samples.jsonl
  sample.py codex gpt-5 6 6 samples.jsonl

Each call is a fresh session with a plain system prompt and no tools, so nothing but the
model's own habits shapes the answer. One name per call, because a model asked for a list
avoids repeating itself within that list.
"""
import json, subprocess, sys, tempfile, threading
from concurrent.futures import ThreadPoolExecutor

PROMPTS = {
    "fantasy-elf-ranger": "Name an elf ranger player character for a D&D campaign.",
    "fantasy-tavern-keeper": "Name the tavern keeper NPC in a fantasy village.",
    "fantasy-dwarf-smith": "Name a dwarf blacksmith NPC for a fantasy RPG.",
    "fantasy-villain": "Name the villainous necromancer for a fantasy campaign.",
    "fantasy-halfling": "Name a halfling rogue for a D&D game.",
    "fantasy-heroine": "Name a human paladin heroine for a fantasy campaign.",
    "grimdark-merc": "Name a mercenary captain in a grimdark fantasy RPG.",
    "scifi-captain": "Name the captain of a starship in a space opera RPG.",
    "scifi-scientist": "Name a xenobiologist on a research station in a sci-fi RPG.",
    "scifi-ai": "Name the shipboard AI in a sci-fi RPG.",
    "cyberpunk-netrunner": "Name a netrunner in a cyberpunk RPG.",
    "cyberpunk-fixer": "Name a fixer NPC in a cyberpunk RPG.",
    "horror-sheriff": "Name the sheriff of a small town in a modern horror RPG.",
    "horror-1920s": "Name a professor investigator for a 1920s Call of Cthulhu game.",
    "gothic-victorian": "Name a widow in Victorian London for a gothic horror campaign.",
    "steampunk-inventor": "Name an inventor in a steampunk RPG.",
    "western-gunslinger": "Name a gunslinger in a Weird West RPG.",
    "postapoc-warlord": "Name a raider warlord in a post-apocalyptic RPG.",
    "historical-roman": "Name a Roman legionary in a historical RPG set in 100 AD.",
    "historical-viking": "Name a Viking raider in a historical RPG.",
    "modern-detective": "Name a homicide detective in a modern-day mystery game.",
    "place-tavern": "Name a tavern in a fantasy RPG.",
    "place-village": "Name a small village in a fantasy RPG.",
    "place-town-horror": "Name the small American town where a horror RPG is set.",
    "thing-starship": "Name a starship in a sci-fi RPG.",
    "thing-megacorp": "Name a megacorporation in a cyberpunk RPG.",
    "thing-guild": "Name a thieves' guild in a fantasy RPG.",
    "thing-cult": "Name a secret cult in a horror RPG.",
}
SUFFIX = " Reply with only the name, nothing else."
SYSTEM = "You are a helpful assistant."

def claude(model, prompt):
    r = subprocess.run(
        ["claude", "-p", "--model", model, "--system-prompt", SYSTEM,
         "--tools", "", "--setting-sources", "", "--disable-slash-commands", "--no-session-persistence",
         prompt + SUFFIX], capture_output=True, text=True, timeout=180)
    return r.stdout.strip()

def codex(model, prompt):
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False) as fh:
        out = fh.name
    subprocess.run(["codex", "exec", "--ephemeral", "--skip-git-repo-check", "-s", "read-only", "-m", model,
                    "-c", 'model_reasoning_effort="low"', "-o", out,
                    prompt + SUFFIX + " Do not run any commands."],
                   capture_output=True, text=True, timeout=300, stdin=subprocess.DEVNULL)
    with open(out) as fh:
        return fh.read().strip()

def main():
    vendor, model, n, workers, path = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
    fn = claude if vendor == "claude" else codex
    lock = threading.Lock()
    jobs = [(pid, p) for pid, p in PROMPTS.items() for _ in range(n)]

    def run(job):
        pid, p = job
        try:
            ans = fn(model, p)
        except Exception as e:
            ans = f"ERROR {e}"
        with lock, open(path, "a") as fh:
            fh.write(json.dumps({"vendor": vendor, "model": model, "prompt": pid, "answer": ans}) + "\n")

    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(run, jobs))

if __name__ == "__main__":
    main()
