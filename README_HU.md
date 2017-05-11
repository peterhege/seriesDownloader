# seriesDownloader

---

A program lényege, hogy különböző oldalakról sorozatokat töltsünk le. Jelenleg:
- tv2.hu
- supertv2.hu

# Használat

Futtasuk a **main**.py fájlt, majd a program kiírásainak megfelelően adjuk meg a kért adatokat.

### Felbontás kiválasztása
A megjelenő listáról válasszuk ki a kívánt felbontást és gépeljük be azt.
Például: 360

Amennyiben a kiválasztott epizódból nem létezik a megadott felbontás, akkor a program a hozzá legközelebbi egyel kisebb felbontást választja.
Ha a legjobb minőséget szeretnénk letöltetni, akkor a listáról válasszuk a legnagyobb felbontást.


### Kiszolgáló kiválasztása
A megjelenő listáról válasszuk ki a kívánt kiszolgálót és gépeljük be az azonosítóját.

       0       http://tv2.hu
       1       http://supertv2.hu
Például, a kívánt a http://tv2.hu, akkor: 0

### Sorozat keresés
Adjunk meg egy kulcsszót (legalább 3 karakter) a keresendő sorozat nevéből.
Például a "Jóban Rosszban" című sorozatot szeretném megkeresni: jób

A kulcsszó alapján a program kilistázza a találatokat, majd a kívánt sorozat azonosítóját gépeljük be.

       0       Jóban rosszban
Jelenleg egy lehetőség van, éppen amit kerestem: 0

Ha nem található a sorozat, jelzi a program, más kiszolgálóval próbálkozzon.

### Letöltendő epizódok megadása

Háromféleképpen lehet megadni a letöltendő sorozatokat:
- Csak egy epizód megadása
Például: 2448
- Intervallum megadása kötőjellel
Például: 5-31
- Több rész megadása vesszővel elválasztva
Például: 5, 12, 54

### A letöltés elindul
Részletesebb hibák és információk megtekinthetőek a log/info.log fájlban

### Példa
[![asciicast](https://asciinema.org/a/ejxxi181ge4lmyzdfxn9vthk2.png)](https://asciinema.org/a/ejxxi181ge4lmyzdfxn9vthk2)