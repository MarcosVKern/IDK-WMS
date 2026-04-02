from model.cargo import Cargo


class Cargo_Controller:
    def __init__(self, dao, view):
        self.dao = dao
        self.view = view
        self.view.controller = self

    def add_cargo(self):
        try:
            dados = self.view.get_cargo_data()

            # Validações de campos obrigatórios
            if not dados:
                self.view.show_error("Erro ao obter dados do formulário!")
                return

            if not dados.get("cargo") or not str(dados["cargo"]).strip():
                self.view.show_error("Nome do cargo é obrigatório!")
                return

            cargo_novo = Cargo(id=None, cargo=dados["cargo"])
            cargo_salvo = self.dao.save(cargo_novo)
            self.view.show_message(
                f"Cargo '{cargo_salvo._nome}' adicionado com id {cargo_salvo._id}!"
            )
        except Exception as e:
            self.view.show_error(f"Erro ao adicionar cargo: {str(e)}")

    def update_cargo(self):
        try:
            id_cargo = self.view.get_id()
            cargo_existente = self.dao.get_by_id(id_cargo)
            if not cargo_existente:
                self.view.show_error(f"Cargo com id {id_cargo} não encontrado!")
                return
            dados_cargo = self.view.get_cargo_data(cargo_existente)

            # Validações de campos obrigatórios
            if not dados_cargo:
                self.view.show_error("Erro ao obter dados do formulário!")
                return

            if not dados_cargo.get("cargo") or not str(dados_cargo["cargo"]).strip():
                self.view.show_error("Nome do cargo é obrigatório!")
                return

            cargo_atualizado = Cargo(id=id_cargo, cargo=dados_cargo["cargo"])
            if self.dao.update(cargo_atualizado):
                self.view.show_message(
                    f"Cargo '{cargo_atualizado._nome}' atualizado com sucesso!"
                )
        except Exception as e:
            self.view.show_error(f"Erro ao atualizar cargo: {str(e)}")

    def delete_cargo(self):
        try:
            id_cargo = self.view.get_id()
            if self.dao.delete(id_cargo):
                self.view.show_message(f"Cargo com id {id_cargo} deletado com sucesso!")
            else:
                self.view.show_error(f"Cargo com id {id_cargo} não encontrado!")
        except Exception as e:
            self.view.show_error(f"Erro ao deletar cargo: {str(e)}")

    def list_cargos(self):
        try:
            cargos = self.dao.get_all()
            self.view.show_cargos(cargos)
        except Exception as e:
            self.view.show_error(f"Erro ao listar cargos: {str(e)}")

    def get_cargo(self):
        try:
            id_cargo = self.view.get_id()
            cargo = self.dao.get_by_id(id_cargo)
            if not cargo:
                self.view.show_error(f"Cargo com id {id_cargo} não encontrado!")
                return
            self.view.show_cargo_details(cargo)
        except Exception as e:
            self.view.show_error(f"Erro ao obter cargo: {str(e)}")

    def list_related_cargo(self):
        try:
            cargos = self.dao.get_all()
            if cargos:
                self.view.preencher_combo_cargo(cargos)
        except Exception as e:
            self.view.show_error(f"Erro ao carregar cargos para o combo: {str(e)}")
