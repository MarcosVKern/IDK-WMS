from model.produto import Produto
from model.dao.base_dao import Base_DAO

class Produto_DAO(Base_DAO):
    def save(self, produto:Produto):
        sql = """insert into (nome, descricao, imagem) values (%s, %s, %s)"""

        values = (produto._nome, produto._descricao, produto._imagem)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        produto._id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return produto
    
    def get_all(self):
        sql = """select id, nome, descricao, imagem from produto"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        produtos = []
        for (id, nome, descricao, imagem) in cursor:
            produtos.append(Produto(id, nome, descricao, imagem))
        cursor.close()
        conn.close()
        return produtos
    
    def get_by_id(self, id):
        sql = """select nome, descricao, imagem from produto where id = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        produto = None
        if row:
            id, nome, descricao, imagem = None
            produto = Produto(id, nome, descricao, imagem)
        cursor.close()
        conn.close()
        return produto
    
    def delete(self, id):
        sql = """delete from produto where id = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
    
    def update(self, produto:Produto):
        sql = """update produto set nome = %s, descricao = %s, imagem = %s where id = %s"""

        values = (produto._nome, produto._descricao, produto._imagem, produto._id)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0