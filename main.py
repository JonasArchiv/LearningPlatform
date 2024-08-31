from models import Benutzer, Kurs, Lektion, Frage, Fortschritt, Datenbank, db


def registrieren():
    print("Benutzerregistrierung")
    benutzername = input("Benutzername: ").strip()
    passwort = input("Passwort: ").strip()
    rolle = input("Was ist deine Rolle? Creator oder Student: ").strip().capitalize()

    if rolle not in ["Creator", "Student"]:
        print("Ungültige Rolle.")
        return

    benutzer = Benutzer(benutzername, passwort, rolle)
    db.add_benutzer(benutzer)
    print(f"Benutzer {benutzername} erfolgreich erstellt!")


def anmelden():
    print("Anmeldung")
    benutzername = input("Benutzername: ").strip()
    passwort = input("Passwort: ").strip()
    benutzer = db.get_benutzer(benutzername, passwort)

    if benutzer:
        print(f"Hallo, {benutzer.benutzername}!")
        if benutzer.rolle == "Creator":
            creator_menu(benutzer)
        elif benutzer.rolle == "Student":
            student_menu(benutzer)
    else:
        print("Ungültiger Login.")


def creator_menu(creator):
    while True:
        print("\nCreator-Menü")
        print("1. Kurs erstellen")
        print("2. Kurse anzeigen")
        print("3. Abmelden")
        wahl = input("Wähle eine Option: ").strip()

        if wahl == "1":
            kurs_erstellen(creator)
        elif wahl == "2":
            kurse_anzeigen()
        elif wahl == "3":
            break
        else:
            print("Ungültige Auswahl.")


def kurs_erstellen(creator):
    print("\nKurs erstellen")
    titel = input("Kurstitel: ").strip()
    kurs = Kurs(titel, creator.benutzername)

    while True:
        lektionstitel = input("Wie soll die Lektion heißen: ").strip()
        if lektionstitel.lower() == "beenden":
            break
        inhalt = input("Lektionstext: ").strip()
        lektion = Lektion(lektionstitel, inhalt)

        while True:
            frage_text = input("Was soll das Quiz sein: ").strip()
            if frage_text.lower() == "beenden":
                break
            richtige_antwort = input("Richtige Antwort: ").strip()
            antworten = input("Antwort Möglichkeiten. Bitte mir Komma trennen: ").strip().split(',')
            frage = Frage(frage_text, richtige_antwort, antworten)
            lektion.add_frage(frage)

        kurs.add_lektion(lektion)

    db.add_kurs(kurs)
    print(f"Kurs mit dem Titel '{titel}' erfolgreich erstellt!")


def kurse_anzeigen():
    print("\nVerfügbare Kurse")
    kurse = db.get_kurse()
    for idx, kurs in enumerate(kurse, start=1):
        print(f"{idx}. {kurs.titel} (Creator: {kurs.creator})")


def student_menu(student):
    while True:
        print("\nStudent-Menü")
        print("1. Kurse anzeigen")
        print("2. Kursinhalte ansehen")
        print("3. Fortschritt anzeigen")
        print("4. Abmelden")
        wahl = input("Wähle eine Option: ").strip()

        if wahl == "1":
            kurse_anzeigen()
        elif wahl == "2":
            kursinhalte_ansehen(student)
        elif wahl == "3":
            fortschritt_anzeigen(student)
        elif wahl == "4":
            break
        else:
            print("Ungültige Auswahl.")


def kursinhalte_ansehen(student):
    kurse = db.get_kurse()
    if not kurse:
        print("Keine verfügbaren Kurse.")
        return

    kursnummer = int(input("Gib die Nummer des Kurses ein: ").strip())
    if 1 <= kursnummer <= len(kurse):
        kurs = kurse[kursnummer - 1]
        print(f"\n{kurs.titel}")
        for idx, lektion in enumerate(kurs.lektionen, start=1):
            print(f"{idx}. {lektion.titel}")
            print(lektion.inhalt)

            for frage_idx, frage in enumerate(lektion.fragen, start=1):
                print(f"Frage {frage_idx}: {frage.frage_text}")
                for i, antwort in enumerate(frage.antworten, start=1):
                    print(f"{i}. {antwort}")
                antwort_idx = int(input("Deine Antwort (Nummer): ").strip())
                if frage.antworten[antwort_idx - 1] == frage.richtige_antwort:
                    print("Richtig!")
                else:
                    print("Falsch.")

            print()

        fortschritt = db.get_fortschritt(student, kurs)
        fortschritt.add_lektion(lektion)
        db.add_fortschritt(fortschritt)
    else:
        print("Ungültige Kursnummer.")


def fortschritt_anzeigen(student):
    print("\nFortschritt")
    kurse = db.get_kurse()
    for kurs in kurse:
        fortschritt = db.get_fortschritt(student, kurs)
        print(f"\nKurs: {kurs.titel}")
        if fortschritt.abgeschlossene_lektionen:
            for lektion in fortschritt.abgeschlossene_lektionen:
                print(f"- {lektion.titel}")
        else:
            print("Keine Lektionen abgeschlossen.")


def hauptmenü():
    while True:
        print("\nLernplattform")
        print("1. Registrieren")
        print("2. Anmelden")
        print("3. Beenden")
        wahl = input("Wähle eine Option: ").strip()

        if wahl == "1":
            registrieren()
        elif wahl == "2":
            anmelden()
        elif wahl == "3":
            print("Auf Wiedersehen!")
            break
        else:
            print("Ungültige Auswahl.")


if __name__ == "__main__":
    hauptmenü()