from app.schemas.pedido_schema import PedidoCreate, PedidoRead, PedidoUpdate
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.pedido import Pedido

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=PedidoRead)
def criar_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    novo_pedido = Pedido(**pedido.dict())

    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)

    return novo_pedido

@router.get("/", response_model=list[PedidoRead])
def listar_pedidos(db: Session = Depends(get_db)):
    return db.query(Pedido).all()

@router.get("/{id_pedido}", response_model=PedidoRead)
def buscar_pedido(id_pedido: str, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    return pedido

@router.put("/{id_pedido}", response_model=PedidoRead)
def atualizar_pedido(id_pedido: str, dados: PedidoUpdate, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    for key, value in dados.dict(exclude_unset=True).items():
        setattr(pedido, key, value)

    db.commit()
    db.refresh(pedido)

    return pedido

@router.delete("/{id_pedido}")
def deletar_pedido(id_pedido: str, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.id_pedido == id_pedido).first()

    if not pedido:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    db.delete(pedido)
    db.commit()

    return {"message": "Pedido deletado"}