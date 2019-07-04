# A
🛰 → 🚌 ↔ 🖧

## logowanie

Każde urządzenie ma swój własny identyfikator po którym je rozpoznajemy.
W bazie trzymamy powiązanie urządzenia z konkretnym pojazdem.
Z każdym zapytaniem do serwera idzie też identyfikator i podpis.
Podpis jest generowany na podstawie przesyłanych danych i klucza urządzenia.
Klucz urządzenia jest wpisany w urządzenie i w bazę, ale nie jest nigdy
przesyłany.
Dzięki urzyciu kucza i podpisu, nie ma potrzeby tworzenia sesji użytkownika -
logowania urządzenia.

Każdorazowo po starcie aplikacji wyświetlany jest ekran logowania kierowcy.
Kierowca loguje się własnym loginem i hasłem. Ponieważ urządzenie i tak jest
powiązane z pojazdem, a pojaz z właścicielem, login kierowcy musi być unikalny
w skali właściciela, ale nie musi być unikalny w skali całego systemu.
Można więc jako loginu użyć np. numeru kierowcy.

## struktura bazy danych

Tabela urządzenia:
id | identyfikator urządzenia | timestamp | czy aktywny | klucz | id pojazdu | id firmy

Tabela pojazdy:
id | vin | nazwa (nr taborowy) | czy aktywny | id firmy | id brygady | id kirowcy | lokalizacja

Tabela firmy:
id | nazwa | czy aktywny

Tabela kierowcy:
id | nazwa | identyfikator | hasło | id firmy

Tabela zarządcy: (?)
id | nazwa

Tabela linie:
id | nazwa | zarządca

Tabela rozkład (dzienny, całościowy):
id | nazwa | zarządca

Tabela brygada ↔ dzień:
id | id brygady | id dnia | id rozkładu
UWAGA: rozkład można traktować jako coś zdenormalizowanego

Tabela brygady:
id | nazwa | id linii

Tabela półkursu:
id | id brygady

Tabela przejazdu:
id | id półkursu | id przystanku początkowego | na żądanie | odjazd | id przystanku końcowego | na żądanie | przyjazd

Tabela przystanki:
id | nazwa | lokalizacja | miasto (?)

przystanek ↔ zarządca
przystanek ↔ miasto

Tabela dni:
id | data | dzień tygodnia | czy święto
UWAGA: dni można trzymać w pamięci, można obliczać id dni na podstawie istniejących
