from fastapi import FastAPI
from app.routers import produto_routers, vendedor_routers, pedido_routers, consumidor_routers, avaliacao_pedido_routers, item_pedido_routers


app = FastAPI(
    title="Sistema de Compras Online",
    description="API para gerenciamento de pedidos, produtos, consumidores e vendedores.",
    version="1.0.0",
)
app.include_router(produto_routers.router)
app.include_router(vendedor_routers.router)
app.include_router(pedido_routers.router)
app.include_router(consumidor_routers.router)
app.include_router(avaliacao_pedido_routers.router)
app.include_router(item_pedido_routers.router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "message": "API rodando com sucesso!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
