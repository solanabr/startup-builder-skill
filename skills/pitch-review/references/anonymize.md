# Anonymize a single-file HTML deck

The deck this pack renders is one HTML file with one `<section class="slide">` per slide and speaker notes in `<aside class="notes">` ([deck-design-system.md](../../pitch-deck/references/deck-design-system.md), [slide-templates.md](../../pitch-deck/references/slide-templates.md)). Anonymizing it takes three files you write, four commands, and a look at every page. Nothing has to be installed beyond `sed`, `perl`, `grep` and a Chrome or Chromium binary.

The output is a neutral folder holding only what the reader may see: `deck.pdf`, one page per slide, and `notes.txt` for a stage deck. The anonymized HTML stays in a separate work folder that no reader opens.

## 1. Write the swap map and the forbidden list

Pick a fake company name the reader cannot know: an invented word, not a real brand. Then write two files next to the deck, outside the folder any reader will open.

`swaps.sed`, one `s/real/fake/g` per line. Order matters, because `sed` applies the lines top to bottom: full strings before their parts (the email before the domain, "Jane Doe" before "Jane"), and one line per case variant. Escape the dots in domains. Illustrative:

```
s/jane@acmepay\.xyz/founder@tallomer.example/g
s/acmepay\.xyz/tallomer.example/g
s/@acmepay/@tallomer/g
s/Acme Pay/Tallomer/g
s/ACME PAY/TALLOMER/g
s/Jane Doe/R. Castell/g
s/Raj Patel/T. Okafor/g
s/Jane/Rui/g
s/Raj/Teo/g
```

`forbidden.txt`, one term per line: everything that identifies the project, matched later as a whole word and ignoring case. List the bare words, so one line catches every variant:

```
Acme
acmepay
Jane
Doe
Raj
Patel
```

What belongs in both files, on Solana in particular: the company and product names, each founder's first and last name, previous employers named on the team slide, the domain and every email, the X, GitHub, Discord and Telegram handles, program IDs and mint addresses, explorer, Dune and DefiLlama URLs that carry your slug, and the operating-system user name if it is a founder's name. Swap a program ID for a placeholder such as `PROGRAM_ID`, not for another real address.

A term in `forbidden.txt` with no swap in `swaps.sed` makes the leak check fire. That is the test that the map is complete.

## 2. Build the anonymized copy and render it

Set the paths once:

```sh
DECK=deck.html                      # the original, never edited
WORK=~/review-work/r1               # anonymized HTML; no reader opens this
READ=~/review/r1                    # what the readers get; neutral name, outside the project repo
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"   # Linux: google-chrome or chromium
mkdir -p "$WORK" "$READ"
```

Reading deck: apply the swaps, then drop HTML comments, every `<img>` and the speaker notes.

```sh
sed -f swaps.sed "$DECK" \
  | perl -0pe 's/<!--.*?-->//gs; s/<img\b[^>]*>//gis; s/<aside\b[^>]*>.*?<\/aside>//gis' \
  > "$WORK/deck.html"
```

Stage deck, instead of the block above: keep the notes, and give the reader what is said on each slide as numbered lines.

```sh
sed -f swaps.sed "$DECK" \
  | perl -0pe 's/<!--.*?-->//gs; s/<img\b[^>]*>//gis' \
  > "$WORK/deck.html"
perl -0ne 'while (/<section\b.*?<\/section>/gs) { $i++; $s = $&; next unless $s =~ /<aside\b[^>]*>(.*?)<\/aside>/s; ($t = $1) =~ s/<[^>]+>//g; $t =~ s/\s+/ /g; print "$i: $t\n" }' "$WORK/deck.html" > "$READ/notes.txt"
```

Then render one PDF page per slide through the shell's print stylesheet (1920x1080, notes hidden):

```sh
"$CHROME" --headless --no-pdf-header-footer \
  --print-to-pdf="$READ/deck.pdf" "file://$WORK/deck.html"
```

`--no-pdf-header-footer` keeps the browser's print footer, which carries the file URL, off the pages; the shell's zero `@page` margin already does, but a deck with its own print CSS may not. Older Chrome builds call it `--print-to-pdf-no-header`. Both flags: [Chrome for Developers, Headless command line](https://developer.chrome.com/docs/automation-and-testing/headless-cli) (read 2026-10-08).

Use a new pair of folders for every run. Re-running into a folder that already holds an earlier copy mixes versions. Keep both paths absolute and outside the project: a path built from inside the project folder (`acme-pay/../review/r1`) still spells the project name and fails the path check below.

## 3. Leak check

```sh
# Everything the reader could be shown, in source form (grep exits 0 on a match, 1 on none):
grep -rn -i -w -F -f forbidden.txt --include='*.html' --include='*.txt' --include='*.md' "$WORK" "$READ"
case $? in 0) echo "LEAK" ;; 1) echo "clean" ;; *) echo "grep error: check the paths" ;; esac

# The folder path and file names reach the reader too:
printf '%s\n' "$READ" "$READ"/* | grep -i -w -F -f forbidden.txt && echo "LEAK in path"

# Optional, if poppler is installed: the text as rendered, which also catches a name
# split across tags or written as HTML entities:
pdftotext "$READ/deck.pdf" - | grep -i -w -F -f forbidden.txt && echo "LEAK in PDF text"
```

Pass: the first check prints "clean" and the other two print nothing. On a leak, add the missing swap and rebuild into new folders; don't patch the output by hand.

The check is a whole-word match, so a forbidden word that also occurs in ordinary text ("Pay", "Bridge") flags every use. Keep such words out of `forbidden.txt` and list the compound ("Acme Pay") instead.

## 4. Look at every page

`grep` cannot read pixels. Open `deck.pdf` and check each page for a logo, a face, a QR code, a screenshot with the product name, a wallet address in an image, or a CSS background image. The commands drop every `<img>`; if a screenshot carries the argument (a demo), edit the name out of the image and keep it, rather than shipping a deck with the proof missing.

## Spoken script and video

- **Script** (`.md` or `.txt`): `sed -f swaps.sed script.md > "$READ/script.md"`, then the same `grep` on it. The reader takes it block by block.
- **Video**: faces and voices can't be swapped. Test it with people who don't know the company instead, as the SKILL.md says.

## What this does not cover

- Text inside images and CSS backgrounds: step 4.
- What the reader already has in its own context (instructions, memory, paths): [blind-reader.md](blind-reader.md). An anonymized deck read by a reader whose instructions name the company is not a blind read.
