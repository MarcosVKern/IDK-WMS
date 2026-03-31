from model.dao.produto_dao import Produto_DAO
from model.dao.armazem_dao import Armazem_DAO
from model.dao.funcionario_dao import Funcionario_DAO
from model.dao.cargo_dao import Cargo_DAO
from model.dao.unidade_armazenamento_dao import UnidadeArmazenamento_DAO
from model.dao.estoque_dao import Estoque_DAO
from model.dao.tipo_movimento_dao import TipoMovimento_DAO
from model.dao.movimento_estoque_dao import MovimentoEstoque_DAO
from model.dao.produto_movimento_dao import ProdutoMovimento_DAO
from view.cargos_view import Cargo_View
from view.produto_view import Produto_View
from view.armazem_view import Armazem_View
from view.funcionarios_view import Funcionario_View
from view.unidade_armazenamento_view import UnidadeArmazenamento_View
from view.movimento_estoque_view import MovimentoEstoque_View
from view.estoque_view import Estoque_View
from view.cargos_view import Cargo_View
from control.produto_controller import Produto_Controller
from control.armazem_controller import Armazem_Controller
from control.funcionarios_controller import Funcionario_Controller
from control.unidade_armazenamento_controller import UnidadeArmazenamento_Controller
from control.movimento_estoque_controller import MovimentoEstoque_Controller
from control.cargos_controller import Cargo_Controller
from control.estoque_controller import Estoque_Controller

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

    def exibir_funcionario(self, parent_frame=None, funcionario_logado=None):
        dao = Funcionario_DAO(self.db_config)
        cargo_dao = Cargo_DAO(self.db_config)
        view = Funcionario_View(parent=parent_frame, funcionario_logado=funcionario_logado)
        control = Funcionario_Controller(dao, cargo_dao, view, funcionario_logado)
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

    def exibir_unidade_armazenamento(self, parent_frame=None):
        dao = UnidadeArmazenamento_DAO(self.db_config)
        armazem_dao = Armazem_DAO(self.db_config)
        view = UnidadeArmazenamento_View(parent=parent_frame)
        control = UnidadeArmazenamento_Controller(dao, armazem_dao, view)
        if parent_frame:
            view.display()
        else:
            view.run()

    def exibir_movimento_estoque(self, parent_frame=None, funcionario_logado=None):
        movimento_dao = MovimentoEstoque_DAO(self.db_config)
        tipo_movimento_dao = TipoMovimento_DAO(self.db_config)
        unidade_dao = UnidadeArmazenamento_DAO(self.db_config)
        funcionario_dao = Funcionario_DAO(self.db_config)
        produto_dao = Produto_DAO(self.db_config)
        estoque_dao = Estoque_DAO(self.db_config)
        view = MovimentoEstoque_View(parent=parent_frame, funcionario_logado=funcionario_logado)
        produto_movimento_dao = ProdutoMovimento_DAO(self.db_config)
        control = MovimentoEstoque_Controller(
            movimento_dao,
            tipo_movimento_dao,
            unidade_dao,
            funcionario_dao,
            view,
            produto_dao=produto_dao,
            estoque_dao=estoque_dao,
            produto_movimento_dao=produto_movimento_dao,
            funcionario_logado=funcionario_logado
        )
        if parent_frame:
            view.display()
        else:
            view.run()

    def exibir_estoque(self, parent_frame=None):
        dao = Estoque_DAO(self.db_config)
        view = Estoque_View(parent=parent_frame)
        control = Estoque_Controller(dao, view)
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