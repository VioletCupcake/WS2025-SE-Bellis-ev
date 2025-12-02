# **Stilrichtlinien für das Python-Projekt**

| Kategorie | Stil |
| :---- | :---- |
| Variablen und Parameter | snake\_case (z.B. user\_name, total\_count) |
| Funktionen / Methoden | PascalCase (z.B. ComputeResult(), ProcessData()) Ausnahme: Getter/Setter kann auch snake\_case sein |
| Typen / Klassen / Enums / Aliase | PascalCase (z.B. MyClass, UserProfile) |
| Konstanten / global sichtbare Konstanten | kPascalCase |
| Datei-/Modulname | snake\_case  |

### 

### **Codeorganisation & Struktur**

**Modulare Struktur:** Teile Code in überschaubare Module/Dateien, wobei jedes Modul klar definiert, was es enthält. Vermeide unnötig große Dateien, um Übersichtlichkeit zu wahren. 

**Logische Gruppierung:** Innerhalb eines Moduls sollten verwandte Elemente (z. B. Klassen, Funktionen, Konstanten) logisch gruppiert sein.

**Eindeutige Schnittstellen:** Für public- bzw. exportierte Funktionen/Klassen sollte klar erkennbar sein, was zur API gehört — und was intern bleibt (z. B. private Helferfunktionen oder Hilfsklassen).

**Minimale Abhängigkeiten:** Jede Datei/Modul soll möglichst nur diejenigen Abhängigkeiten importieren, die tatsächlich gebraucht werden — keine „transitiven Importe“, nur weil eine andere Datei sie evtl. nutzt. Das erhöht die Klarheit und reduziert die Seiteneffekte beim Refactoring.

### 

### **Kommentare & Dokumentation**

**Selbstdokumentierender Code vor überflüssigen Kommentaren.** Gute Namen für Variablen, Funktionen etc. sind oft hilfreicher als lange Kommentare. 

**Kommentare, wo sie Mehrwert bieten:** Besonders bei komplexem Verhalten, unerwarteten Besonderheiten, oder seiteneffektreichen Operationen — dort sollte dokumentiert werden, was der Code tut und warum.

**Einheitlicher Kommentarstil:** Wähle eine Art von Kommentaren (\# … für Python) und nutze sie konsistent. Die Kommentare sollten in vollständigen, gut lesbaren Sätzen verfasst sein und die übliche Groß- und Kleinschreibung verwenden.