from model.movimento_estoque import MovimentoEstoque
from model.dao.base_dao import Base_DAO

class MovimentoEstoque_DAO(Base_DAO):
    def save(self, movimento: MovimentoEstoque):
        sql = """insert into movimento_estoque (origem, destino, dataSaida, dataEntrada, dataAlteracao, status, tipoMovimento, responsavel) 
                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (movimento._origem, movimento._destino, movimento._dataSaida, movimento._dataEntrada,
                  movimento._dataAlteracao, movimento._status, movimento._tipoMovimento, movimento._responsavel)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        movimento._id_movimento = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return movimento
    
    def get_all(self):
        sql = """select me.ID_movimento, me.origem, me.destino, me.dataSaida, me.dataEntrada, me.dataAlteracao, me.status, me.tipoMovimento, me.responsavel 
                from movimento_estoque me
                inner join unidade_armazenamento ua on me.origem = ua.ID_unidade
                inner join unidade_armazenamento ua2 on me.destino = ua2.ID_unidade
                inner join tipo_movimento tm on me.tipoMovimento = tm.ID_tipo
                inner join funcionario f on me.responsavel = f.ID_funcionario"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        movimentos = []
        for (ID_movimento, origem, destino, dataSaida, dataEntrada, dataAlteracao, status, tipoMovimento, responsavel) in cursor:
            movimentos.append(MovimentoEstoque(ID_movimento, origem, destino, dataSaida, dataEntrada,
                                              dataAlteracao, status, tipoMovimento, responsavel))
        cursor.close()
        conn.close()
        return movimentos
    
    def get_by_id(self, id):
        sql = """select origem, destino, dataSaida, dataEntrada, dataAlteracao, status, tipoMovimento, responsavel 
                 from movimento_estoque where ID_movimento = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        movimento = None
        if row:
            origem, destino, dataSaida, dataEntrada, dataAlteracao, status, tipoMovimento, responsavel = row
            movimento = MovimentoEstoque(id, origem, destino, dataSaida, dataEntrada,
                                         dataAlteracao, status, tipoMovimento, responsavel)
        cursor.close()
        conn.close()
        return movimento
    
    def delete(self, id):
        sql = """delete from movimento_estoque where ID_movimento = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
    
    def update(self, movimento: MovimentoEstoque):
        sql = """update movimento_estoque set origem = %s, destino = %s, dataSaida = %s, dataEntrada = %s, 
                 dataAlteracao = %s, status = %s, tipoMovimento = %s, responsavel = %s where ID_movimento = %s"""
        
        values = (movimento._origem, movimento._destino, movimento._dataSaida, movimento._dataEntrada,
                  movimento._dataAlteracao, movimento._status, movimento._tipoMovimento, movimento._responsavel, movimento._id_movimento)
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return movimento