from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic.main import BaseModel
from pydantic.utils import unique_list
from fastapi.params import Body
from typing import List

app = FastAPI()

class BaseCompradorModel(BaseModel):
    nome : str
    cidade : str
    idade : int

class AdicionarCompradorModel(BaseCompradorModel):
    cpf : str

class AlterarCompradorModel(BaseCompradorModel):
    pass

compradores = []

@app.get('/compradores')
def lista_compradores():
    return compradores

@app.post('/compradores', status_code= status.HTTP_201_CREATED)
def adicionar_compradores (comprador: AdicionarCompradorModel):
    compradores.append(comprador)

@app.delete('/compradores/{cpf}', status_code= status.HTTP_204_NO_CONTENT)
def remover_comprador (cpf: str):
        resultado = list(filter(lambda a: a[1].cpf == cpf, enumerate(compradores)))
        if not resultado:
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                                datail = 'Comprador com cpf {} não foi encontrado'.format(cpf))

        i, _ = resultado[0]
        del compradores[i]

@app.put('/compradores {cpf}')
def alterar_comprador(cpf:str, comprador: AlterarCompradorModel):
    resultado = list(filter(lambda a: a.cpf == cpf, compradores))
    # print(resultado)
    if not resultado:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = 'Comprador com cpf {} não foi encontrado'.format(cpf))

    id_encontrado = resultado[0]
    id_encontrado.nome = comprador.nome
    id_encontrado.cidade = comprador.cidade
    id_encontrado.idade = comprador.idade

    return id_encontrado


@app.patch('/compradores/alterar-cpf {cpf}')
def alterar_comprador( cpf: str, cpf_novo: str = Body(...)):
    resultado= list(filter(lambda a:a.cpf== cpf))
    if not resultado:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND,
                            detail = 'Comprador com cpf{} não foi encontrado'.format(cpf))

    cpf_encontrado = resultado[0]
    cpf_encontrado.cpf = cpf_novo

    return cpf_encontrado