=======================================
## POST SUBMISSION TESTING ##
=======================================

Due to the unexpected Wednesday deadline and the... lets say "Limited" participation,
there really weren't any major tests ran on the frontend
A more comprehensive list of UI tests can be found here 

/home/violet/repos/WS2025-SE-Bellis-ev/.FOR_THE_FRONTEND_AND_TESTERS

Backend testing was rather extensive and showed that things basically work

### Violet Post Submission Testing
In the following, i list all issues that i have noticed testing the submission version.
It used basic, generated templates that were onyl design FOR testing, so it's not surprising that a lot of things dont work

Some of these errors might be in line with our MVP definition and constraints.
I need to revisit them later.

A]  People in windows trying to pull the repo get path errors, presumably due to naming         
    conventions in the /docs dir (like the inclusion of < or : or / in document names)
B)  "Neuen Fall erstellen"-Formular
    - Informationsquelle: 
    Name unklar, potenziell kleiner kommentar oder umbennung zur klarstellung ("Woher hat die ratsuchende Person von der Beratungsstelle erfahren?:")
    Außerdem erlaubt "Details zur Informationsquelle (wenn "andere Quelle")" auch bei anderen optionen input
    - felder "Details zur Informationsquelle (wenn "andere Quelle")" ist dauerhaft sichtbar
    - Anzahl Dolmetschungen (Stunden): 
    Schlechter name, dieses Feld und Dolmetschung Sprache feld dauerhaft sichtbar. 
    Entweder umbenennen (Bei Dolmetschung, Anzahl an Stunden + Sprachen) und Sprachen Feld nur sichtbar wenn Stunden > 0. 
    Oder optional Checkbox - wurde Dolmetschung in Anspruch genommen? Wenn ja -> Beiden felder Anzeigen. Sprachen lassen sich auch ausfüllen wenn dolmetschung leer, aber potenziell okay als info?
    - Geschlechtsidentität & Sexualität: Default wenn möglich auf "Keine Angabe" stelle
    - Staatsangehörigkeit Land (wenn nicht deutsch): Immer sichtbar
C) "Fall Bearbeiten"-Formular
 -   Es wird folgender Hinweis ausgeben: Hinweis: In der MVP-Version können nur ausgewählte Felder bearbeitet werden. Personenbezogene Daten sind nicht editierbar.
 - Aber: Es gibt nur die option die Inofrmationsquelle zu bearbeiten + weitere notizen einzugeben. Keine option "Details zur Informationsquelle (wenn "andere Quelle")" zu bearbeiten.
D) "Beratung Hinzufügen"-Formular
   -  Jahr frei wählbar, auch 1
   -  tag und monat falschrum. Unter dem feld steht, nach deutschen muster day/month/year. Imformularfeld selbst mm/dd/yyyy
E) Gewalttat Hinzufügen
   - Feld vielleicht in "Gewaltvorfall" umbenennen
   - komplett leerer Fall lässt sich hinzufügen
   -  Zeitraum gewalttag gleiches problem wie bei Fall bearbeiten. tag und monat falschrum. Unter dem feld steht, nach deutschen muster day/month/year. Imformularfeld selbst mm/dd/yyyy
   - Gewalt-Notizen lable bei textfeld unter notzen unnötig
   - unterkategorien von Sexuelle Belöstigung immer sichtbar/auswählbar
   - Bei  ANzahl und Art der Vorfälle sowie bei TäterInnen - anzahl (für genaue anzahl) auch ausfüllbar wenn keine Angabe.
   - tag und monat falschrum. Unter dem feld steht, nach deutschen muster day/month/year. Imformularfeld selbst mm/dd/yyyy. gleichzeitig probleme wenn DD zu hoch
F) Konkrete Falle Seite
   - Keine Anzeige von Anzahl der Vorfölle, Anzahl der täter wenn genaue anzahl gegeben, oder notizen, oder alter
   - Folgen der Gewalt gar nicht implementiert, weder zur erstellung noch zum anzeigen
G)  Logout-Page:
   - geht nicht, Logout führt zu error, man bleibt eingeloggt. folgender error 
     [07/Jan/2026 14:15:55] "GET /gewalttat/c1f0056d-14a1-463c-953c-a17b4b4d6cef/edit/ HTTP/1.1" 200 18781
Method Not Allowed (GET): /logout/
Method Not Allowed: /logout/
[07/Jan/2026 14:17:44] "GET /logout/ HTTP/1.1" 405 0
- Login bleibt auch nach stoppen und neu starten des servers aktiv, man muss sich nicht neu enloggen
