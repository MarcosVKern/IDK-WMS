import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
from view.cores_padrao import Cores_Padrao

class Produto_View():
    def __init__(self, parent=None):
        self.controller = None
        self.parent = parent
        
        if parent is None:
            self.root = tk.Toplevel()
            self.root.title("Gerenciamento de Produtos")
            self.root.geometry("1280x720")
            self.root.state('zoomed')
            self.is_embedded = False
        else:
            self.root = tk.Frame(parent, bg=Cores_Padrao.COR_FUNDO)
            self.is_embedded = True

        self.var_id = tk.StringVar()
        self.var_nome = tk.StringVar()
        self.var_descricao = tk.StringVar()
        self.var_imagem = tk.StringVar()

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="GERENCIAMENTO DE PRODUTOS", font=("Arial", 16, "bold"), pady=10, bg=Cores_Padrao.COR_FUNDO if self.is_embedded else None).pack()

        frame_form = tk.LabelFrame(self.root, text="Detalhes do Produto", padx=10, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_form.pack(padx=20, pady=5, fill='x')
        frame_form.pack_propagate(False)    
        frame_form.configure(width=900)

        tk.Label(frame_form, text="ID:", bg=Cores_Padrao.COR_FUNDO).grid(row=0, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_id, state="readonly", width=10, bg=Cores_Padrao.COR_INPUT_BG, readonlybackground=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=1, column=0, padx=5, pady=5,sticky="w")

        tk.Label(frame_form, text="Nome:", bg=Cores_Padrao.COR_FUNDO).grid(row=2, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_nome, width=30, bg=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=3, column=0, pady=5)

        tk.Label(frame_form, text="Descrição:", bg=Cores_Padrao.COR_FUNDO).grid(row=4, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_descricao, width=30, bg=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=5, column=0, pady=5)

        tk.Label(frame_form, text="URL da Imagem:", bg=Cores_Padrao.COR_FUNDO).grid(row=6, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_imagem, width=30, bg=Cores_Padrao.COR_INPUT_BG, fg=Cores_Padrao.COR_TEXTO).grid(row=7, column=0, pady=5)

        frame_botoes = tk.Frame(self.root, pady=10, bg=Cores_Padrao.COR_FUNDO if self.is_embedded else None)
        frame_botoes.pack()

        ctk.CTkButton(frame_botoes, text="Adicionar Produto", command=self._acao_adicionar, fg_color=Cores_Padrao.COR_BOTAO_SALVAR, text_color=Cores_Padrao.COR_TEXTO, width=150).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(frame_botoes, text="Atualizar Produto", command=self._acao_atualizar, fg_color=Cores_Padrao.COR_BOTAO_ATUALIZAR, text_color=Cores_Padrao.COR_TEXTO, width=150).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(frame_botoes, text="Deletar Produto", command=self._acao_deletar, fg_color=Cores_Padrao.COR_BOTAO_DELETAR, text_color=Cores_Padrao.COR_TEXTO, width=150).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(frame_botoes, text="Limpar", command=self._limpar_campos, fg_color=Cores_Padrao.COR_BOTAO_LIMPAR, text_color=Cores_Padrao.COR_TEXTO, width=150).pack(side=tk.LEFT, padx=5)

        frame_tabela = tk.Frame(self.root, padx=20, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_tabela.pack(expand=True, fill="both")

        self.colunas = ("id", "nome", "descricao", "imagem")
        style = ttk.Style()
        style.configure("Pink.Treeview", background=Cores_Padrao.COR_TABLE_BG, fieldbackground=Cores_Padrao.COR_TABLE_BG, foreground=Cores_Padrao.COR_TEXTO)
        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings", style="Pink.Treeview")

        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("imagem", text="URL da Imagem")

        for col in self.colunas: self.tree.column(col, anchor="center")

        self.tree.pack(side="left", expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_tabela)
        
        # Configurar efeito zebrado
        self.tree.tag_configure('evenrow', background=Cores_Padrao.COR_ZEBRADO_PAR)
        self.tree.tag_configure('oddrow', background=Cores_Padrao.COR_ZEBRADO_IMPAR)

    def display(self):
        """Exibir quando embutido em um frame"""
        self.root.pack(fill="both", expand=True)
        self.root.after(200, self._acao_listar)

    def run(self):
        """Executar como janela separada"""
        self.root.after(200, self._acao_listar)
        self.root.grab_set()
        self.root.mainloop()

    def get_produto_data(self, produto_existente=None):
        try:
            return {
                "nome": self.var_nome.get(),
                "descricao": self.var_descricao.get(),
                "imagem": self.var_imagem.get()
            }
        except Exception as e:
            messagebox.show_error(f"Erro ao obter dados do produto: {e}")
            return None
        
    def _acao_adicionar(self):
        self.controller.add_produto()
        self._acao_listar()

    def _acao_listar(self):
        if self.controller: self.controller.list_produtos()

    def show_produtos(self, lista):
        for i in self.tree.get_children(): self.tree.delete(i)
        for idx, p in enumerate(lista):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(p._id, p._nome, p._descricao, p._imagem), tags=(tag,))

    def _acao_atualizar(self):
        self.controller.update_produto()
        self._acao_listar()

    def get_id(self):
        val = self.var_id.get()
        return int(val) if val else None
    
    def _acao_deletar(self):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar este produto?"):
            self.controller.delete_produto()
            self._acao_listar()
            self._limpar_campos()

    def _limpar_campos(self):
        for val in [self.var_id, self.var_nome, self.var_descricao, self.var_imagem]: val.set("")

    def _ao_selecionar_tabela(self, event):
        item_sel = self.tree.selection()
        if item_sel:
            v = self.tree.item(item_sel)['values']
            self.var_id.set(v[0])
            self.var_nome.set(v[1])
            self.var_descricao.set(v[2])
            self.var_imagem.set(v[3])

    def show_message(self, msg): messagebox.showinfo("Sucesso", msg)

    def show_error(self, err): messagebox.showerror("Erro", err)