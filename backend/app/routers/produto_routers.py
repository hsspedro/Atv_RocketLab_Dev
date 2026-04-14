from fastapi import Query
from typing import Optional
from app.schemas.produto_schema import ProdutoUpdate, ProdutoCreate, ProdutoRead
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.produto import Produto
from app.models.categoria import Categoria
from app.models.item_pedido import ItemPedido
from app.models.avaliacao_pedido import AvaliacaoPedido
from app.utils.generate_id import generate_id


def imagem_produto_categoria(produto: Produto, db: Session) -> dict:
    categoria = db.query(Categoria).filter(
        Categoria.nome_categoria == produto.categoria_produto
    ).first()

    # Calcular preço médio dos itens de pedidos
    preco_medio = db.query(func.avg(ItemPedido.preco_BRL)).filter(
        ItemPedido.id_produto == produto.id_produto
    ).scalar()

    produto_dict = {
        "id_produto": produto.id_produto,
        "nome_produto": produto.nome_produto,
        "categoria_produto": produto.categoria_produto,
        "peso_produto_gramas": produto.peso_produto_gramas,
        "comprimento_centimetros": produto.comprimento_centimetros,
        "altura_centimetros": produto.altura_centimetros,
        "largura_centimetros": produto.largura_centimetros,
        "preco_BRL": preco_medio if preco_medio else produto.preco_BRL,
        "imagem_categoria": categoria.link_imagem if categoria else None
    }
    return produto_dict


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

    return imagem_produto_categoria(novo_produto, db)


@router.get("/")
def listar_produtos(
    last_id: Optional[str] = Query(None),
    nome: Optional[str] = Query(None),
    limit: int = Query(20, le=20),
    db: Session = Depends(get_db)
):
    query = db.query(Produto)

    if nome:
        query = query.filter(Produto.nome_produto.ilike(f"%{nome}%"))

    if last_id:
        query = query.filter(Produto.id_produto > last_id)

    result = query.order_by(Produto.id_produto).limit(limit).all()

    # Enriquecer produtos com imagens
    produtos_enriquecidos = [
        imagem_produto_categoria(p, db) for p in result]

    next_cursor = result[-1].id_produto if result else None

    return {
        "data": produtos_enriquecidos,
        "next_cursor": next_cursor
    }


@router.get("/buscar")
def buscar_produtos(
    nome: str = Query(..., min_length=1),
    limit: int = Query(20, le=20),
    db: Session = Depends(get_db)
):
    query = db.query(Produto).filter(Produto.nome_produto.ilike(f"%{nome}%"))

    result = query.order_by(Produto.nome_produto).limit(limit).all()

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Nenhum produto encontrado com esse nome"
        )

    produtos_enriquecidos = [
        imagem_produto_categoria(p, db) for p in result]

    return {
        "data": produtos_enriquecidos
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

    return imagem_produto_categoria(produto, db)


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

    return imagem_produto_categoria(produto, db)
