# Reseptit

##Sovelluksen toiminnot

* Sovelluksessa käyttäjät pystyvät jakamaan ruokareseptejään. Reseptissä lukee kuvaus, tarvittavat ainekset ja valmistusohje.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään reseptejä ja muokkaamaan ja poistamaan niitä.
* Käyttäjä pystyy lisäämään kuvia ilmoitukseen
* Käyttäjä näkee sovellukseen lisätyt reseptit.
* Käyttäjä pystyy etsimään reseptejä hakusanalla.
* Käyttäjäsivu näyttää, montako reseptiä käyttäjä on lisännyt ja listan käyttäjän lisäämistä resepteistä.
* Käyttäjä pystyy valitsemaan reseptille yhden tai useamman luokittelun (esim. laktoositon, juhla, vegaaninen).
* Käyttäjä pystyy antamaan reseptille kommentin ja arvosanan. Reseptistä näytetään kommentit ja keskimääräinen arvosana.

## Sovelluksen asennus
```
git clone https://github.com/Mongemon/tsoha-projekti-reseptit
python3 -m venv venv
source venv/bin/activate
pip install flask
cd tsoha-projekti-reseptit/sovellus
sqlite3 database.db < schema.sql
sqlite3 database.db < init.sql
flask run
```
