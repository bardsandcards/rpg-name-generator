# Seed list sources

Every name in these files comes from the source listed for it. Retrieved 2026-10-24.
All files: one name per line, title case, no duplicates, single words of 3–12 Latin-script
letters (the same test as `is_latin()` in `scripts/namegen.py`).

The repo's MIT No Attribution licence covers the code. These data files keep their sources'
terms, given below; the ONS and Wikimedia files ask for attribution, which this file provides.

## US given names by birth decade

`us-1880s-female.txt`, `us-1880s-male.txt`, and the same for 1890s, 1900s, 1910s, 1920s (200 each)

- Source: US Social Security Administration, "Baby Names from Social Security Card Applications – National Data", https://www.ssa.gov/oact/babynames/names.zip
- ssa.gov refused this download, so the file was taken from the Internet Archive's copy of that same URL, captured 2026-10-13: https://web.archive.org/web/20261013094148/https://www.ssa.gov/oact/babynames/names.zip (yearly files dated April 2026).
- Licence: US federal government work, public domain in the US.
- Filtering: counts summed per name and sex over the ten years of each decade (e.g. 1880–1889); the top 200 names that pass the length/letter test.
- Limits: many people born before 1937 never applied for a Social Security card, so the early decades undercount people who died young or before then, and names with fewer than 5 births in a year are left out.

## US surnames

`us-surnames.txt` (1000)

- Source: US Census Bureau, "Frequently Occurring Surnames from the 2010 Census", https://www2.census.gov/topics/genealogy/2010surnames/names.zip (`Names_2010Census.csv`)
- Licence: US federal government work, public domain in the US.
- Filtering: the top 1000 by rank that pass the length/letter test (drops two-letter names such as Li, Le, Wu); "Mc" names cased as McDonald.
- Limits: this is the 2010 population, not a historical one. The census drops apostrophes and inner capitals, so O'Brien and MacDonald appear as Obrien and Macdonald. Surnames of later immigration (Garcia, Nguyen) rank far higher than they would in 1880; weight the list by hand for period games.

## England and Wales, 1904

`england-1904-female.txt`, `england-1904-male.txt` (100 each)

- Source: Office for National Statistics, "Top 100 baby names in England and Wales: historical data", https://www.ons.gov.uk/peoplepopulationandcommunity/birthsdeathsandmarriages/livebirths/datasets/babynamesenglandandwalestop100babynameshistoricaldata (file `historicalnames2024.xlsx`, "1904 to 2024", released 31 July 2025), column 1904 of Tables 1 and 2.
- Licence: Source: Office for National Statistics licensed under the Open Government Licence v3.0 (https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/). © Crown copyright 2025.
- Filtering: the 1904 column (the earliest year), rank 1–100, as published.
- Limits: only the top 100 of one year, with exact spellings from birth registration; enough for a seed file, thin for large batches.

## Roman names

`roman-praenomina.txt` (35), `roman-nomina.txt` (1021), `roman-cognomina.txt` (1811)

- Sources (English Wikipedia, via the MediaWiki API):
  - "Praenomen", revision 1375493778 (2026-09-18), section "Latin praenomina › Masculine names": https://en.wikipedia.org/w/index.php?title=Praenomen&oldid=1375493778
  - "List of Roman nomina", revision 1366434904 (2026-07-28): https://en.wikipedia.org/w/index.php?title=List_of_Roman_nomina&oldid=1366434904
  - "List of Roman cognomina", revision 1370154393 (2026-08-19): https://en.wikipedia.org/w/index.php?title=List_of_Roman_cognomina&oldid=1370154393
- Licence: Wikipedia text is CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/); attribution is to the Wikipedia contributors of those revisions (history linked from each page). These files are lists of attested names, extracted with no other text.
- Filtering: the bulleted names only, with links, references, notes and abbreviations removed; "X or Y" and "X/Y" entries give both. Praenomina: the Latin masculine list only (not Faliscan, Oscan or Etruscan). Cognomina: feminine forms dropped, meaning names ending in -a or -tas cited to Nuorluoto's study of women's cognomina, and -a names whose -us form is also listed (Marcella beside Marcellus). That rule also drops a few masculine names that end in -a (Sura, Atta); one entry its editors marked as doubtful (Drusillus) is left out.
- Limits: Wikipedia lists, built by editors from inscriptions and literature; the nomina and cognomina include many names known from a single inscription, and they cover the Republic through late antiquity without saying which is which.

## Old Norse given names

`old-norse-male.txt` (122), `old-norse-female.txt` (32)

- Sources (English Wiktionary, via the MediaWiki API, `list=categorymembers`, main namespace):
  - https://en.wiktionary.org/wiki/Category:Old_Norse_male_given_names
  - https://en.wiktionary.org/wiki/Category:Old_Norse_female_given_names
  - Their subcategories (names from Latin, Old Irish, Celtic etc.) were checked and add no names not already in the parent category.
- Licence: Wiktionary is CC BY-SA 4.0 (https://creativecommons.org/licenses/by-sa/4.0/); attribution is to the Wiktionary contributors. Only the entry titles (the names) are used.
- Filtering: entry titles as spelled (ð, þ, ǫ, accents kept, nominative -r endings kept); titles in runic script dropped.
- Limits: these are the names Wiktionary editors have added entries for, not a census or a runestone corpus; the female list is short, so `--blend` from it repeats quickly. Names are bare given names; add patronymics (Bjarnarson, Bjarnardóttir) by hand.
