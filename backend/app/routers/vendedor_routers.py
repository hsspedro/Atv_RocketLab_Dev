from app.schemas.vendedor_schema import VendedorCreate, VendedorRead, VendedorUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vendedor import Vendedor


router = APIRouter(prefix="/vendedores", tags=["Vendedores"])


@router.post("/", response_model=VendedorRead)
def criar_vendedor(vendedor: VendedorCreate, db: Session = Depends(get_db)):

    existente = db.query(Vendedor).filter(
        Vendedor.id_vendedor == vendedor.id_vendedor
    ).first()

    if existente:
        raise HTTPException(
            status_code=409,
            detail="Vendedor já existe"
        )

    novo_vendedor = Vendedor(**vendedor.dict())

    db.add(novo_vendedor)
    db.commit()
    db.refresh(novo_vendedor)

    return novo_vendedor


@router.get("/", response_model=list[VendedorRead])
def listar_vendedores(db: Session = Depends(get_db)):
    return db.query(Vendedor).all()


@router.get("/{id_vendedor}", response_model=VendedorRead)
def buscar_vendedor(id_vendedor: str, db: Session = Depends(get_db)):
    vendedor = db.query(Vendedor).filter(
        Vendedor.id_vendedor == id_vendedor
    ).first()

    if not vendedor:
        raise HTTPException(
            status_code=404,
            detail="Vendedor não encontrado"
        )

    return vendedor


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
