from model.dao.produto_dao import Produto_DAO
from model.dao.armazem_dao import Armazem_DAO
from model.dao.funcionario_dao import Funcionario_DAO
from model.dao.cargo_dao import Cargo_DAO
from view.cargos_view import Cargo_View
from view.produto_view import Produto_View
from view.armazem_view import Armazem_View
from view.funcionarios_view import Funcionario_View
from view.cargos_view import Cargo_View
from control.produto_controller import Produto_Controller
from control.armazem_controller import Armazem_Controller
from control.funcionarios_controller import Funcionario_Controller
from control.cargos_controller import Cargo_Controller

class Main_Controller:
    def __init__(self, main_view, db_config):
        self.main_view = main_view
        self.db_config = db_config

    def exibir_produto(self, parent_frame=None):
        dao = Produto_DAO(self.db_config)
        view = Produto_View(parent=parent_frame)
        control = Produto_Controller(dao, view)
        if parent_frame:
            view.display()
        else:
            view.run()
    
    def exibir_armazem(self, parent_frame=None):
        dao = Armazem_DAO(self.db_config)
        view = Armazem_View(parent=parent_frame)
        control = Armazem_Controller(dao, view)
        if parent_frame:
            view.display()
        else:
            view.run()

    def exibir_funcionario(self, parent_frame=None):
        dao = Funcionario_DAO(self.db_config)
        view = Funcionario_View(parent=parent_frame)
        control = Funcionario_Controller(dao, view)
        if parent_frame:
            view.display()
        else:
            view.run()

    def exibir_cargo(self, parent_frame=None):
        dao = Cargo_DAO(self.db_config)
        view = Cargo_View(parent=parent_frame)
        control = Cargo_Controller(dao, view)
        control.list_related_cargo()
        if parent_frame:
            view.display()
        else:
            view.run()

    def login(self, email, senha):
        dao = Funcionario_DAO(self.db_config)
        funcionario = dao.login(senha, email)
        if funcionario:
            funcionario_completo = dao.get_by_id(funcionario._id)
            return funcionario_completo
        return None