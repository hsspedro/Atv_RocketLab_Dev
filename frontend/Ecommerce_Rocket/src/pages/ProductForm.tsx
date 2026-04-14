import { useEffect, useState } from 'react';
import { createProduct, getProduct, updateProduct } from '../api/productApi';
import { useNavigate, useParams, Link } from 'react-router-dom';
import type { Product } from '../types';

export default function ProductForm({ edit }: { edit?: boolean }) {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Partial<Product>>({ nome_produto: '', categoria_produto: '', preco: 0 });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const nav = useNavigate();

  useEffect(() => {
    if (edit && id) {
      setLoading(true);
      getProduct(id)
        .then(setProduct)
        .catch(() => setError('Erro ao carregar produto'))
        .finally(() => setLoading(false));
    }
  }, [edit, id]);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      if (edit && id) {
        await updateProduct(id, product);
        nav(`/produtos/${id}`);
      } else {
        await createProduct(product);
        nav('/');
      }
    } catch (err) {
      setError('Falha ao salvar o produto');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '900px', margin: '0 auto', padding: '16px' }}>
      <Link to={edit && id ? `/produtos/${id}` : '/'} style={{ marginBottom: '24px', display: 'inline-flex', alignItems: 'center', gap: '8px', color: '#7c3aed', textDecoration: 'none', fontWeight: 'bold', cursor: 'pointer' }}>
        ← {edit ? 'Voltar ao produto' : 'Voltar'}
      </Link>

      <section style={{ borderRadius: '20px', border: '2px solid #ddd6fe', background: 'white', padding: '32px', boxShadow: '0 10px 25px rgba(168, 85, 247, 0.1)' }}>
        <h1 style={{ fontSize: '28px', fontWeight: 'bold', color: '#1f2937', margin: '0 0 24px 0' }}>
          {edit ? '✏️ Editar Produto' : '➕ Novo Produto'}
        </h1>

        {error && (
          <div style={{ padding: '16px', borderRadius: '12px', background: '#fee2e2', color: '#991b1b', marginBottom: '24px', fontWeight: '500' }}>
            {error}
          </div>
        )}

        <form onSubmit={submit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '24px', marginBottom: '24px' }}>
            {/* Nome Produto */}
            <div style={{ gridColumn: '1 / -1' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold', color: '#1f2937' }}>
                Nome do Produto <span style={{ color: '#dc2626' }}>*</span>
              </label>
              <input
                type="text"
                value={product.nome_produto ?? ''}
                onChange={(e) => setProduct({ ...product, nome_produto: e.target.value })}
                placeholder="Ex: Notebook Dell Inspiron"
                required
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  border: '2px solid #ddd6fe',
                  borderRadius: '12px',
                  fontSize: '16px',
                  outline: 'none',
                  boxSizing: 'border-box',
                  transition: 'border-color 0.3s'
                }}
                onFocus={(e) => { e.currentTarget.style.borderColor = '#a855f7'; }}
                onBlur={(e) => { e.currentTarget.style.borderColor = '#ddd6fe'; }}
              />
            </div>

            {/* Categoria */}
            <div>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold', color: '#1f2937' }}>
                Categoria <span style={{ color: '#dc2626' }}>*</span>
              </label>
              <input
                type="text"
                value={product.categoria_produto ?? ''}
                onChange={(e) => setProduct({ ...product, categoria_produto: e.target.value })}
                placeholder="Ex: Eletrônicos"
                required
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  border: '2px solid #ddd6fe',
                  borderRadius: '12px',
                  fontSize: '16px',
                  outline: 'none',
                  boxSizing: 'border-box',
                  transition: 'border-color 0.3s'
                }}
                onFocus={(e) => { e.currentTarget.style.borderColor = '#a855f7'; }}
                onBlur={(e) => { e.currentTarget.style.borderColor = '#ddd6fe'; }}
              />
            </div>

            {/* Preço */}
            <div>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold', color: '#1f2937' }}>
                Preço (R$) <span style={{ color: '#dc2626' }}>*</span>
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={product.preco ?? ''}
                onChange={(e) => setProduct({ ...product, preco: e.target.value === '' ? 0 : Number(e.target.value) })}
                placeholder="0.00"
                required
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  border: '2px solid #ddd6fe',
                  borderRadius: '12px',
                  fontSize: '16px',
                  outline: 'none',
                  boxSizing: 'border-box',
                  transition: 'border-color 0.3s'
                }}
                onFocus={(e) => { e.currentTarget.style.borderColor = '#a855f7'; }}
                onBlur={(e) => { e.currentTarget.style.borderColor = '#ddd6fe'; }}
              />
            </div>

            {/* Peso */}
            <div>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold', color: '#1f2937' }}>
                Peso (gramas)
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={product.peso_produto_gramas ?? ''}
                onChange={(e) => setProduct({ ...product, peso_produto_gramas: e.target.value === '' ? undefined : Number(e.target.value) })}
                placeholder="0.00"
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  border: '2px solid #ddd6fe',
                  borderRadius: '12px',
                  fontSize: '16px',
                  outline: 'none',
                  boxSizing: 'border-box',
                  transition: 'border-color 0.3s'
                }}
                onFocus={(e) => { e.currentTarget.style.borderColor = '#a855f7'; }}
                onBlur={(e) => { e.currentTarget.style.borderColor = '#ddd6fe'; }}
              />
            </div>

            {/* Comprimento */}
            <div>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold', color: '#1f2937' }}>
                Comprimento (cm)
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={product.comprimento_centimetros ?? ''}
                onChange={(e) => setProduct({ ...product, comprimento_centimetros: e.target.value === '' ? undefined : Number(e.target.value) })}
                placeholder="0.00"
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  border: '2px solid #ddd6fe',
                  borderRadius: '12px',
                  fontSize: '16px',
                  outline: 'none',
                  boxSizing: 'border-box',
                  transition: 'border-color 0.3s'
                }}
                onFocus={(e) => { e.currentTarget.style.borderColor = '#a855f7'; }}
                onBlur={(e) => { e.currentTarget.style.borderColor = '#ddd6fe'; }}
              />
            </div>

            {/* Altura */}
            <div>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold', color: '#1f2937' }}>
                Altura (cm)
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={product.altura_centimetros ?? ''}
                onChange={(e) => setProduct({ ...product, altura_centimetros: e.target.value === '' ? undefined : Number(e.target.value) })}
                placeholder="0.00"
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  border: '2px solid #ddd6fe',
                  borderRadius: '12px',
                  fontSize: '16px',
                  outline: 'none',
                  boxSizing: 'border-box',
                  transition: 'border-color 0.3s'
                }}
                onFocus={(e) => { e.currentTarget.style.borderColor = '#a855f7'; }}
                onBlur={(e) => { e.currentTarget.style.borderColor = '#ddd6fe'; }}
              />
            </div>

            {/* Largura */}
            <div>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold', color: '#1f2937' }}>
                Largura (cm)
              </label>
              <input
                type="number"
                step="0.01"
                min="0"
                value={product.largura_centimetros ?? ''}
                onChange={(e) => setProduct({ ...product, largura_centimetros: e.target.value === '' ? undefined : Number(e.target.value) })}
                placeholder="0.00"
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  border: '2px solid #ddd6fe',
                  borderRadius: '12px',
                  fontSize: '16px',
                  outline: 'none',
                  boxSizing: 'border-box',
                  transition: 'border-color 0.3s'
                }}
                onFocus={(e) => { e.currentTarget.style.borderColor = '#a855f7'; }}
                onBlur={(e) => { e.currentTarget.style.borderColor = '#ddd6fe'; }}
              />
            </div>

            {/* URL da Imagem */}
            <div style={{ gridColumn: '1 / -1' }}>
              <label style={{ display: 'block', marginBottom: '8px', fontWeight: 'bold', color: '#1f2937' }}>
                URL da Imagem
              </label>
              <input
                type="url"
                value={product.imagem_url ?? ''}
                onChange={(e) => setProduct({ ...product, imagem_url: e.target.value })}
                placeholder="https://exemplo.com/imagem.jpg"
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  border: '2px solid #ddd6fe',
                  borderRadius: '12px',
                  fontSize: '16px',
                  outline: 'none',
                  boxSizing: 'border-box',
                  transition: 'border-color 0.3s'
                }}
                onFocus={(e) => { e.currentTarget.style.borderColor = '#a855f7'; }}
                onBlur={(e) => { e.currentTarget.style.borderColor = '#ddd6fe'; }}
              />
            </div>
          </div>

          <div style={{ display: 'flex', gap: '16px', justifyContent: 'flex-end' }}>
            <Link to={edit && id ? `/produtos/${id}` : '/'} style={{ textDecoration: 'none' }}>
              <button
                type="button"
                style={{
                  padding: '12px 32px',
                  background: '#e5e7eb',
                  color: '#1f2937',
                  border: 'none',
                  borderRadius: '12px',
                  fontWeight: 'bold',
                  cursor: 'pointer',
                  fontSize: '16px',
                  transition: 'background 0.3s'
                }}
                onMouseEnter={(e) => { e.currentTarget.style.background = '#d1d5db'; }}
                onMouseLeave={(e) => { e.currentTarget.style.background = '#e5e7eb'; }}
              >
                Cancelar
              </button>
            </Link>
            <button
              type="submit"
              disabled={loading}
              style={{
                padding: '12px 32px',
                background: loading ? '#d1d5db' : '#a855f7',
                color: 'white',
                border: 'none',
                borderRadius: '12px',
                fontWeight: 'bold',
                cursor: loading ? 'not-allowed' : 'pointer',
                fontSize: '16px',
                transition: 'background 0.3s',
                opacity: loading ? 0.6 : 1
              }}
              onMouseEnter={(e) => { if (!loading) e.currentTarget.style.background = '#9333ea'; }}
              onMouseLeave={(e) => { if (!loading) e.currentTarget.style.background = '#a855f7'; }}
            >
              {loading ? '⏳ Salvando...' : (edit ? '💾 Atualizar' : '➕ Criar Produto')}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}
