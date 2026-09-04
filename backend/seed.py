import random
from datetime import date, datetime, time, timedelta

from core.database import Base, LocalSession, engine
from core.security import hash_password
from models import (
    Appuntamento,
    Disponibilita,
    Medico,
    Pagamento,
    Paziente,
    Prestazione,
    Sede,
    Specialita,
    Utente,
)

DEFAULT_PASSWORD = "Password123!"

NOMI = [
    "Mario", "Laura", "Giuseppe", "Anna", "Marco", "Giulia", "Luca", "Francesca",
    "Alessandro", "Chiara", "Davide", "Elena", "Simone", "Valentina", "Matteo", "Sara",
]
COGNOMI = [
    "Rossi", "Bianchi", "Verdi", "Ferrari", "Esposito", "Colombo", "Ricci",
    "Marino", "Greco", "Bruno", "Gallo", "Conti", "Mancini", "Costa", "Giordano", "Fontana",
]
ORARI = [
    (time(9, 0), time(9, 30)),
    (time(9, 30), time(10, 0)),
    (time(10, 0), time(10, 30)),
    (time(11, 0), time(11, 30)),
    (time(15, 0), time(15, 30)),
    (time(16, 0), time(16, 30)),
]

GIORNI_STORICO_MASSIMI = 75
GIORNI_FUTURI_MASSIMI = 14
DISPONIBILITA_PER_MEDICO = 9
NUMERO_PAZIENTI = 8

GRUPPI_SPECIALITA_CORRELATE = [
    {"Ortopedia", "Fisiatria"},
    {"Ginecologia", "Ostetricia"},
    {"Dermatologia", "Allergologia"},
]


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


def get_or_create_utente(db, email, ruolo) -> Utente:
    utente = db.query(Utente).filter_by(email=email).first()
    if utente:
        return utente
    utente = Utente(
        email=email,
        password_hash=hash_password(DEFAULT_PASSWORD),
        ruolo=ruolo,
        is_active=True,
    )
    db.add(utente)
    db.flush()
    return utente


def crea_catalogo(db) -> tuple[list[Sede], list[Specialita], list[Prestazione]]:
    sedi = [
        get_or_create_sede(db, "Sede Centrale", "Roma", "Via Roma 1"),
        get_or_create_sede(db, "Sede Nord", "Milano", "Via Milano 10"),
    ]

    specialita_catalogo = [
        ("Cardiologia", "Diagnosi e cura delle malattie cardiovascolari"),
        ("Dermatologia", "Diagnosi e cura delle malattie della pelle"),
        ("Allergologia", "Diagnosi e cura delle allergie e delle intolleranze"),
        ("Ortopedia", "Diagnosi e cura di ossa, articolazioni e muscoli"),
        ("Fisiatria", "Riabilitazione motoria e recupero funzionale"),
        ("Pediatria", "Cura della salute dei bambini"),
        ("Oculistica", "Diagnosi e cura delle malattie degli occhi"),
        ("Ginecologia", "Salute dell'apparato riproduttivo femminile"),
        ("Ostetricia", "Assistenza alla gravidanza e al parto"),
        ("Radiologia", "Diagnostica per immagini"),
        ("Otorinolaringoiatria", "Diagnosi e cura di orecchio, naso e gola"),
        ("Neurologia", "Diagnosi e cura delle malattie del sistema nervoso"),
    ]
    specialita = [get_or_create_specialita(db, nome, desc) for nome, desc in specialita_catalogo]
    (
        cardiologia,
        dermatologia,
        allergologia,
        ortopedia,
        fisiatria,
        pediatria,
        oculistica,
        ginecologia,
        ostetricia,
        radiologia,
        otorinolaringoiatria,
        neurologia,
    ) = specialita

    prestazioni_catalogo = [
        (cardiologia, "Visita cardiologica", 30, 80),
        (cardiologia, "Elettrocardiogramma", 20, 50),
        (dermatologia, "Visita dermatologica", 30, 70),
        (dermatologia, "Mappatura nei", 45, 100),
        (allergologia, "Visita allergologica", 30, 75),
        (allergologia, "Test allergologici", 45, 90),
        (ortopedia, "Visita ortopedica", 30, 75),
        (ortopedia, "Infiltrazione", 20, 60),
        (fisiatria, "Visita fisiatrica", 30, 70),
        (fisiatria, "Seduta di riabilitazione", 45, 45),
        (pediatria, "Visita pediatrica", 30, 60),
        (pediatria, "Vaccinazione", 15, 35),
        (oculistica, "Visita oculistica", 30, 70),
        (oculistica, "Esame della vista", 20, 40),
        (ginecologia, "Visita ginecologica", 30, 80),
        (ginecologia, "Ecografia ginecologica", 30, 90),
        (ostetricia, "Visita ostetrica", 30, 85),
        (ostetricia, "Ecografia in gravidanza", 30, 100),
        (radiologia, "TAC", 30, 150),
        (radiologia, "Risonanza magnetica", 45, 220),
        (otorinolaringoiatria, "Visita otorinolaringoiatrica", 30, 70),
        (otorinolaringoiatria, "Esame audiometrico", 20, 50),
        (neurologia, "Visita neurologica", 30, 90),
        (neurologia, "Elettroencefalogramma", 30, 110),
    ]
    prestazioni = [
        get_or_create_prestazione(db, sp, nome, dur, prezzo)
        for sp, nome, dur, prezzo in prestazioni_catalogo
    ]

    return sedi, specialita, prestazioni


def specialita_correlate(specialita_principale: Specialita, tutte: list[Specialita]) -> list[Specialita]:
    for gruppo in GRUPPI_SPECIALITA_CORRELATE:
        if specialita_principale.nome in gruppo:
            return [s for s in tutte if s.nome in gruppo and s.id != specialita_principale.id]
    return []


def crea_disponibilita_per_medico(db, medico: Medico, sedi: list[Sede], quantita: int) -> list[Disponibilita]:
    slot_creati = []
    for _ in range(quantita):
        nel_passato = random.random() < 0.55
        if nel_passato:
            giorno = date.today() - timedelta(days=random.randint(1, GIORNI_STORICO_MASSIMI))
        else:
            giorno = date.today() + timedelta(days=random.randint(1, GIORNI_FUTURI_MASSIMI))
        ora_inizio, ora_fine = random.choice(ORARI)
        sede = random.choice(sedi)
        disponibilita = Disponibilita(
            medico_id=medico.id,
            sede_id=sede.id,
            data=giorno,
            ora_inizio=ora_inizio,
            ora_fine=ora_fine,
        )
        db.add(disponibilita)
        db.flush()
        slot_creati.append(disponibilita)
    return slot_creati


def crea_medici(db, specialita: list[Specialita], sedi: list[Sede]) -> tuple[list[Medico], list[Disponibilita]]:
    nomi_disponibili = NOMI.copy()
    cognomi_disponibili = COGNOMI.copy()
    random.shuffle(nomi_disponibili)
    random.shuffle(cognomi_disponibili)

    medici_creati = []
    slot_totali = []
    for specialita_principale in specialita:
        nome, cognome = nomi_disponibili.pop(), cognomi_disponibili.pop()
        utente = get_or_create_utente(db, crea_email(nome, cognome, "msmedicalcenter.it"), "medico")

        specialita_medico = [specialita_principale]
        correlate = specialita_correlate(specialita_principale, specialita)
        if correlate and random.random() < 0.5:
            specialita_medico.append(random.choice(correlate))

        medico = Medico(
            utente_id=utente.id,
            nome=nome,
            cognome=cognome,
            numero_albo=random_numero_albo(),
            specialita=specialita_medico,
        )
        db.add(medico)
        db.flush()
        medici_creati.append(medico)
        slot_totali.extend(crea_disponibilita_per_medico(db, medico, sedi, DISPONIBILITA_PER_MEDICO))

    return medici_creati, slot_totali


def crea_pazienti(db, quantita: int) -> list[Paziente]:
    nomi_disponibili = NOMI.copy()
    cognomi_disponibili = COGNOMI.copy()
    random.shuffle(nomi_disponibili)
    random.shuffle(cognomi_disponibili)

    pazienti_creati = []
    for _ in range(quantita):
        nome, cognome = nomi_disponibili.pop(), cognomi_disponibili.pop()
        utente = get_or_create_utente(db, crea_email(nome, cognome, "example.com"), "paziente")
        data_nascita = date.today() - timedelta(days=random.randint(18 * 365, 75 * 365))
        paziente = Paziente(
            utente_id=utente.id,
            nome=nome,
            cognome=cognome,
            codice_fiscale=random_codice_fiscale(),
            data_nascita=data_nascita,
            telefono=random_telefono(),
        )
        db.add(paziente)
        db.flush()
        pazienti_creati.append(paziente)
    return pazienti_creati


def prenota_slot(db, disponibilita: Disponibilita, paziente: Paziente, prestazione: Prestazione, stato: str):
    appuntamento = Appuntamento(
        paziente_id=paziente.id,
        disponibilita_id=disponibilita.id,
        prestazione_id=prestazione.id,
        medico_id=disponibilita.medico_id,
        sede_id=disponibilita.sede_id,
        data_ora=datetime.combine(disponibilita.data, disponibilita.ora_inizio),
        stato=stato,
    )
    db.add(appuntamento)
    return appuntamento


def crea_appuntamenti(db, slot_disponibili: list[Disponibilita], pazienti: list[Paziente], prestazioni: list[Prestazione]) -> int:
    appuntamenti_creati = 0
    for disponibilita in slot_disponibili:
        if random.random() >= 0.7:
            continue
        medico = disponibilita.medico
        prestazioni_del_medico = [
            p for p in prestazioni if p.specialita_id in {s.id for s in medico.specialita}
        ] or prestazioni
        prestazione = random.choice(prestazioni_del_medico)
        paziente = random.choice(pazienti)
        if disponibilita.data < date.today():
            stato = "completato" if random.random() < 0.75 else "annullato"
        else:
            stato = random.choice(["prenotato", "confermato"])
        prenota_slot(db, disponibilita, paziente, prestazione, stato)
        appuntamenti_creati += 1
    return appuntamenti_creati


def genera_pagamenti_mancanti(db) -> int:
    completati = db.query(Appuntamento).filter(Appuntamento.stato == "completato").all()
    creati = 0
    for appuntamento in completati:
        if appuntamento.pagamento is not None:
            continue
        prezzo_listino = float(appuntamento.prestazione.prezzo)
        importo = round(prezzo_listino * random.uniform(0.9, 1.1), 2)
        data_pagamento = min(
            appuntamento.data_ora.date() + timedelta(days=random.randint(0, 2)), date.today()
        )
        stato = "rimborsato" if random.random() < 0.08 else "pagato"
        db.add(
            Pagamento(
                appuntamento_id=appuntamento.id,
                importo=importo,
                data=data_pagamento,
                stato=stato,
            )
        )
        creati += 1
    return creati


def seed():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = LocalSession()

    sedi, specialita, prestazioni = crea_catalogo(db)
    get_or_create_utente(db, "admin@msmedicalcenter.it", "admin")

    medici, slot_disponibili = crea_medici(db, specialita, sedi)
    pazienti = crea_pazienti(db, NUMERO_PAZIENTI)

    db.flush()
    appuntamenti_creati = crea_appuntamenti(db, slot_disponibili, pazienti, prestazioni)

    db.flush()
    pagamenti_creati = genera_pagamenti_mancanti(db)

    nomi_medici = [f"{m.nome} {m.cognome}" for m in medici]
    nomi_pazienti = [f"{p.nome} {p.cognome}" for p in pazienti]

    db.commit()
    db.close()

    print("Seed completato:")
    print(f"  Sedi: {len(sedi)}")
    print(f"  Specialita: {len(specialita)}")
    print(f"  Prestazioni: {len(prestazioni)}")
    print(f"  Medici creati: {nomi_medici}")
    print(f"  Disponibilita create: {len(slot_disponibili)}")
    print(f"  Pazienti creati: {nomi_pazienti}")
    print(f"  Appuntamenti creati: {appuntamenti_creati}")
    print(f"  Pagamenti generati: {pagamenti_creati}")


if __name__ == "__main__":
    seed()
