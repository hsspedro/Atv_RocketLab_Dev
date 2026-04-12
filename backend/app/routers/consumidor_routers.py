from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.consumidor import Consumidor
from app.schemas.consumidor_schema import (
    ConsumidorCreate,
    ConsumidorRead,
    ConsumidorUpdate
)

router = APIRouter(prefix="/consumidores", tags=["Consumidores"])


@router.post("/", response_model=ConsumidorRead)
def criar_consumidor(consumidor: ConsumidorCreate, db: Session = Depends(get_db)):

    existente = db.query(Consumidor).filter(
        Consumidor.id_consumidor == consumidor.id_consumidor
    ).first()

    if existente:
        raise HTTPException(
            status_code=409,
            detail="Consumidor já existe"
        )

    novo = Consumidor(**consumidor.dict())

    db.add(novo)
    db.commit()
    db.refresh(novo)

    return novo


@router.get("/")
def listar_consumidores(
    last_id: str | None = Query(None),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Consumidor)

    if last_id:
        query = query.filter(Consumidor.id_consumidor > last_id)

    result = query.order_by(Consumidor.id_consumidor).limit(limit).all()

    next_cursor = result[-1].id_consumidor if result else None

    return {
        "data": result,
        "next_cursor": next_cursor
    }


@router.get("/{id_consumidor}", response_model=ConsumidorRead)
def buscar_consumidor(id_consumidor: str, db: Session = Depends(get_db)):
    consumidor = db.query(Consumidor).filter(
        Consumidor.id_consumidor == id_consumidor
    ).first()

    if not consumidor:
        raise HTTPException(
            status_code=404,
            detail="Consumidor não encontrado"
        )

    return consumidor


@router.put("/{id_consumidor}", response_model=ConsumidorRead)
def atualizar_consumidor(
    id_consumidor: str,
    dados: ConsumidorUpdate,
    db: Session = Depends(get_db)
):
    consumidor = db.query(Consumidor).filter(
        Consumidor.id_consumidor == id_consumidor
    ).first()

    if not consumidor:
        raise HTTPException(
            status_code=404,
            detail="Consumidor não encontrado"
        )

    for key, value in dados.dict(exclude_unset=True).items():
        setattr(consumidor, key, value)

    db.commit()
    db.refresh(consumidor)

    return consumidor


@router.delete("/{id_consumidor}")
def deletar_consumidor(id_consumidor: str, db: Session = Depends(get_db)):
    consumidor = db.query(Consumidor).filter(
        Consumidor.id_consumidor == id_consumidor
    ).first()

    if not consumidor:
        raise HTTPException(
            status_code=404,
            detail="Consumidor não encontrado"
        )

    db.delete(consumidor)
    db.commit()

    return {"message": "Consumidor deletado"}