from app.schemas.vendedor_schema import VendedorCreate, VendedorRead, VendedorUpdate
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vendedor import Vendedor
from app.utils.generate_id import generate_id


router = APIRouter(prefix="/vendedores", tags=["Vendedores"])


@router.post("/", response_model=VendedorRead)
def criar_vendedor(vendedor: VendedorCreate, db: Session = Depends(get_db)):

    id_vendedor = generate_id()
    existente = db.query(Vendedor).filter(
        Vendedor.id_vendedor == id_vendedor
    ).first()

    if existente:
        raise HTTPException(
            status_code=409,
            detail="ID gerado já existe, tente novamente"
        )

    novo_vendedor = Vendedor(id_vendedor=id_vendedor, **vendedor.dict())

    db.add(novo_vendedor)
    db.commit()
    db.refresh(novo_vendedor)

    return novo_vendedor


@router.get("/")
def listar_vendedores(
    last_id: str | None = Query(None),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Vendedor)

    if last_id:
        query = query.filter(Vendedor.id_vendedor > last_id)

    result = query.order_by(Vendedor.id_vendedor).limit(limit).all()

    next_cursor = result[-1].id_vendedor if result else None

    return {
        "data": result,
        "next_cursor": next_cursor
    }


@router.get("/buscar")
def buscar_vendedor(
    nome: str = Query(..., min_length=1),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    result = db.query(Vendedor).filter(
        Vendedor.nome_vendedor.ilike(f"%{nome}%")
    ).order_by(Vendedor.nome_vendedor).limit(limit).all()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Nenhum vendedor encontrado com esse nome"
        )

    return {
        "data": result
    }



@router.put("/{id_vendedor}", response_model=VendedorRead)
def atualizar_vendedor(
    id_vendedor: str,
    dados: VendedorUpdate,
    db: Session = Depends(get_db)
):
    vendedor = db.query(Vendedor).filter(
        Vendedor.id_vendedor == id_vendedor
    ).first()

    if not vendedor:
        raise HTTPException(
            status_code=404,
            detail="Vendedor não encontrado"
        )

    for key, value in dados.dict(exclude_unset=True).items():
        setattr(vendedor, key, value)

    db.commit()
    db.refresh(vendedor)

    return vendedor


@router.delete("/{id_vendedor}")
def deletar_vendedor(id_vendedor: str, db: Session = Depends(get_db)):
    vendedor = db.query(Vendedor).filter(
        Vendedor.id_vendedor == id_vendedor
    ).first()

    if not vendedor:
        raise HTTPException(
            status_code=404,
            detail="Vendedor não encontrado"
        )

    db.delete(vendedor)
    db.commit()

    return {"message": "Vendedor deletado"}
