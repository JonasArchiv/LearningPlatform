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


