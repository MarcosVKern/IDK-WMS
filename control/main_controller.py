from model.dao.produto_dao import Produto_DAO
from view.produto_view import Produto_View
from control.produto_controller import Produto_Controller

class Main_Controller:
    def __init__(self, main_view, db_config):
        self.main_view = main_view
        self.db_config = db_config

    def exibir_produto(self):
        dao = Produto_DAO(self.db_config)
        view = Produto_View()
        control = Produto_Controller(dao, view)
        view.run()