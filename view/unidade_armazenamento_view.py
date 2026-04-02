import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from view.cores_padrao import Cores_Padrao
from view.notificacao import Notificacao

class UnidadeArmazenamento_View():
    def __init__(self, parent=None):
        self.controller = None
        self.parent = parent
        
        if parent is None:
            self.root = tk.Toplevel()
            self.root.title("Gerenciamento de Unidades de Armazenamento")
            self.root.geometry("1280x720")
            self.root.state('zoomed')
            self.is_embedded = False
        else:
            self.root = tk.Frame(parent, bg=Cores_Padrao.COR_FUNDO)
            self.is_embedded = True

        self.var_id = tk.StringVar()
        self.var_unidade = tk.StringVar()
        self.var_armazem = tk.StringVar()
        self.armazens = []

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="GERENCIAMENTO DE UNIDADES DE ARMAZENAMENTO", font=("Arial", 16, "bold"), pady=10, bg=Cores_Padrao.COR_FUNDO).pack()

        frame_form = tk.LabelFrame(self.root, text="Detalhes da Unidade de Armazenamento", padx=10, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_form.pack(padx=20, pady=5, fill='x')
        frame_form.pack_propagate(False)    
        frame_form.configure(width=900)

        tk.Label(frame_form, text="ID:", bg=Cores_Padrao.COR_FUNDO).grid(row=0, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_id, state="readonly", width=10, bg=Cores_Padrao.COR_INPUT_BG, readonlybackground=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=1, column=0, padx=5, pady=5, sticky="w")

        tk.Label(frame_form, text="Unidade:", bg=Cores_Padrao.COR_FUNDO).grid(row=2, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_unidade, width=30, bg=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=3, column=0, pady=5)

        tk.Label(frame_form, text="Armazém:", bg=Cores_Padrao.COR_FUNDO).grid(row=4, column=0, sticky="w")
        self.combobox_armazem = ttk.Combobox(frame_form, textvariable=self.var_armazem, width=27, state="readonly")
        self.combobox_armazem.grid(row=5, column=0, pady=5)

        frame_botoes = tk.Frame(self.root, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_botoes.pack()

        ctk.CTkButton(frame_botoes, text="Adicionar", command=self._acao_adicionar, fg_color=Cores_Padrao.COR_BOTAO_SALVAR, hover_color=Cores_Padrao.COR_BOTAO_SALVAR_HOVER, text_color=Cores_Padrao.COR_TEXTO_BOTAO, width=150).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(frame_botoes, text="Deletar", command=self._acao_deletar, fg_color=Cores_Padrao.COR_BOTAO_DELETAR, hover_color=Cores_Padrao.COR_BOTAO_DELETAR_HOVER, text_color=Cores_Padrao.COR_TEXTO_BOTAO, width=150).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(frame_botoes, text="Limpar", command=self._limpar_campos, fg_color=Cores_Padrao.COR_BOTAO_LIMPAR, hover_color=Cores_Padrao.COR_BOTAO_LIMPAR_HOVER, text_color=Cores_Padrao.COR_TEXTO, width=150).pack(side=tk.LEFT, padx=5)

        frame_tabela = tk.Frame(self.root, padx=20, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_tabela.pack(expand=True, fill="both")

        self.colunas = ("id", "unidade", "armazem")
        style = ttk.Style()
        style.configure("Pink.Treeview", background=Cores_Padrao.COR_TABLE_BG, fieldbackground=Cores_Padrao.COR_TABLE_BG, foreground=Cores_Padrao.COR_TEXTO)
        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings", style="Pink.Treeview")

        self.tree.heading("id", text="ID")
        self.tree.heading("unidade", text="Unidade")
        self.tree.heading("armazem", text="Armazém")

        for col in self.colunas: 
            self.tree.column(col, anchor="center")

        self.tree.pack(side="left", expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_tabela)
        
        # Configurar efeito zebrado
        self.tree.tag_configure('evenrow', background=Cores_Padrao.COR_ZEBRADO_PAR)
        self.tree.tag_configure('oddrow', background=Cores_Padrao.COR_ZEBRADO_IMPAR)

    def run(self):
        self.root.after(200, self._acao_listar)
        self.root.grab_set()
        self.root.mainloop()

    def display(self):
        """Exibir quando embutido em um frame"""
        self.root.pack(fill="both", expand=True)
        self.root.after(200, self._acao_listar)

    def get_unidade_armazenamento_data(self, unidade_existente=None):
        try:
            armazem_selecionado = self.var_armazem.get()
            if armazem_selecionado:
                armazem_id = armazem_selecionado.split(' - ')[0]
            else:
                armazem_id = ""
            
            return {
                "unidade": self.var_unidade.get(),
                "armazem": armazem_id
            }
        except Exception as e:
            Notificacao.erro("Erro", f"Erro ao obter dados da unidade de armazenamento: {e}", parent=self.root)
            return None
        
    def _acao_adicionar(self):
        self.controller.add_unidade_armazenamento()
        self._acao_listar()

    def _acao_listar(self):
        if self.controller: 
            self.controller.list_unidades_armazenamento()

    def show_unidades_armazenamento(self, lista):
        for i in self.tree.get_children(): 
            self.tree.delete(i)
        for idx, u in enumerate(lista):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(u._id, u._unidade, u._armazem), tags=(tag,))

    def get_id(self):
        val = self.var_id.get()
        return val if val else None
    
    def _acao_deletar(self):
        if Notificacao.confirmacao("Confirmação", "Tem certeza que deseja deletar esta unidade de armazenamento?", parent=self.root):
            self.controller.delete_unidade_armazenamento()
            self._acao_listar()
            self._limpar_campos()

    def _limpar_campos(self):
        for val in [self.var_id, self.var_unidade, self.var_armazem]: 
            val.set("")
        if hasattr(self, 'combobox_armazem') and self.armazens:
            self.combobox_armazem.current(0)

    def _ao_selecionar_tabela(self, event):
        item_sel = self.tree.selection()
        if item_sel:
            v = self.tree.item(item_sel)['values']
            self.var_id.set(v[0])
            self.var_unidade.set(v[1])
            self.var_armazem.set(v[2])

    def show_message(self, msg):
        Notificacao.sucesso("Sucesso", msg, parent=self.root)

    def show_error(self, err):
        Notificacao.erro("Erro", err, parent=self.root)

    def set_armazens_disponiveis(self, armazens):
        self.armazens = armazens
        valores = [f"{a._id} - {a._nome}" for a in armazens]
        self.combobox_armazem['values'] = valores
        if valores:
            self.combobox_armazem.current(0)
