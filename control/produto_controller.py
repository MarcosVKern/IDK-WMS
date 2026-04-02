from model.produto import Produto


class Produto_Controller:
    def __init__(self, dao, view):
        self.dao = dao
        self.view = view
        self.view.controller = self

    def add_produto(self):
        try:
            dados = self.view.get_produto_data()

            # Validações de campos obrigatórios
            if not dados or not dados.get("nome") or not str(dados["nome"]).strip():
                self.view.show_error("Nome do produto é obrigatório!")
                return

            produto_novo = Produto(
                id=None,
                nome=dados["nome"],
                descricao=dados["descricao"],
                imagem=dados["imagem"],
            )
            produto_salvo = self.dao.save(produto_novo)
            self.view.show_message(
                f"Produto '{produto_salvo._nome}' adicionado com id {produto_salvo._id}!"
            )
        except Exception as e:
            self.view.show_error(f"Erro ao adicionar produto: {str(e)}")

    def update_produto(self):
        try:
            id_produto = self.view.get_id()
            produto_existente = self.dao.get_by_id(id_produto)
            if not produto_existente:
                self.view.show_error(f"Produto com id {id_produto} não encontrado!")
                return
            dados_produto = self.view.get_produto_data(produto_existente)

            # Validações de campos obrigatórios
            if (
                not dados_produto
                or not dados_produto.get("nome")
                or not str(dados_produto["nome"]).strip()
            ):
                self.view.show_error("Nome do produto é obrigatório!")
                return

            produto_atualizado = Produto(
                id=id_produto,
                nome=dados_produto["nome"],
                descricao=dados_produto["descricao"],
                imagem=dados_produto["imagem"],
            )
            if self.dao.update(produto_atualizado):
                self.view.show_message(
                    f"Produto '{produto_atualizado._nome}' atualizado com sucesso!"
                )
        except Exception as e:
            self.view.show_error(f"Erro ao atualizar produto: {str(e)}")

    def delete_produto(self):
        try:
            id_produto = self.view.get_id()
            if self.dao.delete(id_produto):
                self.view.show_message(
                    f"Produto com id {id_produto} deletado com sucesso!"
                )
            else:
                self.view.show_message(f"Produto com id {id_produto} não encontrado!")
        except Exception as e:
            self.view.show_error(f"Erro ao deletar produto: {str(e)}")

    def list_produtos(self):
        try:
            produtos = self.dao.get_all()
            self.view.show_produtos(produtos)
        except Exception as e:
            self.view.show_error(f"Erro ao listar produtos: {str(e)}")

    def get_produto(self):
        try:
            id_produto = self.view.get_id()
            produto = self.dao.get_by_id(id_produto)
            if not produto:
                self.view.show_error(f"Produto com id {id_produto} não encontrado!")
                return
            self.view.show_produto_details(produto)
        except Exception as e:
            self.view.show_error(f"Erro ao buscar produto: {str(e)}")
