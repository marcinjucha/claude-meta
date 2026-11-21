# <Nazwa etapu>: wymagania

> Pełna specyfikacja etapu. Cel do wklejenia w `/goal` (limit 4000 znaków): `<slug>.md`.

Zbuduj w <repo> etap „<Nazwa etapu>” (<skąd zakres: plik z decyzjami produktu / wyceną, ścieżka w vaulcie>). Wymaga etapów „<…>”. <Co ten etap ZNOSI z wcześniejszych decyzji, jeśli coś>. [decyzja Marcina] = pytasz Marcina przed przyrostem, nie rozstrzygasz sam; [do decyzji w decisions.md] = rozstrzygasz sam i zapisujesz z odrzuconymi wariantami. Gotowe, gdy:
1. <punkt, który hook może sprawdzić w rozmowie: wklejona linia wyjścia, liczba, nazwany plik>
2. <…> [decyzja Marcina przed przyrostem N: <pytanie>]
3. Bezpieczeństwo: <negatywy izolacji, każdy z nazwaną ścianą, którą etap DODAJE: baza / adapter / server fn>. Każda odmowa, która jest JEDYNĄ ścianą na swojej ścieżce, ma dowód z wyłączonym zabezpieczeniem (linia w skrypcie dowodowym albo ręcznie, zapisana w decisions.md: `RĘCZNE: n/n`, n = numerowane wpisy); odmowa, którą powtarza baza, ma tylko zapis, dlaczego nie ma osobnego dowodu.
4. <punkt z działaniem człowieka lub procesu: zrzuty obejrzane, inwentarz, przeklikanie> — kończy się linią, którą wypisuje nazwany skrypt z listy pozycji i raportu podagenta (nigdy liczba napisana przez model), skrypt przed linią: <course-platform: `python3 scripts/judgment_report.py tally ZRZUTY`> → `ZRZUTY: n/m obejrzane, k usterek, 0 brakujących` (m = wszystkie zrzuty każdej powierzchni, którą etap zmienił, obie marki, każda szerokość).
N. <pakiet weryfikacji repo: lista z CLAUDE.md „Stage process”>, teksty dla ludzi po human-language-check, linia ze skryptu <course-platform: `python3 scripts/judgment_report.py tally HLC`>: `HLC: n/m obejrzane, k usterek, 0 brakujących` (m = <lista z narzędzia repo; course-platform: `judgment_report.py expected strings`>).
Poza zakresem: <jedna linia; trafia też do celu, gdy się zmieści>

<WKLEJ z CLAUDE.md „Stage process”: regułę przeglądów według prawdopodobieństwa>
<WKLEJ z CLAUDE.md „Stage process”: dwie reguły MUST (testy jak kod produkcyjny, Boy Scout)>
Przyrosty osobno (<0. linia bazowa>, <1. …>, …): każdy projekt → implementacja → review tylko tego przyrostu → <weryfikacja repo> → osobny commit, zanim ruszy następny. Niezależny przegląd innym narzędziem i wszystkie poprawki PRZED długim skryptem dowodowym, potem dowody raz. Na koniec `/code-review high` całego etapu (diff od bazy etapu do HEAD): najwyżej 3 rundy, koniec wcześniej po rundzie z zerem potwierdzonych znalezisk albo z samymi węższymi przypadkami niż poprzednia; każda runda z filtrem prawdopodobieństwa, reszta jako przyjęte klasy w decisions.md; poprawki ostatniej rundy jedną rundą `/code-review medium` na ich własnym diffie, jej znaleziska do przyjętych klas albo nowego wątku, nie do kolejnej rundy; przed rundą high jeden przebieg prawdziwego narzędzia dla każdego zewnętrznego formatu, na którym stoi kod; potem końcowe dowody.
<WKLEJ z CLAUDE.md „Stage process”: linię „Advisor:”>
<WKLEJ z CLAUDE.md „Stage process”: blok „Zamknięcie (dla stop hooka):” z listą dowodów repo — jedna linia; „Dowody na <SHA>” zaczyna się od linii na punkt, potem linie podsumowania, punkt 0 nazwany wprost, nigdy „linie bazowe”; pozycja przeglądu w bloku = klauzula `/code-review high` z SKILL.md (high na baza..H, medium na H..finalny SHA, linia `CODE-REVIEW: <SHA>, high: <baza>..<H>, rundy: <N>, ostatnia: …, medium: <H>..<SHA>|brak, przyjęte klasy: <K>`)>
