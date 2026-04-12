from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.item_pedido import ItemPedido
from app.schemas.item_pedido_schema import ItemPedidoCreate, ItemPedidoRead, ItemPedidoUpdate
from app.utils.generate_id import generate_id


router = APIRouter(prefix="/itens", tags=["ItensPedido"])


@router.post("/", response_model=ItemPedidoRead)
def criar_item_pedido(item: ItemPedidoCreate, db: Session = Depends(get_db)):
    id_item = generate_id()
    existente = db.query(ItemPedido).filter(
        ItemPedido.id_item == id_item).first()

    if existente:
        raise HTTPException(
            status_code=409,
            detail="ID gerado já existe, tente novamente"
        )

    novo_item = ItemPedido(
        id_pedido=item.id_pedido,
        id_item=id_item,
        id_produto=item.id_produto,
        id_vendedor=item.id_vendedor,
        preco_BRL=item.preco_BRL,
        preco_frete=item.preco_frete
    )

    db.add(novo_item)
    db.commit()
    db.refresh(novo_item)

    return novo_item


@router.get("/")
def listar_itens(
    last_id: str | None = Query(None),
    limit: int = Query(50, le=100),
    id_pedido: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(ItemPedido)

    if id_pedido:
        query = query.filter(ItemPedido.id_pedido == id_pedido)

    if last_id:
        query = query.filter(ItemPedido.id_item > last_id)

    result = query.order_by(ItemPedido.id_item).limit(limit).all()

    next_cursor = result[-1].id_item if result else None

    return {
        "data": result,
        "next_cursor": next_cursor
    }


@router.get("/{id_pedido}/{id_item}", response_model=ItemPedidoRead)
def buscar_item(id_pedido: str, id_item: str, db: Session = Depends(get_db)):
    item = db.query(ItemPedido).filter(
        ItemPedido.id_pedido == id_pedido,
        ItemPedido.id_item == id_item
    ).first()

    if not item:
        raise HTTPException(404, "Item não encontrado")

    return item


@router.put("/{id_pedido}/{id_item}", response_model=ItemPedidoRead)
def atualizar_item(
    id_pedido: str,
    id_item: str,
    dados: ItemPedidoUpdate,
    db: Session = Depends(get_db)
):
    item = db.query(ItemPedido).filter(
        ItemPedido.id_pedido == id_pedido,
        ItemPedido.id_item == id_item
    ).first()

    if not item:
        raise HTTPException(404, "Item não encontrado")

    for key, value in dados.dict(exclude_unset=True).items():
        setattr(item, key, value)

    db.commit()
    db.refresh(item)

    return item


@router.delete("/{id_pedido}/{id_item}")
def deletar_item(id_pedido: str, id_item: str, db: Session = Depends(get_db)):
    item = db.query(ItemPedido).filter(
        ItemPedido.id_pedido == id_pedido,
        ItemPedido.id_item == id_item
    ).first()

    if not item:
        raise HTTPException(404, "Item não encontrado")

    db.delete(item)
    db.commit()

    return {"message": "Item deletado"}
