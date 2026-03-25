from model.produto_movimento import ProdutoMovimento
from model.dao.base_dao import Base_DAO

class ProdutoMovimento_DAO(Base_DAO):
    def save(self, movimento: ProdutoMovimento):
        sql = """insert into produto_movimento (quantidade, movimento, produto) VALUES (%s, %s, %s)"""

        values = (movimento._quantidade, movimento._movimento, movimento._produto)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        cursor.close()
        conn.close()
        return movimento
    
    def get_all(self):
        sql = """select pm.quantidade, pm.movimento, pm.produto 
                from produto_movimento pm
                inner join produto p on pm.produto = p.ID_produto
                inner join movimento m on pm.movimento = m.ID_movimento"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        movimentos = []
        for (ID_movimento, quantidade, movimento, produto) in cursor:
            movimentos.append(ProdutoMovimento(quantidade, movimento, produto, ID_movimento))
        cursor.close()
        conn.close()
        return movimentos
    
    def get_by_id(self, id_movimento, id_produto):
        sql = """select quantidade, movimento, produto from produto_movimento where ID_movimento = %s and produto = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id_movimento, id_produto))
        row = cursor.fetchone()
        movimento = None
        if row:
            quantidade, movimento, produto = row
            movimento = ProdutoMovimento(quantidade, movimento, produto, id_movimento, id_produto)
        cursor.close()
        conn.close()
        return movimento
    
    def delete(self, id_movimento, id_produto):
        sql = """delete from produto_movimento where ID_movimento = %s and produto = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id_movimento, id_produto))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
    
    def update(self, movimento: ProdutoMovimento):
        sql = """update produto_movimento set quantidade = %s where ID_movimento = %s and produto = %s"""

        values = (movimento._quantidade, movimento._movimento, movimento._produto)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0