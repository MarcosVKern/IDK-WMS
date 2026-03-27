from model.armazem import Armazem

class Armazem_Controller:
    def __init__(self, dao, view):
        self.dao = dao
        self.view = view
        self.view.controller = self


    def add_armazem(self):
        try:
            dados = self.view.get_armazem_data()
            armazem_novo = Armazem(
                id=None,
                cep=dados['cep'],
                bairro=dados['bairro'],
                cidade=dados['cidade'],
                uf=dados['uf'],
                pais=dados['pais'],
                nome=dados['nome']
            )
            armazem_salvo = self.dao.save(armazem_novo)
            self.view.show_message(f"Armazém '{armazem_salvo._nome}' adicionado com id {armazem_salvo._id}!")
        except Exception as e:
            self.view.show_error(f"Erro ao adicionar armazém: {str(e)}")

    def update_armazem(self):
        try:
            id_armazem = self.view.get_id()
            armazem_existente = self.dao.get_by_id(id_armazem)
            if not armazem_existente:
                self.view.show_error(f"Armazém com id {id_armazem} não encontrado!")
                return
            dados_armazem = self.view.get_armazem_data(armazem_existente)
            armazem_atualizado = Armazem(
                id=id_armazem,
                cep=dados_armazem['cep'],
                bairro=dados_armazem['bairro'],
                cidade=dados_armazem['cidade'],
                uf=dados_armazem['uf'],
                pais=dados_armazem['pais'],
                nome=dados_armazem['nome']
            )
            if self.dao.update(armazem_atualizado):
                self.view.show_message(f"Armazém '{armazem_atualizado._nome}' atualizado com sucesso!")
        except Exception as e:
            self.view.show_error(f"Erro ao atualizar armazém: {str(e)}")

    def delete_armazem(self):
        try:
            id_armazem = self.view.get_id()
            if self.dao.delete(id_armazem):
                self.view.show_message(f"Armazém com id {id_armazem} deletado com sucesso!")
            else:
                self.view.show_message(f"Armazém com id {id_armazem} não encontrado!")
        except Exception as e:
            self.view.show_error(f"Erro ao deletar armazém: {str(e)}")

    def list_armazens(self):
        try:
            armazens = self.dao.get_all()
            self.view.show_armazens(armazens)
        except Exception as e:
            self.view.show_error(f"Erro ao listar armazéns: {str(e)}")

    def get_armazem(self):
        try:
            id_armazem = self.view.get_id()
            armazem = self.dao.get_by_id(id_armazem)
            if not armazem:
                self.view.show_error(f"Armazém com id {id_armazem} não encontrado!")
                return
            self.view.show_armazem_details(armazem)
        except Exception as e:
            self.view.show_error(f"Erro ao obter armazém: {str(e)}")