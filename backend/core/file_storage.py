import uuid
from pathlib import Path

from core.config import settings

ESTENSIONI_CONSENTITE = {
    "application/pdf": ".pdf",
    "image/jpeg": ".jpg",
    "image/png": ".png",
}


class FileStorage:
    def __init__(self) -> None:
        self.cartella = Path(settings.referti_storage_path)
        self.cartella.mkdir(parents=True, exist_ok=True)

    def valida(self, content_type: str | None, dimensione: int) -> None:
        if content_type not in ESTENSIONI_CONSENTITE:
            raise ValueError("Formato file non supportato: sono ammessi solo PDF o immagini (JPEG, PNG)")
        limite = settings.referti_max_size_mb * 1024 * 1024
        if dimensione > limite:
            raise ValueError(f"Il file supera la dimensione massima di {settings.referti_max_size_mb} MB")

    def salva(self, content_type: str, contenuto: bytes) -> str:
        nome_file = f"{uuid.uuid4()}{ESTENSIONI_CONSENTITE[content_type]}"
        percorso = self.cartella / nome_file
        percorso.write_bytes(contenuto)
        return str(percorso)

    def elimina(self, percorso: str) -> None:
        Path(percorso).unlink(missing_ok=True)
