import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getProduct, getAverageRating } from '../api/productApi';
import type { Product } from '../types';

export default function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [rating, setRating] = useState<number | null>(null);
  const [totalRatings, setTotalRatings] = useState<number>(0);

  useEffect(() => {
    if (!id) return;
    getProduct(id).then(setProduct).catch(console.error);
    getAverageRating(id)
      .then((res: { media: number; total?: number }) => {
        setRating(res.media ?? null);
        setTotalRatings(res.total ?? 0);
      })
      .catch(() => {
        setRating(null);
        setTotalRatings(0);
      });
  }, [id]);

  if (!product) return <div style={{ padding: '40px', textAlign: 'center', color: '#7c3aed' }}>⏳ Carregando produto...</div>;

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '16px' }}>
      <Link to="/" style={{ marginBottom: '24px', display: 'inline-flex', alignItems: 'center', gap: '8px', color: '#7c3aed', textDecoration: 'none', fontWeight: 'bold', cursor: 'pointer' }}>
        ← Voltar aos produtos
      </Link>

      <section style={{ borderRadius: '20px', border: '2px solid #ddd6fe', background: 'white', padding: '32px', boxShadow: '0 10px 25px rgba(168, 85, 247, 0.1)' }}>
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '40px' }}>
          <div style={{ overflow: 'hidden', borderRadius: '16px', background: 'linear-gradient(135deg, #a855f7 0%, #ec4899 100%)', minHeight: '400px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
            {product.imagem_url ? (
              <img
                src={product.imagem_url}
                alt={product.nome_produto}
                style={{ height: '100%', width: '100%', objectFit: 'cover' }}
              />
            ) : (
              <div style={{ color: 'white', fontSize: '80px' }}>📦</div>
            )}
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
            <h1 style={{ fontSize: '32px', fontWeight: 'bold', color: '#1f2937', margin: 0 }}>{product.nome_produto}</h1>
            <p style={{ display: 'inline-block', borderRadius: '20px', background: '#f3e8ff', padding: '8px 16px', fontSize: '14px', fontWeight: 'bold', color: '#7c3aed', margin: 0, width: 'fit-content' }}>{product.categoria_produto}</p>
            <p style={{ fontSize: '28px', fontWeight: 'bold', background: 'linear-gradient(to right, #a855f7, #ec4899)', backgroundClip: 'text', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent', margin: 0 }}>R$ {product.preco?.toFixed(2) ?? '0.00'}</p>
            
            <div style={{ borderTop: '2px solid #ddd6fe', paddingTop: '24px', display: 'flex', flexDirection: 'column', gap: '12px', color: '#374151' }}>
              <p style={{ fontWeight: 'bold', color: '#1f2937', margin: 0 }}>📦 Informações do Produto</p>
              <p style={{ margin: 0 }}>Peso: <span style={{ fontWeight: 'bold' }}>{product.peso_produto_gramas ?? '—'} g</span></p>
              <p style={{ margin: 0 }}>Dimensões: <span style={{ fontWeight: 'bold' }}>{product.comprimento_centimetros ?? '—'} × {product.altura_centimetros ?? '—'} × {product.largura_centimetros ?? '—'} cm</span></p>
            </div>

            <div style={{ borderTop: '2px solid #ddd6fe', paddingTop: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
              <p style={{ fontWeight: 'bold', color: '#1f2937', margin: 0 }}>⭐ Avaliações</p>
              <div style={{ display: 'flex', gap: '24px', alignItems: 'center', fontSize: '18px' }}>
                <div>
                  <p style={{ color: '#7c3aed', fontWeight: 'bold', fontSize: '24px', margin: 0 }}>{rating ? rating.toFixed(1) : '—'}</p>
                  <p style={{ color: '#6b7280', fontSize: '14px', margin: '4px 0 0 0' }}>de 5 estrelas</p>
                </div>
                <div style={{ borderLeft: '2px solid #ddd6fe', paddingLeft: '24px' }}>
                  <p style={{ color: '#1f2937', fontWeight: 'bold', fontSize: '20px', margin: 0 }}>{totalRatings}</p>
                  <p style={{ color: '#6b7280', fontSize: '14px', margin: '4px 0 0 0' }}>avaliações</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}
