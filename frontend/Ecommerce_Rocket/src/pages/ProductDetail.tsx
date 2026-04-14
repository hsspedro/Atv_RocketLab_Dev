import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getProduct, getAverageRating, getProductReviews } from '../api/productApi';
import type { Product, ProductReview } from '../types';

export default function ProductDetail() {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Product | null>(null);
  const [rating, setRating] = useState<number | null>(null);
  const [totalRatings, setTotalRatings] = useState<number>(0);
  const [reviews, setReviews] = useState<ProductReview[]>([]);
  const [loadingReviews, setLoadingReviews] = useState(false);

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
    
    setLoadingReviews(true);
    getProductReviews(id)
      .then(setReviews)
      .catch(() => setReviews([]))
      .finally(() => setLoadingReviews(false));
  }, [id]);

  if (!product) return <div style={{ padding: '40px', textAlign: 'center', color: '#7c3aed' }}>⏳ Carregando produto...</div>;

  const renderStars = (rating: number) => {
    return [...Array(5)].map((_, i) => (
      <span key={i} style={{ fontSize: '16px', color: i < rating ? '#fbbf24' : '#d1d5db', marginRight: '2px' }}>★</span>
    ));
  };

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

      {/* Seção de Avaliações Detalhadas */}
      <section style={{ marginTop: '40px', borderRadius: '20px', border: '2px solid #ddd6fe', background: 'white', padding: '32px', boxShadow: '0 10px 25px rgba(168, 85, 247, 0.1)' }}>
        <h2 style={{ fontSize: '24px', fontWeight: 'bold', color: '#1f2937', margin: '0 0 24px 0' }}>💬 Avaliações dos Clientes</h2>
        
        {loadingReviews ? (
          <div style={{ padding: '40px', textAlign: 'center', color: '#7c3aed' }}>⏳ Carregando avaliações...</div>
        ) : reviews.length === 0 ? (
          <div style={{ padding: '40px', textAlign: 'center', color: '#6b7280' }}>Nenhuma avaliação disponível ainda.</div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {reviews.map((review) => (
              <div key={review.id_avaliacao} style={{ padding: '16px', borderRadius: '12px', border: '1px solid #e5e7eb', background: '#f9fafb' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '8px' }}>
                  <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                    <div style={{ display: 'flex' }}>
                      {renderStars(review.avaliacao)}
                    </div>
                    <span style={{ fontWeight: 'bold', color: '#1f2937' }}>({review.avaliacao}/5)</span>
                  </div>
                  {review.data_comentario && (
                    <span style={{ fontSize: '12px', color: '#6b7280' }}>
                      {new Date(review.data_comentario).toLocaleDateString('pt-BR')}
                    </span>
                  )}
                </div>
                
                {review.titulo_comentario && (
                  <h3 style={{ fontWeight: 'bold', color: '#1f2937', margin: '8px 0', fontSize: '16px' }}>
                    {review.titulo_comentario}
                  </h3>
                )}
                
                {review.comentario && (
                  <p style={{ color: '#374151', margin: '8px 0', lineHeight: '1.5' }}>
                    {review.comentario}
                  </p>
                )}
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}
