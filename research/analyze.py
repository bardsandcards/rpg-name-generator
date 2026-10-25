#!/usr/bin/env python3
"""Summarize sample.py output: per request, the most common answers and the most repeated word.

Usage: analyze.py samples.jsonl [more.jsonl ...]
"""
import json, re, sys
from collections import Counter, defaultdict

TITLES = re.compile(r"^(Sheriff|Detective|Det\.|Professor|Prof\.|Dr\.|Captain|Capt\.|Mrs\.|Mr\.)\s+")

def clean(answer):
    return TITLES.sub("", answer.strip().splitlines()[0].strip("*\"'. "))

def main():
    rows = [json.loads(l) for f in sys.argv[1:] for l in open(f)]
    by = defaultdict(list)
    for r in rows:
        by[r["prompt"]].append(clean(r["answer"]))
    models = Counter(r["model"] for r in rows)
    print(f"{len(rows)} draws: " + ", ".join(f"{m} {n}" for m, n in models.items()) + "\n")
    print("| Request | Draws | Distinct | Most common answers | Most repeated word |")
    print("|---|---|---|---|---|")
    for prompt, answers in by.items():
        names = Counter(answers)
        words = Counter(w for a in answers for w in set(re.findall(r"[A-Za-z]{3,}", a)) if w != "The")
        top = "; ".join(f"{a} ×{n}" for a, n in names.most_common(3))
        word, n = words.most_common(1)[0]
        print(f"| {prompt} | {len(answers)} | {len(names)} | {top} | {word} ×{n} |")

if __name__ == "__main__":
    main()
