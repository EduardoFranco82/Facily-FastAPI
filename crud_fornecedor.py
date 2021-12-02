from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic.main import BaseModel
from pydantic.utils import unique_list
from fastapi.params import Body
from typing import List

app = FastAPI()

class BaseFornecedorModel(BaseModel):
    nome: str
    cidade: str
    

class AdicionarFornecedorModel(BaseFornecedorModel):
    id : int

class AlterarFornecedorModel(BaseFornecedorModel):
    pass


fornecedores = []


@app.get('/fornecedores')
def lista_fornecedores():
    return fornecedores


@app.post('/fornecedores', status_code=status.HTTP_201_CREATED)
def adicionar_fornecedores(fornecedor: AdicionarFornecedorModel):
    fornecedores.append(fornecedor)


@app.delete('/fornecedores/{id}', status_code=status.HTTP_204_NO_CONTENT)
def remover_fornecedor(id: int):
    resultado = list(filter(lambda a: a[1].id == id, enumerate(fornecedores)))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Fornecedor com id: {id} nao foi encontrado')

    i, _ = resultado[0]
    del fornecedores[i]


@app.put('/fornecedores/{id}')
def alterar_categoria(id: int, fornecedor: AlterarFornecedorModel):
    resultado = list(filter(lambda a: a.id == id, fornecedores))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Fornecedor com o id: {id} nao foi encontrado')

    id_encontrado = resultado[0]
    id_encontrado.nome = fornecedor.nome
    id_encontrado.cidade = fornecedor.cidade
     

    return id_encontrado

@app.patch('/fornecedores/alterar-id/{id}')
def alterar_id_fornecedor(id: int, id_novo: int = Body(...)):
    resultado = list(filter(lambda a: a.id == id, fornecedores))
    if not resultado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Categoria com id: {id} nao foi encontrado')

    id_encontrado = resultado[0]
    id_encontrado.id = id_novo

    return id_encontrado