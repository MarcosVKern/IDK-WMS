class MovimentoEstoque:
    def __init__(self, id_movimento, origem, destino, dataSaida, dataEntrada, dataAlteracao, status, tipoMovimento, responsavel):
        self._id_movimento = id_movimento
        self._origem = origem
        self._destino = destino
        self._dataSaida = dataSaida
        self._dataEntrada = dataEntrada
        self._dataAlteracao = dataAlteracao
        self._status = status
        self._tipoMovimento = tipoMovimento
        self._responsavel = responsavel