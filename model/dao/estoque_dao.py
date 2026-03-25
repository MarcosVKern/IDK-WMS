from model.estoque import Estoque
from model.dao.base_dao import Base_DAO

class Estoque_DAO(Base_DAO):
    def save(self, estoque: Estoque):
        sql = """insert into estoque (produto, UNarmazenamento, quantidade) VALUES (%s, %s, %s)"""

        values = (estoque._produto, estoque._UNarmazenamento, estoque._quantidade)
        
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        estoque._id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return estoque
    
    def get_all(self):
        sql = """select e.produto, e.UNarmazenamento, e.quantidade
                from estoque e
                inner join produto p on e.produto = p.ID_produto
                inner join unidade_armazenamento u on e.UNarmazenamento = u.ID_unidade"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        estoques = []
        for (produto, UNarmazenamento, quantidade) in cursor:
            estoques.append(Estoque(produto, UNarmazenamento, quantidade))
        cursor.close()
        conn.close()
        return estoques
    
    def get_by_id(self, id_produto, id_unidade):
        sql = """select e.produto, e.UNarmazenamento, e.quantidade 
                from estoque e
                inner join produto p on e.produto = p.ID_produto
                inner join unidade_armazenamento u on e.UNarmazenamento = u.ID_unidade
                where e.produto = %s and e.UNarmazenamento = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id_produto, id_unidade))
        row = cursor.fetchone()
        estoque = None
        if row:
            produto, UNarmazenamento, quantidade = row
            estoque = Estoque(produto, UNarmazenamento, quantidade)
        cursor.close()
        conn.close()
        return estoque

    def delete(self, id_produto, id_unidade):
        sql = """delete from estoque where produto = %s and UNarmazenamento = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id_produto, id_unidade))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0

    def update(self, estoque: Estoque):
        sql = """update estoque set quantidade = %s where produto = %s and UNarmazenamento = %s"""

        values = (estoque._quantidade, estoque._produto, estoque._UNarmazenamento)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0