"""
Script para calcular e atualizar os preços médios dos produtos
baseado nos preços dos itens de pedidos
"""

from app.database import SessionLocal
from app.models.produto import Produto
from app.models.item_pedido import ItemPedido
from sqlalchemy import func


def atualizar_precos():
    db = SessionLocal()

    try:
        # Obter todos os produtos
        produtos = db.query(Produto).all()

        for produto in produtos:
            # Calcular preço médio dos itens para este produto
            preco_medio = db.query(func.avg(ItemPedido.preco_BRL)).filter(
                ItemPedido.id_produto == produto.id_produto
            ).scalar()

            if preco_medio:
                produto.preco_BRL = float(preco_medio)
                print(
                    f"Produto {produto.id_produto} ({produto.nome_produto}): R$ {preco_medio:.2f}")
            else:
                print(
                    f"Produto {produto.id_produto} ({produto.nome_produto}): Sem preço encontrado")

        db.commit()
        print("✓ Preços atualizados com sucesso!")

    except Exception as e:
        db.rollback()
        print(f"✗ Erro ao atualizar preços: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    atualizar_precos()
