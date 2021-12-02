from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic.main import BaseModel
from pydantic.utils import unique_list
from fastapi.params import Body
from typing import List

######### inicio do projeto######

app = FastAPI()

class BaseCategoriaModel(BaseModel):
    nome: str
    

class AdicionarCategoriaModel(BaseCategoriaModel):
    id : int

class AlterarCategoriaModel(BaseCategoriaModel):
    pass


categorias = []

@app.get('/categorias')
def lista_categorias():
    return categorias


@app.post('/categorias', status_code=status.HTTP_201_CREATED)
def adicionar_categorias(categoria: AdicionarCategoriaModel):
    categorias.append(categoria)


@app.delete('/categorias/{id}', status_code=status.HTTP_204_NO_CONTENT)
def remover_categoria(id: int):
    resultado = list(filter(lambda a: a[1].id == id, enumerate(categorias)))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Categoria com id: {id} nao foi encontrado')

    i, _ = resultado[0]
    del categorias[i]


@app.put('/categorias/{id}')
def alterar_categoria(id: int, categoria: AlterarCategoriaModel):
    resultado = list(filter(lambda a: a.id == id, categorias))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Categoria com o id: {id} nao foi encontrado')

    id_encontrado = resultado[0]
    id_encontrado.nome = categoria.nome
    
    return id_encontrado

@app.patch('/categorias/alterar-id/{id}')
def alterar_id_categoria(id: int, id_novo: int = Body(...)):
    resultado = list(filter(lambda a: a.id == id, categorias))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Categoria com id: {id} nao foi encontrado')

    id_encontrado = resultado[0]
    id_encontrado.id = id_novo

    return id_encontrado