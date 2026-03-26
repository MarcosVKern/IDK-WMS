from model.cargo import Cargo
from model.dao.base_dao import Base_DAO

class Cargo_DAO(Base_DAO):
    def get_all(self):
        sql = """select ID_cargo, cargo from cargo"""
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        cargos = []
        for (id, cargo) in cursor:
            cargos.append(Cargo(id, cargo))
        cursor.close()
        conn.close()
        return cargos
    
    def get_by_id(self):
        pass

    def save(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass