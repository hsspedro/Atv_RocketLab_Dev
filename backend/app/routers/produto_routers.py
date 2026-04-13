from fastapi import Query
from typing import Optional
from app.schemas.produto_schema import ProdutoUpdate, ProdutoCreate, ProdutoRead
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.produto import Produto
from app.models.item_pedido import ItemPedido
from app.models.avaliacao_pedido import AvaliacaoPedido
from app.utils.generate_id import generate_id


router = APIRouter(prefix="/produtos", tags=["Produtos"])


@router.post("/", response_model=ProdutoRead)
def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    produto_data = produto.model_dump(exclude_none=True)
    id_produto = produto_data.pop("id_produto", None) or generate_id()

    existente = db.query(Produto).filter(
        Produto.id_produto == id_produto
    ).first()

    if existente:
        raise HTTPException(
            status_code=409,
            detail="Produto já existe"
        )

    novo_produto = Produto(id_produto=id_produto, **produto_data)

    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)

    return novo_produto


@router.get("/")
def listar_produtos(
    last_id: Optional[str] = Query(None),
    nome: Optional[str] = Query(None),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Produto)

    if nome:
        query = query.filter(Produto.nome_produto.ilike(f"%{nome}%"))

    if last_id:
        query = query.filter(Produto.id_produto > last_id)

    result = query.order_by(Produto.id_produto).limit(limit).all()

    next_cursor = result[-1].id_produto if result else None

    return {
        "data": result,
        "next_cursor": next_cursor
    }


@router.get("/buscar")
def buscar_produtos(
    nome: str = Query(..., min_length=1),
    limit: int = Query(50, le=100),
    db: Session = Depends(get_db)
):
    query = db.query(Produto).filter(Produto.nome_produto.ilike(f"%{nome}%"))

    result = query.order_by(Produto.nome_produto).limit(limit).all()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Nenhum produto encontrado com esse nome"
        )

    return {
        "data": result
    }


@router.get("/{id_produto}/media-avaliacoes")
def media_avaliacoes_produto(id_produto: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(
        Produto.id_produto == id_produto
    ).first()

    if not produto:
        raise HTTPException(404, "Produto não encontrado")

    return {
        "media": produto.media_avaliacoes or 0.0,
        "total": produto.total_avaliacoes or 0
    }


@router.get("/{id_produto}", response_model=ProdutoRead)
def buscar_produto(id_produto: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(
        Produto.id_produto == id_produto).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return produto


@router.delete("/{id_produto}")
def deletar_produto(id_produto: str, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(
        Produto.id_produto == id_produto).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    db.delete(produto)
    db.commit()

    return {"message": "Produto deletado"}


@router.put("/{id_produto}", response_model=ProdutoRead)
def atualizar_produto(id_produto: str, dados: ProdutoUpdate, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(
        Produto.id_produto == id_produto).first()

    if not produto:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    for key, value in dados.model_dump(exclude_unset=True).items():
        setattr(produto, key, value)

    db.commit()
    db.refresh(produto)

    return produto
