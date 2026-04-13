from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.produto import Produto
from app.models.item_pedido import ItemPedido
from app.models.avaliacao_pedido import AvaliacaoPedido
from sqlalchemy import func


def atualizar_medias():
    db: Session = SessionLocal()

    resultados = db.query(
        ItemPedido.id_produto,
        func.avg(AvaliacaoPedido.avaliacao).label("media"),
        func.count(AvaliacaoPedido.id_avaliacao).label("total")
    ).join(
        AvaliacaoPedido, ItemPedido.id_pedido == AvaliacaoPedido.id_pedido
    ).group_by(
        ItemPedido.id_produto
    ).all()

    for r in resultados:
        produto = db.query(Produto).filter(
            Produto.id_produto == r.id_produto
        ).first()

        if produto:
            produto.media_avaliacoes = float(r.media)
            produto.total_avaliacoes = r.total

    db.commit()
    db.close()


if __name__ == "__main__":
    atualizar_medias()
