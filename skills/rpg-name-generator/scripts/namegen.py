#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["faker"]
# ///
"""namegen.py: raw name candidates from real-world name data, to reshape by hand afterward.

Examples:
  namegen.py --locales en_GB,de_DE,nl_NL --part full --n 15   # real names from those places
  namegen.py --locales cs_CZ,de_DE --blend --n 15             # new names in that sound (Markov blend)
  namegen.py --seed-file seeds.txt --blend --n 15             # new names in the sound of your own list
  namegen.py --locales de_DE,cs_CZ --part place --blend       # town and village names
  namegen.py --compound --n 10                                # whimsical compound surnames (Copperbottom)
  add --avoid cast.txt to drop anything that sounds like a name already in the campaign
  namegen.py --avoid cast.txt --check "Ostra Vell" "Hollis"   # test names you reshaped by hand

Needs: pip install faker   (not needed for --seed-file without --compound),
       or run it with uv run scripts/namegen.py, which installs faker itself
Locales: Latin-script Faker locales work directly (en_GB, de_DE, nl_NL, fr_FR, it_IT, es_ES,
pt_PT, pl_PL, cs_CZ, sv_SE, no_NO, fi_FI, ...); ja_JP and zh_CN work through Faker's romanized
names. Some locales (e.g. ar_EG) quietly return English names; check the output. For cultures and
eras Faker doesn't cover, find a real name list and use --seed-file.

Seed and avoid files hold one name per line. In a seed file, a line's first word feeds first
names and its last word feeds surnames, so a list of full names works for --part full.
"""
import argparse, difflib, random, sys, unicodedata
from collections import defaultdict

# Names language models reach for again and again, first names and surnames alike
# (see research/). Any word of a candidate matching one of these drops it. Real names a
# period genuinely used a lot (Gaius, Marcus, Eirik) stay out, so historical seed files work.
CLICHES = {
    "elara", "lyra", "kael", "kaelen", "thorne", "seraphina", "aldric", "mira", "vex", "brennan",
    "garrick", "elowen", "aria", "aurora", "finn", "rowan", "sable", "caspian", "cedric", "theron",
    "zephyr", "nyx", "ash", "ember", "silas", "eldrin", "lirael", "kira", "talia", "darian", "jarek",
    "grimm", "grimble", "thistle", "bramble", "corvin", "alaric", "varis", "elric", "lysander",
    "aelar", "thalia", "liora", "kestrel", "wren", "ravenna", "draven", "valen", "selene",
    # fantasy
    "seraphine", "valcourt", "valebright", "thalindra", "thalion", "sylvaris", "moonwhisper",
    "pip", "underbough", "thistlewick", "thistlebrook", "thornwick", "bramwick", "malachar",
    "veyra", "veyr", "harrowmere", "blacktithe", "grimjaw",
    # sci-fi, cyberpunk, modern, horror
    "cassian", "vesper", "venn", "mara", "voss", "vance", "dale", "pruitt", "hargrove", "marisol",
    "calloway", "halloran", "kade", "blackwood", "whitcombe", "thaddeus", "cogsworth", "brasswick",
}
# Words that carry no sound of their own; ignored when comparing names.
STOPWORDS = {"the", "and", "of", "sir", "lady", "lord", "dame", "von", "van", "der", "den", "del",
             "de", "la", "le", "dr", "captain", "mr", "mrs", "miss"}

def is_latin(word):
    return 3 <= len(word) <= 12 and all(
        c.isalpha() and unicodedata.name(c, "").startswith("LATIN") for c in word)

def words(name):
    return [w for w in name.lower().replace("-", " ").split() if len(w) >= 3 and w not in STOPWORDS]

def too_similar(a, b):
    """True if word a would be easy to confuse with word b at the table."""
    return a[:3] == b[:3] or difflib.SequenceMatcher(None, a, b).ratio() >= 0.75

def clashes(name, others):
    return any(too_similar(a, b) for a in words(name) for b in others)

def faker_names(locales, n, part):
    from faker import Faker
    fakes = []
    for loc in locales:
        try:
            f = Faker(loc)
        except AttributeError:
            print(f"namegen: unknown locale {loc}, skipped", file=sys.stderr)
            continue
        kind = "address" if part == "place" else "person"
        source = next(type(pr).__module__ for pr in f.providers if f".{kind}." in type(pr).__module__)
        if not source.endswith(loc):
            print(f"namegen: Faker has no {kind} data for {loc}; it falls back to "
                  f"{source.rsplit('.', 1)[1]}. Use --seed-file for this culture.", file=sys.stderr)
        fakes.append(f)
    if not fakes:
        sys.exit("namegen: no usable locales")
    out, tries = set(), 0
    while len(out) < n and tries < n * 50:
        tries += 1
        f = random.choice(fakes)
        if part == "place":
            raw = f.city_name() if hasattr(f, "city_name") else f.city()
        else:
            kind = "first" if part == "first" else "last"
            romanized = getattr(f, f"{kind}_romanized_name", None)
            raw = romanized() if romanized else getattr(f, f"{kind}_name")()
        tokens = raw.replace("-", " ").split()
        name = max(tokens, key=len) if part == "place" else tokens[0]
        if is_latin(name):
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

def read_seeds(path, part):
    with open(path) as fh:
        lines = [l.split() for l in fh if l.strip()]
    firsts = [l[0] for l in lines]
    lasts = [l[-1] for l in lines if len(l) > 1]
    pool = lasts if part == "last" and lasts else firsts
    return list(dict.fromkeys(pool))

COMPOUND_A = ("tumble hook pocket lock rattle thimble button ditch mud kettle whistle burr fiddle "
              "copper lark nettle pipe ladle").split()
COMPOUND_B = "foot finger toe sleeve wick bottom nose knee spinner snatch trot tip hand skip".split()

def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--locales", default="en_GB", help="comma-separated Faker locales")
    p.add_argument("--part", choices=["first", "last", "full", "place"], default="first")
    p.add_argument("--blend", action="store_true", help="invent new names in the sound of the source")
    p.add_argument("--seed-file", help="one real name per line; replaces --locales as the source")
    p.add_argument("--compound", "--kender", action="store_true", help="compound surnames (Copperbottom)")
    p.add_argument("--avoid", help="file of names already in the campaign; drops anything that sounds like them")
    p.add_argument("--check", nargs="+", metavar="NAME",
                   help="instead of generating, report whether these names clash with --avoid or the clichés")
    p.add_argument("--n", type=int, default=15)
    a = p.parse_args()
    locales = a.locales.split(",")
    avoid = []
    if a.avoid:
        with open(a.avoid) as fh:
            avoid = [w for l in fh for w in words(l)]
    if a.check:
        for nm in a.check:
            hits = [w for w in words(nm) if w in CLICHES]
            hits += [f"{w}~{b}" for w in words(nm) for b in avoid if too_similar(w, b)]
            print(f"{nm}: {'clashes with ' + ', '.join(hits) if hits else 'ok'}")
        return

    def gen(part):
        if a.seed_file:
            seeds = read_seeds(a.seed_file, part)
            pool = markov(seeds, a.n * 3) if a.blend else seeds
        else:
            base = faker_names(locales, 300 if a.blend else a.n * 3, part)
            pool = markov(base, a.n * 3) if a.blend else base
        random.shuffle(pool)
        return pool

    if a.compound:
        names = [f"{first} {random.choice(COMPOUND_A).capitalize()}{random.choice(COMPOUND_B)}"
                 for first in gen("first")[:a.n * 2]]
    elif a.part == "full":
        names = [f"{x} {y}" for x, y in zip(gen("first"), gen("last")) if x != y]
    else:
        names = gen(a.part)

    # Keep names that avoid the clichés, the existing cast and each other, so a batch
    # of new NPCs doesn't hand the table two names that start the same way.
    keep, taken = [], list(avoid)
    for nm in dict.fromkeys(names):
        if any(w in CLICHES for w in words(nm)) or clashes(nm, taken):
            continue
        keep.append(nm)
        taken += words(nm)
        if len(keep) == a.n:
            break
    if len(keep) < a.n:
        print(f"namegen: only {len(keep)} names survived the filters; widen the source or rerun",
              file=sys.stderr)
    print("\n".join(keep))

if __name__ == "__main__":
    main()
