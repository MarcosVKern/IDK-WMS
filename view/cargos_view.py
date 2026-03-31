import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
from view.cores_padrao import Cores_Padrao

class Cargo_View():
    def __init__(self, parent=None):
        self.controller = None
        self.parent = parent
        
        if parent is None:
            self.root = tk.Toplevel()
            self.root.title("Gerenciamento de Cargos")
            self.root.geometry("1280x720")
            self.root.state('zoomed')
            self.is_embedded = False
        else:
            self.root = tk.Frame(parent, bg=Cores_Padrao.COR_FUNDO)
            self.is_embedded = True

        self.var_id = tk.StringVar()
        self.var_cargo = tk.StringVar()

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="GERENCIAMENTO DE CARGOS", font=("Arial", 16, "bold"), pady=10).pack()

        frame_form = tk.LabelFrame(self.root, text="Detalhes do Cargo", padx=10, pady=10)
        frame_form.pack(padx=20, pady=5, fill='x')
        frame_form.pack_propagate(False)
        frame_form.configure(width=900)

        tk.Label(frame_form, text="ID:").grid(row=0, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_id, state="readonly", width=10, bg=Cores_Padrao.COR_FUNDO).grid(row=0, column=1, padx=5, pady=5,sticky="w")

        tk.Label(frame_form, text="Cargo:").grid(row=0, column=2, sticky="w")
        self.combo_cargo = ttk.Combobox(frame_form, textvariable=self.var_cargo, width=50, state="readonly")
        self.combo_cargo.grid(row=0, column=3, padx=5, pady=5)

        frame_botoes = tk.Frame(self.root, pady=10)
        frame_botoes.pack()

        #tk.Button(frame_botoes, text="Adicionar Cargo", command=self._acao_adicionar, bg=Cores_Padrao.COR_BOTAO_SALVAR, width=15).pack(side=tk.LEFT, padx=5)
        #tk.Button(frame_botoes, text="Atualizar Cargo", command=self._acao_atualizar, bg=Cores_Padrao.COR_BOTAO_ATUALIZAR, width=15).pack(side=tk.LEFT, padx=5)
        #tk.Button(frame_botoes, text="Deletar Cargo", command=self._acao_deletar, bg=Cores_Padrao.COR_BOTAO_DELETAR, width=15).pack(side=tk.LEFT, padx=5)
        #tk.Button(frame_botoes, text="Limpar", command=self._limpar_campos, bg=Cores_Padrao.COR_BOTAO_LIMPAR, width=15).pack(side=tk.LEFT, padx=5)

        frame_tabela = tk.Frame(self.root, padx=20, pady=10)
        frame_tabela.pack(expand=True, fill="both")

        self.colunas = ("id", "cargo")
        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("cargo", text="Cargo")

        for col in self.colunas: self.tree.column(col, anchor="center")

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

    def get_cargo_data(self, cargo_existente=None):
        try:
            return {
                "cargo": self.var_cargo.get()
            }
        except Exception as e:
            messagebox.show_error(f"Erro ao obter dados do cargo: {e}")
            return None
        
    def _acao_adicionar(self):
        self.controller.add_cargo()
        self._acao_listar()

    def _acao_listar(self):
        if self.controller: self.controller.list_cargos()

    def show_cargos(self, lista):
        for i in self.tree.get_children(): self.tree.delete(i)
        for idx, c in enumerate(lista):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(c._id, c._cargo), tags=(tag,))

    def preencher_combo_cargo(self, lista):
        self.combo_cargo['values'] = [c._cargo for c in lista]

    def _acao_atualizar(self):
        self.controller.update_cargo()
        self._acao_listar()

    def get_id(self):
        val = self.var_id.get()
        return int(val) if val else None
    
    def _acao_deletar(self):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja deletar este cargo?"):
            self.controller.delete_cargo()
            self._acao_listar()
            self._limpar_campos()

    def _limpar_campos(self):
        for val in [self.var_id, self.var_cargo]: val.set("")

    def _ao_selecionar_tabela(self, event):
        item_sel = self.tree.selection()
        if item_sel:
            v = self.tree.item(item_sel)['values']
            self.var_id.set(v[0])
            self.var_cargo.set(v[1])

    def show_message(self, msg): messagebox.showinfo("Sucesso", msg)

    def show_error(self, err): messagebox.showerror("Erro", err)