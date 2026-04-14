from pydantic import BaseModel, Field


class CategoriaBase(BaseModel):
    nome_categoria: str = Field(..., min_length=1, max_length=100)
    link_imagem: str = Field(..., min_length=1, max_length=500)


class CategoriaRead(CategoriaBase):
    model_config = {"from_attributes": True}
