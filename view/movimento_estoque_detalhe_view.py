import tkinter as tk
from tkinter import ttk
from view.cores_padrao import Cores_Padrao


class MovimentoEstoque_Detalhe_View:
    def __init__(self, movimento, tipo_movimento=None, unidade_origem=None, unidade_destino=None, funcionario=None, produtos_movimento=None, parent=None):
        self.movimento = movimento
        self.tipo_movimento = tipo_movimento
        self.unidade_origem = unidade_origem
        self.unidade_destino = unidade_destino
        self.funcionario = funcionario
        self.produtos_movimento = produtos_movimento or []
        self.parent = parent
        
        if parent is None:
            self.root = tk.Toplevel()
            self.root.title(f"Detalhes do Movimento #{movimento._id_movimento}")
            self.root.geometry("700x700")
            self.root.grab_set()
        else:
            self.root = tk.Frame(parent, bg=Cores_Padrao.COR_FUNDO)
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Cria a interface do detalhamento"""
        # Título
        tk.Label(
            self.root,
            text=f"Detalhes do Movimento #{self.movimento._id_movimento}",
            font=("Arial", 14, "bold"),
            pady=10,
            bg=Cores_Padrao.COR_FUNDO
        ).pack(fill="x")
        
        # Frame principal com scroll
        frame_principal = tk.LabelFrame(
            self.root,
            text="Informações do Movimento",
            padx=15,
            pady=15,
            bg=Cores_Padrao.COR_FUNDO
        )
        frame_principal.pack(padx=15, pady=10, fill="both", expand=True)
        
        tk.Label(frame_principal, text="ID Movimento:", font=("Arial", 10, "bold"), bg=Cores_Padrao.COR_FUNDO).grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(frame_principal, text=str(self.movimento._id_movimento), font=("Arial", 10), bg=Cores_Padrao.COR_FUNDO).grid(row=0, column=1, sticky="w", pady=5, padx=10)

        tipo_texto = f"{self.tipo_movimento._tipo}" if self.tipo_movimento else "N/A"
        tk.Label(frame_principal, text="Tipo de Movimento:", font=("Arial", 10, "bold"), bg=Cores_Padrao.COR_FUNDO).grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(frame_principal, text=tipo_texto, font=("Arial", 10), bg=Cores_Padrao.COR_FUNDO).grid(row=1, column=1, sticky="w", pady=5, padx=10)

        origem_texto = f"{self.unidade_origem._unidade}" if self.unidade_origem else "N/A"
        tk.Label(frame_principal, text="Unidade de Origem:", font=("Arial", 10, "bold"), bg=Cores_Padrao.COR_FUNDO).grid(row=2, column=0, sticky="w", pady=5)
        tk.Label(frame_principal, text=origem_texto, font=("Arial", 10), bg=Cores_Padrao.COR_FUNDO).grid(row=2, column=1, sticky="w", pady=5, padx=10)

        destino_texto = f"{self.unidade_destino._unidade}" if self.unidade_destino else "N/A"
        tk.Label(frame_principal, text="Unidade de Destino:", font=("Arial", 10, "bold"), bg=Cores_Padrao.COR_FUNDO).grid(row=3, column=0, sticky="w", pady=5)
        tk.Label(frame_principal, text=destino_texto, font=("Arial", 10), bg=Cores_Padrao.COR_FUNDO).grid(row=3, column=1, sticky="w", pady=5, padx=10)
 
        func_texto = f"{self.funcionario._nome}" if self.funcionario else str(self.movimento._responsavel)
        tk.Label(frame_principal, text="Responsável:", font=("Arial", 10, "bold"), bg=Cores_Padrao.COR_FUNDO).grid(row=4, column=0, sticky="w", pady=5)
        tk.Label(frame_principal, text=func_texto, font=("Arial", 10), bg=Cores_Padrao.COR_FUNDO).grid(row=4, column=1, sticky="w", pady=5, padx=10)

        tk.Label(frame_principal, text="Status:", font=("Arial", 10, "bold"), bg=Cores_Padrao.COR_FUNDO).grid(row=5, column=0, sticky="w", pady=5)
        tk.Label(frame_principal, text=self.movimento._status, font=("Arial", 10), bg=Cores_Padrao.COR_FUNDO).grid(row=5, column=1, sticky="w", pady=5, padx=10)

        data_saida = self.movimento._dataSaida if self.movimento._dataSaida else "Não definida"
        tk.Label(frame_principal, text="Data de Saída:", font=("Arial", 10, "bold"), bg=Cores_Padrao.COR_FUNDO).grid(row=6, column=0, sticky="w", pady=5)
        tk.Label(frame_principal, text=str(data_saida), font=("Arial", 10), bg=Cores_Padrao.COR_FUNDO).grid(row=6, column=1, sticky="w", pady=5, padx=10)

        data_entrada = self.movimento._dataEntrada if self.movimento._dataEntrada else "Não definida"
        tk.Label(frame_principal, text="Data de Entrada:", font=("Arial", 10, "bold"), bg=Cores_Padrao.COR_FUNDO).grid(row=7, column=0, sticky="w", pady=5)
        tk.Label(frame_principal, text=str(data_entrada), font=("Arial", 10), bg=Cores_Padrao.COR_FUNDO).grid(row=7, column=1, sticky="w", pady=5, padx=10)

        data_alteracao = self.movimento._dataAlteracao if self.movimento._dataAlteracao else "Não definida"
        tk.Label(frame_principal, text="Data de Alteração:", font=("Arial", 10, "bold"), bg=Cores_Padrao.COR_FUNDO).grid(row=8, column=0, sticky="w", pady=5)
        tk.Label(frame_principal, text=str(data_alteracao), font=("Arial", 10), bg=Cores_Padrao.COR_FUNDO).grid(row=8, column=1, sticky="w", pady=5, padx=10)

        frame_produtos = tk.LabelFrame(
            self.root,
            text="Produtos Movimentados",
            padx=15,
            pady=10,
            bg=Cores_Padrao.COR_FUNDO
        )
        frame_produtos.pack(padx=15, pady=10, fill="both", expand=True)

        colunas = ("id", "nome", "quantidade")
        self.tree_produtos = ttk.Treeview(frame_produtos, columns=colunas, show="headings", height=8)
        
        self.tree_produtos.heading("id", text="ID Produto")
        self.tree_produtos.heading("nome", text="Nome do Produto")
        self.tree_produtos.heading("quantidade", text="Quantidade")
        
        self.tree_produtos.column("id", anchor="center", width=80)
        self.tree_produtos.column("nome", anchor="w", width=300)
        self.tree_produtos.column("quantidade", anchor="center", width=120)
        
        self.tree_produtos.pack(side="left", expand=True, fill="both")

        scrollbar = ttk.Scrollbar(frame_produtos, orient="vertical", command=self.tree_produtos.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree_produtos.config(yscroll=scrollbar.set)
        
        # Configurar efeito zebrado
        self.tree_produtos.tag_configure('evenrow', background=Cores_Padrao.COR_ZEBRADO_PAR)
        self.tree_produtos.tag_configure('oddrow', background=Cores_Padrao.COR_ZEBRADO_IMPAR)

        self._popular_produtos()
        
        frame_botoes = tk.Frame(self.root, bg=Cores_Padrao.COR_FUNDO)
        frame_botoes.pack(pady=10, fill="x")
        
        tk.Button(
            frame_botoes,
            text="Fechar",
            command=self._fechar,
            bg=Cores_Padrao.COR_BOTAO_ATUALIZAR,
            width=15
        ).pack(side=tk.LEFT, padx=5)
        
        if isinstance(self.root, tk.Toplevel):
            self.root.protocol("WM_DELETE_WINDOW", self._fechar)
    
    def _popular_produtos(self):
        """Preenche a tabela de produtos movimentados"""
        for i in self.tree_produtos.get_children():
            self.tree_produtos.delete(i)
        
        for idx, produto in enumerate(self.produtos_movimento):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree_produtos.insert("", "end", values=(
                produto.get('produto_id', ''),
                produto.get('nome', ''),
                produto.get('quantidade', '')
            ), tags=(tag,))
    
    def _fechar(self):
        """Fecha a janela de detalhes"""
        if isinstance(self.root, tk.Toplevel):
            self.root.destroy()
    
    def show(self):
        """Exibe a janela de forma modal (bloqueante)"""
        if isinstance(self.root, tk.Toplevel):
            self.root.wait_window(self.root)
    
    def display(self):
        """Exibe quando embutida em um frame"""
        self.root.pack(fill="both", expand=True)
