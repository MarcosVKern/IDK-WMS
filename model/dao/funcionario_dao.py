from model.funcionario import Funcionario
from model.dao.base_dao import Base_DAO

class Funcionario_DAO(Base_DAO):
    def save(self, funcionario: Funcionario):
        sql = """insert into funcionario (cep, bairro, cidade, uf, pais, 
                nome, cargo, senha, email, situacao) values 
                (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        values = (funcionario._cep, funcionario._bairro, funcionario._cidade, funcionario._uf,
                  funcionario._pais, funcionario._nome, funcionario._cargo,
                  funcionario._senha, funcionario._email, funcionario._situacao)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        funcionario._id = cursor.lastrowid
        conn.commit()
        cursor.close()
        conn.close()
        return funcionario
    
    def get_all(self):
        sql = """select f.ID_funcionario, f.cep, f.bairro, f.cidade, f.uf, f.pais, f.nome, f.cargo, f.email, f.situacao 
                from funcionario f 
                inner join cargo c on f.cargo = c.ID_cargo
                order by f.nome, f.cargo asc"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        funcionarios = []
        for (id, cep, bairro, cidade, uf, pais, nome, cargo, email, situacao) in cursor:
            funcionarios.append(Funcionario(id, cep, bairro, cidade, uf, pais, nome, cargo, email, situacao))
        cursor.close()
        conn.close()
        return funcionarios
    
    def get_by_id(self, id):
        sql = """select cep, bairro, cidade, uf, pais, nome, cargo, email, situacao from funcionario where ID_funcionario = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        row = cursor.fetchone()
        funcionario = None
        if row:
            cep, bairro, cidade, uf, pais, nome, cargo, email, situacao = row
            funcionario = Funcionario(id, cep, bairro, cidade, uf, pais, nome, cargo, email, situacao)
        cursor.close()
        conn.close()
        return funcionario
    
    def delete(self, id):
        sql = """delete from funcionario where ID_funcionario = %s"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id,))
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
    
    def update(self, funcionario: Funcionario):
        sql = """update funcionario set cep = %s, bairro = %s, cidade = %s, uf = %s, 
                pais = %s, nome = %s, cargo = %s, senha = %s, email = %s, situacao = %s where ID_funcionario = %s"""

        values = (funcionario._cep, funcionario._bairro, funcionario._cidade, funcionario._uf,
                  funcionario._pais, funcionario._nome, funcionario._cargo,
                  funcionario._senha, funcionario._email, funcionario._situacao, funcionario._id)

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, values)
        conn.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        conn.close()
        return affected_rows > 0
    
    def login(self, senha, email):
        sql = """select ID_funcionario, cep, bairro, cidade, uf, pais, nome, cargo, email, situacao
                from funcionario
                where senha = %s and email = %s and situacao = 'Ativo'"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (senha, email))
        row = cursor.fetchone()
        if not row:
            cursor.close()
            conn.close()
            raise Exception("Email ou senha inválidos")
        id, cep, bairro, cidade, uf, pais, nome, cargo, email, situacao = row
        funcionario = Funcionario(id, cep, bairro, cidade, uf, pais, nome, cargo, email, situacao)
        cursor.close()
        conn.close()
        return funcionario