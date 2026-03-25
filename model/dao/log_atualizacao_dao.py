from model.log_atualizacao import LogAtualizacao
from model.dao.base_dao import Base_DAO

class LogAtualizacao_DAO(Base_DAO):
    def get_all(self):
        sql = """select data from log"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        logs = []
        for (data,) in cursor:
            logs.append(LogAtualizacao(data))
        cursor.close()
        conn.close()
        return logs
    
    def save(self):
        pass

    def get_by_id(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass