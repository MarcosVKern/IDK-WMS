import tkinter as tk
from tkinter import messagebox, ttk
from view.cores_padrao import Cores_Padrao

class MovimentoEstoque_View():
    def __init__(self, parent=None, funcionario_logado=None):
        self.controller = None
        self.parent = parent
        self.funcionario_logado = funcionario_logado
        
        if parent is None:
            self.root = tk.Toplevel()
            self.root.title("Gerenciamento de Movimentos de Estoque")
            self.root.geometry("1280x720")
            self.root.state('zoomed')
            self.is_embedded = False
        else:
            self.root = tk.Frame(parent, bg=Cores_Padrao.COR_FUNDO)
            self.is_embedded = True

        self.var_id = tk.StringVar()
        self.var_tipo_movimento = tk.StringVar()
        self.var_origem = tk.StringVar()
        self.var_destino = tk.StringVar()
        self.var_responsavel = tk.StringVar()
        self.var_status = tk.StringVar()

        self.tipos_movimento = []
        self.unidades = []
        self.funcionarios = []

        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self.root, text="GERENCIAMENTO DE MOVIMENTOS DE ESTOQUE", font=("Arial", 16, "bold"), pady=10, bg=Cores_Padrao.COR_FUNDO).pack()

        frame_form = tk.LabelFrame(self.root, text="Detalhes do Movimento", padx=10, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_form.pack(padx=20, pady=5, fill='x')
        frame_form.pack_propagate(False)    
        frame_form.configure(width=900)

        tk.Label(frame_form, text="ID:", bg=Cores_Padrao.COR_FUNDO).grid(row=0, column=0, sticky="w")
        tk.Entry(frame_form, textvariable=self.var_id, state="readonly", width=10, bg=Cores_Padrao.COR_FUNDO).grid(row=1, column=0, padx=5, pady=5, sticky="w")

        tk.Label(frame_form, text="Tipo de Movimento:", bg=Cores_Padrao.COR_FUNDO).grid(row=2, column=0, sticky="w")
        self.combo_tipo = ttk.Combobox(frame_form, textvariable=self.var_tipo_movimento, width=27, state="readonly")
        self.combo_tipo.grid(row=3, column=0, pady=5)
        self.combo_tipo.bind("<<ComboboxSelected>>", self._ao_mudar_tipo_movimento)

        tk.Label(frame_form, text="Unidade de Origem:", bg=Cores_Padrao.COR_FUNDO).grid(row=4, column=0, sticky="w")
        self.combo_origem = ttk.Combobox(frame_form, textvariable=self.var_origem, width=27, state="readonly")
        self.combo_origem.grid(row=5, column=0, pady=5)

        tk.Label(frame_form, text="Unidade de Destino:", bg=Cores_Padrao.COR_FUNDO).grid(row=6, column=0, sticky="w")
        self.combo_destino = ttk.Combobox(frame_form, textvariable=self.var_destino, width=27, state="readonly")
        self.combo_destino.grid(row=7, column=0, pady=5)

        tk.Label(frame_form, text="Funcionário Responsável:", bg=Cores_Padrao.COR_FUNDO).grid(row=0, column=1, sticky="w")
        self.combo_responsavel = ttk.Combobox(frame_form, textvariable=self.var_responsavel, width=27, state="readonly")
        self.combo_responsavel.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text="Status:", bg=Cores_Padrao.COR_FUNDO).grid(row=2, column=1, sticky="w")
        self.combo_status = ttk.Combobox(frame_form, textvariable=self.var_status, width=27, state="readonly")

        frame_botoes = tk.Frame(self.root, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_botoes.pack()

        self.btn_adicionar = tk.Button(frame_botoes, text="Criar Movimento", command=self._acao_adicionar, bg=Cores_Padrao.COR_BOTAO_SALVAR, width=15)
        self.btn_adicionar.pack(side=tk.LEFT, padx=5)
        
        self.btn_atualizar = tk.Button(frame_botoes, text="Atualizar Status", command=self._acao_atualizar, bg=Cores_Padrao.COR_BOTAO_ATUALIZAR, width=15)
        self.btn_atualizar.pack(side=tk.LEFT, padx=5)
        
        self.btn_deletar = tk.Button(frame_botoes, text="Cancelar", command=self._acao_deletar, bg=Cores_Padrao.COR_BOTAO_DELETAR, width=15)
        self.btn_deletar.pack(side=tk.LEFT, padx=5)
        
        tk.Button(frame_botoes, text="Limpar", command=self._limpar_campos, bg=Cores_Padrao.COR_BOTAO_LIMPAR, width=15).pack(side=tk.LEFT, padx=5)

        frame_tabela = tk.Frame(self.root, padx=20, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_tabela.pack(expand=True, fill="both")

        self.colunas = ("id", "tipo", "origem", "destino", "responsavel", "status", "dataSaida")
        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings")

        self.tree.heading("id", text="ID")
        self.tree.heading("tipo", text="Tipo")
        self.tree.heading("origem", text="Origem")
        self.tree.heading("destino", text="Destino")
        self.tree.heading("responsavel", text="Responsável")
        self.tree.heading("status", text="Status")
        self.tree.heading("dataSaida", text="Data Saída")

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

    def get_movimento_data(self):
        try:
            tipo_selecionado = self.var_tipo_movimento.get()
            origem_selecionada = self.var_origem.get()
            destino_selecionado = self.var_destino.get()
            responsavel_selecionado = self.var_responsavel.get()

            if tipo_selecionado:
                tipo_id = tipo_selecionado.split(' - ')[0]
            else:
                tipo_id = None

            # Verificar se origem está desabilitada
            if self.combo_origem.cget('state') == 'disabled':
                origem_id = None
            elif origem_selecionada:
                origem_id = origem_selecionada.split(' - ')[0]
            else:
                origem_id = None

            # Verificar se destino está desabilitada
            if self.combo_destino.cget('state') == 'disabled':
                destino_id = None
            elif destino_selecionado:
                destino_id = destino_selecionado.split(' - ')[0]
            else:
                destino_id = None

            if responsavel_selecionado:
                responsavel_id = responsavel_selecionado.split(' - ')[0]
            else:
                responsavel_id = None

            return {
                "tipo_movimento": tipo_id,
                "origem": origem_id,
                "destino": destino_id,
                "responsavel": responsavel_id,
                "status": self.var_status.get()
            }
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao obter dados do movimento: {e}")
            return None

    def _acao_adicionar(self):
        self.controller.add_movimento()
        self._acao_listar()

    def _acao_listar(self):
        if self.controller: 
            self.controller.list_movimentos()

    def _acao_atualizar(self):
        self.controller.update_movimento()
        self._acao_listar()

    def _acao_deletar(self):
        if messagebox.askyesno("Confirmação", "Tem certeza que deseja cancelar este movimento?"):
            self.controller.delete_movimento()
            self._acao_listar()
            self._limpar_campos()

    def show_movimentos(self, lista):
        for i in self.tree.get_children(): 
            self.tree.delete(i)
        for idx, m in enumerate(lista):
            tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
            self.tree.insert("", "end", values=(m._id_movimento, m._tipoMovimento, m._origem, m._destino, m._responsavel, m._status, m._dataSaida), tags=(tag,))

    def get_id(self):
        val = self.var_id.get()
        return int(val) if val else None

    def _limpar_campos(self):
        for var in [self.var_id, self.var_tipo_movimento, self.var_origem, self.var_destino, self.var_responsavel, self.var_status]:
            var.set("")
        self._atualizar_campos_disponibilidade()

    def _ao_selecionar_tabela(self, event):
        item_sel = self.tree.selection()
        if item_sel:
            v = self.tree.item(item_sel)['values']
            self.var_id.set(v[0])
            
            # Encontrar e setar tipo de movimento
            for tipo in self.tipos_movimento:
                if str(tipo._id) == str(v[1]):
                    self.var_tipo_movimento.set(f"{tipo._id} - {tipo._tipo}")
                    break
            
            self.var_origem.set(v[2])
            self.var_destino.set(v[3])
            
            # Encontrar e setar responsável
            for func in self.funcionarios:
                if str(func._id) == str(v[4]):
                    self.var_responsavel.set(f"{func._id} - {func._nome}")
                    break
            
            self.var_status.set(v[5])

    def _ao_mudar_tipo_movimento(self, event=None):
        self._atualizar_campos_disponibilidade()

    def _atualizar_campos_disponibilidade(self):
        tipo_selecionado = self.var_tipo_movimento.get()
        if not tipo_selecionado:
            self.combo_origem.config(state="disabled")
            self.combo_destino.config(state="disabled")
            return

        tipo_nome = tipo_selecionado.split(' - ', 1)[1].lower().strip() if ' - ' in tipo_selecionado else ""

        # Saída: apenas origem
        if "saída" in tipo_nome or "saida" in tipo_nome:
            self.combo_origem.config(state="readonly")
            self.combo_destino.config(state="disabled")
            self.var_destino.set("")
        # Entrada: apenas destino
        elif "entrada" in tipo_nome:
            self.combo_origem.config(state="disabled")
            self.combo_destino.config(state="readonly")
            self.var_origem.set("")
        # Interno: ambos
        elif "interno" in tipo_nome:
            self.combo_origem.config(state="readonly")
            self.combo_destino.config(state="readonly")

    def set_tipos_movimento(self, tipos):
        self.tipos_movimento = tipos
        valores = [f"{t._id} - {t._tipo}" for t in tipos]
        self.combo_tipo['values'] = valores

    def set_unidades(self, unidades):
        self.unidades = unidades
        valores = [f"{u._id} - {u._unidade}" for u in unidades]
        self.combo_origem['values'] = valores
        self.combo_destino['values'] = valores

    def set_funcionarios(self, funcionarios):
        self.funcionarios = funcionarios
        valores = [f"{f._id} - {f._nome}" for f in funcionarios]
        self.combo_responsavel['values'] = valores
        if valores:
            self.combo_responsavel.current(0)

    def habilitar_criacao(self, habilitado):
        state = "normal" if habilitado else "disabled"
        self.btn_adicionar.config(state=state)
        self.combo_tipo.config(state="readonly" if habilitado else "disabled")

    def show_message(self, msg): 
        messagebox.showinfo("Sucesso", msg)

    def show_error(self, err): 
        messagebox.showerror("Erro", err)
