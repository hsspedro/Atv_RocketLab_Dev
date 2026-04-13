import type { Product } from '../../types';
import ProductCard from '../molecules/ProductCard';

interface ProductGridProps {
  products: Product[];
  loading?: boolean;
}

export default function ProductGrid({ products, loading = false }: ProductGridProps) {
  if (loading) {
    return (
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '24px' }}>
        {Array.from({ length: 6 }).map((_, index) => (
          <div key={index} style={{ height: '400px', borderRadius: '20px', background: '#e5e7eb', animation: 'pulse 2s infinite' }} />
        ))}
      </div>
    );
  }

  if (products.length === 0) {
    return (
      <div style={{ borderRadius: '20px', border: '2px dashed #a855f7', background: '#f3e8ff', padding: '48px', textAlign: 'center' }}>
        <p style={{ fontSize: '18px', color: '#7c3aed', margin: 0 }}>Nenhum produto encontrado.</p>
        <p style={{ marginTop: '8px', color: '#9333ea', margin: 0 }}>Tente uma busca diferente</p>
      </div>
    );
  }

  return (
    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))', gap: '24px' }}>
      {products.map((product) => (
        <ProductCard key={product.id_produto} product={product} />
      ))}
    </div>
  );
}
