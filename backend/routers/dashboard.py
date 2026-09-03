from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from core.database import get_db
from core.dependencies import RoleChecker
from schemas.dashboard import DashboardKPI, IncassoRaggruppato, PrestazioneStat
from services.dashboard import DashboardService

router = APIRouter(
    prefix="/api/dashboard",
    tags=["dashboard"],
    dependencies=[Depends(RoleChecker(["admin"]))],
)


@router.get(
    "/kpi",
    response_model=DashboardKPI,
    summary="KPI aggregati del periodo: incasso totale, numero prestazioni, ticket medio",
)
def get_kpi(da: date | None = None, a: date | None = None, db: Session = Depends(get_db)):
    return DashboardService(db).kpi(da, a)


@router.get(
    "/incassi",
    response_model=list[IncassoRaggruppato],
    summary="Incassi del periodo raggruppati per specialita, sede o mese",
)
def get_incassi(
    raggruppa: str = "specialita",
    da: date | None = None,
    a: date | None = None,
    db: Session = Depends(get_db),
):
    try:
        return DashboardService(db).incassi(da, a, raggruppa)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get(
    "/prestazioni",
    response_model=list[PrestazioneStat],
    summary="Numero di prestazioni erogate e relativo incasso nel periodo, per prestazione",
)
def get_prestazioni(da: date | None = None, a: date | None = None, db: Session = Depends(get_db)):
    return DashboardService(db).prestazioni(da, a)
