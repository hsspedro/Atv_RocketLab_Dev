import client from './client';
import type { Product, ProductReview } from '../types';

export const getProducts = (q?: string, lastId?: string, limit = 50) => {
  const params = new URLSearchParams();
  if (q) params.set('nome', q);
  if (lastId) params.set('last_id', lastId);
  if (limit) params.set('limit', String(limit));
  const query = params.toString() ? `?${params.toString()}` : '';

  return client.request(`/produtos${query}`).then((res: { data: Product[] }) => res.data);
};

export const getProduct = (id: string) => client.request(`/produtos/${id}`);

export const createProduct = (payload: Partial<Product>) =>
  client.request('/produtos', { method: 'POST', body: JSON.stringify(payload) });

export const updateProduct = (id: string, payload: Partial<Product>) =>
  client.request(`/produtos/${id}`, { method: 'PUT', body: JSON.stringify(payload) });

export const deleteProduct = (id: string) =>
  client.request(`/produtos/${id}`, { method: 'DELETE' });

export const getAverageRating = (id: string) =>
  client.request(`/produtos/${id}/media-avaliacoes`);

export const getProductReviews = (id: string): Promise<ProductReview[]> =>
  client.request(`/avaliacoes/${id}/avaliacoes`).then((res: ProductReview[]) => res);
