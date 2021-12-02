from fastapi import FastAPI, status
from pydantic.main import BaseModel
from pydantic.utils import unique_list
from fastapi.params import Body
from typing import List

 

app = FastAPI()


class BaseProdutoModel(BaseModel):
    nome: str
    valor: float

class AdicionarProdutoModel(BaseProdutoModel):
    id : int

class AlterarProdutoModel(BaseProdutoModel):
    pass

produtos = []


@app.get('/produtos')
def lista_produtos():
    return produtos


@app.post('/produtos', status_code=status.HTTP_201_CREATED)
def adicionar_produto(produto: AdicionarProdutoModel):
    produtos.append(produto)


@app.delete('/produtos/{id}', status_code=status.HTTP_204_NO_CONTENT)
def remover_produto(id: int):
    resultado = list(filter(lambda a: a[1].id == id, enumerate(produtos)))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Produto com o id: {id} nao foi encontrado')

    i, _ = resultado[0]
    del produtos[i]


@app.put('/produtos/{id}')
def alterar_produto(id: int, produto: AlterarProdutoModel):
    resultado = list(filter(lambda a: a.id == id, produtos))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Produto com o id: {id} nao foi encontrado')

    id_encontrado = resultado[0]
    id_encontrado.nome = produto.nome
    id_encontrado.valor = produto.valor
    

    return id_encontrado

@app.patch('/produtos/alterar-id/{id}')
def alterar_id_produto(id: int, id_novo: int = Body(...)):
    resultado = list(filter(lambda a: a.id == id, produtos))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Produto com id: {id} nao foi encontrado')

    id_encontrado = resultado[0]
    id_encontrado.id = id_novo

    return id_encontrado
