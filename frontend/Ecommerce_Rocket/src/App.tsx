import { Routes, Route, Navigate } from 'react-router-dom';
import Header from './components/Header';
import ProductList from './pages/ProductList';
import ProductDetail from './pages/ProductDetail';
import ProductForm from './pages/ProductForm';

function App() {
  return (
    <>
      <Header />
      <main style={{ flex: 1, backgroundColor: '#f9fafb', padding: '40px 0', minHeight: 'calc(100vh - 100px)' }}>
        <Routes>
          <Route path="/" element={<ProductList />} />
          <Route path="/produtos/:id" element={<ProductDetail />} />
          <Route path="/produtos/:id/editar" element={<ProductForm edit={true} />} />
          <Route path="/novo-produto" element={<ProductForm edit={false} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </>
  );
}

export default App;