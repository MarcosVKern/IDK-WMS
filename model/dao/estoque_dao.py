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
            p.ID_produto,
            ua.unidade,
            ua.ID_unidade,
            a.nome as nome_armazem,
            a.ID_armazem
        from 
            estoque e
                inner join produto p on e.produto = p.ID_produto
                inner join unidade_armazenamento ua on e.UNarmazenamento = ua.ID_unidade
                inner join armazem a on ua.armazem = a.ID_armazem
        where e.quantidade > 0
        order by p.nome"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        estoque = []
        for row in cursor:
            quantidade, nome_produto, id_produto, unidade, id_unidade, nome_armazem, id_armazem = row
            estoque.append({
                'quantidade': quantidade,
                'nome_produto': nome_produto,
                'id_produto': id_produto,
                'unidade': unidade,
                'id_unidade': id_unidade,
                'nome_armazem': nome_armazem,
                'id_armazem': id_armazem
            })
        cursor.close()
        conn.close()
        return estoque

    def get_produtos(self):
        """Retorna lista de produtos para dropdown"""
        sql = """select ID_produto, nome from produto order by nome"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        produtos = []
        for (id_produto, nome) in cursor:
            produtos.append({'id': id_produto, 'nome': nome})
        cursor.close()
        conn.close()
        return produtos

    def get_armazens(self):
        """Retorna lista de armazéns para dropdown"""
        sql = """select ID_armazem, nome from armazem order by nome"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql)
        armazens = []
        for (id_armazem, nome) in cursor:
            armazens.append({'id': id_armazem, 'nome': nome})
        cursor.close()
        conn.close()
        return armazens

    def get_unidades_by_armazem(self, id_armazem):
        """Retorna unidades de um armazém específico"""
        sql = """select ID_unidade, unidade from unidade_armazenamento where armazem = %s order by unidade"""

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, (id_armazem,))
        unidades = []
        for (id_unidade, unidade) in cursor:
            unidades.append({'id': id_unidade, 'unidade': unidade})
        cursor.close()
        conn.close()
        return unidades

    def get_estoque_filtrado(self, id_produto=None, id_armazem=None, id_unidade=None):
        """Retorna estoque com filtros opcionais"""
        sql = """select
            e.quantidade,
            p.nome as nome_produto,
            p.ID_produto,
            ua.unidade,
            ua.ID_unidade,
            a.nome as nome_armazem,
            a.ID_armazem
        from 
            estoque e
                inner join produto p on e.produto = p.ID_produto
                inner join unidade_armazenamento ua on e.UNarmazenamento = ua.ID_unidade
                inner join armazem a on ua.armazem = a.ID_armazem
        where e.quantidade > 0"""

        params = []
        
        if id_produto:
            sql += " and p.ID_produto = %s"
            params.append(id_produto)
        
        if id_armazem:
            sql += " and a.ID_armazem = %s"
            params.append(id_armazem)
        
        if id_unidade:
            sql += " and ua.ID_unidade = %s"
            params.append(id_unidade)
        
        sql += " order by p.nome"

        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(sql, params if params else None)
        estoque = []
        for row in cursor:
            quantidade, nome_produto, id_produto, unidade, id_unidade, nome_armazem, id_armazem = row
            estoque.append({
                'quantidade': quantidade,
                'nome_produto': nome_produto,
                'id_produto': id_produto,
                'unidade': unidade,
                'id_unidade': id_unidade,
                'nome_armazem': nome_armazem,
                'id_armazem': id_armazem
            })
        cursor.close()
        conn.close()
        return estoque