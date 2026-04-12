from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.consumidor import Consumidor
from app.schemas.consumidor_schema import (
    ConsumidorCreate,
    ConsumidorRead,
    ConsumidorUpdate
)
from app.utils.generate_id import generate_id

router = APIRouter(prefix="/consumidores", tags=["Consumidores"])


@router.post("/", response_model=ConsumidorRead)
def criar_consumidor(consumidor: ConsumidorCreate, db: Session = Depends(get_db)):

    id_consumidor = generate_id()
    existente = db.query(Consumidor).filter(
        Consumidor.id_consumidor == id_consumidor
    ).first()

    if existente:
        raise HTTPException(
            status_code=409,
            detail="ID gerado já existe, tente novamente"
        )

    novo = Consumidor(id_consumidor=id_consumidor, **consumidor.dict())

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


@router.get("/buscar")
def buscar_consumidor(
    nome: str = Query(..., min_length=1),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    result = db.query(Consumidor).filter(
        Consumidor.nome_consumidor.ilike(f"%{nome}%")
    ).order_by(Consumidor.nome_consumidor).limit(limit).all()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Nenhum consumidor encontrado com esse nome"
        )

    return {
        "data": result
    }


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
