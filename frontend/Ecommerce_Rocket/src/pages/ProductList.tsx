import { useEffect, useState } from 'react';
import { getProducts } from '../api/productApi';
import type { Product } from '../types';
import ProductGrid from '../components/organisms/ProductGrid';

export default function ProductList() {
  const [query, setQuery] = useState('');
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function loadProducts() {
      setLoading(true);
      try {
        const data = await getProducts(query);
        setProducts(data);
      } catch (error) {
        console.error(error);
        setProducts([]);
      } finally {
        setLoading(false);
      }
    }
    loadProducts();
  }, [query]);

  return (
    <div style={{ maxWidth: '1400px', margin: '0 auto', padding: '16px', width: '100%' }}>
      <section style={{ background: 'linear-gradient(to bottom right, #a855f7, #ec4899)', borderRadius: '20px', padding: '32px', color: 'white', marginBottom: '24px', boxShadow: '0 10px 25px rgba(168, 85, 247, 0.3)' }}>
        <h1 style={{ fontSize: '40px', fontWeight: 'bold', margin: '0 0 20px 0' }}>🚀 Sua Loja de Produtos</h1>
        <p style={{ fontSize: '18px', marginTop: '16px', maxWidth: '700px', color: '#f3e8ff' }}>
          Descubra produtos incríveis com a melhor experiência de compra. Rápido, seguro e confiável.
        </p>
      </section>

      <section style={{ marginBottom: '40px' }}>
        <div style={{ marginBottom: '32px', display: 'flex', flexDirection: 'column', gap: '16px' }}>
          <div>
            <h2 style={{ fontSize: '28px', fontWeight: 'bold', color: '#1f2937', margin: '0 0 8px 0' }}>Nossos Produtos</h2>
            <p style={{ color: '#6b7280', margin: '0' }}>Explore nossa seleção completa</p>
          </div>
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="🔍 Buscar produtos..."
            style={{
              maxWidth: '400px',
              width: '100%',
              borderRadius: '16px',
              border: '2px solid #a855f7',
              padding: '12px 20px',
              fontSize: '16px',
              outline: 'none',
              boxShadow: '0 4px 10px rgba(168, 85, 247, 0.1)'
            }}
          />
        </div>

        <ProductGrid products={products} loading={loading} />
      </section>
    </div>
  );
}
