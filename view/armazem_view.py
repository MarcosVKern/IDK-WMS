import tkinter as tk
from tkinter import messagebox, ttk
from view.cores_padrao import Cores_Padrao

class Armazem_View():
    def __init__(self, parent=None):
        self.controller = None
        self.parent = parent
        
        if parent is None:
            self.root = tk.Toplevel()
            self.root.title("Gerenciamento de Armazéns")
            self.root.geometry("1280x720")
            self.root.state('zoomed')
            self.is_embedded = False
        else:
            self.root = tk.Frame(parent, bg=Cores_Padrao.COR_FUNDO)
            self.is_embedded = True

        self.var_id = tk.StringVar()
        self.var_cep = tk.StringVar()
        self.var_bairro = tk.StringVar()
        self.var_cidade = tk.StringVar()
        self.var_uf = tk.StringVar()
        self.var_pais = tk.StringVar()
        self.var_nome = tk.StringVar()

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="GERENCIAMENTO DE ARMAZÉNS", font=("Arial", 16, "bold"), pady=10, bg=Cores_Padrao.COR_FUNDO).pack()

        frame_form = tk.LabelFrame(self.root, text="Detalhes do Armazém", padx=10, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_form.pack(padx=20, pady=5, fill='x')
        frame_form.pack_propagate(False)    
        frame_form.configure(width=900)

        tk.Label(frame_form, text="ID:", bg=Cores_Padrao.COR_FUNDO).grid(row=0, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_id, state="readonly", width=10, bg=Cores_Padrao.COR_FUNDO).grid(row=1, column=0, padx=5, pady=5,sticky="w")

        tk.Label(frame_form, text="CEP:", bg=Cores_Padrao.COR_FUNDO).grid(row=2, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cep, width=30).grid(row=3, column=0, pady=5)

        tk.Label(frame_form, text="Bairro:", bg=Cores_Padrao.COR_FUNDO).grid(row=4, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_bairro, width=30).grid(row=5, column=0, pady=5)

        tk.Label(frame_form, text="Cidade:", bg=Cores_Padrao.COR_FUNDO).grid(row=6, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cidade, width=30).grid(row=7, column=0, pady=5)

        tk.Label(frame_form, text="UF:", bg=Cores_Padrao.COR_FUNDO).grid(row=0, column=1, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_uf, width=30).grid(row=1, column=1, pady=5)

        tk.Label(frame_form, text="País:", bg=Cores_Padrao.COR_FUNDO).grid(row=2, column=1, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_pais, width=30).grid(row=3, column=1, pady=5)

        tk.Label(frame_form, text="Nome:", bg=Cores_Padrao.COR_FUNDO).grid(row=4, column=1, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_nome, width=30).grid(row=5, column=1, pady=5)

        frame_botoes = tk.Frame(self.root, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_botoes.pack()

        tk.Button(frame_botoes, text="Adicionar Armazém", command=self._acao_adicionar, bg=Cores_Padrao.COR_BOTAO_SALVAR, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Atualizar Armazém", command=self._acao_atualizar, bg=Cores_Padrao.COR_BOTAO_ATUALIZAR, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Deletar Armazém", command=self._acao_deletar, bg=Cores_Padrao.COR_BOTAO_DELETAR, width=15).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_botoes, text="Limpar", command=self._limpar_campos, bg=Cores_Padrao.COR_BOTAO_LIMPAR, width=15).pack(side=tk.LEFT, padx=5)

        frame_tabela = tk.Frame(self.root, padx=20, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_tabela.pack(expand=True, fill="both")

        self.colunas = ("id", "cep", "bairro", "cidade", "uf", "pais", "nome")
        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("cep", text="CEP")
        self.tree.heading("bairro", text="Bairro")
        self.tree.heading("cidade", text="Cidade")
        self.tree.heading("uf", text="UF")
        self.tree.heading("pais", text="País")
        self.tree.heading("nome", text="Nome")

        for col in self.colunas: self.tree.column(col, anchor="center")

        self.tree.pack(side="left", expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_tabela)
        
        # Configurar efeito zebrado
        self.tree.tag_configure('evenrow', background=Cores_Padrao.COR_ZEBRADO_PAR)
        self.tree.tag_configure('oddrow', background=Cores_Padrao.COR_ZEBRADO_IMPAR)
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

    def get_armazem_data(self, armazem_existente=None):
        try:
            return {
                "cep": self.var_cep.get(),
                "bairro": self.var_bairro.get(),
                "cidade": self.var_cidade.get(),
                "uf": self.var_uf.get(),
                "pais": self.var_pais.get(),
                "nome": self.var_nome.get()
            }
        except Exception as e:
            messagebox.show_error(f"Erro ao obter dados do armazém: {e}")
            return None
        
    def _acao_adicionar(self):
        self.controller.add_armazem()
        self._acao_listar()

    def _acao_listar(self):
        if self.controller: self.controller.list_armazens()

    def show_armazens(self, lista):
        for i in self.tree.get_children(): self.tree.delete(i)
        for idx, a in enumerate(lista):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(a._id, a._cep, a._bairro, a._cidade, a._uf, a._pais, a._nome), tags=(tag,))

    def _acao_atualizar(self):
        self.controller.update_armazem()
        self._acao_listar()

    def get_id(self):
        val = self.var_id.get()
        return int(val) if val else None
    
    def _acao_deletar(self):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar este armazém?"):
            self.controller.delete_armazem()
            self._acao_listar()
            self._limpar_campos()

    def _limpar_campos(self):
        for val in [self.var_id, self.var_cep, self.var_bairro, self.var_cidade, self.var_uf, self.var_pais, self.var_nome]: val.set("")

    def _ao_selecionar_tabela(self, event):
        item_sel = self.tree.selection()
        if item_sel:
            v = self.tree.item(item_sel)['values']
            self.var_id.set(v[0])
            self.var_cep.set(v[1])
            self.var_bairro.set(v[2])
            self.var_cidade.set(v[3])
            self.var_uf.set(v[4])
            self.var_pais.set(v[5])
            self.var_nome.set(v[6])

    def show_message(self, msg): messagebox.showinfo("Sucesso", msg)

    def show_error(self, err): messagebox.showerror("Erro", err)