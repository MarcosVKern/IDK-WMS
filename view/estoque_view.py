import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from view.cores_padrao import Cores_Padrao
from view.notificacao import Notificacao


class Estoque_View:
    def __init__(self, parent=None):
        self.controller = None
        self.parent = parent
        
        if parent is None:
            self.root = tk.Toplevel()
            self.root.title("Consultar Estoque")
            self.root.geometry("1280x720")
            self.root.state('zoomed')
            self.is_embedded = False
        else:
            self.root = tk.Frame(parent, bg=Cores_Padrao.COR_FUNDO)
            self.is_embedded = True

        # Variáveis para os filtros
        self.var_produto = tk.StringVar()
        self.var_armazem = tk.StringVar()
        self.var_unidade = tk.StringVar()

        # Dicts para manter os IDs dos filtros
        self.produtos_dict = {}
        self.armazens_dict = {}
        self.unidades_dict = {}

        self._setup_ui()

    def _setup_ui(self):
        """Configura a interface"""
        # Título
        titulo = tk.Label(
            self.root,
            text="CONSULTAR ESTOQUE",
            font=("Arial", 16, "bold"),
            pady=10,
            bg=Cores_Padrao.COR_FUNDO if self.is_embedded else None
        )
        titulo.pack()

        # Frame de filtros
        frame_filtros = tk.LabelFrame(
            self.root,
            text="Filtros",
            padx=10,
            pady=10,
            bg=Cores_Padrao.COR_FUNDO if self.is_embedded else None
        )
        frame_filtros.pack(padx=20, pady=5, fill='x')

        # Linha 1 - Filtros
        # Produto
        tk.Label(frame_filtros, text="Produto:", bg=Cores_Padrao.COR_FUNDO if self.is_embedded else None).grid(
            row=0, column=0, sticky="w", padx=5, pady=5
        )
        self.combo_produto = ttk.Combobox(frame_filtros, textvariable=self.var_produto, state="readonly", width=25)
        self.combo_produto.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Armazém
        tk.Label(frame_filtros, text="Armazém:", bg=Cores_Padrao.COR_FUNDO if self.is_embedded else None).grid(
            row=0, column=2, sticky="w", padx=5, pady=5
        )
        self.combo_armazem = ttk.Combobox(frame_filtros, textvariable=self.var_armazem, state="readonly", width=25)
        self.combo_armazem.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.combo_armazem.bind("<<ComboboxSelected>>", self._on_armazem_mudou)

        # Unidade de Armazenamento
        tk.Label(frame_filtros, text="Unidade:", bg=Cores_Padrao.COR_FUNDO if self.is_embedded else None).grid(
            row=0, column=4, sticky="w", padx=5, pady=5
        )
        self.combo_unidade = ttk.Combobox(frame_filtros, textvariable=self.var_unidade, state="readonly", width=25)
        self.combo_unidade.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

        # Configurar peso das colunas
        for i in range(6):
            frame_filtros.grid_columnconfigure(i, weight=1)

        # Frame de botões
        frame_botoes = tk.Frame(self.root, pady=10, bg=Cores_Padrao.COR_FUNDO if self.is_embedded else None)
        frame_botoes.pack()

        ctk.CTkButton(
            frame_botoes,
            text="Aplicar Filtros",
            command=self._acao_aplicar_filtros,
            fg_color=Cores_Padrao.COR_BOTAO_SALVAR,
            text_color=Cores_Padrao.COR_TEXTO,
            width=150
        ).pack(side=tk.LEFT, padx=5)

        ctk.CTkButton(
            frame_botoes,
            text="Limpar Filtros",
            command=self._acao_limpar_filtros,
            fg_color=Cores_Padrao.COR_BOTAO_LIMPAR,
            text_color=Cores_Padrao.COR_TEXTO,
            width=150
        ).pack(side=tk.LEFT, padx=5)

        # Frame da tabela
        frame_tabela = tk.Frame(self.root, padx=20, pady=10, bg=Cores_Padrao.COR_FUNDO if self.is_embedded else None)
        frame_tabela.pack(expand=True, fill="both")

        # Colunas da tabela
        self.colunas = ("produto", "quantidade", "unidade", "armazem")
        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings", height=20)

        self.tree.heading("produto", text="Produto")
        self.tree.heading("quantidade", text="Quantidade")
        self.tree.heading("unidade", text="Unidade de Armazenamento")
        self.tree.heading("armazem", text="Armazém")

        self.tree.column("produto", anchor="w", width=400)
        self.tree.column("quantidade", anchor="center", width=150)
        self.tree.column("unidade", anchor="w", width=300)
        self.tree.column("armazem", anchor="w", width=250)

        # Configurar efeito zebrado
        self.tree.tag_configure('evenrow', background=Cores_Padrao.COR_ZEBRADO_PAR)
        self.tree.tag_configure('oddrow', background=Cores_Padrao.COR_ZEBRADO_IMPAR)

        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)

        self.tree.pack(side="left", expand=True, fill="both")
        scrollbar.pack(side="right", fill="y")

    def display(self):
        """Exibir quando embutido em um frame"""
        self.root.pack(fill="both", expand=True)
        if self.controller:
            self.controller.carregar_filtros()
            self.controller.listar_estoque()
        self.root.after(200, lambda: None)

    def run(self):
        """Executar como janela separada"""
        if self.controller:
            self.controller.carregar_filtros()
            self.controller.listar_estoque()
        self.root.grab_set()
        self.root.mainloop()

    def set_produtos(self, produtos):
        """Popula o dropdown de produtos"""
        self.produtos_dict = {'': None}  # Opção em branco
        valores = ['']
        for produto in produtos:
            self.produtos_dict[produto['nome']] = produto['id']
            valores.append(produto['nome'])
        self.combo_produto['values'] = valores
        self.combo_produto.current(0)

    def set_armazens(self, armazens):
        """Popula o dropdown de armazéns"""
        self.armazens_dict = {'': None}  # Opção em branco
        valores = ['']
        for armazem in armazens:
            self.armazens_dict[armazem['nome']] = armazem['id']
            valores.append(armazem['nome'])
        self.combo_armazem['values'] = valores
        self.combo_armazem.current(0)
        # Limpar unidades
        self.combo_unidade['values'] = ['']
        self.combo_unidade.current(0)

    def set_unidades(self, unidades):
        """Popula o dropdown de unidades"""
        self.unidades_dict = {'': None}  # Opção em branco
        valores = ['']
        for unidade in unidades:
            self.unidades_dict[unidade['unidade']] = unidade['id']
            valores.append(unidade['unidade'])
        self.combo_unidade['values'] = valores
        self.combo_unidade.current(0)

    def _on_armazem_mudou(self, event=None):
        """Atualiza unidades quando armazém é selecionado"""
        armazem_selecionado = self.var_armazem.get()
        id_armazem = self.armazens_dict.get(armazem_selecionado)
        
        if self.controller:
            self.controller.on_armazem_selecionado(id_armazem)

    def get_filtros(self):
        """Retorna os valores dos filtros"""
        produto_selecionado = self.var_produto.get()
        armazem_selecionado = self.var_armazem.get()
        unidade_selecionada = self.var_unidade.get()

        return {
            'id_produto': self.produtos_dict.get(produto_selecionado),
            'id_armazem': self.armazens_dict.get(armazem_selecionado),
            'id_unidade': self.unidades_dict.get(unidade_selecionada)
        }

    def popular_tabela(self, estoque):
        """Popula a tabela com dados de estoque"""
        # Limpar dados existentes
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Adicionar dados com alternância de cores
        for i, item_estoque in enumerate(estoque):
            valores = (
                item_estoque['nome_produto'],
                item_estoque['quantidade'],
                item_estoque['unidade'],
                item_estoque['nome_armazem']
            )
            tag = 'evenrow' if i % 2 == 0 else 'oddrow'
            self.tree.insert('', 'end', values=valores, tags=(tag,))

    def limpar_campos_filtro(self):
        """Limpa todos os campos de filtro"""
        self.combo_produto.current(0)
        self.combo_armazem.current(0)
        self.combo_unidade.current(0)

    def _acao_aplicar_filtros(self):
        """Ação ao clicar no botão Aplicar Filtros"""
        if self.controller:
            self.controller.aplicar_filtros()

    def _acao_limpar_filtros(self):
        """Ação ao clicar no botão Limpar Filtros"""
        if self.controller:
            self.controller.limpar_filtros()

    def show_message(self, mensagem):
        """Exibe mensagem de sucesso"""
        Notificacao.sucesso("Sucesso", mensagem, parent=self.root)

    def show_error(self, mensagem):
        """Exibe mensagem de erro"""
        Notificacao.erro("Erro", mensagem, parent=self.root)
