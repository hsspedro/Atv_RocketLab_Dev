import { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { getProduct, deleteProduct, getAverageRating } from '../api/productApi';
import type { Product } from '../types';

export default function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [avg, setAvg] = useState<number | null>(null);
  const nav = useNavigate();

  useEffect(() => {
    if (!id) return;
    getProduct(id).then(setProduct).catch(console.error);
    getAverageRating(id)
      .then((res: { media: number }) => setAvg(res.media ?? null))
      .catch(() => setAvg(null));
  }, [id]);

  if (!product) return <p>Carregando...</p>;

  return (
    <div>
      <h2>{product.nome_produto}</h2>
      <p>Categoria: {product.categoria_produto}</p>
      <p>Peso: {product.peso_produto_gramas ?? '—'} g</p>
      <p>Dimensões: {product.comprimento_centimetros ?? '—'} x {product.altura_centimetros ?? '—'} x {product.largura_centimetros ?? '—'} cm</p>
      <p>Média de avaliações: {avg !== null ? avg.toFixed(2) : '—'}</p>
      <div style={{ marginTop: 12 }}>
        <Link to={`/produtos/${product.id_produto}/edit`}>Editar</Link>
        <button onClick={async () => {
          if (!confirm('Excluir produto?')) return;
          try {
            await deleteProduct(product.id_produto);
            nav('/');
          } catch (e) { alert('Falha ao excluir'); }
        }}>Excluir</button>
      </div>
    </div>
  );
}
