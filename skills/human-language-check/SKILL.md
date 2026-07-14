---
name: human-language-check
description: Dwuprzebiegowy przegląd tekstu dla odbiorcy — (1) poprawność (gramatyka, składnia, interpunkcja, zgodność rodzaju/przypadka, zeugma, kolokacje), (2) de-AI + klarowność (usuwa AI-tells, upraszcza, zachowuje głos autora). Bramka bezpieczeństwa: czyść TYLKO tekst, który zobaczy odbiorca; zostaw scaffolding (tytuły robocze, instrukcje operatorskie w nawiasach, notatki wewnętrzne). Używaj przy TWORZENIU lub sprawdzaniu dowolnego tekstu dla ludzi — treść na stronę/landing/www, copy dla klienta, posty, reklamy/ads, copy sprzedażowe, maile, skrypty do nagrań, ankiety, wiadomości. Trigger na "sprawdź językowo", "popraw polski/gramatykę", "czy to brzmi jak AI", "de-AI", "odaiuj tekst", "wygładź tekst", "zrób to bardziej ludzkie", "uprość ten tekst", "przeczytaj i popraw", "czy to dobrze napisane", "treść na stronę", "copy dla klienta", "tekst na landing", "napisz copy", "napisz posta/reklamę/maila", "website content", "client copy", "landing page copy", "sales copy", "write copy/post/ad". NIE do kodu ani czysto wewnętrznych notatek roboczych (tam em-dashy, skróty i żargon są funkcjonalne). Działa na PL i EN, nigdy mieszane w jednym tekście dla odbiorcy.
---

# Human Language Check — poprawność + głos ludzki

Dwa przebiegi na tym samym tekście, w tej kolejności: **najpierw poprawność, potem de-AI/klarowność.** Odwrotna kolejność marnuje robotę — wygładzasz zdanie, które i tak trzeba przepisać, bo jest błędne.

Wynik: poprawiony tekst + krótka lista **konkretnych** zmian (co i dlaczego), nie ogólniki typu „poprawiłem styl".

**To OBOWIĄZKOWA ostatnia bramka przed oddaniem jakiegokolwiek tekstu dla odbiorcy** — zwłaszcza treści na stronę i copy dla klienta. Przepuść tekst przez oba przebiegi, zanim trafi do czytelnika.

---

## Zasada #0 (bramka bezpieczeństwa) — czyść TYLKO tekst dla odbiorcy

To najważniejsza reguła, łamana najczęściej. Zanim cokolwiek zmienisz, rozdziel tekst na dwie warstwy:

- **Dla odbiorcy** (czyść): intro, nagłówki które widzi czytelnik (np. w Tally „Blok 1: X"), treść pytań i odpowiedzi, zamknięcie, posty, maile, skrypty mówione, opisy.
- **Scaffolding** (NIE ruszaj): tytuły robocze dokumentu (H1), instrukcje operatorskie w nawiasach („(opcjonalne — pole na imię)"), notatki wewnętrzne/strategiczne, etykiety kroków. Em-dashy, skróty i żargon są tam **funkcjonalne**, nie AI-tell.

**WHY:** czyszczenie scaffoldingu psuje działający dokument roboczy, a przy powierzchni współdzielonej z klientem — ujawnia wewnętrzną kuchnię. Jak nie masz pewności, czy dana linia jest dla odbiorcy → zapytaj albo zostaw.

Dodatkowo: jeśli tekst podaje LICZBY o samym sobie (np. „8 pytań"), sprawdź czy zgadzają się z rzeczywistością (formularz ma 10 pól → popraw liczbę, nie zostawiaj rozjazdu).

---

## Przebieg 1 — Poprawność (gramatyka, składnia, interpunkcja)

Czytaj zdanie po zdaniu. Konkretne klasy błędów, które realnie wychodzą w tekstach marketingowych PL (przykłady ilustracyjne):

- **Zeugma / zły rząd czasownika** — jeden czasownik „obsługuje" dwa dopełnienia, z których jedno do niego nie pasuje. „*wyślę Ci oba i miejsce na liście*" (miejsca nie da się wysłać) → „wyślę Ci oba i zapiszę Cię na listę".
- **Zgodność rodzaju/liczby** — orzeczenie/imiesłów nie zgadza się z podmiotem. „*Głosowanie… pokazywany*" (nijaki) → „pokazywane".
- **Zły przyimek / przypadek** — zwłaszcza gdy „+" udaje spójnik. „*Post + klikalnym linkiem*" czyta się „plus klikalnym linkiem" (zły przypadek) → „Post z klikalnym linkiem".
- **Rejestr: potoczne zamiast poprawnego** — „*jak*" w znaczeniu „jeśli" w tekście pisanym → „jeśli je chcesz". (Wyjątek: świadomy rejestr mówiony w skrypcie do kamery — wtedy zostaw.)
- **Kolokacje** — czy te słowa realnie chodzą w parze po polsku. Kalka lub „prawie-poprawne" złączenie brzmi obco.
- **Interpunkcja** — polskie cudzysłowy „…" (nie "…"), przecinek przed „że/który/bo", brak przecinka przed „i" w prostym wyliczeniu.
- **Zaimki i odniesienia** — czy „to/które/ich" ma jednoznaczny antecedent.

Jak coś jest niepewne (np. świadoma decyzja stylistyczna autora) — oznacz jako propozycję, nie wymuszaj.

---

## Przebieg 2 — De-AI: usuń AI-tells, zrób tekst ludzkim

Konkretne sygnały „pisane przez AI" do wycięcia (kolejność = częstotliwość):

1. **Konstrukcje kontrastujące „X, a nie Y"** — „*pod to, czego potrzebujecie, a nie co mi się wydaje*". Zostaw samo X.
2. **Wypełniacze-wzmacniacze** — „realnie", „naprawdę", „tak naprawdę", „dosłownie", „po prostu" jako podkładka. Tnij. **Wyjątek:** gdy słowo niesie treść (np. „ile **realnie** urośnie portfel" = po podatku i inflacji) — zostaw JEDNO takie, resztę usuń.
3. **Powtórzenia słowa** — to samo słowo w sąsiednich zdaniach (buduję/zbudować; „realnie" 3× w jednym skrypcie). Zamień lub usuń nadmiar.
4. **Kursywa na zaimkach** dla emfazy (*Wy*, *Ty*, *you*) — usuń, akcent kładź szykiem albo treścią.
5. **Jednostajny rytm myślników** — każda opcja listy z tym samym em-dashem w środku. Rozbij rytm.
6. **Mieszanie PL/EN** w jednym tekście dla odbiorcy — jeden język. (Żargon w rodzaju „popyt", „ciepła widownia", „konwersja", „lead" też out z tekstu dla laika — powiedz to po ludzku.)
7. **Symetryczne trójki / „nie tylko… ale i…"** i inne zbyt gładkie równoległości — brzmią jak szablon.

---

## Przebieg 2b — Klarowność, prostota, konkret

Cel: wysoka jakość napisana **prostym** językiem. Nie „mądrzej", tylko jaśniej.

- **Krótsze zdania.** Jedna myśl na zdanie. Rozbij wielokrotnie złożone.
- **Konkret zamiast abstrakcji.** Liczba, rzecz, czynność — nie „wartość", „rozwiązanie", „efektywność".
- **Czasownik zamiast rzeczownika odczasownikowego.** „pomaga wybrać" > „stanowi wsparcie w procesie wyboru".
- **Tnij, nie dopisuj.** Domyślnie usuwaj zbędne — meta-uzasadnienia, powtórzone „dlaczego", oczywiste zdania. Dodawaj tylko gdy trzeba coś **wzmocnić, przekazać albo pokazać anty-pattern** — i wtedy RAZ, nie w kółko.
- **Zachowaj głos autora.** De-AI ≠ przepisanie na swój styl. Usuwasz tells i błędy, nie osobowość tekstu.

---

## Checklista (odhacz przed oddaniem)

- [ ] Rozdzielone: tekst dla odbiorcy vs scaffolding — ruszony tylko ten pierwszy
- [ ] Przebieg 1: brak zeugmy, zgodność rodzaju/przypadka, dobre przyimki, polskie cudzysłowy
- [ ] Przebieg 2: brak „X a nie Y", wypełniaczy, powtórzeń słowa, kursywy na zaimkach, jednego języka
- [ ] Przebieg 2b: zdania krótkie, konkretne, głos autora zachowany
- [ ] Liczby o samym tekście zgadzają się z rzeczywistością
- [ ] Oddana **lista konkretnych zmian** (co + dlaczego), nie „poprawiłem styl"

