from model.tipo_movimento import TipoMovimento
from model.dao.base_dao import Base_DAO


class TipoMovimento_DAO(Base_DAO):
    def save(self, tipo_movimento: TipoMovimento):
        sql = "insert into tipo_movimento (tipoMovimento) values (%s)"

        values = tipo_movimento._tipo

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        tipo_movimento._id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return tipo_movimento

    def get_all(self):
        sql = "select ID_tipo, tipoMovimento from tipo_movimento"

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        tipos_movimento = []
        for id, tipo in cursor:
            tipos_movimento.append(TipoMovimento(id, tipo))
        cursor.close()
        conn.close()
        return tipos_movimento

    def get_by_id(self, id):
        sql = "select ID_tipo, tipoMovimento from tipo_movimento where ID_tipo = %s"

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        tipo_movimento = None
        if row:
            tipo_id, tipo = row
            tipo_movimento = TipoMovimento(tipo_id, tipo)
        cursor.close()
        conn.close()
        return tipo_movimento

    def delete(self, id):
        sql = "delete from tipo_movimento where ID_tipo = %s"

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0

    def update(self, tipo_movimento: TipoMovimento):
        sql = "update tipo_movimento set tipoMovimento = %s where ID_tipo = %s"

        values = (tipo_movimento._tipo, tipo_movimento._id)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
