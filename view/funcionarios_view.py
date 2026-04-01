import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
from view.cores_padrao import Cores_Padrao

class Funcionario_View():
    def __init__(self, parent=None):
        self.controller = None
        self.parent = parent
        
        if parent is None:
            self.root = tk.Toplevel()
            self.root.title("Gerenciamento de Funcionarios")
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
        self.var_cargo = tk.StringVar()
        self.var_email = tk.StringVar()
        self.var_senha = tk.StringVar()
        self.var_situacao = tk.StringVar()

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="GERENCIAMENTO DE FUNCIONARIOS", font=("Arial", 16, "bold"), pady=10, bg=Cores_Padrao.COR_FUNDO).pack()

        frame_form = tk.LabelFrame(self.root, text="Detalhes do Funcionario", padx=10, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_form.pack(padx=20, pady=5, fill='x')
        frame_form.pack_propagate(False)    
        frame_form.configure(width=900)

        tk.Label(frame_form, text="ID:", bg=Cores_Padrao.COR_FUNDO).grid(row=0, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_id, state="readonly", width=10, bg=Cores_Padrao.COR_INPUT_BG, readonlybackground=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=1, column=0, padx=5, pady=5,sticky="w")

        tk.Label(frame_form, text="CEP:", bg=Cores_Padrao.COR_FUNDO).grid(row=2, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cep, width=30, bg=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=3, column=0, pady=5)

        tk.Label(frame_form, text="Bairro:", bg=Cores_Padrao.COR_FUNDO).grid(row=4, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_bairro, width=30, bg=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=5, column=0, pady=5)

        tk.Label(frame_form, text="Cidade:", bg=Cores_Padrao.COR_FUNDO).grid(row=6, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cidade, width=30, bg=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=7, column=0, pady=5)

        tk.Label(frame_form, text="UF:", bg=Cores_Padrao.COR_FUNDO).grid(row=8, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_uf, width=30, bg=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=9, column=0, pady=5)

        tk.Label(frame_form, text="País:", bg=Cores_Padrao.COR_FUNDO).grid(row=10, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_pais, width=30, bg=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=11, column=0, pady=5)

        tk.Label(frame_form, text="Nome:", bg=Cores_Padrao.COR_FUNDO).grid(row=2, column=1, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_nome, width=30, bg=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=3, column=1, pady=5)

        tk.Label(frame_form, text="Cargo:", bg=Cores_Padrao.COR_FUNDO).grid(row=4, column=1, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_cargo, width=30, bg=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=5, column=1, pady=5)

        tk.Label(frame_form, text="Email:", bg=Cores_Padrao.COR_FUNDO).grid(row=6, column=1, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_email, width=30, bg=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=7, column=1, pady=5)

        tk.Label(frame_form, text="Senha:", bg=Cores_Padrao.COR_FUNDO).grid(row=8, column=1, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_senha, state="readonly", width=30, show="*", bg=Cores_Padrao.COR_INPUT_BG, readonlybackground=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=9, column=1, pady=5)

        tk.Label(frame_form, text="Situação:", bg=Cores_Padrao.COR_FUNDO).grid(row=10, column=1, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_situacao, state="readonly", width=30, bg=Cores_Padrao.COR_INPUT_BG, readonlybackground=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=11, column=1, pady=5)

        ctk.CTkButton(frame_form, text="Ativar/Inativar", command=self._acao_ativar, fg_color=Cores_Padrao.COR_BOTAO_ATIVAR, text_color=Cores_Padrao.COR_TEXTO, width=150).grid(row=11, column=2, pady=5, sticky="w")
        ctk.CTkButton(frame_form, text="Bloquear/Desbloquear", command=self._acao_bloquear, fg_color=Cores_Padrao.COR_BOTAO_BLOQUEAR, text_color=Cores_Padrao.COR_TEXTO, width=150).grid(row=11, column=4, pady=5, sticky="w")

        frame_botoes = tk.Frame(self.root, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_botoes.pack()

        ctk.CTkButton(frame_botoes, text="Adicionar Funcionário", command=self._acao_adicionar, fg_color=Cores_Padrao.COR_BOTAO_SALVAR, text_color=Cores_Padrao.COR_TEXTO, width=150).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(frame_botoes, text="Atualizar Funcionário", command=self._acao_atualizar, fg_color=Cores_Padrao.COR_BOTAO_ATUALIZAR, text_color=Cores_Padrao.COR_TEXTO, width=150).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(frame_botoes, text="Deletar Funcionário", command=self._acao_deletar, fg_color=Cores_Padrao.COR_BOTAO_DELETAR, text_color=Cores_Padrao.COR_TEXTO, width=150).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(frame_botoes, text="Limpar", command=self._limpar_campos, fg_color=Cores_Padrao.COR_BOTAO_LIMPAR, text_color=Cores_Padrao.COR_TEXTO, width=150).pack(side=tk.LEFT, padx=5)

        frame_tabela = tk.Frame(self.root, padx=20, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_tabela.pack(expand=True, fill="both")

        self.colunas = ("id", "cep", "bairro", "cidade", "uf", "pais", "nome", "cargo", "email", "senha", "situacao")
        style = ttk.Style()
        style.configure("Pink.Treeview", background=Cores_Padrao.COR_TABLE_BG, fieldbackground=Cores_Padrao.COR_TABLE_BG, foreground=Cores_Padrao.COR_TEXTO)
        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings", style="Pink.Treeview")

        vsb = ttk.Scrollbar(frame_tabela, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(frame_tabela, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.heading("id", text="ID")
        self.tree.heading("cep", text="CEP")
        self.tree.heading("bairro", text="Bairro")
        self.tree.heading("cidade", text="Cidade")
        self.tree.heading("uf", text="UF")
        self.tree.heading("pais", text="País")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("cargo", text="Cargo")
        self.tree.heading("email", text="Email")
        self.tree.heading("senha", text="Senha")
        self.tree.heading("situacao", text="Situação")

        for col in self.colunas: self.tree.column(col, anchor="center")

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")

        # Configurar efeito zebrado
        self.tree.tag_configure('evenrow', background=Cores_Padrao.COR_ZEBRADO_PAR)
        self.tree.tag_configure('oddrow', background=Cores_Padrao.COR_ZEBRADO_IMPAR)

        self.tree.pack(side="left", expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_tabela)

    def run(self):
        self.root.after(200, self._acao_listar)
        self.root.grab_set()
        self.root.mainloop()

    def display(self):
        """Exibir quando embutido em um frame"""
        self.root.pack(fill="both", expand=True)
        self.root.after(200, self._acao_listar)

    def get_funcionario_data(self, funcionario_existente=None):
        try:
            return {
                "cep": self.var_cep.get(),
                "bairro": self.var_bairro.get(),
                "cidade": self.var_cidade.get(),
                "uf": self.var_uf.get(),
                "pais": self.var_pais.get(),
                "nome": self.var_nome.get(),
                "cargo": self.var_cargo.get(),
                "email": self.var_email.get(),
                "senha": self.var_senha.get(),
                "situacao": self.var_situacao.get()
            }
        except Exception as e:
            messagebox.show_error(f"Erro ao obter dados do funcionário: {e}")
            return None
        
    def _acao_adicionar(self):
        self.controller.add_funcionario()
        self._acao_listar()

    def _acao_listar(self):
        if self.controller: self.controller.list_funcionarios()

    def show_funcionarios(self, lista):
        for i in self.tree.get_children(): self.tree.delete(i)
        for idx, f in enumerate(lista):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            senha_oculta = "*" * len(f._senha)
            self.tree.insert("", "end", values=(f._id, f._cep, f._bairro, f._cidade, f._uf, f._pais, f._nome, f._cargo, f._email, senha_oculta, f._situacao), tags=(tag,))

    def _acao_atualizar(self):
        self.controller.update_funcionario()
        self._acao_listar()

    def get_id(self):
        val = self.var_id.get()
        return int(val) if val else None
    
    def _acao_deletar(self):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar este funcionário?"):
            self.controller.delete_funcionario()
            self._acao_listar()
            self._limpar_campos()

    def _limpar_campos(self):
        for val in [self.var_id, self.var_cep, self.var_bairro, self.var_cidade, 
                    self.var_uf, self.var_pais, self.var_nome, self.var_cargo, 
                    self.var_email, self.var_senha, self.var_situacao]: val.set("")

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
            self.var_cargo.set(v[7])
            self.var_email.set(v[8])
            self.var_senha.set(v[9])
            self.var_situacao.set(v[10])

    def show_message(self, msg): messagebox.showinfo("Sucesso", msg)

    def show_error(self, err): messagebox.showerror("Erro", err)

    def _acao_ativar(self):
        if self.var_situacao.get() != "Ativo":
            self.var_situacao.set("Ativo")
        else:
            self.var_situacao.set("Inativo")

    def _acao_bloquear(self):
        if self.var_situacao.get() == "Bloqueado":
            self.var_situacao.set("Ativo")
        else:
            self.var_situacao.set("Bloqueado")