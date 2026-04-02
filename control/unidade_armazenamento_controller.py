from model.unidade_armazenamento import UnidadeArmazenamento


class UnidadeArmazenamento_Controller:
    def __init__(self, dao, armazem_dao, view):
        self.dao = dao
        self.armazem_dao = armazem_dao
        self.view = view
        self.view.controller = self

    def add_unidade_armazenamento(self):
        try:
            dados = self.view.get_unidade_armazenamento_data()

            # Validações de campos obrigatórios
            if not dados:
                self.view.show_error("Erro ao obter dados do formulário!")
                return

            if not dados.get("unidade") or not str(dados["unidade"]).strip():
                self.view.show_error("Nome da unidade é obrigatório!")
                return

            if not dados.get("armazem") or not str(dados["armazem"]).strip():
                self.view.show_error("Armazém é obrigatório!")
                return

            unidade_nova = UnidadeArmazenamento(
                id=f"{dados['armazem'].zfill(3)}-{dados['unidade']}",
                unidade=dados["unidade"],
                armazem=dados["armazem"],
            )
            unidade_salva = self.dao.save(unidade_nova)
            self.view.show_message(
                f"Unidade de armazenamento '{unidade_salva._unidade}' adicionada com id {unidade_salva._id}!"
            )
        except Exception as e:
            self.view.show_error(
                f"Erro ao adicionar unidade de armazenamento: {str(e)}"
            )

    def delete_unidade_armazenamento(self):
        try:
            id_unidade = self.view.get_id()
            if self.dao.delete(id_unidade):
                self.view.show_message(
                    f"Unidade de armazenamento com id {id_unidade} deletada com sucesso!"
                )
            else:
                self.view.show_message(
                    f"Unidade de armazenamento com id {id_unidade} não encontrada!"
                )
        except Exception as e:
            self.view.show_error(f"Erro ao deletar unidade de armazenamento: {str(e)}")

    def list_unidades_armazenamento(self):
        try:
            unidades = self.dao.get_all()
            armazens = self.armazem_dao.get_all()
            self.view.show_unidades_armazenamento(unidades)
            self.view.set_armazens_disponiveis(armazens)
        except Exception as e:
            self.view.show_error(f"Erro ao listar unidades de armazenamento: {str(e)}")

    def get_unidade_armazenamento(self):
        try:
            id_unidade = self.view.get_id()
            unidade = self.dao.get_by_id(id_unidade)
            if not unidade:
                self.view.show_error(
                    f"Unidade de armazenamento com id {id_unidade} não encontrada!"
                )
                return
            self.view.show_unidade_armazenamento_details(unidade)
        except Exception as e:
            self.view.show_error(f"Erro ao obter unidade de armazenamento: {str(e)}")
