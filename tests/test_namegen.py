"""Behavior tests for namegen.py, run through its command line the way the skill runs it."""
import os, subprocess, sys, tempfile, unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILL = os.path.join(ROOT, "skills", "rpg-name-generator")
SCRIPT = os.path.join(SKILL, "scripts", "namegen.py")

DWARVES = """Thorin Oakenshield
Balin Fundinul
Dwalin Fundinul
Gloin Groinul
Bifur Hammerhand
Bofur Stonebrow
Bombur Barrelside
Dori Ironfoot
Nori Coalbeard
Ori Quillsmith
Fili Durinson
Kili Ashdelver
Dain Ironfoot
Thrain Throrul
Fundin Flintvein
Nain Copperhelm
"""


def run(*args):
    r = subprocess.run([sys.executable, SCRIPT, *args], capture_output=True, text=True, check=True)
    return r.stdout.splitlines(), r.stderr


def tmpfile(text):
    fh = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False)
    fh.write(text)
    fh.close()
    return fh.name


class SeedFiles(unittest.TestCase):
    def test_full_names_never_pair_a_name_with_itself(self):
        seeds = tmpfile("\n".join(l.split()[0] for l in DWARVES.splitlines()))
        for _ in range(20):
            names, _ = run("--seed-file", seeds, "--part", "full", "--n", "10")
            for nm in names:
                first, last = nm.split()
                self.assertNotEqual(first, last, nm)

    def test_full_names_take_surnames_from_the_last_word(self):
        seeds = tmpfile(DWARVES)
        surnames = {l.split()[-1] for l in DWARVES.splitlines()}
        names, _ = run("--seed-file", seeds, "--part", "full", "--n", "5")
        self.assertTrue(names)
        for nm in names:
            self.assertIn(nm.split()[1], surnames)


class Filters(unittest.TestCase):
    def test_cliche_surnames_are_dropped(self):
        seeds = tmpfile("Dale Thorne\nMara Voss\nJonas Bell\nPetra Vance\nOtto Kraus\n")
        names, _ = run("--seed-file", seeds, "--part", "full", "--n", "5")
        for nm in names:
            self.assertNotIn(nm.split()[1], {"Thorne", "Voss", "Vance"})

    def test_avoid_blocks_names_that_sound_like_any_word_of_the_cast(self):
        cast = tmpfile("Captain Ilse Marten\nThe Widow Calloway\n")
        seeds = tmpfile("Ilsa\nCallow\nMartina\nHollis\nBrandt\nOdile\n")
        names, _ = run("--seed-file", seeds, "--avoid", cast, "--n", "6")
        self.assertEqual(sorted(names), ["Brandt", "Hollis", "Odile"])

    def test_a_batch_never_repeats_a_first_sound(self):
        seeds = tmpfile("Hollis\nHolland\nHolger\nBrandt\nBranwen\nOdile\nPetra\n")
        for _ in range(20):
            names, _ = run("--seed-file", seeds, "--n", "7")
            prefixes = [nm.lower()[:3] for nm in names]
            self.assertEqual(len(prefixes), len(set(prefixes)), names)


class Check(unittest.TestCase):
    def test_check_reports_clashes_and_clean_names(self):
        cast = tmpfile("Captain Ilse Marten\n")
        out, _ = run("--avoid", cast, "--check", "Hollis Brandt", "Ilsa Moor", "Dale Pruitt")
        self.assertEqual(out[0], "Hollis Brandt: ok")
        self.assertIn("ilsa~ilse", out[1])
        self.assertIn("dale", out[2])
        self.assertIn("pruitt", out[2])


try:
    import faker  # noqa: F401
    HAVE_FAKER = True
except ImportError:
    HAVE_FAKER = False


@unittest.skipUnless(HAVE_FAKER, "faker not installed")
class Locales(unittest.TestCase):
    def test_locale_without_data_warns_about_the_english_fallback(self):
        _, err = run("--locales", "ar_EG", "--n", "3")
        self.assertIn("falls back to en_US", err)

    def test_places_come_back_as_single_words(self):
        names, _ = run("--locales", "de_DE,cs_CZ", "--part", "place", "--n", "10")
        self.assertEqual(len(names), 10)
        for nm in names:
            self.assertNotIn(" ", nm)


class SeedLists(unittest.TestCase):
    def test_every_bundled_seed_list_yields_names(self):
        seeds = os.path.join(SKILL, "seeds")
        files = sorted(f for f in os.listdir(seeds) if f.endswith(".txt"))
        self.assertTrue(files)
        for f in files:
            names, _ = run("--seed-file", os.path.join(seeds, f), "--n", "10")
            self.assertGreaterEqual(len(names), 5, f)


if __name__ == "__main__":
    unittest.main()
