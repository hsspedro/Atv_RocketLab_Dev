from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.avaliacao_pedido import AvaliacaoPedido
from app.schemas.avaliacao_pedido_schema import AvaliacaoPedidoCreate, AvaliacaoPedidoRead, AvaliacaoPedidoUpdate
from app.utils.generate_id import generate_id
from app.utils.media_produto import atualizar_media
from app.models.produto import Produto
from app.models.item_pedido import ItemPedido
router = APIRouter(prefix="/avaliacoes", tags=["Avaliações"])


@router.post("/", response_model=AvaliacaoPedidoRead)
def criar_avaliacao(dados: AvaliacaoPedidoCreate, db: Session = Depends(get_db)):

    id_avaliacao = generate_id()

    existente = db.query(AvaliacaoPedido).filter(
        AvaliacaoPedido.id_avaliacao == id_avaliacao
    ).first()

    if existente:
        raise HTTPException(409, "ID gerado já existe, tente novamente")

    nova = AvaliacaoPedido(id_avaliacao=id_avaliacao, **dados.dict())
    db.add(nova)

    itens = db.query(ItemPedido).filter(
        ItemPedido.id_pedido == dados.id_pedido
    ).all()

    for item in itens:
        produto = db.query(Produto).filter(
            Produto.id_produto == item.id_produto
        ).first()

        if produto:
            atualizar_media(produto, dados.avaliacao)

    if item:
        produto = db.query(Produto).filter(
            Produto.id_produto == item.id_produto
        ).first()

        if produto:
            atualizar_media(produto, dados.avaliacao)
    
    db.commit()
    db.refresh(nova)

    return nova


@router.get("/")
def listar_avaliacoes(
    last_id: str | None = Query(None),
    limit: int = Query(50, le=100),
    id_pedido: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(AvaliacaoPedido)

    if id_pedido:
        query = query.filter(AvaliacaoPedido.id_pedido == id_pedido)

    if last_id:
        query = query.filter(AvaliacaoPedido.id_avaliacao > last_id)

    result = query.order_by(AvaliacaoPedido.id_avaliacao).limit(limit).all()

    next_cursor = result[-1].id_avaliacao if result else None

    return {
        "data": result,
        "next_cursor": next_cursor
    }


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
