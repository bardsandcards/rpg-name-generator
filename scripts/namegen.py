#!/usr/bin/env python3
"""namegen.py: raw name candidates from real-world name data, to reshape by hand afterward.

Examples:
  namegen.py --locales en_GB,de_DE,nl_NL --part full --n 15   # real names from those places
  namegen.py --locales cs_CZ,de_DE --blend --n 15             # new names in that sound (Markov blend)
  namegen.py --seed-file seeds.txt --blend --n 15             # new names in the sound of your own list
  namegen.py --compound --n 10                                # whimsical compound surnames (Copperbottom)
  add --avoid existing.txt to drop anything sharing its first three letters with an existing name

Needs: pip install faker   (not needed for --seed-file without --compound)
Locales: Latin-script Faker locales work directly (en_GB, de_DE, nl_NL, fr_FR, it_IT, es_ES,
pt_PT, pl_PL, cs_CZ, sv_SE, no_NO, fi_FI, ...); ja_JP works through Faker's romanized names.
Some locales (e.g. ar_EG) quietly return English names; check the output. For cultures Faker
doesn't cover in Latin script, find a real name list and use --seed-file.
"""
import argparse, random, re, sys
from collections import defaultdict

# Names language models reach for again and again. Never offer these.
CLICHES = {
    "elara", "lyra", "kael", "kaelen", "thorne", "seraphina", "aldric", "mira", "vex", "brennan",
    "garrick", "elowen", "aria", "aurora", "finn", "rowan", "sable", "caspian", "cedric", "theron",
    "zephyr", "nyx", "ash", "ember", "silas", "eldrin", "lirael", "kira", "talia", "darian", "jarek",
    "grimm", "grimble", "thistle", "bramble", "corvin", "alaric", "varis", "elric", "lysander",
    "aelar", "thalia", "liora", "kestrel", "wren", "ravenna", "draven", "valen", "selene",
}
LATIN = re.compile(r"[A-Za-zÀ-ÿĀ-žŁłŚśŹźŻżĆćŃńÓóĘęĄą']{3,12}")

def faker_names(locales, n, part):
    from faker import Faker
    fakes = []
    for loc in locales:
        try:
            fakes.append(Faker(loc))
        except AttributeError:
            print(f"namegen: unknown locale {loc}, skipped", file=sys.stderr)
    if not fakes:
        sys.exit("namegen: no usable locales")
    out, tries = set(), 0
    while len(out) < n and tries < n * 50:
        tries += 1
        f = random.choice(fakes)
        romanized = getattr(f, f"{'first' if part == 'first' else 'last'}_romanized_name", None)
        try:
            raw = romanized() if romanized else (f.first_name() if part == "first" else f.last_name())
        except AttributeError:
            raw = f.first_name() if part == "first" else f.last_name()
        name = raw.split()[0].split("-")[0]
        if LATIN.fullmatch(name):
            out.add(name.capitalize() if name.isupper() else name)
    if len(out) < n // 3:
        print(f"namegen: only {len(out)} usable {part} names from {','.join(locales)}; "
              "a non-Latin locale? Try --seed-file with a real name list.", file=sys.stderr)
    return list(out)

def markov(seeds, n, order=2):
    seeds = [s.lower() for s in seeds if len(s) >= 3]
    if not seeds:
        sys.exit("namegen: no usable seeds (need names of 3+ letters)")
    if len(seeds) < 10:
        print("namegen: fewer than 10 seeds; expect thin, repetitive results", file=sys.stderr)
    chains = defaultdict(list)
    for s in seeds:
        s = "^" * order + s + "$"
        for i in range(len(s) - order):
            chains[s[i:i + order]].append(s[i + order])
    out, real, tries = set(), set(seeds), 0
    while len(out) < n and tries < n * 200:
        tries += 1
        k, w = "^" * order, ""
        while True:
            nxt = chains.get(k)
            if not nxt:
                break
            c = random.choice(nxt)
            if c == "$" or len(w) > 11:
                break
            w += c
            k = k[1:] + c
        if 4 <= len(w) <= 10 and w not in real:
            out.add(w.capitalize())
    return list(out)

COMPOUND_A = ("tumble hook pocket lock rattle thimble button ditch mud kettle whistle burr fiddle "
              "copper lark nettle pipe ladle").split()
COMPOUND_B = "foot finger toe sleeve wick bottom nose knee spinner snatch trot tip hand skip".split()

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--locales", default="en_GB", help="comma-separated Faker locales")
    p.add_argument("--part", choices=["first", "last", "full"], default="first")
    p.add_argument("--blend", action="store_true", help="invent new names in the sound of the source")
    p.add_argument("--seed-file", help="one real name per line; replaces --locales as the source")
    p.add_argument("--compound", "--kender", action="store_true", help="compound surnames (Copperbottom)")
    p.add_argument("--avoid", help="file of existing names; drops candidates sharing the first 3 letters")
    p.add_argument("--n", type=int, default=15)
    a = p.parse_args()
    locales = a.locales.split(",")
    avoid = set()
    if a.avoid:
        with open(a.avoid) as fh:
            avoid = {l.strip().lower()[:3] for l in fh if l.strip()}

    def gen(part):
        if a.seed_file:
            with open(a.seed_file) as fh:
                seeds = [l.strip() for l in fh if l.strip()]
            return markov(seeds, a.n * 3) if a.blend else seeds
        base = faker_names(locales, 300 if a.blend else a.n * 3, part)
        return markov(base, a.n * 3) if a.blend else base

    if a.compound:
        firsts = gen("first")
        random.shuffle(firsts)
        names = [f"{first} {random.choice(COMPOUND_A).capitalize()}{random.choice(COMPOUND_B)}"
                 for first in firsts[:a.n * 2]]
    elif a.part == "full":
        names = [f"{x} {y}" for x, y in zip(gen("first"), gen("last"))]
    else:
        names = gen(a.part)
    keep = [nm for nm in dict.fromkeys(names)
            if nm.lower().split()[0] not in CLICHES and nm.lower()[:3] not in avoid]
    random.shuffle(keep)
    print("\n".join(keep[:a.n]))

if __name__ == "__main__":
    main()
