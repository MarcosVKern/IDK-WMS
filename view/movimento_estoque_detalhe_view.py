import tkinter as tk
from tkinter import ttk, messagebox
import customtkinter as ctk
from view.cores_padrao import Cores_Padrao
from view.notificacao import Notificacao
from datetime import date


class MovimentoEstoque_Detalhe_View:
    def __init__(
        self,
        movimento,
        tipo_movimento=None,
        unidade_origem=None,
        unidade_destino=None,
        funcionario=None,
        produtos_movimento=None,
        controller=None,
        parent=None,
    ):
        self.movimento = movimento
        self.tipo_movimento = tipo_movimento
        self.unidade_origem = unidade_origem
        self.unidade_destino = unidade_destino
        self.funcionario = funcionario
        self.produtos_movimento = produtos_movimento or []
        self.controller = controller
        self.parent = parent

        self.em_confirmacao = False
        self.checkbox_vars = {}
        self.btn_atualizar = None
        self.btn_cancelar = None
        self.frame_checkboxes = None
        self.tree_produtos = None

        if parent is None:
            self.root = tk.Toplevel()
            self.root.title(f"Detalhes do Movimento #{movimento._id_movimento}")
            self.root.geometry("700x800")
            self.root.configure(bg=Cores_Padrao.COR_FUNDO)
            self.root.grab_set()
        else:
            self.root = tk.Frame(parent, bg=Cores_Padrao.COR_FUNDO)

        self._setup_ui()
        self._configurar_estado_botoes()

    def _formatar_data(self, data):
        """Formata data para DD/MM/YYYY"""
        if not data:
            return "Não definida"
        if isinstance(data, date):
            return data.strftime("%d/%m/%Y")
        try:
            # Se for string, tentar parsear
            if isinstance(data, str):
                # Assumir que vem do banco em YYYY-MM-DD
                data_obj = date.fromisoformat(data)
                return data_obj.strftime("%d/%m/%Y")
            return str(data)
        except:
            return str(data)

    def _setup_ui(self):
        """Cria a interface do detalhamento"""
        # Título
        tk.Label(
            self.root,
            text=f"Detalhes do Movimento #{self.movimento._id_movimento}",
            font=("Arial", 14, "bold"),
            pady=10,
            bg=Cores_Padrao.COR_FUNDO,
        ).pack(fill="x")

        frame_principal = tk.LabelFrame(
            self.root,
            text="Informações do Movimento",
            padx=15,
            pady=15,
            bg=Cores_Padrao.COR_FUNDO,
        )
        frame_principal.pack(padx=15, pady=10, fill="both")

        tk.Label(
            frame_principal,
            text="ID Movimento:",
            font=("Arial", 10, "bold"),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=0, column=0, sticky="w", pady=5)
        tk.Label(
            frame_principal,
            text=str(self.movimento._id_movimento),
            font=("Arial", 10),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=0, column=1, sticky="w", pady=5, padx=10)

        tipo_texto = f"{self.tipo_movimento._tipo}" if self.tipo_movimento else "N/A"
        tk.Label(
            frame_principal,
            text="Tipo de Movimento:",
            font=("Arial", 10, "bold"),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=1, column=0, sticky="w", pady=5)
        tk.Label(
            frame_principal,
            text=tipo_texto,
            font=("Arial", 10),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=1, column=1, sticky="w", pady=5, padx=10)

        origem_texto = (
            f"{self.unidade_origem._unidade}" if self.unidade_origem else "N/A"
        )
        tk.Label(
            frame_principal,
            text="Unidade de Origem:",
            font=("Arial", 10, "bold"),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=2, column=0, sticky="w", pady=5)
        tk.Label(
            frame_principal,
            text=origem_texto,
            font=("Arial", 10),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=2, column=1, sticky="w", pady=5, padx=10)

        destino_texto = (
            f"{self.unidade_destino._unidade}" if self.unidade_destino else "N/A"
        )
        tk.Label(
            frame_principal,
            text="Unidade de Destino:",
            font=("Arial", 10, "bold"),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=3, column=0, sticky="w", pady=5)
        tk.Label(
            frame_principal,
            text=destino_texto,
            font=("Arial", 10),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=3, column=1, sticky="w", pady=5, padx=10)

        func_texto = (
            f"{self.funcionario._nome}"
            if self.funcionario
            else str(self.movimento._responsavel)
        )
        tk.Label(
            frame_principal,
            text="Responsável:",
            font=("Arial", 10, "bold"),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=4, column=0, sticky="w", pady=5)
        tk.Label(
            frame_principal,
            text=func_texto,
            font=("Arial", 10),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=4, column=1, sticky="w", pady=5, padx=10)

        tk.Label(
            frame_principal,
            text="Status:",
            font=("Arial", 10, "bold"),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=5, column=0, sticky="w", pady=5)
        tk.Label(
            frame_principal,
            text=self.movimento._status,
            font=("Arial", 10),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=5, column=1, sticky="w", pady=5, padx=10)

        data_saida_formatted = self._formatar_data(self.movimento._dataSaida)
        tk.Label(
            frame_principal,
            text="Data de Saída:",
            font=("Arial", 10, "bold"),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=6, column=0, sticky="w", pady=5)
        tk.Label(
            frame_principal,
            text=data_saida_formatted,
            font=("Arial", 10),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=6, column=1, sticky="w", pady=5, padx=10)

        data_entrada_formatted = self._formatar_data(self.movimento._dataEntrada)
        tk.Label(
            frame_principal,
            text="Data de Entrada:",
            font=("Arial", 10, "bold"),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=7, column=0, sticky="w", pady=5)
        tk.Label(
            frame_principal,
            text=data_entrada_formatted,
            font=("Arial", 10),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=7, column=1, sticky="w", pady=5, padx=10)

        data_alteracao_formatted = self._formatar_data(self.movimento._dataAlteracao)
        tk.Label(
            frame_principal,
            text="Data de Alteração:",
            font=("Arial", 10, "bold"),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=8, column=0, sticky="w", pady=5)
        tk.Label(
            frame_principal,
            text=data_alteracao_formatted,
            font=("Arial", 10),
            bg=Cores_Padrao.COR_FUNDO,
        ).grid(row=8, column=1, sticky="w", pady=5, padx=10)

        frame_produtos = tk.LabelFrame(
            self.root,
            text="Produtos Movimentados",
            padx=15,
            pady=10,
            bg=Cores_Padrao.COR_FUNDO,
        )
        frame_produtos.pack(padx=15, pady=10, fill="both", expand=True)

        colunas = ("id", "nome", "quantidade")
        style = ttk.Style()
        style.configure(
            "Pink.Treeview",
            background=Cores_Padrao.COR_TABLE_BG,
            fieldbackground=Cores_Padrao.COR_TABLE_BG,
            foreground=Cores_Padrao.COR_TEXTO,
        )
        self.tree_produtos = ttk.Treeview(
            frame_produtos,
            columns=colunas,
            show="headings",
            height=8,
            style="Pink.Treeview",
        )

        self.tree_produtos.heading("id", text="ID Produto")
        self.tree_produtos.heading("nome", text="Nome do Produto")
        self.tree_produtos.heading("quantidade", text="Quantidade")

        self.tree_produtos.column("id", anchor="center", width=80)
        self.tree_produtos.column("nome", anchor="w", width=300)
        self.tree_produtos.column("quantidade", anchor="center", width=120)

        self.tree_produtos.pack(side="left", expand=True, fill="both")

        scrollbar = ttk.Scrollbar(
            frame_produtos, orient="vertical", command=self.tree_produtos.yview
        )
        scrollbar.pack(side="right", fill="y")
        self.tree_produtos.config(yscroll=scrollbar.set)

        self.tree_produtos.tag_configure(
            "evenrow", background=Cores_Padrao.COR_ZEBRADO_PAR
        )
        self.tree_produtos.tag_configure(
            "oddrow", background=Cores_Padrao.COR_ZEBRADO_IMPAR
        )

        self._popular_produtos()

        frame_botoes = tk.Frame(self.root, bg=Cores_Padrao.COR_FUNDO)
        frame_botoes.pack(pady=10, fill="x", padx=15)

        ctk.CTkButton(
            frame_botoes,
            text="Fechar",
            command=self._fechar,
            fg_color=Cores_Padrao.COR_BOTAO_ATUALIZAR,
            hover=Cores_Padrao.COR_BOTAO_ATUALIZAR_HOVER,
            text_color=Cores_Padrao.COR_TEXTO_BOTAO,
            width=150,
        ).pack(side=tk.LEFT, padx=5)

        self.btn_atualizar = ctk.CTkButton(
            frame_botoes,
            text="Confirmar",
            command=self._atualizar_movimento,
            fg_color=Cores_Padrao.COR_BOTAO_ATUALIZAR,
            hover=Cores_Padrao.COR_BOTAO_ATUALIZAR_HOVER,
            text_color=Cores_Padrao.COR_TEXTO_BOTAO,
            width=150,
        )
        self.btn_atualizar.pack(side=tk.RIGHT, padx=5)

        self.btn_cancelar = ctk.CTkButton(
            frame_botoes,
            text="Cancelar",
            command=self._cancelar_movimento,
            fg_color=Cores_Padrao.COR_BOTAO_DELETAR,
            text_color=Cores_Padrao.COR_TEXTO_BOTAO,
            width=150,
        )
        self.btn_cancelar.pack(side=tk.RIGHT, padx=5)

        if isinstance(self.root, tk.Toplevel):
            self.root.protocol("WM_DELETE_WINDOW", self._fechar)

    def _popular_produtos(self):
        """Preenche a tabela de produtos movimentados"""
        for i in self.tree_produtos.get_children():
            self.tree_produtos.delete(i)

        for idx, produto in enumerate(self.produtos_movimento):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree_produtos.insert(
                "",
                "end",
                values=(
                    produto.get("produto_id", ""),
                    produto.get("nome", ""),
                    produto.get("quantidade", ""),
                ),
                tags=(tag,),
            )

    def _configurar_estado_botoes(self):
        """Configura o estado dos botões baseado em permissões e status"""
        tipo_nome = (
            self.tipo_movimento._tipo.lower().strip() if self.tipo_movimento else ""
        )
        status_atual = self.movimento._status

        pode_atualizar = self._pode_atualizar()
        self.btn_atualizar.configure(state="normal" if pode_atualizar else "disabled")

        pode_cancelar = self._pode_cancelar()
        self.btn_cancelar.configure(state="normal" if pode_cancelar else "disabled")

    def _pode_atualizar(self):
        """Verifica se o movimento pode ser atualizado"""
        tipo_nome = (
            self.tipo_movimento._tipo.lower().strip() if self.tipo_movimento else ""
        )
        status_atual = self.movimento._status

        if status_atual == "Cancelado":
            return False

        if "entrada" in tipo_nome or "entrada" in tipo_nome:
            if status_atual == "Efetivado":
                return False

        if "saída" in tipo_nome or "saida" in tipo_nome or "interno" in tipo_nome:
            if status_atual == "Despachado" and "saida" in tipo_nome:
                return False
            if status_atual == "Efetivado" and "interno" in tipo_nome:
                return False

        return True

    def _pode_cancelar(self):
        """Verifica se o movimento pode ser cancelado"""
        tipo_nome = (
            self.tipo_movimento._tipo.lower().strip() if self.tipo_movimento else ""
        )
        status_atual = self.movimento._status

        if status_atual == "Cancelado":
            return False

        if "interno" in tipo_nome and status_atual == "Efetivado":
            return False

        return True

    def _atualizar_movimento(self):
        """Atualiza o status do movimento"""
        if self.controller:
            try:
                self.controller.update_movimento(self.movimento._id_movimento)
                self._fechar()
            except Exception as e:
                Notificacao.erro(
                    "Erro", f"Erro ao atualizar movimento: {str(e)}", parent=self.root
                )

    def _cancelar_movimento(self):
        """Cancela o movimento"""
        if self.controller:
            try:
                if Notificacao.confirmacao(
                    "Confirmação",
                    "Tem certeza que deseja cancelar este movimento?",
                    parent=self.root,
                ):
                    self.controller.cancela_movimento(self.movimento._id_movimento)
                    self._fechar()
            except Exception as e:
                Notificacao.erro(
                    "Erro", f"Erro ao cancelar movimento: {str(e)}", parent=self.root
                )

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
