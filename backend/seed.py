import random
from datetime import date, timedelta

import bcrypt

from core.database import Base, LocalSession, engine
from models import Medico, Paziente, Prestazione, Sede, Specialita, Utente

DEFAULT_PASSWORD = "Password123!"

NOMI = [
    "Mario", "Laura", "Giuseppe", "Anna", "Marco", "Giulia", "Luca", "Francesca",
    "Alessandro", "Chiara", "Davide", "Elena", "Simone", "Valentina", "Matteo", "Sara",
]
COGNOMI = [
    "Rossi", "Bianchi", "Verdi", "Ferrari", "Esposito", "Colombo", "Ricci",
    "Marino", "Greco", "Bruno", "Gallo", "Conti", "Mancini", "Costa", "Giordano", "Fontana",
]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def random_codice_fiscale() -> str:
    lettere = "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ", k=6))
    anno = "".join(random.choices("0123456789", k=2))
    mese = random.choice("ABCDEHLMPRST")
    giorno = "".join(random.choices("0123456789", k=2))
    comune = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") + "".join(random.choices("0123456789", k=3))
    controllo = random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    return f"{lettere}{anno}{mese}{giorno}{comune}{controllo}"


def random_telefono() -> str:
    return "3" + "".join(random.choices("0123456789", k=9))


def random_numero_albo() -> str:
    return "ALB" + "".join(random.choices("0123456789", k=5))


def crea_email(nome: str, cognome: str, dominio: str) -> str:
    base = f"{nome}.{cognome}".lower()
    return f"{base}@{dominio}"


def get_or_create_sede(db, nome, citta, indirizzo) -> Sede:
    sede = db.query(Sede).filter_by(nome=nome).first()
    if sede:
        return sede
    sede = Sede(nome=nome, citta=citta, indirizzo=indirizzo)
    db.add(sede)
    db.flush()
    return sede


def get_or_create_specialita(db, nome, descrizione) -> Specialita:
    specialita = db.query(Specialita).filter_by(nome=nome).first()
    if specialita:
        return specialita
    specialita = Specialita(nome=nome, descrizione=descrizione)
    db.add(specialita)
    db.flush()
    return specialita


def get_or_create_prestazione(db, specialita, nome, durata_min, prezzo) -> Prestazione:
    prestazione = (
        db.query(Prestazione).filter_by(nome=nome, specialita_id=specialita.id).first()
    )
    if prestazione:
        return prestazione
    prestazione = Prestazione(
        specialita=specialita, nome=nome, durata_min=durata_min, prezzo=prezzo
    )
    db.add(prestazione)
    db.flush()
    return prestazione


def get_or_create_utente(db, email, ruolo) -> tuple[Utente, bool]:
    utente = db.query(Utente).filter_by(email=email).first()
    if utente:
        return utente, False
    utente = Utente(
        email=email,
        password_hash=hash_password(DEFAULT_PASSWORD),
        ruolo=ruolo,
        is_active=True,
    )
    db.add(utente)
    db.flush()
    return utente, True


def seed():
    Base.metadata.create_all(bind=engine)
    db = LocalSession()

    sedi = [
        get_or_create_sede(db, "Sede Centrale", "Roma", "Via Roma 1"),
        get_or_create_sede(db, "Sede Nord", "Milano", "Via Milano 10"),
    ]

    specialita_catalogo = [
        ("Cardiologia", "Diagnosi e cura delle malattie cardiovascolari"),
        ("Dermatologia", "Diagnosi e cura delle malattie della pelle"),
        ("Ortopedia", "Diagnosi e cura di ossa, articolazioni e muscoli"),
        ("Pediatria", "Cura della salute dei bambini"),
        ("Oculistica", "Diagnosi e cura delle malattie degli occhi"),
        ("Ginecologia", "Salute dell'apparato riproduttivo femminile"),
    ]
    specialita = [get_or_create_specialita(db, nome, desc) for nome, desc in specialita_catalogo]
    cardiologia, dermatologia, ortopedia, pediatria, oculistica, ginecologia = specialita

    prestazioni_catalogo = [
        (cardiologia, "Visita cardiologica", 30, 80),
        (cardiologia, "Elettrocardiogramma", 20, 50),
        (dermatologia, "Visita dermatologica", 30, 70),
        (dermatologia, "Mappatura nei", 45, 100),
        (ortopedia, "Visita ortopedica", 30, 75),
        (ortopedia, "Infiltrazione", 20, 60),
        (pediatria, "Visita pediatrica", 30, 60),
        (oculistica, "Visita oculistica", 30, 70),
        (oculistica, "Esame della vista", 20, 40),
        (ginecologia, "Visita ginecologica", 30, 80),
    ]
    prestazioni = [
        get_or_create_prestazione(db, sp, nome, dur, prezzo)
        for sp, nome, dur, prezzo in prestazioni_catalogo
    ]

    get_or_create_utente(db, "admin@msmedicalcenter.it", "admin")

    nomi_disponibili = NOMI.copy()
    cognomi_disponibili = COGNOMI.copy()
    random.shuffle(nomi_disponibili)
    random.shuffle(cognomi_disponibili)

    medici_creati = []
    for _ in range(random.randint(3, 4)):
        nome, cognome = nomi_disponibili.pop(), cognomi_disponibili.pop()
        utente, creato = get_or_create_utente(
            db, crea_email(nome, cognome, "msmedicalcenter.it"), "medico"
        )
        if not creato:
            continue
        db.add(
            Medico(
                utente_id=utente.id,
                nome=nome,
                cognome=cognome,
                numero_albo=random_numero_albo(),
                specialita=random.sample(specialita, k=random.randint(1, 2)),
            )
        )
        medici_creati.append((nome, cognome))

    pazienti_creati = []
    for _ in range(random.randint(2, 3)):
        nome, cognome = nomi_disponibili.pop(), cognomi_disponibili.pop()
        utente, creato = get_or_create_utente(
            db, crea_email(nome, cognome, "example.com"), "paziente"
        )
        if not creato:
            continue
        data_nascita = date.today() - timedelta(days=random.randint(18 * 365, 75 * 365))
        db.add(
            Paziente(
                utente_id=utente.id,
                nome=nome,
                cognome=cognome,
                codice_fiscale=random_codice_fiscale(),
                data_nascita=data_nascita,
                telefono=random_telefono(),
            )
        )
        pazienti_creati.append((nome, cognome))

    db.commit()
    db.close()

    print("Seed completato:")
    print(f"  Sedi: {len(sedi)}")
    print(f"  Specialita: {len(specialita)}")
    print(f"  Prestazioni: {len(prestazioni)}")
    print(f"  Medici aggiunti: {medici_creati}")
    print(f"  Pazienti aggiunti: {pazienti_creati}")


if __name__ == "__main__":
    seed()
