class Funcionario():
    def __init__(self, id, cep, bairro, cidade, uf, pais, nome, cargo, senha, email, situacao):
        self._id = id
        self._cep = cep
        self._bairro = bairro
        self._cidade = cidade
        self._uf = uf
        self._pais = pais
        self._nome = nome
        self._cargo = cargo
        self._email = email
        self._senha = senha
        self._situacao = situacao