import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from view.cores_padrao import Cores_Padrao
from view.notificacao import Notificacao


class MovimentoEstoqueProdutos_View:
    def __init__(
        self, tipo_movimento, origem, destino, produtos_disponiveis, parent=None
    ):
        self.tipo_movimento = tipo_movimento
        self.origem = origem
        self.destino = destino
        self.produtos_disponiveis = produtos_disponiveis
        self.selected = {}

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

        tk.Label(
            frame_top,
            text=f"Tipo: {self.tipo_movimento} | Origem: {self.origem or '-'} | Destino: {self.destino or '-'}",
            bg=Cores_Padrao.COR_FUNDO,
        ).pack(anchor="w")

        frame_form = tk.Frame(self.root, bg=Cores_Padrao.COR_FUNDO)
        frame_form.pack(fill="x", padx=10)

        tk.Label(frame_form, text="Produto:", bg=Cores_Padrao.COR_FUNDO).grid(
            row=0, column=0, sticky="w"
        )
        self.combo_produto = ttk.Combobox(
            frame_form, textvariable=self.var_produto, width=50, state="readonly"
        )
        self.combo_produto.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Quantidade:", bg=Cores_Padrao.COR_FUNDO).grid(
            row=1, column=0, sticky="w"
        )
        tk.Entry(
            frame_form,
            textvariable=self.var_quantidade,
            width=20,
            bg=Cores_Padrao.COR_INPUT_BG,
            fg=Cores_Padrao.COR_TEXTO,
        ).grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkButton(
            frame_form,
            text="Incluir/Atualizar",
            command=self._incluir_produto,
            fg_color=Cores_Padrao.COR_BOTAO_SALVAR,
            text_color=Cores_Padrao.COR_TEXTO,
            width=150,
        ).grid(row=0, column=2, rowspan=2, padx=5)

        cols = ("id", "nome", "qtd_disponivel", "qtd_selecionada")
        style = ttk.Style()
        style.configure(
            "Pink.Treeview",
            background=Cores_Padrao.COR_TABLE_BG,
            fieldbackground=Cores_Padrao.COR_TABLE_BG,
            foreground=Cores_Padrao.COR_TEXTO,
        )
        self.tree = ttk.Treeview(
            self.root, columns=cols, show="headings", style="Pink.Treeview"
        )
        for c in cols:
            self.tree.heading(c, text=c.capitalize())
            self.tree.column(c, anchor="center", width=150)
        self.tree.pack(expand=True, fill="both", padx=10, pady=10)
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_produto)

        bot_frame = tk.Frame(self.root, bg=Cores_Padrao.COR_FUNDO)
        bot_frame.pack(pady=10)
        ctk.CTkButton(
            bot_frame,
            text="Remover Selecionado",
            command=self._remover_produto,
            fg_color=Cores_Padrao.COR_BOTAO_DELETAR,
            hover_color=Cores_Padrao.COR_BOTAO_DELETAR_HOVER,
            text_color=Cores_Padrao.COR_TEXTO_BOTAO,
            width=150,
        ).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(
            bot_frame,
            text="Confirmar",
            command=self._confirmar,
            fg_color=Cores_Padrao.COR_BOTAO_SALVAR,
            hover_color=Cores_Padrao.COR_BOTAO_SALVAR_HOVER,
            text_color=Cores_Padrao.COR_TEXTO_BOTAO,
            width=150,
        ).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(
            bot_frame,
            text="Cancelar",
            command=self._cancelar,
            fg_color=Cores_Padrao.COR_BOTAO_LIMPAR,
            hover_color=Cores_Padrao.COR_BOTAO_LIMPAR_HOVER,
            text_color=Cores_Padrao.COR_TEXTO,
            width=150,
        ).pack(side=tk.LEFT, padx=5)

        self._atualizar_combo_produtos()
        self._refresh_tree()

        self.root.protocol("WM_DELETE_WINDOW", self._cancelar)

        self.result = None

    def _atualizar_combo_produtos(self):
        valores = [
            f"{p['id']} - {p['nome']} (disp: {p['quantidade']})"
            for p in self.produtos_disponiveis
        ]
        self.combo_produto["values"] = valores
        if valores:
            self.combo_produto.current(0)

    def _incluir_produto(self):
        if not self.var_produto.get():
            Notificacao.erro("Erro", "Selecione um produto", parent=self.root)
            return
        try:
            quantidade = float(self.var_quantidade.get())
            if quantidade <= 0:
                raise ValueError
        except Exception:
            Notificacao.erro("Erro", "Quantidade inválida", parent=self.root)
            return

        pid = self.var_produto.get().split(" - ")[0]
        pid = int(pid)

        produto_info = next(
            (p for p in self.produtos_disponiveis if p["id"] == pid), None
        )
        if not produto_info:
            Notificacao.erro("Erro", "Produto não encontrado", parent=self.root)
            return

        if self.tipo_movimento.lower().startswith(
            "saída"
        ) or self.tipo_movimento.lower().startswith("interno"):
            if quantidade > produto_info["quantidade"]:
                Notificacao.erro(
                    "Erro", "Quantidade maior que disponível", parent=self.root
                )
                return

        self.selected[pid] = quantidade
        self._refresh_tree()

    def _refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for p in self.produtos_disponiveis:
            qtd_selecionada = self.selected.get(p["id"], 0)
            if self.tipo_movimento.lower().startswith("entrada") or p["quantidade"] > 0:
                self.tree.insert(
                    "",
                    "end",
                    values=(p["id"], p["nome"], p["quantidade"], qtd_selecionada),
                )

    def _ao_selecionar_produto(self, event):
        sel = self.tree.selection()
        if sel:
            item = self.tree.item(sel[0])
            values = item["values"]
            if values:
                pid, nome, qtd_disp, qtd_sel = values
                self.var_produto.set(f"{pid} - {nome}")
                self.var_quantidade.set(str(qtd_disp))  # or '' if not want to set

    def _remover_produto(self):
        sel = self.tree.selection()
        if not sel:
            return
        for item in sel:
            pid = int(self.tree.item(item)["values"][0])
            if pid in self.selected:
                del self.selected[pid]
        self._refresh_tree()

    def _confirmar(self):
        if not self.selected:
            Notificacao.erro("Erro", "Selecione ao menos um produto", parent=self.root)
            return
        self.result = [
            {"produto": pid, "quantidade": qty} for pid, qty in self.selected.items()
        ]
        self.root.destroy()

    def _cancelar(self):
        self.result = None
        self.root.destroy()

    def show(self):
        self.root.wait_window(self.root)
        return self.result
