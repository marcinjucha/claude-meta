---
description: "Ulepsz PROCES wykonywalny przez człowieka — lekcje sesji + rozjazd instancja↔źródło → dedup → werdykty → bramka blok po bloku → zapis. Usage: /improve-process [etap|twórca]"
argument-hint: [etap|twórca]
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Task
---

# /improve-process — ulepszanie checklisty procesu, nie notatki twórcy

Komenda bierze to, czego nauczył się TEN przebieg pracy, i nanosi to na **checklistę procesu**
w `03-Resources/<ctx>/procesy/<etap>.md` — dom procesu wykonywalnego przez CZŁOWIEKA, trzeciej
kategorii obok pamięci projektu i wiedzy domenowej (podstawa: wiersz „proces wykonywalny" w tabeli
„Co gdzie ląduje" w `_system/knowledge-system.md`).

**Jedna reguła nad wszystkimi: TREŚĆ idzie tylko do źródła.** W instancji (notatce twórcy) komenda
zapisuje wyłącznie **jednolinijkowy marker decyzji** o źródle. WHY: bez markera Faza 2 nie ma pamięci
i przy każdym przebiegu podnosi ten sam rozjazd do arbitrażu w nieskończoność — marker jest tym, co
sprawia, że rozjazd ZBIEGA.

`$ARGUMENTS` = etap pipeline'u albo nazwa twórcy (opcjonalny; brak → Faza 0 pyta).
Silnik mózgu (config/skrypty): `/Users/marcinjucha/Prywatne/projects/brain-vault/.brain`.

## Fazy

```
0: Preflight — <ctx>/<etap>/<źródło>/<instancja>/<memory>, tryb, inwentarz   (INLINE, zawsze)
1: Lekcje z TEJ sesji — 0–3 kandydatów z CYTATEM                            (INLINE, gated)
2: Rozjazd instancja ↔ źródło — skrypt + semantyka                (SKRYPT + so-agent, gated)
3: DEDUP przez 5 powierzchni — skrypt + osąd                     (SKRYPT + INLINE, BLOKUJĄCA)
4: Werdykty — ❌ / PUNKT DECYZYJNY / nowy KROK / LOKALNE                      (INLINE, zawsze)
5: Bramka hybrydowa — jedna pozycja na turę, „jest" → „będzie"               (INLINE, zawsze)
6: Zapis — źródło inline, skille przez ai-manager-agent, marker, MOC   (INLINE + agent)
7: Raport — 6 punktów, stała numeracja                                       (INLINE, zawsze)
```

**Kolejność jest WYMUSZONA. Trzy sprzężenia:**
- **1 → 3:** kandydat bez `origin` nie da się zdedupować — Faza 3 musi wiedzieć, z którego pliku
  kandydat przyszedł, żeby pominąć jego własne źródło (inaczej odrzuci kandydata jako duplikat
  samego siebie).
- **2 → 4:** rozjazd bez semantyki wchodzi do werdyktu jako „brak pozycji", a to nieprawda — pozycja
  bywa obecna, tylko przeformułowana.
- **3 → 5:** do bramki nie wchodzi nic, czego dedup nie przepuścił. Pozycja z trafieniem idzie do
  bramki jako WSKAŻ albo ROZSZERZ U WŁAŚCICIELA, nigdy jako nowa treść.

## ⚠️ KRYTYCZNE: MUSISZ WYWOŁYWAĆ AGENTÓW

```
NIE:
❌ JAKAKOLWIEK delegacja Fazy 1 — także `subagent_type: "fork"`, którego na tej maszynie nie ma
❌ Agent(subagent_type: "general-purpose") dla Fazy 2
❌ opisywać, co zwróciłby agent, zamiast go wywołać
❌ zapisywać SKILL.md inline w orkiestratorze

TAK:
✅ Faza 1 INLINE — źródłem jest TA konwersacja, a agenta dziedziczącego ją tu NIE MA
✅ Agent(subagent_type: "so-agent") dla Fazy 2 — semantykę czyta doktryna, nie grep
✅ Agent(subagent_type: "ai-manager-agent"), jeden na JEDEN plik, dla zapisów do skilli (Faza 6)
✅ Fazy 0, 3, 4, 5, 7 i zapis do źródła inline
```

## Krytyczne reguły

**1. Faza 1 jest INLINE.** Orkiestrator sam wypisuje kandydatów z TEJ konwersacji. Delegacja
dopuszczalna WYŁĄCZNIE do agenta dziedziczącego kontekst sesji; na tej maszynie taki agent
**nie istnieje** (`~/.claude/agents/`: ai-manager-agent, brain-manager · `claude-marketing/agents/`:
mrk-agent, so-agent), więc **delegacji w Fazie 1 nie ma**. Świeży agent w Fazie 1 = wymyślone lekcje.
Źródłem lekcji jest bieżąca konwersacja, której świeży agent nie widzi — zwróci puste albo wymyślone.
**Precedens, nie hipoteza:** wrapper `/ai-extract-memory` delegował do ŚWIEŻEGO agenta z instrukcją
„analyze the current conversation" — naprawione 2026-08-04. Cała rodzina `ai-*` nadal deleguje do
świeżych agentów, więc pierwszy przebieg będzie chciał dopasować się do tego zakazanego wzorca.

**2. Faza 2 czyta SEMANTYKĘ, nie ID — i dlatego idzie przez `so-agent`.**
Diff po ID zwróci czysto i BĘDZIE KŁAMAŁ. Zmierzone: `kacper-snela-walidacja.md` ma 356 linii i
4 checkboxy; `kacper-snela-nastepne-kroki.md` — 570 linii, 114 checkboxów, a jego własna reguła
„nadpisuj, nie dopisuj obok" była łamana trzy sesje z rzędu. To bliźniak buga „SUMA 0 słów" czytanego
jako czysty przebieg. Odróżnienie PROMUJ od PUNKTU DECYZYJNEGO wymaga doktryny `so-*`, której
`general-purpose` nie ma i nie doładuje.

**3. Faza 3 (DEDUP) jest BLOKUJĄCA i jej negatyw musi być MECHANICZNY.**
Lista miejsc przeszukanych z zerem trafień jest wiarygodna tylko wtedy, gdy generuje ją skrypt,
nie model. Brak skryptu → faza raportuje wprost „dedup modelowy, nie mechaniczny" i przebieg
NIE twierdzi, że gdzieś nie ma tej tezy.

**4. Faza 2 jest NIEBLOKUJĄCA, Faza 3 jest.** Rozjazd, którego nie umiemy przeczytać mechanicznie,
raportujemy jako UNANCHORED i idziemy dalej. Duplikat, którego nie sprawdziliśmy, zatrzymuje przebieg.
WHY asymetria: nieprzeczytany rozjazd kosztuje jeden pominięty wpis, nieodkryty duplikat kosztuje
rozjechanie dwóch źródeł prawdy o tej samej tezie.

**5. Cytat vs odczytanie — każde pole oznaczone.** `[CYTAT]` = literalne słowa z sesji / pliku /
kanonu. `[MOJE ODCZYTANIE]` = moja inferencja. Parafraza podana jako cytat to **błąd przebiegu, nie
styl**. WHY: silna i słaba pozycja podane bez etykiety trafiają do bramki z tą samą powagą, a te
oparte na moim odczytaniu są dokładnie tym, co Marcin chce rozstrzygać sam.

**6. Pytania kontrolne po KAŻDEJ fazie agentowej i po Fazie 0.** Parafraza DECYZJI (2–3 zdania,
nie streszczenie wyjścia agenta) + **3–5 pytań skalowanych złożonością** (proste 3, złożone 5),
zamkniętych i konkretnych („dla X bierzemy A czy B?", nie „czy dobrze?"). Dopiero po potwierdzeniu
oferuj komendy.

**7. Zero kandydatów i zero rozjazdów to POPRAWNY, częsty wynik.** Przebieg, który promuje wszystko
do nowych kroków, jest **raportem awarii** — znaczy, że nie sprawdzono istniejących kroków przy
zmierzonych przesłankach (Faza 4a) albo pominięto dedup.

**8. Nigdy nie twórz nowego pliku procesu przy niejednoznaczności.** Niejednoznaczny etap → STOP
i pytanie. Cichy fallback do „najbliższego" pliku podszywa zapis pod zły cel, a przebieg wygląda
na udany (ta sama reguła co `/brain-finish` Faza 0(a)).

**Brak fazy „Knowledge Capture" na końcu — świadomie.** Ta komenda W CAŁOŚCI jest fazą knowledge
capture; osobna faza pytałaby, czego nauczył się przebieg ulepszający proces o ulepszaniu procesu.
Lekcje o samej komendzie idą normalną ścieżką: `/ai-extract-memory` → `<memory>`.

**Bramka autorefleksji tylko dla faz z RĘCZNIE budowanym kontekstem** (Faza 2 i zapisy Fazy 6):
przed wywołaniem zadaj sobie 2–3 pytania sokratejskie („co ten agent źle zrozumie, mając tylko ten
wycinek?", „która przesłanka mojego routingu jest założona, nie zmierzona?"), odpowiedz i wnioski
WŁÓŻ DO PROMPTU. Faza 1 jest z tego wyjęta — jest inline, więc nie ma promptu do dopasowania.

---

## Faza 0 — Preflight (INLINE, zawsze)

(a) **Rozwiąż i przekaż dalej JAKO WARTOŚCI:**

| Wartość | Jak rozwiązać |
|---|---|
| `<ctx>` | `$ARGUMENTS` > cwd → `config.json` `.paths`; domyślnie `shadow-operator` |
| `<etap>` | **CYTAT** z `01-Projects/shadow-operator/_shadow-operator.md` §Pipeline (8 etapów, przy każdym skill) — jedyna istniejąca mapa etapów |
| `<źródło>` | `03-Resources/<ctx>/procesy/<etap>.md` — checklista właściciela |
| `<instancja>` | **WYŁĄCZNIE** `01-Projects/<ctx>/<twórca>/<twórca>-proces-<etap>.md` — kopia źródła z zachowanymi nagłówkami `### P-…`. To **NIE** jest `<twórca>-nastepne-kroki.md`: notatka robocza nie nosi ID, więc `--diff` na niej zwraca sam UNANCHORED. Plik nie istnieje → `<instancja>` = **BRAK**, tryb wymuszony na LEKCJA, Faza 2 = SKIPPED (powód: „brak kopii procesu"), Faza 6(c) pomijana. |
| `<memory>` | `01-Projects/<ctx>/memory.md` — **obowiązkowo w kontrakcie** |
| tryb | LEKCJA (tylko Faza 1) / ROZJAZD (tylko Faza 2) / OBA |

`<memory>` jest w kontrakcie, bo `01-Projects/shadow-operator/CLAUDE.md` wymaga, by wołający podał
**rozwiązaną per-kontekst ścieżkę** — komenda nie ma prawa jej domyślać z cwd.

**`<źródło>` rozwiązuj GLOBEM, nie sklejaniem nazwy.** Zrób `03-Resources/<ctx>/procesy/*.md`
i dopasuj po polu frontmattera `etap:` (w `launch-tworcy.md` jest
`etap: "7 — launch (so-pilot-launch → so-launch-sequence)"`). **NIGDY** nie buduj nazwy pliku przez
sklejenie cytatu z §Pipeline. Zero dopasowań **oraz** jednoznaczny etap → dopiero wtedy Faza 0(c).
Dwa dopasowania → STOP i pytanie (Reguła 8).

WHY: dla etapu launch sklejanie daje `procesy/launch.md` albo `procesy/7. so-pilot-launch….md` —
żadnego z nich nie ma, a jedyny istniejący plik nazywa się `launch-tworcy.md`. Skutek sklejania:
albo STOP przy gotowym procesie, albo Faza 0(c) zakłada DRUGI plik o launchu w dniu pierwszego użycia.

(b) **Inwentarz kroków źródła — ze SKRYPTU, nie z czytania pliku:**
```bash
python3 /Users/marcinjucha/Prywatne/projects/brain-vault/.brain/scripts/procesy-scan.py \
  --inventory <źródło>
```
Zwraca: **ID + KIEDY + PRZESŁANKI** (skrócone, z zachowanymi etykietami `[ZMIERZONA]` /
`[ZAŁOŻONA]` / `[MOJE ODCZYTANIE]`) **+ licznik ❌** — to wystarcza Fazie 4a bez wciągania całej
checklisty do kontekstu.

WHY przesłanki są w kontrakcie inwentarza: Faza 4(a) pyta, czy krok „sprawdzony przy **ZMIERZONYCH**
przesłankach" zapobiegłby incydentowi. Bez przesłanek w inwentarzu odpowiedź brzmi „nie wiem" →
lekcja awansuje do NOWEGO kroku, czyli awaria z Reguły 7 wywołana brakiem danych, nie osądem.

(c) **Pierwszy przebieg dla etapu** (`<źródło>` nie istnieje): założenie katalogu
`03-Resources/<ctx>/procesy/` i wpisu w `02-Areas/procesy/_MOC Procesy.md` jest DOZWOLONE — ale
tylko gdy `<etap>` rozwiązał się jednoznacznie z §Pipeline (Reguła 8).

(d) **Degradacja skryptu vs BŁĄD WYWOŁANIA — dwie różne rzeczy, nie mieszaj ich:**

- **Skryptu NIE MA** (`command not found`) → **degradacja**: przebieg jedzie dalej, inwentarz i dedup
  czytane modelowo, a Faza 7 punkt 4 mówi wprost „dedup modelowy, nie mechaniczny".
- **Skrypt JEST, ale zwrócił kod ≠ 0** → to **BŁĄD WYWOŁANIA, NIE degradacja**: pokaż komunikat
  skryptu, popraw wywołanie, powtórz. Fazy, która tak padła, **nie wolno** zaraportować jako RAN
  z wynikiem „brak rozjazdu" / „brak trafień".

**Kody wyjścia:** `0` ok · `1` błąd użycia/IO · `2` zła flaga (argparse) · `3` negatyw NIEPEŁNY albo
nie umiem odczytać.

WHY to jest nośne: Faza 2 jest nieblokująca, więc bez tego rozróżnienia EXIT=2 (zła flaga) przechodzi
jako „brak rozjazdu" — i jedyny MECHANICZNY detektor rozjazdu nie odpala się ani razu, a przebieg
raportuje sukces.

(e) **Brak instancji przy podanym twórcy** → zaproponuj JEDNĄ komendę i wykonaj ją po potwierdzeniu:
```bash
cp "<źródło>" "01-Projects/<ctx>/<twórca>/<twórca>-proces-<etap>.md"
```
potem dopisz twórcę do tabeli `## Instancje` w źródle, z wartością pola `updated:` źródła jako wersją.

WHY ta faza w ogóle istnieje: dziś nie ma ani jednej instancji, nikt jej nie tworzy, a bramka Fazy 0
wymaga podania `<instancja>`. Zmierzone: bez 0(e) pierwszy przebieg podstawi 570-linijkowe
`kacper-snela-nastepne-kroki.md` i dostanie „0 pozycji z ID", wszystkie 8 kroków jako „instancja
w tyle" i 119 UNANCHORED — wynik formalnie poprawny i całkowicie fałszywy.
WHY nazwa `<twórca>-proces-<etap>.md`, a nie `proces-<etap>.md`: folder twórcy trzyma konwencję
prefiksu (11 plików u Basi), a `[[proces-launch]]` przy dwóch twórcach jest dwuznaczny.

**Bramka: JEDNO zamknięte pytanie** — „`<etap>` = X, źródło = Y, instancja = Z, tryb = OBA. Zgadza się?"
Niejednoznaczność → STOP, nie zgadywanie (Reguła 8).

**Kontrakt dalej:** `<ctx>` · `<etap>` · `<źródło>` · `<instancja>` · `<memory>` · tryb · inwentarz kroków.

## Faza 1 — Lekcje z TEJ sesji (INLINE, gated)

**Pomiń, gdy tryb = ROZJAZD.**

**Wykonuje ORKIESTRATOR, bez delegacji** (Reguła 1). W ręku ma: `<etap>` · `<źródło>` · `<memory>` ·
inwentarz kroków z Fazy 0(b) — i całą sesję, bo nią JEST.

**Zadanie (to samo, co szłoby do agenta dziedziczącego sesję, gdyby taki istniał):**
```
Wyciągnij z TEJ konwersacji 0–3 kandydatów na ulepszenie procesu etapu <etap>.

Dla KAŻDEGO kandydata podaj wszystkie sześć pól:
- teza (jedno zdanie)
- [CYTAT] literalny cytat incydentu z tej sesji — parafraza jest błędem, nie stylem
- data incydentu
- zapłacony rachunek (co ta pomyłka realnie kosztowała: przebieg, sesja, wysłany asset)
- proponowany etap (z inwentarza kroków, który dostałeś)
- WYKONAWCA pozycji (operator / twórca / narzędzie)
Każde pole poza cytatem oznacz [CYTAT] albo [MOJE ODCZYTANIE].

Materiał wtórny — wpisy <memory> — pobierz SKRYPTEM, nie czytaj pliku całością:
  python3 …/procesy-scan.py --dedup "<słowa etapu>" --ctx <ctx>
i przy każdym takim kandydacie podaj origin w postaci <ścieżka>:<linia> — ta postać idzie do
RAPORTU. Origin jest load-bearing: Faza 3 pominie ten plik przy dedupie, inaczej odrzuci
kandydata jako duplikat samego siebie.

ZERO kandydatów to poprawna, częsta odpowiedź. Nie dobieraj do liczby.
```

### Bramka po Fazie 1 (3 pytania — faza prosta)

```
Parafraza DECYZJI (nie streszczenia listy kandydatów), 2–3 zdania:
„Do dalszych faz wchodzi <k> kandydatów. Rozstrzygamy o nich: etap docelowy <…>,
wykonawca <…>. <j> kandydatów odpada już teraz jako <powód>."

1. Kandydat <n> wrócił bez literalnego cytatu incydentu — odrzucamy go, czy podajesz cytat?
2. Dla kandydata <n> proponowany etap to <etap>. Bierzemy ten etap, czy <etap alternatywny>?
3. Kandydat <n> wygląda na nawyk operatora (→ `_operator-debrief.md`) albo trwałą tezę
   (→ `/brain-extract-knowledge`), nie na krok procesu. Routujemy go tam, czy zostaje tutaj?
```
**Zero kandydatów → nie pytaj o nic, powiedz „zero, przechodzę do Fazy 2" i idź dalej.**

Dopiero po potwierdzeniu: `continue` / `skip` / `back` / `status` / `stop`.

## Faza 2 — Rozjazd instancja ↔ źródło (SKRYPT + `so-agent`, gated, NIEBLOKUJĄCA)

**Pomiń, gdy tryb = LEKCJA albo `<instancja>` = BRAK** (Faza 0(a)) — powód SKIPPED brzmi wtedy
„brak kopii procesu".

(a) **Skrypt zwraca WYCINEK, nigdy plik:**
```bash
python3 /Users/marcinjucha/Prywatne/projects/brain-vault/.brain/scripts/procesy-scan.py \
  --diff "<źródło>" "<instancja>"
```
`--diff` bierze **dwa argumenty pozycyjne**, nie flagi `--source` / `--instance`. Ścieżki vaulta mają
spacje — cudzysłowy są OBOWIĄZKOWE.
Cztery kategorie: pozycje źródła nieobecne w instancji · pozycje instancji bez odpowiednika ·
odhaczone z przesłanką ZAŁOŻONĄ · **UNANCHORED** (linie bez ID).

**Kategoria UNANCHORED istnieje po to, żeby raportować „nie umiem tego przeczytać mechanicznie",
zamiast milczeć.** Bez niej 570-linijkowa notatka z 114 checkboxami zwróciłaby czysty diff.

(b) **Semantykę czyta `so-agent`** — `Agent(subagent_type: "so-agent")`.

**Prompt do agenta (WYCIĄG, nie historia):**
```
Etap: <etap>. Źródło: <źródło>. Instancja: <instancja>.
Wycinek diffu (4 kategorie): <wklej wyjście skryptu>

Doładuj leniwie skill etapu i dla każdej pozycji rozstrzygnij:
- pozycja jest obecna, tylko przeformułowana → nie rozjazd, podaj oba brzmienia
- pozycja realnie brakuje w źródle → kandydat na PROMUJ
- pozycja rozgałęzia się per twórca → kandydat na PUNKT DECYZYJNY, nie na PROMUJ
- pozycja jest lokalna dla tego twórcy → LOKALNE

Oznacz każde rozstrzygnięcie [CYTAT] (kanon / plik) albo [MOJE ODCZYTANIE].
UNANCHORED raportuj jako UNANCHORED — nie zgaduj, czego nie da się zakotwiczyć.
```

### Bramka po Fazie 2 (3–4 pytania)

```
Parafraza DECYZJI, 2–3 zdania:
„Rozjazd sprowadza się do <k> pozycji do rozstrzygnięcia + <u> UNANCHORED.
Z <k>: <a> to PROMUJ, <b> to PUNKT DECYZYJNY, <c> to LOKALNE — i o tym pytam."

1. Jest <u> pozycji UNANCHORED (skrypt ich nie zakotwiczył). Czytamy je teraz ręcznie,
   czy odkładamy do raportu Fazy 7?
2. Pozycja „<cytat>" — bierzemy jako PROMUJ (jedno brzmienie dla wszystkich twórców)
   czy jako PUNKT DECYZYJNY (pytanie do rozstrzygnięcia per twórca)?
   ← to jedyne pytanie, którego skrypt NIE rozstrzyga
3. Krok <numer> jest odhaczony przy przesłance ZAŁOŻONEJ, nie zmierzonej.
   Zostawiamy odhaczony, czy cofamy do niesprawdzonego?
4. [gdy pozycji >3] Pozycja „<cytat>" istnieje w źródle w innym brzmieniu.
   Traktujemy to jako obecną (bez zmiany), czy jako rozjazd sformułowania do ujednolicenia?
```
Faza jest NIEBLOKUJĄCA — niejasny rozjazd idzie do raportu, nie zatrzymuje przebiegu (Reguła 4).
Bramka natomiast jest OBOWIĄZKOWA: nieblokująca znaczy „nie zatrzymuje na braku danych",
nie „nie pyta".

Dopiero po potwierdzeniu: `continue` / `skip` / `back` / `status` / `stop`.

## Faza 3 — DEDUP (SKRYPT + osąd inline, ZAWSZE, BLOKUJĄCA)

Dla KAŻDEGO kandydata z Faz 1 i 2:
```bash
python3 /Users/marcinjucha/Prywatne/projects/brain-vault/.brain/scripts/procesy-scan.py \
  --dedup "<teza>" --ctx <ctx> --exclude-origin "<ścieżka originu bez :linia>"
```
**Origin przekazywany do skryptu to ŚCIEŻKA, nie `ścieżka:linia`** — inaczej wykluczenie nie działa
i kandydat jest duplikatem samego siebie. W Fazie 1 i w raporcie origin nosi `:linia`; tutaj urwij
wszystko od dwukropka.

**PIĘĆ powierzchni. Skrypt zwraca trafienia (`path:line` + 2 linie kontekstu) ORAZ wygenerowaną listę
miejsc przeszukanych z ZEREM trafień:**
1. `01-Projects/<ctx>/memory.md` — minus origin kandydata
2. `03-Resources/<ctx>/knowledge/` + bazy z `inherits` **czytane z `config.json`**, nie wpisane na
   sztywno (dziś: shadow-operator → general-business; agency → general-business + general-technical)
3. `resources/*checklist*.md` i `SKILL.md` skilli `so-*` / `copy-*`
4. `_operator-debrief.md` — §Siły / §Słabości / §Aktywne eksperymenty
5. istniejące `03-Resources/<ctx>/procesy/*.md`

**Trafienie → dwa werdykty, oba BEZ nowej treści w vaulcie:**
- **WSKAŻ** — pozycja dostaje `[[slug]]` albo nazwę pliku właściciela. Zero nowej treści.
- **ROZSZERZ U WŁAŚCICIELA** — dopisek idzie do pliku właściciela, nie do vaulta.

**Konkret, na którym to się już zdarzyło:**
`03-Resources/general-business/knowledge/archival-audience-data-beats-a-new-instrument.md` niesie
flagową pozycję z tym samym incydentem i tą samą datą. Dedup ma ją WSKAZAĆ, nie przepisać.

**WHY negatyw generuje skrypt:** „sprawdziłem i nie ma" wypowiedziane przez model jest nieweryfikowalne
i dokładnie tam powstają dwa źródła prawdy o jednej tezie. Brak skryptu → Reguła 3.

⚠️ **Negatyw skryptu jest LEKSYKALNY** — dopasowuje słowa, nie znaczenie, więc parafraza się w nim
NIE pojawi. **Obowiązkowy krok przed werdyktem NOWA POZYCJA:** przeczytaj `--inventory` źródła
i orzeknij SEMANTYCZNIE, czy któryś istniejący krok nie niesie tej samej tezy innymi słowami.
Bez tego kroku werdykt „nowa pozycja" stoi na negatywie, który nigdy nie miał prawa go unieść.

### Bramka po Fazie 3 (3–5 pytań — faza złożona, BLOKUJĄCA)

```
Parafraza DECYZJI, 2–3 zdania:
„Z <k> kandydatów <t> ma trafienie u właściciela, <n> przechodzi jako nowa treść.
Rozstrzygamy: dla trafień WSKAŻ vs ROZSZERZ, i czy wiarygodność negatywu wystarcza,
żeby <n> wpuścić do bramki Fazy 5."

1. Trafienie: teza „<teza>" siedzi już w `<path:line>`. Bierzemy WSKAŻ (pozycja dostaje
   `[[slug]]`, zero nowej treści) czy ROZSZERZ U WŁAŚCICIELA (dopisek idzie do tego pliku)?
   ← pytaj OSOBNO dla każdego trafienia
2. Negatyw był <mechaniczny ze skryptu | modelowy>. Przy modelowym: idziemy dalej ze
   świadomością, że „nie ma tego nigdzie" jest niesprawdzone, czy zatrzymujemy przebieg?
3. Właściciel „<plik>" to plik-definicja artefaktu (`SKILL.md` / `resources/*.md`) — to pociąga
   `ai-manager-agent` w Fazie 6. Zapisujemy tam, czy zostawiamy pozycję tylko w źródle?
4. [gdy trafień >2] Ta sama teza wraca u <k> właścicieli. Wskazujemy jednego kanonicznego
   (którego?), czy rozszerzamy u każdego?
5. [gdy kandydatów >3] Kandydat <n> przeszedł dedup, ale jego trafienie jest częściowe.
   Traktujemy jako nowy, czy jako rozszerzenie istniejącej pozycji?
```
**BLOKUJĄCA** — bez potwierdzenia nie wchodź do Fazy 4 (Reguła 3). Przy negatywie modelowym
odpowiedź „idziemy dalej" MUSI trafić do raportu Fazy 7 punkt 4.

Dopiero po potwierdzeniu: `continue` / `back` / `status` / `stop` (`skip` tu NIE jest dostępny).

## Faza 4 — Werdykty (INLINE, zawsze)

**Kolejność pytań jest wymuszona. Pierwsze „tak" ZAMYKA pozycję:**

**(a) Czy któryś ISTNIEJĄCY krok, sprawdzony przy ZMIERZONYCH przesłankach, zapobiegłby temu
incydentowi?**
→ **jednolinijkowy ❌ pod TYM krokiem**, z datą i rachunkiem. KONIEC. Bez nowego kroku.

Literalny format (myślnik w kolumnie 1, **bez wcięcia**):
```
- ❌ 2026-08-11 — planowaliśmy przy 135 wpm, pomiar dał 158
```
Wcięcie łamie parser: `--inventory` liczy antywzorce regexem `^-\s+❌`, więc wcięty wiersz NIE zostanie
zliczony i licznik ❌ w inwentarzu skłamie.

**(b) Czy to cecha twórcy albo rozgałęzienie?**
→ **PUNKT DECYZYJNY**: do źródła wchodzi **PYTANIE**, nie reguła — np. „ustal, czy live kosztuje tego
twórcę ekspozycję". Precedens jako jedna linia pod pytaniem.

**(c) Czy PROMUJ czytałby się INACZEJ u drugiego twórcy?**
→ to nie PROMUJ. Wróć do (b).

**(d) Realna luka, której nie pokrywa żaden krok?**
→ **nowy KROK**, status `kandydat`.

**(e) W pozostałych przypadkach** → **LOKALNE**.

**Test rozdzielający dom:** „czy to samo zdanie ma sens u Basi?" Nie → `<twórca>-nastepne-kroki.md`.

**Granice — pozycje wyrzutowe ROUTUJ z nazwą narzędzia-właściciela, nie wykonuj i nie porzucaj:**
- trwała TEZA („dlaczego to jest jakie jest") → `/brain-extract-knowledge`
- nawyk operatora → `_operator-debrief.md`

Każde pole werdyktu oznaczone `[CYTAT]` / `[MOJE ODCZYTANIE]` (Reguła 5).

**Po Fazie 4:** parafraza rozkładu werdyktów + 3–5 pytań kontrolnych. Jeśli rozkład to „wszystko
nowe KROKI" — powiedz to jako **ostrzeżenie o awarii przebiegu** (Reguła 7) i wróć do (a).

## Faza 5 — Bramka hybrydowa (INLINE, zawsze)

**Nowe KROKI i PUNKTY DECYZYJNE idą przez bramkę pozycja po pozycji:**
```
Pozycja k/n · <typ: nowy KROK | PUNKT DECYZYJNY> · <źródło>, krok <numer>

JEST:    "<literalny cytat obecnego brzmienia — albo: brak pozycji>"
BĘDZIE:  "<literalny cytat proponowanego brzmienia>"
Dlaczego: <jedno zdanie: incydent + rachunek>

Bierzemy?
```
**JEDNO zalecenie na turę.** Drugie warianty i uwagi meta albo odpadają, albo idą osobną linią
oznaczoną „do Twojej decyzji".

**Antywzorce, które ta bramka wyklucza:**
- ❌ jedna lista zbiorcza wszystkich pozycji per plik — nieprzetwarzalna w czacie
- ❌ opis zamiaru zamiast cytatu „będzie" — pokazuj propozycję, nie opisuj jej
- ❌ cicha zbiorcza przepisanka — ukrywa, które edycje stoją na kanonie, a które na moim odczytaniu

**Przy >5 pozycjach:** najpierw **plik przewodnika w folderze twórcy** w układzie
**A** (zmiany źródła) / **B** (kandydaci na wiedzę) / **C** (czego świadomie NIE biorę),
każda pozycja z WHY i ŹRÓDŁEM — potem arbitraż pozycja po pozycji z tego pliku.

**Nic nie opuszcza kolejki, dopóki zapis nie jest POTWIERDZONY.**

Pozycje ❌ pod istniejącym krokiem i markery LOKALNE **nie potrzebują bramki per pozycja** — idą
jedną listą do potwierdzenia zbiorczego (są jednolinijkowe i addytywne, trywialnie odwracalne).

## Faza 6 — Zapis (INLINE + `ai-manager-agent`, per target warunkowo)

**(a) Źródło `03-Resources/<ctx>/procesy/<etap>.md` — INLINE, NIE delegować.**
- wklej **literalny blok „będzie"** z Fazy 5 — nie przeredagowuj go w chwili zapisu
- **po edycji pozycja NIE MOŻE być dłuższa** niż przed — **z jawnym wyjątkiem dodania linii
  `- ❌ <data> — <incydent + rachunek>`, która ma prawo wydłużyć pozycję dokładnie o JEDEN wiersz;
  każde inne wydłużenie jest rozjazdem**
- **pokaż diff**

**Dwa tryby zapisu — nie mieszaj ich:**
- **(i) nowy KROK / PUNKT DECYZYJNY → REPLACE** całej pozycji literalnym blokiem „będzie".
  Pozycja jest nadpisywana, nie dostawiana obok.
- **(ii) antywzorzec ❌ i marker LOKALNE → APPEND jednego wiersza** na końcu listy pól tej pozycji,
  bez dotykania pozostałych pól.

**Bramka Fazy 6 punkt 2 (reguła „nie dłuższa niż przed") dotyczy TYLKO trybu (i).**

WHY ten rozdział jest nośny: ❌ pod istniejącym krokiem to DOMYŚLNY werdykt tej komendy (Faza 4a).
Bez wyjątku bramka klasyfikuje dopisany wiersz ❌ jako rozjazd i każe edycję COFNĄĆ — komenda
systematycznie odrzuca swój własny domyślny werdykt, a plik po każdym przebiegu zostaje
z „0 antywzorców".

WHY inline: to jedyny plik, w którym treść naprawdę ląduje, a jego edycja musi być widoczna Marcinowi
bez filtra wyjścia podagenta.

**(b) Skill-właściciel — przez `Agent(subagent_type: "ai-manager-agent")`, jeden podagent na JEDEN plik.**
Zapis inline do `SKILL.md` jest **ZABRONIONY** (globalna reguła: zapisy do plików-definicji artefaktów
idą przez `ai-manager-agent`).

**Prompt (kontrakt czterech pól):**
```
MODE: MODIFY
FILE: <absolutna ścieżka do jednego SKILL.md albo resources/*.md>
ENTRIES: <pozycje potwierdzone w Fazie 5, każda z [CYTAT]/[MOJE ODCZYTANIE] i WHY>
RECONCILE: <co w pliku już to niesie — z Fazy 3 — i czy WSKAZUJEMY, czy ROZSZERZAMY>

Rządzi `ai-skill-fine-tuning` Pattern 4 (dodawanie brakującego anty-wzorca).
Nie dopisuj treści, której nie ma w ENTRIES.
```

**(c) Marker w instancji — JEDNA linia, nic więcej:**
```
LOKALNE (2026-08-11): <powód, jedno zdanie>
```
Treść do instancji nie idzie NIGDY (reguła nadrzędna w nagłówku pliku).

**(d) `sync-procesy.py` — WOŁANY, nie implementowany w komendzie.** Nie istnieje → raport mówi
„snapshot należny, skrypt nie istnieje".

**(e) Odświeżenie `02-Areas/procesy/_MOC Procesy.md`** — mechaniczne, bez osądu, należy do tej fazy.

### Bramka po Fazie 6 (4 pytania)

```
Parafraza DECYZJI, 2–3 zdania:
„Zapisane: źródło <ścieżka> (<k> pozycji), skille <pliki>, marker w <instancja>, MOC.
Rozstrzygamy: czy diff zgadza się z tym, co potwierdziłeś w Fazie 5, i czy commitujemy."

1. Per system — źródło <k> pozycji · skille <pliki> · MOC <tak/nie> · marker <tak/nie>.
   Ten rozkład jest ten, który zatwierdziłeś, czy czegoś brakuje / coś wjechało za dużo?
2. Diff źródła (pokazany wyżej) niesie DOSŁOWNIE blok „będzie" z Fazy 5 dla pozycji <n>?
   Jeśli się rozjechał — cofamy edycję, czy akceptujesz nowe brzmienie?
   ← dotyczy TYLKO trybu (i) (REPLACE): pozycja po edycji nie może być dłuższa niż przed,
     z jawnym wyjątkiem jednego wiersza `- ❌ …`; jeśli urosła inaczej, to jest ten rozjazd.
     Tryb (ii) (APPEND wiersza ❌ / LOKALNE) tej reguły NIE podlega.
3. Snapshot do skilla jest należny dla <plik>. `sync-procesy.py` <istnieje / nie istnieje>.
   Odpalamy teraz, czy idzie do raportu jako „snapshot należny, skrypt nie istnieje"?
4. Commitujemy te ścieżki teraz i wypychamy repo vaulta (telefon widzi tylko wypchnięte),
   czy zostawiamy niescommitowane do Twojego przeglądu?
```
**Push repo vaulta** (`/Users/marcinjucha/Prywatne/projects/brain-vault`) po commicie — ta sama reguła
co `/brain-finish` Faza 5 krok 8: najpierw `git -C <vault-repo> push`; tylko gdy odrzucony, a
`git -C <vault-repo> status --porcelain` jest puste → `pull --rebase` (BEZ `--autostash`) i push;
niepuste → nie pulluj, raport „NIE wypchnięty — vault ma niezacommitowaną pracę innych sesji; push
po ich commicie". Nigdy `--force`; konflikt rebase'u → `rebase --abort` i stan do raportu. Inne repo
(skille u właściciela) → bez pusha. **WHY:** vault bywa brudny od pracy równoległych sesji,
a `--autostash` nakłada ją z powrotem i przy konflikcie z telefonem zostawia znaczniki w cudzych plikach.
Przy braku zgody na punkcie 2 **cofnij edycję źródła przed przejściem do Fazy 7** — raport nie
ma prawa twierdzić, że zapisano brzmienie, którego Marcin nie potwierdził.

Dopiero po potwierdzeniu: `continue` / `back` / `status` / `stop`.

## Faza 7 — Raport (INLINE, zawsze)

**Numeracja STAŁA — sześć punktów, w tej kolejności:**
1. **Jak rozwiązano etap** + pliki (`<etap>`, `<źródło>`, `<instancja>`, `<memory>`) — i czy z
   argumentu, czy z cwd.
2. **Per faza RAN / SKIPPED + powód** — skip jest normalnym wynikiem, nie awarią do ponowienia.
3. **Co zapisano, per system** — źródło · skille (po nazwach plików) · MOC · instancja (marker).
4. **DEDUP: co znaleziono I GDZIE SZUKANO Z ZEREM.** Jeśli negatyw był modelowy, nie mechaniczny —
   powiedz to w tym punkcie (Reguła 3). Dopisz linię:
   `dedup leksykalny: TAK/NIE · semantyczny: <kto orzekł>`
5. **Czego NIE promowano i dlaczego** — w tym pozycje wyrzutowe z nazwą narzędzia-właściciela.
6. **Stosunek nowych ❌ do nowych kroków.**

**Przebieg, który promuje wszystko do nowych kroków, jest raportem awarii.** Napisz to w raporcie
wprost, razem z punktem 6 — to sygnał, że Faza 4a nie sprawdziła istniejących kroków przy zmierzonych
przesłankach.

## Komendy

- `continue` — następna faza (albo następna pozycja w bramce Fazy 5)
- `skip` — pomiń fazę; Fazy 3 **nie wolno** pominąć (Reguła 3)
- `back` — wróć do poprzedniej pozycji bramki albo poprzedniej fazy
- `status` — gdzie jesteśmy: faza, pozycja k/n, co już potwierdzone
- `stop` — wyjdź; potwierdzone zapisy zostają, kolejka niepotwierdzona idzie do raportu

## Wystarczający kontekst

**Faza 1 jest INLINE** → nie ma komu przekazywać kontekstu. Orkiestrator ma sesję i rozwiązane
wartości Fazy 0. Delegacja tej fazy do świeżego agenta jest zakazana (Reguła 1).

**Świeży agent (`so-agent` w Fazie 2, `ai-manager-agent` w Fazie 6)** ma izolowany kontekst →
przekazuj WARTOŚCI, nigdy odwołań do „poprzedniej fazy":
- ✅ wycinek ze skryptu, rozwiązane ścieżki, potwierdzone brzmienia z Fazy 5, wynik dedupu
- ❌ pełne wyjścia poprzednich faz, cała checklista, cała notatka twórcy, historia rozmowy

**Pytanie testowe:** „czy ten agent trafi do złego pliku, wyprowadzi ponownie listę, którą mu podano,
albo dopisze treść, której nie ma w ENTRIES?" — jeśli tak, brakuje jednej z rozwiązanych wartości
i nic innego tam nie należy.
