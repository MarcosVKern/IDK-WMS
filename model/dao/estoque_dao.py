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

    def get_by_unidade(self, id_unidade):
        sql = """select e.produto, p.nome, e.quantidade from estoque e
                inner join produto p on e.produto = p.ID_produto
                where e.UNarmazenamento = %s and e.quantidade > 0"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id_unidade,))
        produtos = []
        for (produto, nome, quantidade) in cursor:
            produtos.append({'id': produto, 'nome': nome, 'quantidade': quantidade})
        cursor.close()
        conn.close()
        return produtos

    def upsert(self, id_produto, id_unidade, quantidade):
        existe = self.get_by_id(id_produto, id_unidade)
        if existe:
            existe._quantidade = quantidade
            return self.update(existe)
        else:
            novo = Estoque(id_produto, id_unidade, quantidade)
            return self.save(novo)

    def get_estoque(self):
        sql = """select
            e.quantidade,
            p.nome,
            e.UNarmazenamento,
            a.nome
        from 
            estoque e
                inner join produto p on e.produto = p.ID_produto
                inner join unidade_armazenamento ua on e.UNarmazenamento = ID_unidade
                inner join armazem a on ua.armazem = a.ID_armazem
        where e.quantidade > 0;"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        estoque = []
        for (quantidade, nome, UNarmazenamento, armazem) in cursor:
            estoque.append({
                'quantidade': quantidade,
                'nome': nome,
                'UNarmazenamento': UNarmazenamento,
                'armazem': armazem
            })
        cursor.close()
        conn.close()
        return estoque