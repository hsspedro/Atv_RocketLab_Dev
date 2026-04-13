import { useEffect, useState } from 'react';
import { getProducts } from '../api/productApi';
import type { Product } from '../types';
import { Link } from 'react-router-dom';
import useDebounce from '../hooks/useDebounce';

export default function ProductList() {
  const [q, setQ] = useState('');
  const dq = useDebounce(q, 300);
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    setLoading(true);
    getProducts(dq).then((res: Product[]) => {
      setProducts(res || []);
    }).catch(console.error)
      .finally(() => setLoading(false));
  }, [dq]);

  return (
    <div>
      <h1>Produtos</h1>
      <input value={q} onChange={(e) => setQ(e.target.value)} placeholder="Buscar produtos..." />
      {loading ? <p>Carregando...</p> : (
        <ul>
          {products.map(p => (
            <li key={p.id_produto}>
              <Link to={`/produtos/${p.id_produto}`}>
                {p.nome_produto} — {p.categoria_produto}
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
