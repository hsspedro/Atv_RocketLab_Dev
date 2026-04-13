import { useEffect, useState } from 'react';
import { createProduct, getProduct, updateProduct } from '../api/productApi';
import { useNavigate, useParams } from 'react-router-dom';
import type { Product } from '../types';

export default function ProductForm({ edit }: { edit?: boolean }) {
  const { id } = useParams<{ id: string }>();
  const [product, setProduct] = useState<Partial<Product>>({ nome_produto: '', categoria_produto: '' });
  const nav = useNavigate();

  useEffect(() => {
    if (edit && id) {
      getProduct(id).then(setProduct as any).catch(console.error);
    }
  }, [edit, id]);

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (edit && id) {
        await updateProduct(id, product);
      } else {
        await createProduct(product);
      }
      nav('/');
    } catch (err) {
      alert('Falha ao salvar');
    }
  };

  
  return (
    <form onSubmit={submit}>
      <h2>{edit ? 'Editar' : 'Novo'} Produto</h2>
      <div>
        <label>Nome<input value={product.nome_produto ?? ''} onChange={(e) => setProduct({ ...product, nome_produto: e.target.value })} required /></label>
      </div>
      <div>
        <label>Categoria<input value={product.categoria_produto ?? ''} onChange={(e) => setProduct({ ...product, categoria_produto: e.target.value })} required /></label>
      </div>
      <div>
        <label>Peso (g)<input type="number" step="0.01" value={product.peso_produto_gramas ?? ''} onChange={(e) => setProduct({ ...product, peso_produto_gramas: e.target.value === '' ? undefined : Number(e.target.value) })} /></label>
      </div>
      <div>
        <label>Comprimento (cm)<input type="number" step="0.01" value={product.comprimento_centimetros ?? ''} onChange={(e) => setProduct({ ...product, comprimento_centimetros: e.target.value === '' ? undefined : Number(e.target.value) })} /></label>
      </div>
      <div>
        <label>Altura (cm)<input type="number" step="0.01" value={product.altura_centimetros ?? ''} onChange={(e) => setProduct({ ...product, altura_centimetros: e.target.value === '' ? undefined : Number(e.target.value) })} /></label>
      </div>
      <div>
        <label>Largura (cm)<input type="number" step="0.01" value={product.largura_centimetros ?? ''} onChange={(e) => setProduct({ ...product, largura_centimetros: e.target.value === '' ? undefined : Number(e.target.value) })} /></label>
      </div>
      <button type="submit">Salvar</button>
    </form>
  );
}
