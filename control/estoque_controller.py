class Estoque_Controller:
    def __init__(self, dao, view):
        self.dao = dao
        self.view = view
        self.view.controller = self

    def listar_estoque(self):
        """Lista todo o estoque"""
        try:
            estoque = self.dao.get_estoque()
            self.view.popular_tabela(estoque)
        except Exception as e:
            self.view.show_error(f"Erro ao listar estoque: {str(e)}")

    def carregar_filtros(self):
        """Carrega os dados para os dropdowns de filtro"""
        try:
            produtos = self.dao.get_produtos()
            armazens = self.dao.get_armazens()
            self.view.set_produtos(produtos)
            self.view.set_armazens(armazens)
        except Exception as e:
            self.view.show_error(f"Erro ao carregar filtros: {str(e)}")

    def on_armazem_selecionado(self, id_armazem):
        """Atualiza as unidades quando um armazém é selecionado"""
        try:
            if id_armazem:
                unidades = self.dao.get_unidades_by_armazem(id_armazem)
                self.view.set_unidades(unidades)
            else:
                self.view.set_unidades([])
        except Exception as e:
            self.view.show_error(f"Erro ao carregar unidades: {str(e)}")

    def aplicar_filtros(self):
        """Aplica os filtros e busca o estoque"""
        try:
            filtros = self.view.get_filtros()
            estoque = self.dao.get_estoque_filtrado(
                filtros["id_produto"], filtros["id_armazem"], filtros["id_unidade"]
            )
            self.view.popular_tabela(estoque)
            if estoque:
                self.view.show_message(f"Encontrados {len(estoque)} itens")
            else:
                self.view.show_message(
                    "Nenhum item encontrado com os filtros selecionados"
                )
        except Exception as e:
            self.view.show_error(f"Erro ao aplicar filtros: {str(e)}")

    def limpar_filtros(self):
        """Limpa os filtros e recarrega o estoque"""
        try:
            self.view.limpar_campos_filtro()
            self.listar_estoque()
            self.view.show_message("Filtros limpos")
        except Exception as e:
            self.view.show_error(f"Erro ao limpar filtros: {str(e)}")
