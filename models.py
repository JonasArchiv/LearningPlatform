import json
import os

DATABASE_PATH = "database.json"

ROLLE_CREATOR = "Creator"
ROLLE_STUDENT = "Student"

class Benutzer:
    def __init__(self, benutzername, passwort, rolle):
        self.benutzername = benutzername
        self.passwort = passwort
        self.rolle = rolle

    def to_dict(self):
        return {"benutzername": self.benutzername, "passwort": self.passwort, "rolle": self.rolle}

class Kurs:
    def __init__(self, titel, creator):
        self.titel = titel
        self.creator = creator
        self.lektionen = []

    def add_lektion(self, lektion):
        self.lektionen.append(lektion)

    def to_dict(self):
        return {
            "titel": self.titel,
            "creator": self.creator,
            "lektionen": [lektion.to_dict() for lektion in self.lektionen]
        }

class Lektion:
    def __init__(self, titel, inhalt):
        self.titel = titel
        self.inhalt = inhalt
        self.fragen = []

    def add_frage(self, frage):
        self.fragen.append(frage)

    def to_dict(self):
        return {
            "titel": self.titel,
            "inhalt": self.inhalt,
            "fragen": [frage.to_dict() for frage in self.fragen]
        }

class Frage:
    def __init__(self, frage_text, richtige_antwort, antworten):
        self.frage_text = frage_text
        self.richtige_antwort = richtige_antwort
        self.antworten = antworten

    def to_dict(self):
        return {
            "frage_text": self.frage_text,
            "richtige_antwort": self.richtige_antwort,
            "antworten": self.antworten
        }

class Fortschritt:
    def __init__(self, student, kurs):
        self.student = student
        self.kurs = kurs
        self.abgeschlossene_lektionen = []

    def add_lektion(self, lektion):
        if lektion not in self.abgeschlossene_lektionen:
            self.abgeschlossene_lektionen.append(lektion)

    def to_dict(self):
        return {
            "student": self.student.benutzername,
            "kurs": self.kurs.titel,
            "abgeschlossene_lektionen": [lektion.titel for lektion in self.abgeschlossene_lektionen]
        }

class Datenbank:
    def __init__(self, path=DATABASE_PATH):
        self.path = path
        self.daten = {"benutzer": [], "kurse": [], "fortschritte": []}
        self.load()

    def load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, "r", encoding="utf-8") as file:
                    content = file.read().strip()
                    if content:  # Überprüfen, ob die Datei nicht leer ist
                        self.daten = json.loads(content)
                    else:
                        print("Die Datei ist leer. Verwende Standardwerte.")
            except json.JSONDecodeError as e:
                print(f"Fehler beim Laden der JSON-Daten: {e}")
                print("Verwende Standardwerte.")
        else:
            print("Datenbankdatei nicht gefunden. Erstelle eine neue.")

    def save(self):
        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(self.daten, file, ensure_ascii=False, indent=4)

    def add_benutzer(self, benutzer):
        self.daten["benutzer"].append(benutzer.to_dict())
        self.save()

    def add_kurs(self, kurs):
        self.daten["kurse"].append(kurs.to_dict())
        self.save()

    def add_fortschritt(self, fortschritt):
        self.daten["fortschritte"].append(fortschritt.to_dict())
        self.save()

    def get_benutzer(self, benutzername, passwort):
        for benutzer in self.daten["benutzer"]:
            if benutzer["benutzername"] == benutzername and benutzer["passwort"] == passwort:
                return Benutzer(**benutzer)
        return None

    def get_kurse(self):
        return [Kurs(kurs["titel"], kurs["creator"]) for kurs in self.daten["kurse"]]

    def get_fortschritt(self, student, kurs):
        for fortschritt in self.daten["fortschritte"]:
            if fortschritt["student"] == student.benutzername and fortschritt["kurs"] == kurs.titel:
                return Fortschritt(student, kurs)
        return Fortschritt(student, kurs)


db = Datenbank()
