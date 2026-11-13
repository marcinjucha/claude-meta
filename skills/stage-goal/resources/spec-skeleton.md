# <Nazwa etapu>: wymagania

> Pełna specyfikacja etapu. Cel do wklejenia w `/goal` (limit 4000 znaków): `<slug>.md`.

Zbuduj w <repo> etap „<Nazwa etapu>” (<skąd zakres: plik z decyzjami produktu / wyceną, ścieżka w vaulcie>). Wymaga etapów „<…>”. <Co ten etap ZNOSI z wcześniejszych decyzji, jeśli coś>. [decyzja Marcina] = pytasz Marcina przed przyrostem, nie rozstrzygasz sam; [do decyzji w decisions.md] = rozstrzygasz sam i zapisujesz z odrzuconymi wariantami. Gotowe, gdy:
1. <punkt, który hook może sprawdzić w rozmowie: wklejona linia wyjścia, liczba, nazwany plik>
2. <…> [decyzja Marcina przed przyrostem N: <pytanie>]
3. Bezpieczeństwo: <negatywy izolacji> — każdy z wyłączonym zabezpieczeniem w <skrypcie dowodowym repo>.
4. <punkt z działaniem człowieka lub procesu: zrzuty obejrzane, inwentarz, przeklikanie> — kończy się linią dowodu w stałej formie, opartą na wyjściu narzędzia z tej sesji: `ZRZUTY: marka A n/n, marka B n/n obejrzane`, `INVENTORY: 0 bez rozstrzygnięcia (N pozycji)`.
N. <pakiet weryfikacji repo: lista z CLAUDE.md „Stage process”>, teksty dla ludzi po human-language-check: `HLC: n/n tekstów`.
Poza zakresem: <jedna linia; trafia też do celu, gdy się zmieści>

<WKLEJ z CLAUDE.md „Stage process”: regułę przeglądów według prawdopodobieństwa>
<WKLEJ z CLAUDE.md „Stage process”: dwie reguły MUST (testy jak kod produkcyjny, Boy Scout)>
Przyrosty osobno (<0. linia bazowa>, <1. …>, …): każdy projekt → implementacja → review tylko tego przyrostu → <weryfikacja repo> → osobny commit, zanim ruszy następny. Niezależny przegląd innym narzędziem i wszystkie poprawki PRZED długim skryptem dowodowym, potem dowody raz. Na koniec review całego etapu (diff od startu do HEAD) do zera potwierdzonych znalezisk.
<WKLEJ z CLAUDE.md „Stage process”: linię „Advisor:”>
<WKLEJ z CLAUDE.md „Stage process”: blok „Zamknięcie (dla stop hooka):” z listą dowodów repo — jedna linia; „Dowody na <SHA>” zaczyna się od linii na punkt, potem linie podsumowania, punkt 0 nazwany wprost, nigdy „linie bazowe”>
