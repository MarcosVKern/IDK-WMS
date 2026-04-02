from model.armazem import Armazem
from model.dao.base_dao import Base_DAO


class Armazem_DAO(Base_DAO):
    def save(self, armazem: Armazem):
        sql = """insert into armazem (cep, bairro, cidade, uf, pais, nome) values (%s, %s, %s, %s, %s, %s)"""

        values = (
            armazem._cep,
            armazem._bairro,
            armazem._cidade,
            armazem._uf,
            armazem._pais,
            armazem._nome,
        )

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        armazem._id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return armazem

    def get_all(self):
        sql = """select ID_armazem, cep, bairro, cidade, uf, pais, nome from armazem"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        armazens = []
        for id, cep, bairro, cidade, uf, pais, nome in cursor:
            armazens.append(Armazem(id, cep, bairro, cidade, uf, pais, nome))
        cursor.close()
        conn.close()
        return armazens

    def get_by_id(self, id):
        sql = """select cep, bairro, cidade, uf, pais, nome from armazem where ID_armazem = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        armazem = None
        if row:
            cep, bairro, cidade, uf, pais, nome = row
            armazem = Armazem(id, cep, bairro, cidade, uf, pais, nome)
        cursor.close()
        conn.close()
        return armazem

    def delete(self, id):
        sql = """delete from armazem where ID_armazem = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0

    def update(self, armazem: Armazem):
        sql = """update armazem set cep = %s, bairro = %s, cidade = %s, uf = %s, pais = %s, nome = %s where ID_armazem = %s"""

        values = (
            armazem._cep,
            armazem._bairro,
            armazem._cidade,
            armazem._uf,
            armazem._pais,
            armazem._nome,
            armazem._id,
        )

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
