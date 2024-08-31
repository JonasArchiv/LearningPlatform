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
