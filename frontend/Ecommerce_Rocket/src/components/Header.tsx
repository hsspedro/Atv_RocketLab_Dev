import { Link } from 'react-router-dom';
export default function Header() {
  return (
    <header style={{ padding: 12, borderBottom: '1px solid #ddd', display: 'flex', gap: 12 }}>
      <Link to="/">Catálogo</Link>
      <Link to="/produtos/new">Adicionar produto</Link>
    </header>
  );
}
