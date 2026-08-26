#!/usr/bin/env python3
'''audit-summary.py — surface-scoped noise detector for summaries / status updates.

Usage:
    audit-summary.py <file.md> --surface {advisor,partner,buyer,self}

Exit codes: 0 = no findings, 1 = findings, 2 = could not read / nothing to scan.

Skipped by design: YAML frontmatter and every '>' quote block. Those carry operator
scaffolding (what was cut and why), which must never be flagged.

SEVEN THINGS THIS SCRIPT CANNOT SEE (the judgment stays with the reader):
  1. whether the lead line actually carries the delta since the recipient last looked
  2. whether something CUT should have stayed (the expensive error; silence hides it)
  3. whether a number's stated reading is the right reading
  4. whether an open question was already answered by the recipient (the stale-queue trap)
  5. whether an item is finished-and-therefore-irrelevant to this recipient
  6. whether the asks are ordered so the most important one is read first
  7. tone, register (Ty/Pani), grammar, AI-tells — that is human-language-check
'''

import argparse
import re
import sys

# --- detector dictionaries (all constants live here, not inside functions) ---

# D1: operator-process leaks. Narrow on purpose: bare 'split' also means 'split by
# production cost', which is legitimate product description on every surface.
PROCESS_LEAK = [
    (r'\b(70/30|80/20)\b', 'split przychodow'),
    (r'(?i)\b(revenue split|podzia\w* przychod\w*)', 'split przychodow'),
    (r'(?i)\b(GO/NIE-GO|GO/NO-GO)\b', 'brama GO/NIE-GO'),
    (r'(?i)blok po bloku|section by section', 'przejscie blok po bloku'),
    (r'(?i)\brund\w* poprawek|rounds of (deck )?fixes', 'rundy poprawek'),
    (r'(?i)audyt (ukladu|układu|slajd\w*)|layout audit', 'audyt ukladu'),
    (r'(?i)\bTrello\b|\bNotion\b(?! link)', 'narzedzie operatora'),
    (r'(?i)\bhipotez\w*|\bhypothesis\b', 'status hipotezy'),
    (r'(?i)wariant\w* odrzucon\w*|rejected variant', 'odrzucony wariant'),
    (r'(?i)\bgit commit\b|\bsubagent\b|\bsystem prompt\b|\.claude/', 'warstwa narzedziowa'),
    (r'(?i)nota wiedzy|knowledge note', 'nazwa noty wiedzy'),
]

# D2: the surface talking about itself instead of its topic.
DOC_META = [
    (r'(?i)(tabel|list|sekcj|wykres|diagram|kolumn)\w*\s+(powyżej|poniżej|powyzej|ponizej)',
     'nawigacja po dokumencie'),
    (r'(?i)(the )?(table|list|chart|section) (below|above)', 'nawigacja po dokumencie'),
    (r'(?i)na (nastepn|następn)\w*\s+(slajdzie|ekranie|stronie)', 'zapowiedz struktury'),
    (r'(?i)jak (mowilem|mówiłem|wspominalem|wspominałem)|as I (mentioned|said)',
     'odwolanie do wlasnej narracji'),
    (r'(?i)\bkolor\w*\s+(oznacza|znaczy)|color (means|indicates)', 'legenda komponentu'),
    (r'(?i)w tej sekcji (opisuj|przedstawiam)|in this section I', 'opis wlasnej struktury'),
    (r'(?i)każd\w* (slajd|ekran|sekcja) (pokazuje|zawiera)', 'zapowiedz struktury'),
]

# D3: promises about US instead of what the recipient GETS. Buyer surface only —
# on a partner surface these describe the partner's own burden and are signal.
ABOUT_US = [
    (r'(?i)nic nie jest (rozciagane|rozciągane)', 'obietnica o nas, nie o korzysci'),
    (r'(?i)\b(zawsze )?(dbamy|pilnujemy|nie robimy|nigdy nie)\b', 'zdanie o naszej dyscyplinie'),
    (r'(?i)\bwe (always|never) \w+', 'zdanie o naszej dyscyplinie'),
    (r'(?i)\bnasz\w* (proces|dyscyplin\w*|standard\w*)', 'nasz proces w copy'),
]

# D4: markers that must not leave on a recipient-facing surface.
UNRESOLVED = [
    (r'\[do potwierdzenia\]', 'niepotwierdzona teza'),
    (r'\b(TODO|TBD|FIXME|XXX)\b', 'placeholder'),
    (r'\?\?\?', 'placeholder'),
    (r'<[a-ząćęłńóśźż /|-]{2,40}>', 'nieuzupelniony slot szablonu'),
]

SURFACES = {
    'advisor': ['D1', 'D2', 'D4', 'D5'],
    'partner': ['D1', 'D2', 'D4', 'D5'],
    'buyer':   ['D1', 'D2', 'D3', 'D4'],
    'self':    ['D2'],
}


def body_lines(text):
    '''Return [(lineno, line)] with frontmatter and '>' blocks removed.'''
    lines = text.splitlines()
    out = []
    i = 0
    if lines and lines[0].strip() == '---':
        i = 1
        while i < len(lines) and lines[i].strip() != '---':
            i += 1
        i += 1
    fence = False
    for n in range(i, len(lines)):
        raw = lines[n]
        if raw.lstrip().startswith('```'):
            fence = not fence
            continue
        if fence:
            continue
        if raw.lstrip().startswith('>'):
            continue
        out.append((n + 1, raw))
    return out


def scan(patterns, code, lines):
    hits = []
    for lineno, line in lines:
        if not line.strip():
            continue
        for rx, label in patterns:
            m = re.search(rx, line)
            if m:
                hits.append((code, lineno, label, m.group(0).strip()))
                break
    return hits


def structure(text, lines):
    hits = []
    head = text.splitlines()[:40]
    if not any(l.lstrip().startswith('>') for l in head):
        hits.append(('D5', 0, 'brak bloku scaffoldingu (co wyciete i dlaczego)', '-'))
    if not any('?' in l for _, l in lines):
        hits.append(('D5', 0, 'zero pytan w tekscie - nie ma o co poprosic', '-'))
    return hits


def main():
    ap = argparse.ArgumentParser(description='Surface-scoped noise detector for summaries.')
    ap.add_argument('file')
    ap.add_argument('--surface', required=True, choices=sorted(SURFACES))
    args = ap.parse_args()

    try:
        with open(args.file, encoding='utf-8') as fh:
            text = fh.read()
    except OSError as exc:
        print('BLAD: nie mozna odczytac pliku: %s' % exc, file=sys.stderr)
        return 2

    lines = body_lines(text)
    if not lines:
        print('BLAD: po odjeciu frontmatteru i blokow > nie zostalo nic do skanowania.',
              file=sys.stderr)
        return 2

    active = SURFACES[args.surface]
    hits = []
    if 'D1' in active:
        hits += scan(PROCESS_LEAK, 'D1', lines)
    if 'D2' in active:
        hits += scan(DOC_META, 'D2', lines)
    if 'D3' in active:
        hits += scan(ABOUT_US, 'D3', lines)
    if 'D4' in active:
        hits += scan(UNRESOLVED, 'D4', lines)
    if 'D5' in active:
        hits += structure(text, lines)

    names = {'D1': 'wyciek procesu operatora', 'D2': 'powierzchnia mowi o sobie',
             'D3': 'obietnica o nas', 'D4': 'nierozstrzygniety marker',
             'D5': 'struktura'}
    print('%s  [surface=%s]' % (args.file, args.surface))
    print('detektory aktywne: %s' % ', '.join(active))
    for code, lineno, label, frag in sorted(hits, key=lambda h: (h[1], h[0])):
        where = ('linia %d' % lineno) if lineno else 'caly plik'
        print('  %s %-28s %-11s %s | %s' % (code, names[code], where, label, frag))
    if not hits:
        print('  brak trafien')
    print('---')
    print('Cisza nie jest sukcesem: przeskanowano %d linii tresci, %d trafien. '
          'Zero trafien nie znaczy, ze podsumowanie jest dobre - siedem rzeczy '
          'niewidocznych dla skryptu wypisano w docstringu tego pliku.'
          % (len(lines), len(hits)))
    return 1 if hits else 0


if __name__ == '__main__':
    sys.exit(main())
