from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.avaliacao_pedido import AvaliacaoPedido
from app.schemas.avaliacao_pedido_schema import AvaliacaoPedidoCreate, AvaliacaoPedidoRead, AvaliacaoPedidoUpdate

router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])


@router.post("/", response_model=AvaliacaoPedidoRead)
def criar_avaliacao(dados: AvaliacaoPedidoCreate, db: Session = Depends(get_db)):

    existente = db.query(AvaliacaoPedido).filter(
        AvaliacaoPedido.id_avaliacao == dados.id_avaliacao
    ).first()

    if existente:
        raise HTTPException(409, "Avaliação já existe")

    nova = AvaliacaoPedido(**dados.dict())

    db.add(nova)
    db.commit()
    db.refresh(nova)

    return nova


@router.get("/", response_model=list[AvaliacaoPedidoRead])
def listar_avaliacoes(db: Session = Depends(get_db)):
    return db.query(AvaliacaoPedido).all()


@router.get("/{id_avaliacao}", response_model=AvaliacaoPedidoRead)
def buscar_avaliacao(id_avaliacao: str, db: Session = Depends(get_db)):
    avaliacao = db.query(AvaliacaoPedido).filter(
        AvaliacaoPedido.id_avaliacao == id_avaliacao
    ).first()

    if not avaliacao:
        raise HTTPException(404, "Avaliação não encontrada")

    return avaliacao


@router.put("/{id_avaliacao}", response_model=AvaliacaoPedidoRead)
def atualizar_avaliacao(
    id_avaliacao: str,
    dados: AvaliacaoPedidoUpdate,
    db: Session = Depends(get_db)
):
    avaliacao = db.query(AvaliacaoPedido).filter(
        AvaliacaoPedido.id_avaliacao == id_avaliacao
    ).first()

    if not avaliacao:
        raise HTTPException(404, "Avaliação não encontrada")

    for key, value in dados.dict(exclude_unset=True).items():
        setattr(avaliacao, key, value)

    db.commit()
    db.refresh(avaliacao)

    return avaliacao


@router.delete("/{id_avaliacao}")
def deletar_avaliacao(id_avaliacao: str, db: Session = Depends(get_db)):
    avaliacao = db.query(AvaliacaoPedido).filter(
        AvaliacaoPedido.id_avaliacao == id_avaliacao
    ).first()

    if not avaliacao:
        raise HTTPException(404, "Avaliação não encontrada")

    db.delete(avaliacao)
    db.commit()

    return {"message": "Avaliação deletada"}