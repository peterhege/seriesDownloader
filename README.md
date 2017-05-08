# seriesDownloader

---

A program lényege, hogy különböző oldalakról sorozatokat töltsünk le. Jelenleg:
- tv2.hu
- supertv2.hu

# Használat

Futtasuk a **main**.py fájlt, majd a program kiírásainak megfelelően adjuk meg a kért adatokat.
- felbontás: csak szám (pl.: 720)
- host azonosító
- kívánt sorozat neve ( vagy egy része )
- találati listából választás
- letöltendő epizódok ( lista, range vagy csak egy )

A letöltés elindul

# Felépítés

### **main**.py

Betölti a nyelvi fájlt. Gondoskodik a felbontás és a host megadásáról, majd a host alapján példányosítja a megfelelő osztályt és futtatja az objektum "download_videos" metódusát, mely vezérli a letöltési folyamatot.

### **classes**.py

A különböző osztályok itt vannak deklarálva.
Minden osztálynak három adatszótára kell hogy legyen:

###### host_settings
host.json leírásánál részletesebben

###### settings
Innen töltjük be a felhasználó által megadott paramétereket

###### lang
Nyelvi adatok

Kötelező (más osztályoknál használható) metódusok:

##### Adatbányászat
```python
def data_mining( self, link, xpath_desc ):
```
Kinyeri a megadott link-ről az xpath_desc-nek megfelelő adatokat és visszatér egy listával.

##### A megtalált sorozatok listázása
```python
def print_series( self, series ):
```
Sorozatok egy listáját várja, melyben tuple típusok vannak:
```python
( "sorozat_neve", "sorozat_azonosítója" )
```
Ezek közül választhat a felhasználó

##### Megadott epizódok ellenőrzése
```python
def valid_episodes( self, episodes ):
```
Egy list típust vár, amiben csak számok lehetnek, ezt ellenőrzi.

##### Epizódok beolvasása
```python
def get_episodes(self):
```

Az epízódokat háromféleképpen lehet megadni:
- lista ( pl.: 1,5,3 )
- range ( pl.: 1-5 )
- csak egy ( pl.: 1 )

Ezt elmenti a "settings" adatszótár "episodes" indexéhez, majd ezen fogunk végigiterálni. Egy elem esetén egy egy elemű listát ment el.

A további metódusokat az adott host alapján kell megírni.

### **functs**.py

Letöltéshez szükséges függvények.
- json fájl beolvasása
- Ékezetes karakterek dekódolása
- Nyelvi adatok visszaadása
- Ékezetes karakterek cseréje (mentéshez)
- Letöltő

### **mylogging**.py
Logolásért felelős fájl.

### **hosts**.json
A különböző hostok egyedi beállításai, főként a megfelelő xpath leírások az adatok kinyeréséhez.