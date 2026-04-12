import csv
import os
from datetime import datetime

from app.database import SessionLocal

from app.models.produto import Produto
from app.models.pedido import Pedido
from app.models.consumidor import Consumidor
from app.models.vendedor import Vendedor
from app.models.item_pedido import ItemPedido
from app.models.avaliacao_pedido import AvaliacaoPedido

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")

def parse_datetime(value):
    if not value or value.strip() == "":
        return None
    try:
        return datetime.fromisoformat(value)
    except:
        return None


def parse_float(value):
    if not value or value == "":
        return None
    try:
        return float(value)
    except:
        return None


def load_all():
    db = SessionLocal()

    print(" Iniciando ingestão...")

    with open(os.path.join(DATA_DIR, "dim_consumidores.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)

        existentes = {c[0] for c in db.query(Consumidor.id_consumidor).all()}
        novos = []

        for row in reader:
            if row["id_consumidor"] in existentes:
                continue

            novos.append(Consumidor(
                id_consumidor=row["id_consumidor"],
                nome_consumidor=row["nome_consumidor"],
                prefixo_cep=row["prefixo_cep"],
                cidade=row["cidade"],
                estado=row["estado"]
            ))

        db.bulk_save_objects(novos)

    db.commit()
    print(f" Consumidores inseridos: {len(novos)}")

    with open(os.path.join(DATA_DIR, "dim_vendedores.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)

        existentes = {v[0] for v in db.query(Vendedor.id_vendedor).all()}
        novos = []

        for row in reader:
            if row["id_vendedor"] in existentes:
                continue

            novos.append(Vendedor(
                id_vendedor=row["id_vendedor"],
                nome_vendedor=row["nome_vendedor"],
                prefixo_cep=row["prefixo_cep"],
                cidade=row["cidade"],
                estado=row["estado"]
            ))

        db.bulk_save_objects(novos)

    db.commit()
    print(f" Vendedores inseridos: {len(novos)}")

    with open(os.path.join(DATA_DIR, "dim_produtos.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)

        existentes = {p[0] for p in db.query(Produto.id_produto).all()}
        novos = []

        for row in reader:
            if row["id_produto"] in existentes:
                continue

            novos.append(Produto(
                id_produto=row["id_produto"],
                nome_produto=row["nome_produto"],
                categoria_produto=row["categoria_produto"],
                peso_produto_gramas=parse_float(row.get("peso_produto_gramas")),
                comprimento_centimetros=parse_float(row.get("comprimento_centimetros")),
                altura_centimetros=parse_float(row.get("altura_centimetros")),
                largura_centimetros=parse_float(row.get("largura_centimetros")),
            ))

        db.bulk_save_objects(novos)

    db.commit()
    print(f" Produtos inseridos: {len(novos)}")

    with open(os.path.join(DATA_DIR, "fat_pedidos.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)

        existentes = {p[0] for p in db.query(Pedido.id_pedido).all()}
        novos = []

        for row in reader:
            if row["id_pedido"] in existentes:
                continue

            novos.append(Pedido(
                id_pedido=row["id_pedido"],
                id_consumidor=row["id_consumidor"],
                status=row.get("status"),
                pedido_compra_timestamp=parse_datetime(row.get("pedido_compra_timestamp")),
                pedido_entregue_timestamp=parse_datetime(row.get("pedido_entregue_timestamp")),
                data_estimada_entrega=parse_datetime(row.get("data_estimada_entrega")),
                tempo_entrega_dias=parse_float(row.get("tempo_entrega_dias")),
                tempo_entrega_estimado_dias=parse_float(row.get("tempo_entrega_estimado_dias")),
                diferenca_entrega_dias=parse_float(row.get("diferenca_entrega_dias")),
                entrega_no_prazo=row.get("entrega_no_prazo"),
            ))

        db.bulk_save_objects(novos)

    db.commit()
    print(f" Pedidos inseridos: {len(novos)}")

    with open(os.path.join(DATA_DIR, "fat_itens_pedidos.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)

        existentes = {
            (i.id_pedido, i.id_item)
            for i in db.query(ItemPedido.id_pedido, ItemPedido.id_item).all()
        }

        novos = []

        for row in reader:
            chave = (row["id_pedido"], int(row["id_item"]))

            if chave in existentes:
                continue

            novos.append(ItemPedido(
                id_pedido=row["id_pedido"],
                id_item=int(row["id_item"]),
                id_produto=row["id_produto"],
                id_vendedor=row["id_vendedor"],
                preco_BRL=float(row["preco_BRL"]),
                preco_frete=float(row["preco_frete"]),
            ))

        db.bulk_save_objects(novos)

    db.commit()
    print(f" Itens inseridos: {len(novos)}")

    with open(os.path.join(DATA_DIR, "fat_avaliacoes_pedidos.csv"), encoding="utf-8") as f:
        reader = csv.DictReader(f)

        existentes_db = {a[0] for a in db.query(AvaliacaoPedido.id_avaliacao).all()}
        existentes_csv = set()

        novos = []

        for row in reader:
            id_avaliacao = row["id_avaliacao"]

            # evita duplicado no banco
            if id_avaliacao in existentes_db:
                continue

            # evita duplicado dentro do CSV
            if id_avaliacao in existentes_csv:
                continue

            existentes_csv.add(id_avaliacao)

            novos.append(AvaliacaoPedido(
                id_avaliacao=id_avaliacao,
                id_pedido=row["id_pedido"],
                avaliacao=int(row["avaliacao"]),
                titulo_comentario=row.get("titulo_comentario"),
                comentario=row.get("comentario"),
                data_comentario=parse_datetime(row.get("data_comentario")),
                data_resposta=parse_datetime(row.get("data_resposta")),
            ))

        db.bulk_save_objects(novos)

    db.commit()
    print(f" Avaliações inseridas: {len(novos)}")
    db.close()
    print(" Ingestão finalizada com sucesso!")


if __name__ == "__main__":
    load_all()