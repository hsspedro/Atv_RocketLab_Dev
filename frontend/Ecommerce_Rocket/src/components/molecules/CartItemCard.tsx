import type { CartItem } from '../../types';
import Button from '../atoms/Button';

interface CartItemCardProps {
  item: CartItem;
  onChangeQuantity: (quantity: number) => void;
  onRemove: () => void;
}

export default function CartItemCard({ item, onChangeQuantity, onRemove }: CartItemCardProps) {
  return (
    <div className="rounded-[28px] border border-slate-200 bg-white p-6 shadow-sm">
      <div className="flex flex-col gap-4 lg:flex-row lg:items-center">
        <div className="h-28 w-28 overflow-hidden rounded-3xl bg-slate-100">
          <img
            src={item.produto?.imagem_url ?? 'https://via.placeholder.com/200'}
            alt={item.produto?.nome_produto}
            className="h-full w-full object-cover"
          />
        </div>
        <div className="flex-1">
          <h3 className="text-lg font-semibold text-slate-900">{item.produto?.nome_produto}</h3>
          <p className="mt-2 text-sm text-slate-600">R$ {item.preco_unitario.toFixed(2)} cada</p>
          <div className="mt-4 flex items-center gap-3">
            <Button variant="secondary" size="sm" onClick={() => onChangeQuantity(item.quantidade - 1)}>-</Button>
            <span className="min-w-[2rem] text-center text-base font-semibold">{item.quantidade}</span>
            <Button variant="secondary" size="sm" onClick={() => onChangeQuantity(item.quantidade + 1)}>+</Button>
          </div>
        </div>
        <div className="flex flex-col items-start gap-3 lg:items-end">
          <p className="text-lg font-semibold text-slate-900">R$ {(item.preco_unitario * item.quantidade).toFixed(2)}</p>
          <Button variant="danger" size="sm" onClick={onRemove}>
            Remover
          </Button>
        </div>
      </div>
    </div>
  );
}
