from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime, date


class PedidoBase(BaseModel):
    id_consumidor: str = Field(..., min_length=1, max_length=32)
    pedido_compra_timestamp: Optional[datetime] = None


class PedidoCreate(PedidoBase):
    id_pedido: str = Field(..., min_length=1, max_length=32)


class PedidoUpdate(BaseModel):
    id_consumidor: Optional[str] = Field(None, min_length=1, max_length=32)
    status: Optional[str] = Field(None, min_length=1, max_length=50)
    pedido_compra_timestamp: Optional[datetime] = None
    pedido_entregue_timestamp: Optional[datetime] = None
    data_estimada_entrega: Optional[date] = None
    tempo_entrega_dias: Optional[float] = None
    tempo_entrega_estimado_dias: Optional[float] = None
    diferenca_entrega_dias: Optional[float] = None
    entrega_no_prazo: Optional[str] = None


class PedidoRead(PedidoBase):
    id_pedido: str = Field(..., min_length=1, max_length=32)
    status: Optional[str] = None
    pedido_compra_timestamp: Optional[datetime] = None
    pedido_entregue_timestamp: Optional[datetime] = None
    data_estimada_entrega: Optional[date] = None
    tempo_entrega_dias: Optional[float] = None
    tempo_entrega_estimado_dias: Optional[float] = None
    diferenca_entrega_dias: Optional[float] = None
    entrega_no_prazo: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
