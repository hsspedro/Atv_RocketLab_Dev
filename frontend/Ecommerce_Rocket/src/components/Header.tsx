import { Link } from 'react-router-dom';

export default function Header() {
  return (
    <header style={{ background: 'linear-gradient(to right, #a855f7, #ec4899, #ef4444)', borderBottom: '1px solid #ccc', padding: '0' }}>
      <div style={{ maxWidth: '1400px', margin: '0 auto', display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '20px 16px', gap: '16px', flexWrap: 'wrap' }}>
        <Link to="/" style={{ fontSize: '28px', fontWeight: 'bold', color: 'white', textDecoration: 'none', cursor: 'pointer' }}>
          🚀 Rocket E-cormmece
        </Link>

        <nav style={{ display: 'flex', gap: '24px', alignItems: 'center' }}>
          <Link to="/" style={{ color: 'white', fontWeight: 'bold', textDecoration: 'none', cursor: 'pointer' }}>
            Produtos
          </Link>
        </nav>
      </div>
    </header>
  );
}
