from model.armazem import Armazem
import mysql.connector

class Armazem_Controller:
    def __init__(self, dao, view):
        self.dao = dao
        self.view = view
        self.view.controller = self


    def add_armazem(self):
        try:
            dados = self.view.get_armazem_data()
            
            # Validações de campos obrigatórios
            if not dados:
                self.view.show_error("Erro ao obter dados do formulário!")
                return
            
            if not dados.get('nome') or not str(dados['nome']).strip():
                self.view.show_error("Nome do armazém é obrigatório!")
                return
            
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
            
            # Validações de campos obrigatórios
            if not dados_armazem:
                self.view.show_error("Erro ao obter dados do formulário!")
                return
            
            if not dados_armazem.get('nome') or not str(dados_armazem['nome']).strip():
                self.view.show_error("Nome do armazém é obrigatório!")
                return
            
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
        except mysql.connector.IntegrityError:
            self.view.show_error("Não é possível excluir este armazém pois ele possui vínculos com outros dados!")
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