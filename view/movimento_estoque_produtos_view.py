import tkinter as tk
from tkinter import messagebox, ttk
from view.cores_padrao import Cores_Padrao

class MovimentoEstoqueProdutos_View:
    def __init__(self, tipo_movimento, origem, destino, produtos_disponiveis, parent=None):
        self.tipo_movimento = tipo_movimento
        self.origem = origem
        self.destino = destino
        self.produtos_disponiveis = produtos_disponiveis  # lista dict {id,nome,quantidade}
        self.selected = {}  # produto_id -> quantidade

        if parent is None:
            self.root = tk.Toplevel()
            self.root.title("Seleção de Produtos para Movimento")
            self.root.geometry("800x600")
            self.root.configure(bg=Cores_Padrao.COR_FUNDO)
            self.root.grab_set()
        else:
            self.root = tk.Frame(parent, bg=Cores_Padrao.COR_FUNDO)

        self.var_produto = tk.StringVar()
        self.var_quantidade = tk.StringVar()

        self._setup_ui()

    def _setup_ui(self):
        frame_top = tk.Frame(self.root, bg=Cores_Padrao.COR_FUNDO)
        frame_top.pack(fill="x", padx=10, pady=10)

        tk.Label(frame_top, text=f"Tipo: {self.tipo_movimento} | Origem: {self.origem or '-'} | Destino: {self.destino or '-'}", bg=Cores_Padrao.COR_FUNDO).pack(anchor="w")

        frame_form = tk.Frame(self.root, bg=Cores_Padrao.COR_FUNDO)
        frame_form.pack(fill="x", padx=10)

        tk.Label(frame_form, text="Produto:", bg=Cores_Padrao.COR_FUNDO).grid(row=0, column=0, sticky="w")
        self.combo_produto = ttk.Combobox(frame_form, textvariable=self.var_produto, width=50, state="readonly")
        self.combo_produto.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Quantidade:", bg=Cores_Padrao.COR_FUNDO).grid(row=1, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_quantidade, width=20).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Button(frame_form, text="Incluir/Atualizar", command=self._incluir_produto).grid(row=0, column=2, rowspan=2, padx=5)

        cols = ("id", "nome", "qtd_disponivel", "qtd_selecionada")
        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor="center", width=150)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_produto)

        bot_frame = tk.Frame(self.root, bg=Cores_Padrao.COR_FUNDO)
        bot_frame.pack(pady=10)
        tk.Button(bot_frame, text="Remover Selecionado", command=self._remover_produto).pack(side=tk.LEFT, padx=5)
        tk.Button(bot_frame, text="Confirmar", command=self._confirmar).pack(side=tk.LEFT, padx=5)
        tk.Button(bot_frame, text="Cancelar", command=self._cancelar).pack(side=tk.LEFT, padx=5)

        self._atualizar_combo_produtos()
        self._refresh_tree()

        if isinstance(self.root, tk.Toplevel):
            self.root.protocol("WM_DELETE_WINDOW", self._cancelar)

        self.result = None

    def _atualizar_combo_produtos(self):
        valores = [f"{p['id']} - {p['nome']} (disp: {p['quantidade']})" for p in self.produtos_disponiveis]
        self.combo_produto['values'] = valores
        if valores:
            self.combo_produto.current(0)

    def _incluir_produto(self):
        if not self.var_produto.get():
            messagebox.showerror("Erro", "Selecione um produto")
            return
        try:
            quantidade = float(self.var_quantidade.get())
            if quantidade <= 0:
                raise ValueError
        except Exception:
            messagebox.showerror("Erro", "Quantidade inválida")
            return

        pid = self.var_produto.get().split(' - ')[0]
        pid = int(pid)

        produto_info = next((p for p in self.produtos_disponiveis if p['id'] == pid), None)
        if not produto_info:
            messagebox.showerror("Erro", "Produto não encontrado")
            return

        if self.tipo_movimento.lower().startswith("saída") or self.tipo_movimento.lower().startswith("interno"):
            if quantidade > produto_info['quantidade']:
                messagebox.showerror("Erro", "Quantidade maior que disponível")
                return

        self.selected[pid] = quantidade
        self._refresh_tree()

    def _refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in self.produtos_disponiveis:
            qtd_selecionada = self.selected.get(p['id'], 0)
            if self.tipo_movimento.lower().startswith("entrada") or p['quantidade'] > 0:
                self.tree.insert("", "end", values=(p['id'], p['nome'], p['quantidade'], qtd_selecionada))

    def _ao_selecionar_produto(self, event):
        sel = self.tree.selection()
        if sel:
            item = self.tree.item(sel[0])
            values = item['values']
            if values:
                pid, nome, qtd_disp, qtd_sel = values
                self.var_produto.set(f"{pid} - {nome}")
                self.var_quantidade.set(str(qtd_disp))  # or '' if not want to set

    def _remover_produto(self):
        sel = self.tree.selection()
        if not sel:
            return
        for item in sel:
            pid = int(self.tree.item(item)['values'][0])
            if pid in self.selected:
                del self.selected[pid]
        self._refresh_tree()

    def _confirmar(self):
        if not self.selected:
            messagebox.showerror("Erro", "Selecione ao menos um produto")
            return
        self.result = [{'produto': pid, 'quantidade': qty} for pid, qty in self.selected.items()]
        if isinstance(self.root, tk.Toplevel):
            self.root.destroy()

    def _cancelar(self):
        self.result = None
        if isinstance(self.root, tk.Toplevel):
            self.root.destroy()

    def show(self):
        if isinstance(self.root, tk.Toplevel):
            self.root.wait_window(self.root)
        return self.result