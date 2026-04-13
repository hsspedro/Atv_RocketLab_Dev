import { Link } from 'react-router-dom';
import type { Product } from '../../types';

interface ProductCardProps {
  product: Product;
}

export default function ProductCard({ product }: ProductCardProps) {
  return (
    <article style={{ overflow: 'hidden', borderRadius: '16px', border: '1px solid #ddd6fe', backgroundColor: 'white', boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)', transition: 'all 0.3s ease', cursor: 'pointer' }} onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.boxShadow = '0 10px 20px rgba(168, 85, 247, 0.2)'; (e.currentTarget as HTMLElement).style.transform = 'translateY(-8px)'; }} onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)'; (e.currentTarget as HTMLElement).style.transform = 'translateY(0)'; }}>
      <Link to={`/produtos/${product.id_produto}`} style={{ display: 'block', height: '240px', overflow: 'hidden', background: 'linear-gradient(135deg, #a855f7 0%, #ec4899 100%)', textDecoration: 'none', position: 'relative' }}>
        {product.imagem_url ? (
          <img
            src={product.imagem_url}
            alt={product.nome_produto}
            style={{ height: '100%', width: '100%', objectFit: 'cover', transition: 'transform 0.5s ease' }}
          />
        ) : (
          <div style={{ height: '100%', width: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'white', fontSize: '48px' }}>
            🛍️
          </div>
        )}
      </Link>
      <div style={{ padding: '24px' }}>
        <p style={{ margin: '0 0 8px 0', display: 'inline-block', borderRadius: '20px', background: '#f3e8ff', padding: '4px 12px', fontSize: '12px', fontWeight: 'bold', textTransform: 'uppercase', color: '#7c3aed' }}>
          {product.categoria_produto}
        </p>
        <h3 style={{ margin: '8px 0', fontSize: '18px', fontWeight: 'bold', color: '#1f2937', overflow: 'hidden', textOverflow: 'ellipsis', display: '-webkit-box', WebkitLineClamp: 2, WebkitBoxOrient: 'vertical' }}>{product.nome_produto}</h3>
        <p style={{ margin: '16px 0', fontSize: '24px', fontWeight: 'bold', background: 'linear-gradient(to right, #a855f7, #ec4899)', backgroundClip: 'text', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>R$ {product.preco?.toFixed(2) ?? '0.00'}</p>
        <Link to={`/produtos/${product.id_produto}`} style={{ textDecoration: 'none', width: '100%' }}>
          <button style={{ width: '100%', padding: '12px 16px', background: '#a855f7', color: 'white', border: 'none', borderRadius: '12px', fontWeight: 'bold', cursor: 'pointer', fontSize: '14px', transition: 'background 0.3s ease' }} onMouseEnter={(e) => { (e.currentTarget as HTMLElement).style.background = '#9333ea'; }} onMouseLeave={(e) => { (e.currentTarget as HTMLElement).style.background = '#a855f7'; }}>
            Ver Detalhes →
          </button>
        </Link>
      </div>
    </article>
  );
}
