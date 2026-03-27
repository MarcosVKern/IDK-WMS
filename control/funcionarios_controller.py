from model.funcionario import Funcionario

class Funcionario_Controller:
    def __init__(self, dao, view):
        self.dao = dao
        self.view = view
        self.view.controller = self


    def add_funcionario(self):
        try:
            dados = self.view.get_funcionario_data()
            funcionario_novo = Funcionario(
                id=None,
                cep=dados['cep'],
                bairro=dados['bairro'],
                cidade=dados['cidade'],
                uf=dados['uf'],
                pais=dados['pais'],
                nome=dados['nome'],
                cargo=dados['cargo'],
                email=dados['email'],
                senha=dados['senha'],
                situacao=dados['situacao']
            )
            funcionario_salvo = self.dao.save(funcionario_novo)
            self.view.show_message(f"Funcionário '{funcionario_salvo._nome}' adicionado com id {funcionario_salvo._id}!")
        except Exception as e:
            self.view.show_error(f"Erro ao adicionar funcionário: {str(e)}")

    def update_funcionario(self):
        try:
            id_funcionario = self.view.get_id()
            funcionario_existente = self.dao.get_by_id(id_funcionario)
            if not funcionario_existente:
                self.view.show_error(f"Funcionário com id {id_funcionario} não encontrado!")
                return
            dados_funcionario = self.view.get_funcionario_data(funcionario_existente)
            funcionario_atualizado = Funcionario(
                id=id_funcionario,
                cep=dados_funcionario['cep'],
                bairro=dados_funcionario['bairro'],
                cidade=dados_funcionario['cidade'],
                uf=dados_funcionario['uf'],
                pais=dados_funcionario['pais'],
                nome=dados_funcionario['nome'],
                cargo=dados_funcionario['cargo'],
                email=dados_funcionario['email'],
                senha=dados_funcionario['senha'],
                situacao=dados_funcionario['situacao']
            )
            if self.dao.update(funcionario_atualizado):
                self.view.show_message(f"Funcionário '{funcionario_atualizado._nome}' atualizado com sucesso!")
        except Exception as e:
            self.view.show_error(f"Erro ao atualizar funcionário: {str(e)}")

    def delete_funcionario(self):
        try:
            id_funcionario = self.view.get_id()
            if self.dao.delete(id_funcionario):
                self.view.show_message(f"Funcionário com id {id_funcionario} deletado com sucesso!")
            else:
                self.view.show_message(f"Funcionário com id {id_funcionario} não encontrado!")
        except Exception as e:
            self.view.show_error(f"Erro ao deletar funcionário: {str(e)}")

    def list_funcionarios(self):
        try:
            funcionarios = self.dao.get_all()
            self.view.show_funcionarios(funcionarios)
        except Exception as e:
            self.view.show_error(f"Erro ao listar funcionários: {str(e)}")

    def get_funcionario(self):
        try:
            id_funcionario = self.view.get_id()
            funcionario = self.dao.get_by_id(id_funcionario)
            if not funcionario:
                self.view.show_message(f"Funcionário com id {id_funcionario} não encontrado!")
                return
            self.view.show_funcionario_details(funcionario)
        except Exception as e:
            self.view.show_error(f"Erro ao obter funcionário: {str(e)}")