from datetime import date

from model.movimento_estoque import MovimentoEstoque
from model.dao.base_dao import Base_DAO

class MovimentoEstoque_DAO(Base_DAO):
    def save(self, movimento: MovimentoEstoque):
        sql = """call sp_criar_movimento(%s, %s, %s, %s)"""

        values = (movimento._origem, movimento._destino, movimento._tipoMovimento, movimento._responsavel)
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)

        cursor.execute("SELECT LAST_INSERT_ID()")
        row = cursor.fetchone()
        if row:
            movimento._id_movimento = row[0]
        else:
            cursor.execute("SELECT MAX(ID_movimento) FROM movimento_estoque")
            row2 = cursor.fetchone()
            if row2:
                movimento._id_movimento = row2[0]

        conn.commit()
        cursor.close()
        conn.close()
        return movimento
    
    def get_all(self):
        sql = """select me.ID_movimento, me.origem, me.destino, me.dataSaida, me.dataEntrada, me.dataAlteracao, me.status, tm.tipoMovimento as tipoMovimento, f.nome as responsavel 
                from movimento_estoque me
                left join unidade_armazenamento ua on me.origem = ua.ID_unidade
                left join unidade_armazenamento ua2 on me.destino = ua2.ID_unidade
                left join tipo_movimento tm on me.tipoMovimento = tm.ID_tipo
                left join funcionario f on me.responsavel = f.ID_funcionario"""

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
    
    def delete(self):
        pass
    
    def update(self, movimento: MovimentoEstoque):
        sql = """update movimento_estoque set origem = %s, destino = %s, dataSaida = %s, dataEntrada = %s, 
                 dataAlteracao = %s, status = %s, tipoMovimento = %s, responsavel = %s where ID_movimento = %s"""
        
        status = movimento._status
        if movimento._tipoMovimento == 1:  # Entrada
            movimento._dataAlteracao = date.today()
            status = "Efetivado"
        elif movimento._tipoMovimento == 2: # Saída
            match status:
                case "Pendente":
                    status = "Em separação"
                case "Em separação":
                    status = "Despachado"
        elif movimento._tipoMovimento == 3: # Interno
            match status:
                case "Pendente":
                    status = "Em separação"
                case "Em separação":
                    status = "Despachado"
                case "Despachado":
                    status = "Efetivado"

        values = (movimento._origem, movimento._destino, movimento._dataSaida, movimento._dataEntrada,
                  movimento._dataAlteracao, status, movimento._tipoMovimento, movimento._responsavel, movimento._id_movimento)
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return movimento
    
    def cancela_movimento(self, id):
        sql = """update movimento_estoque set status = 'Cancelado', dataAlteracao = %s where ID_movimento = %s"""

        values = (date.today(), id)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        affected_rows = cursor.rowcount
        conn.commit()
        cursor.close()
        conn.close()
        return affected_rows > 0
