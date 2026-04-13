import { Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import ProductList from './pages/ProductList';
import ProductDetail from './pages/ProductDetail';

function App() {
  return (
    <>
      <Header />
      <main style={{ flex: 1, backgroundColor: '#f9fafb', padding: '40px 0', minHeight: 'calc(100vh - 100px)' }}>
        <Routes>
          <Route path="/" element={<ProductList />} />
          <Route path="/produtos/:id" element={<ProductDetail />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </>
  );
}

export default App;