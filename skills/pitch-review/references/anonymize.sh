#!/usr/bin/env bash
# Anonymize a single-file HTML deck (or a spoken script) for blind readers, then check it for leaks.
# Documented in anonymize.md, next to this file. Needs perl and, for a deck, Chrome or Chromium;
# pdftotext (poppler) is optional.
#
# Usage: anonymize.sh MODE INPUT SWAPS FORBIDDEN READ_DIR
#   MODE       reading  deck read alone: drops comments, <img> and speaker notes
#              stage    deck with a speaker: drops comments and <img>, notes go to notes.txt
#              paired   deck for the paired comparison: drops comments and notes, keeps <img>
#              script   spoken script (.md or .txt): swaps only, written as script.md
#   INPUT      the original file; it is never edited
#   SWAPS      one "real => fake" pair per line
#   FORBIDDEN  one term per line, no empty line
#   READ_DIR   a new folder for the readers, outside your home and the project (e.g. /tmp/review-r1)
# Env: CHROME       browser binary, if it isn't found on its own
#      CHROME_FLAGS extra flags, e.g. --no-sandbox when running as root (container, CI)
# Last line printed: clean | LEAK | NO PDF | ERROR. Exit 0 clean, 1 leak, 2 anything else.

set -u

fail() { echo "$*" >&2; echo "ERROR"; exit 2; }

[ $# -eq 5 ] || fail "usage: anonymize.sh reading|stage|paired|script INPUT SWAPS FORBIDDEN READ_DIR"
MODE=$1 INPUT=$2 SWAPS=$3 FORBIDDEN=$4 READ=$5
case $MODE in reading|stage|paired|script) ;; *) fail "unknown mode: $MODE" ;; esac
for f in "$INPUT" "$SWAPS" "$FORBIDDEN"; do [ -s "$f" ] || fail "missing or empty file: $f"; done

# 1. Check the two lists before anything is written.
bad=$(perl -CSD -ne 's/\r?\n\z//; next if /^\s*(#|$)/; next if /\S\s*=>\s*\S/; print "$ARGV line $.: expected \"real => fake\"\n"' "$SWAPS")
[ -z "$bad" ] || fail "$bad"
bad=$(perl -CSD -ne 's/\r?\n\z//; print "$ARGV line $.: empty line (it would match everything)\n" if /^\s*$/' "$FORBIDDEN")
[ -z "$bad" ] || fail "$bad"

# 2. A new readers' folder per run; a reused one mixes versions.
if [ -e "$READ" ] && [ -n "$(ls -A "$READ" 2>/dev/null)" ]; then fail "$READ is not empty: use a new folder for every run"; fi
mkdir -p "$READ" || fail "cannot create $READ"
READ=$(cd "$READ" && pwd -P)
case $READ/ in "$HOME"/*) echo "warning: $READ is inside your home folder, and the reader sees this path" >&2 ;; esac
TMPBASE=${TMPDIR:-/tmp}
WORK=$(mktemp -d "${TMPBASE%/}/pitch-work.XXXXXX") || fail "cannot create a work folder"

# 3. Swaps: one pass, longest first, whole words only, case-sensitive, UTF-8 aware.
swap() {
  SWAPS_FILE=$SWAPS perl -CSD -Mutf8 -0777 -pe '
    BEGIN {
      open my $fh, "<:encoding(UTF-8)", $ENV{SWAPS_FILE} or die "cannot read $ENV{SWAPS_FILE}\n";
      local $/ = "\n";
      while (<$fh>) {
        s/\r?\n\z//; next if /^\s*(#|$)/;
        my ($real, $fake) = /^\s*(.*?)\s*=>\s*(.*?)\s*$/;
        $map{$real} = $fake;
      }
      $re = join "|", map { quotemeta } sort { length $b <=> length $a } keys %map;
    }
    s/(?<!\w)($re)(?!\w)/$map{$1}/g;
  ' "$1"
}

if [ "$MODE" = script ]; then
  swap "$INPUT" > "$READ/script.md" || fail "swap failed"
else
  case $MODE in
    reading) STRIP='s/<!--.*?-->//gs; s/<img\b[^>]*>//gis; s/<aside\b[^>]*>.*?<\/aside>//gis' ;;
    stage)   STRIP='s/<!--.*?-->//gs; s/<img\b[^>]*>//gis' ;;
    paired)  STRIP='s/<!--.*?-->//gs; s/<aside\b[^>]*>.*?<\/aside>//gis' ;;
  esac
  swap "$INPUT" | perl -CSD -Mutf8 -0777 -pe "$STRIP" > "$WORK/deck.html" || fail "swap failed"
  if [ "$MODE" = stage ]; then
    perl -CSD -Mutf8 -0777 -ne 'while (/<section\b.*?<\/section>/gs) { $i++; $s = $&; next unless $s =~ /<aside\b[^>]*>(.*?)<\/aside>/s; ($t = $1) =~ s/<[^>]+>//g; $t =~ s/\s+/ /g; $t =~ s/^ | $//g; print "$i: $t\n" }' \
      "$WORK/deck.html" > "$READ/notes.txt"
  fi

  # 4. One PDF page per slide through the deck's print CSS.
  if [ -z "${CHROME:-}" ]; then
    for c in "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
             "/Applications/Chromium.app/Contents/MacOS/Chromium" \
             google-chrome google-chrome-stable chromium chromium-browser; do
      if command -v "$c" >/dev/null 2>&1; then CHROME=$(command -v "$c"); break; fi
    done
  fi
  [ -n "${CHROME:-}" ] || fail "no Chrome or Chromium found: set CHROME=/path/to/binary"
  # CHROME_FLAGS is split on spaces on purpose, so it can carry more than one flag.
  # shellcheck disable=SC2086
  "$CHROME" --headless ${CHROME_FLAGS:-} --no-pdf-header-footer \
    --print-to-pdf="$READ/deck.pdf" "file://$WORK/deck.html" > "$WORK/chrome.log" 2>&1
  if ! test -s "$READ/deck.pdf"; then
    tail -n 5 "$WORK/chrome.log" >&2
    echo "Chrome wrote no PDF. Running as root? Set CHROME_FLAGS=--no-sandbox." >&2
    echo "NO PDF"; exit 2
  fi
fi

# 5. Leak check: everything the reader could see, in source form, as rendered, and in the path.
printf '%s\n' "$READ" "$READ"/* > "$WORK/reader-path.txt"
CHECK=("$WORK/reader-path.txt")
[ -f "$WORK/deck.html" ] && CHECK+=("$WORK/deck.html")
for f in "$READ"/*.txt "$READ"/*.md; do [ -f "$f" ] && CHECK+=("$f"); done
if [ -f "$READ/deck.pdf" ]; then
  if command -v pdftotext >/dev/null 2>&1; then
    pdftotext -enc UTF-8 "$READ/deck.pdf" "$WORK/deck.pdf.txt" && CHECK+=("$WORK/deck.pdf.txt")
  else
    echo "pdftotext not found: the rendered text was not checked (optional; install poppler)" >&2
  fi
fi

echo "Readers' folder: $READ"
echo "Work folder (no reader opens it): $WORK"
FORBIDDEN_FILE=$FORBIDDEN perl -CSD -Mutf8 -ne '
  BEGIN {
    open my $fh, "<:encoding(UTF-8)", $ENV{FORBIDDEN_FILE} or die "cannot read $ENV{FORBIDDEN_FILE}\n";
    my @t; while (<$fh>) { s/\r?\n\z//; s/^\s+|\s+$//g; push @t, $_ if length }
    $re = join "|", map { quotemeta } sort { length $b <=> length $a } @t;
  }
  while (/(?<!\w)($re)(?!\w)/gi) { print "$ARGV:$.: $1\n"; $hits++ }
  close ARGV if eof;
  END { $? = $hits ? 1 : 0 }
' "${CHECK[@]}"
case $? in
  0) echo "clean"; exit 0 ;;
  1) echo "LEAK"; exit 1 ;;
  *) echo "ERROR"; exit 2 ;;
esac
