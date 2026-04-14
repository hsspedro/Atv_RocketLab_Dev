export interface Product {
  id_produto: string;
  nome_produto: string;
  categoria_produto: string;
  peso_produto_gramas?: number;
  comprimento_centimetros?: number;
  altura_centimetros?: number;
  largura_centimetros?: number;
  preco?: number;
  preco_BRL?: number;
  imagem_url?: string;
  imagem_categoria?: string;
}

export interface CartItem {
  id_produto: string;
  quantidade: number;
  preco_unitario: number;
  produto?: Product;
}

export interface Cart {
  items: CartItem[];
  total: number;
}

export interface OrderItem {
  id_item?: string;
  id_produto: string;
  quantidade: number;
  preco_unitario: number;
  produto?: Product;
}

export interface Order {
  id_pedido?: string;
  id_consumidor: string;
  total: number;
  status?: string;
  items: OrderItem[];
}

export interface Review {
  id: number;
  product_id: number;
  rating: number; // 1-5
  comment?: string;
  created_at?: string;
}

export interface ProductReview {
  id_avaliacao: string;
  id_pedido: string;
  avaliacao: number; // 1-5
  titulo_comentario?: string;
  comentario?: string;
  data_comentario?: string;
  data_resposta?: string;
}

export interface Sale {
  id: number;
  product_id: number;
  quantity: number;
  total_price: number;
  sold_at: string;
}
