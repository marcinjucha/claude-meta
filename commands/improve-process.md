---
description: "Silnik checklist procesu — lekcje (z /brain-finish, sesji albo kolejki) → dedup → filtr Checklist Manifesto → bramka punkt po punkcie → zapis do 03-Resources/<ctx>/procesy/. Usage: /improve-process [<ctx>/]<repo>-<proces>"
argument-hint: "[<ctx>/]<repo>-<proces>"
allowed-tools: Read, Edit, Write, Bash, Grep, Glob, Task
---

# /improve-process — silnik, który zapisuje do checklisty procesu

Bierze LEKCJE PROCESU („jak robić ten proces”: krok pominięty, zła kolejność, brakująca bramka) i nanosi je
na checklistę `03-Resources/<ctx>/procesy/<repo>-<proces>.md`. Woła go `/brain-finish` po raporcie, gdy sesja
ma lekcję procesu, albo Marcin wprost (także w przeglądzie tygodniowym dla pozycji kolejki „checklista …”).
Format pliku: `_system/templates/proces-checklista.md` (jedyna definicja). Silnik mózgu (`<brain>`):
`/Users/marcinjucha/Prywatne/projects/brain-vault/.brain`.

**Dlaczego ta komenda jest jedyną drogą zapisu:** zamknięcie wątku Tech Leada wołało ją bez checklisty
i dopisywało reguły do `tech-lead/CLAUDE.md`, który spuchł od nakładających się reguł (17.11). Lekcja
procesu ma jeden dom — checklistę — i jedną bramkę — Marcina w terminalu.

## Reguły

1. **Zapis tylko w sesji z rozmówcą.** Na starcie `echo "$CLAUDE_CODE_SESSION_ATTENDED"`: zapisujesz
   WYŁĄCZNIE przy wartości `1`. Każda inna (`0` w `claude -p`, pusta) → nic nie zapisujesz, oddajesz blok
   „Lekcje procesu — niezapisane” (format w `/brain-finish` Faza 6) i kończysz. [do potwierdzenia: wartość
   w prawdziwej turze zamknięcia mostu; zmierzone tylko na ręcznym `claude -p`.] **Why:** „Discord zbiera,
   terminal wprowadza” (Marcin, 17.11) — inaczej zgubi się big picture.
2. **Nowy punkt i zmiana treści: bramka punkt po punkcie.** Podbicia `złapał:`: JEDNO zbiorcze „tak” na
   końcu (Marcin, 17.11 — data nie zmienia treści punktu).
3. **Origin jest obowiązkowy i prawdziwy:** data + gdzie (wątek/sesja) + co poszło źle i ile kosztowało,
   z sesji, raportu albo pozycji kolejki. Kandydat bez originu odpada. Zero kandydatów to poprawny wynik.
4. **Checklist Manifesto:** 5–9 punktów na punkt pauzy, DO-CONFIRM, punkt = jedna linia do potwierdzenia
   w kilka sekund, nie instrukcja „jak”. 9 to sufit: dziesiąty wchodzi tylko przez scalenie albo usunięcie.
5. **Nie zgaduj pliku.** Dwa dopasowania albo niejasny proces → jedno zamknięte pytanie. Checklistę
   zakładasz dopiero przy PIERWSZEJ lekcji danego procesu, nigdy na zapas.

## Faza 0 — rozwiąż plik (INLINE)

- `<ctx>` i `<repo>`: argument > `python3 <brain>/scripts/resolve-context.py "$PWD"` (`context`;
  `<repo>` = basename `matchPrefix`). Proces bez repo (np. vault-only) → plik bez pola `repo:`.
- `python3 <brain>/scripts/procesy-scan.py --list --ctx <ctx> --repo <repo>` → wybierz plik po `proces:` /
  `kiedy:`. Nazwa nowego pliku: `<repo>-<proces>.md` (bez repo: `<proces>.md`) — jednoznaczna w folderze,
  bo kontekst trzyma kilka repo (`agency`: course-platform, pezetpetki-hub…). Procesy per platforma to
  osobne pliki (`digital-shelf-kmp-release-ios`, `-release-android`, `-publish-kmp`); development jest
  jeden na repo, różnice platform jako pojedyncze punkty. Repo `digital-shelf-ios` (wygaszane): bez checklist.
- Istniejący plik → `procesy-scan.py --inventory <plik>` (punkty pauzy, punkty, `złapał`) zamiast czytania
  całości. Plik bez `format: checklista` → **tryb źródło↔instancja** (niżej).

## Faza 1 — kandydaci (INLINE albo `fork`, nigdy świeży agent)

Źródło: lista od `/brain-finish`, pozycje kolejki „checklista <ctx>/<plik>: …”, albo TA konwersacja (świeży
agent jej nie widzi → wymyśli lekcje). Każdy kandydat: teza · origin · punkt pauzy · „trafienie” (istniejący
punkt złapał błąd) albo „luka”.

## Faza 2 — dedup (SKRYPT)

`procesy-scan.py --dedup "<teza>" --ctx <ctx> --repo-dir <repo w checkoucie, gdy jest> --exclude-origin <plik>`.
Negatyw jest LEKSYKALNY: przed werdyktem „nowy punkt” przeczytaj inventory i orzeknij, czy któryś punkt
nie niesie tej tezy innymi słowami. Trafienie w `CLAUDE.md` / `memory.md` / skillu → punkt przejmuje tezę,
a w propozycji wskaż linię do usunięcia u tamtego właściciela (pliki-definicje artefaktów edytuje
`ai-manager-agent`, `CLAUDE.md` repo — osobna zgoda Marcina).

## Faza 3 — filtr (INLINE, pierwsze „tak” zamyka)

1. Istniejący punkt by to złapał / złapał → podbij `złapał: <data>` (zbiorczo, Reguła 2). Bez nowego punktu.
2. Opisuje, jak działa albo psuje się narzędzie → `memory.md` (`/ai-extract-memory`), nie checklista.
3. To „dlaczego projekt jest jaki jest” → `/brain-extract-knowledge`.
4. Rzecz do POTWIERDZENIA w konkretnym momencie pracy → nowy punkt w odpowiednim punkcie pauzy (H2 nazwany
   po momencie: „Przed startem”, „Przed ship / merge”, „Przed odpowiedzią klientowi”…). Pełny (9) → propozycja
   ma postać „zastąp X” albo „scal X i Y”.

Rozkład „wszystko nowe punkty” = awaria przebiegu (nie sprawdzono kroku 1): powiedz to i wróć do 1.

## Faza 4 — bramka (INLINE, jeden punkt na turę)

```
Punkt k/n · <plik> · <punkt pauzy>
JEST:    "<obecne brzmienie albo: brak>"
BĘDZIE:  "- <punkt> — origin: <data> <gdzie>: <co poszło źle> · złapał: —"
Dlaczego: <jedno zdanie: incydent + koszt>
Bierzemy?
```
Jedno zalecenie na turę; warianty odpadają albo idą linią „do Twojej decyzji”. Na końcu jedna linia:
„Podbijam `złapał:` dla: <punkty> — tak?”.

## Faza 5 — zapis (INLINE — plik vaulta, nie definicja artefaktu)

- Wklej DOSŁOWNIE zatwierdzone „będzie”; nowy plik z szablonu; `updated:` na dziś.
- `02-Areas/procesy/_MOC Procesy.md`: jedna linia na plik (proces, repo, liczba punktów).
- Wołany z `/brain-finish` → commit + push vaulta tutaj (raport `/brain-finish` już poszedł). Push wg
  `/brain-finish` Faza 5 krok 8: najpierw `push`; odrzucony przy czystym drzewie → `pull --rebase` (bez
  `--autostash`), nigdy `--force`.
- Raport: 2–4 linie — co zapisano (plik, punkty), co poszło gdzie indziej, czego nie wzięto.

## Tryb źródło↔instancja (opcjonalny, stary format `### P-ETAP-nn`)

Dla plików bez `format: checklista` (dziś `shadow-operator/procesy/launch-tworcy.md` z kopiami u twórców,
`scandit-shelfview/procesy/obsluga-brain-meeting.md`). Lekcja → linia `- ❌ <data> — <incydent + koszt>`
(myślnik w kolumnie 1, inaczej `--inventory` jej nie policzy) pod krokiem, który by ją złapał; nowy krok
tylko przy realnej luce. Rozjazd kopii twórcy wobec źródła: `procesy-scan.py --diff "<źródło>" "<instancja>"`
(instancja z tabeli `## Instancje` źródła), semantykę rozjazdu czyta `Agent(subagent_type: "so-agent")`;
do instancji idzie tylko marker `LOKALNE (<data>): <powód>`, treść wyłącznie do źródła. Po edycji źródła
z polem `snapshot-do:`: `sync-procesy.py --context <ctx> --check`, potem bez `--check`.
