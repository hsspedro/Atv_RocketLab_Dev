from app.database import engine
from sqlalchemy import text

with engine.connect() as conn:
    conn.execute(text("CREATE INDEX IF NOT EXISTS idx_pedido_id ON pedidos(id_pedido)"))
    conn.commit()