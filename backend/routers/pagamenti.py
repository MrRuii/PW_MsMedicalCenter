from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import RoleChecker
from schemas.pagamento import PagamentoRead
from services.pagamento import PagamentoService

router = APIRouter(
    prefix="/api/pagamenti",
    tags=["pagamenti"],
    dependencies=[Depends(RoleChecker(["admin"]))],
)


@router.get(
    "",
    response_model=list[PagamentoRead],
    summary="Elenco pagamenti, con filtri opzionali per periodo e stato",
)
def get_pagamenti(
    da: date | None = None,
    a: date | None = None,
    stato: str | None = None,
    db: Session = Depends(get_db),
):
    return PagamentoService(db).lista_filtrata(da, a, stato)


@router.patch(
    "/{pagamento_id}/rimborsa",
    response_model=PagamentoRead,
    summary="Segna un pagamento come rimborsato",
)
def rimborsa_pagamento(pagamento_id: int, db: Session = Depends(get_db)):
    try:
        return PagamentoService(db).rimborsa(pagamento_id)
    except LookupError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
