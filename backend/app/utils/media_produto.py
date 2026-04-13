def atualizar_media(produto, nova_avaliacao):
    total = produto.total_avaliacoes or 0
    media = produto.media_avaliacoes or 0.0

    nova_media = ((media * total) + nova_avaliacao) / (total + 1)

    produto.media_avaliacoes = nova_media
    produto.total_avaliacoes = total + 1