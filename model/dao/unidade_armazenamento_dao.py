from model.unidade_armazenamento import UnidadeArmazenamento
from model.dao.base_dao import Base_DAO

class UnidadeArmazenamento_DAO(Base_DAO):
    def save(self, unidade: UnidadeArmazenamento):
        sql = """insert into unidade_armazenamento (unidade, armazem) VALUES (%s, %s)"""

        values = (unidade._unidade, unidade._armazem)
        
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        unidade._id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return unidade
    
    def get_all(self):
        sql = """select u.ID_unidade, u.unidade, u.armazem 
                from unidade_armazenamento u
                inner join armazem a on u.armazem = a.ID_armazem"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        unidades = []
        for (ID_unidade, unidade, armazem) in cursor:
            unidades.append(UnidadeArmazenamento(unidade, armazem, ID_unidade))
        cursor.close()
        conn.close()
        return unidades
    
    def get_by_id(self, id):
        sql = """select unidade, armazem from unidade_armazenamento where ID_unidade = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        unidade = None
        if row:
            unidade, armazem = row
            unidade = UnidadeArmazenamento(unidade, armazem, id)
        cursor.close()
        conn.close()
        return unidade
    
    def delete(self, id):
        sql = """delete from unidade_armazenamento where ID_unidade = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
    
    def update(self, unidade: UnidadeArmazenamento):
        sql = """update unidade_armazenamento set unidade = %s, armazem = %s where ID_unidade = %s"""

        values = (unidade._unidade, unidade._armazem, unidade._id)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0