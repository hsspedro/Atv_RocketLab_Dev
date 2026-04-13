import { Routes, Route, Navigate } from 'react-router-dom';
import ProductList from './pages/ProductList';
import ProductDetail from './pages/ProductDetail';
import ProductForm from './pages/ProductForm';
import Header from './components/Header';

function App() {
  return (
    <>
      <Header />
      <main style={{ padding: 20 }}>
        <Routes>
          <Route path="/" element={<ProductList />} />
          <Route path="/produtos/new" element={<ProductForm />} />
          <Route path="/produtos/:id/edit" element={<ProductForm edit />} />
          <Route path="/produtos/:id" element={<ProductDetail />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </>
  );
}

export default App;