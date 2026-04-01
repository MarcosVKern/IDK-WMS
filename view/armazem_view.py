import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from view.cores_padrao import Cores_Padrao
from view.notificacao import Notificacao

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

        # Frame principal contendo os formulários lado a lado
        frame_formularios = tk.Frame(self.root, bg=Cores_Padrao.COR_FUNDO)
        frame_formularios.pack(padx=10, pady=10, fill="both")

        # Frame esquerdo - Detalhes
        frame_form = tk.LabelFrame(frame_formularios, text="Detalhes do Armazém", padx=10, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_form.pack(side="left", fill="both", expand=True, padx=5)

        tk.Label(frame_form, text="ID:", bg=Cores_Padrao.COR_FUNDO).grid(row=0, column=0, sticky="w", pady=5)
        tk.Entry(frame_form, textvariable=self.var_id, state="readonly", width=15, bg=Cores_Padrao.COR_FUNDO).grid(row=1, column=0, pady=5, sticky="w")

        tk.Label(frame_form, text="Nome:", bg=Cores_Padrao.COR_FUNDO).grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(frame_form, textvariable=self.var_nome, width=20).grid(row=3, column=0, pady=5, sticky="ew")

        frame_form.grid_columnconfigure(0, weight=1)

        # Frame direito - Endereço
        frame_endereco = tk.LabelFrame(frame_formularios, text="Endereço", padx=10, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_endereco.pack(side="right", fill="both", expand=True, padx=5)

        # Frame para CEP com link
        frame_cep = tk.Frame(frame_endereco, bg=Cores_Padrao.COR_FUNDO)
        frame_cep.grid(row=0, column=0, columnspan=2, sticky="w", pady=5)

        tk.Label(frame_cep, text="CEP:", bg=Cores_Padrao.COR_FUNDO).pack(side="left", padx=(0, 5))
        tk.Entry(frame_cep, textvariable=self.var_cep, width=15).pack(side="left")

        # Link "Buscar endereço"
        link_buscar = tk.Label(frame_cep, text="Buscar endereço", fg="blue", bg=Cores_Padrao.COR_FUNDO, cursor="hand2", font=("Arial", 9, "underline"))
        link_buscar.pack(side="left", padx=(10, 0))
        link_buscar.bind("<Button-1>", lambda e: self._buscar_endereco_cep())

        tk.Label(frame_endereco, text="Bairro:", bg=Cores_Padrao.COR_FUNDO).grid(row=2, column=0, sticky="w", pady=5)
        tk.Entry(frame_endereco, textvariable=self.var_bairro, width=20).grid(row=3, column=0, pady=5, sticky="ew", padx=(0, 5))

        tk.Label(frame_endereco, text="Cidade:", bg=Cores_Padrao.COR_FUNDO).grid(row=2, column=1, sticky="w", pady=5, padx=(5, 0))
        tk.Entry(frame_endereco, textvariable=self.var_cidade, width=20).grid(row=3, column=1, pady=5, sticky="ew", padx=(5, 0))

        tk.Label(frame_endereco, text="UF:", bg=Cores_Padrao.COR_FUNDO).grid(row=4, column=0, sticky="w", pady=5)
        tk.Entry(frame_endereco, textvariable=self.var_uf, width=20).grid(row=5, column=0, pady=5, sticky="ew", padx=(0, 5))

        tk.Label(frame_endereco, text="País:", bg=Cores_Padrao.COR_FUNDO).grid(row=4, column=1, sticky="w", pady=5, padx=(5, 0))
        tk.Entry(frame_endereco, textvariable=self.var_pais, width=20).grid(row=5, column=1, pady=5, sticky="ew", padx=(5, 0))

        frame_endereco.grid_columnconfigure(0, weight=1)
        frame_endereco.grid_columnconfigure(1, weight=1)

        frame_botoes = tk.Frame(self.root, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_botoes.pack()

        ctk.CTkButton(frame_botoes, text="Adicionar Armazém", command=self._acao_adicionar, 
                        fg_color=Cores_Padrao.COR_BOTAO_SALVAR, 
                        text_color=Cores_Padrao.COR_TEXTO, 
                        hover_color=Cores_Padrao.COR_BOTAO_HOVER, width=150).pack(side=tk.LEFT, padx=5)
        
        ctk.CTkButton(frame_botoes, text="Atualizar Armazém", command=self._acao_atualizar, 
                        fg_color=Cores_Padrao.COR_BOTAO_ATUALIZAR, 
                        text_color=Cores_Padrao.COR_TEXTO, 
                        hover_color=Cores_Padrao.COR_BOTAO_HOVER, width=150).pack(side=tk.LEFT, padx=5)
        
        ctk.CTkButton(frame_botoes, text="Deletar Armazém", command=self._acao_deletar, 
                        fg_color=Cores_Padrao.COR_BOTAO_DELETAR, 
                        text_color=Cores_Padrao.COR_TEXTO, 
                        hover_color=Cores_Padrao.COR_BOTAO_HOVER, width=150).pack(side=tk.LEFT, padx=5)
        
        ctk.CTkButton(frame_botoes, text="Limpar", command=self._limpar_campos, 
                        fg_color=Cores_Padrao.COR_BOTAO_LIMPAR, 
                        text_color=Cores_Padrao.COR_TEXTO, 
                        hover_color=Cores_Padrao.COR_BOTAO_HOVER, width=150).pack(side=tk.LEFT, padx=5)

        frame_tabela = tk.Frame(self.root, padx=20, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_tabela.pack(expand=True, fill="both")

        self.colunas = ("id", "cep", "bairro", "cidade", "uf", "pais", "nome")
        style = ttk.Style()
        style.configure("Pink.Treeview", background=Cores_Padrao.COR_TABLE_BG, fieldbackground=Cores_Padrao.COR_TABLE_BG, foreground=Cores_Padrao.COR_TEXTO)
        self.tree = ttk.Treeview(frame_tabela, columns=self.colunas, show="headings", style="Pink.Treeview")

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
            Notificacao.erro("Erro", f"Erro ao obter dados do armazém: {e}", parent=self.root)
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
        if Notificacao.confirmacao("Confirmação", "Tem certeza que deseja deletar este armazém?", parent=self.root):
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

    def _buscar_endereco_cep(self):
        """Busca endereço usando a API ViaCEP"""
        cep = self.var_cep.get().replace("-", "").replace(" ", "")
        
        if not cep:
            Notificacao.aviso("Aviso", "Por favor, digite um CEP!", parent=self.root)
            return
        
        if len(cep) != 8:
            Notificacao.erro("Erro", "CEP deve ter 8 dígitos!", parent=self.root)
            return
        
        try:
            import requests
            response = requests.get(f"https://viacep.com.br/ws/{cep}/json/")
            
            if response.status_code == 200:
                dados = response.json()
                
                if "erro" in dados:
                    Notificacao.erro("Erro", "CEP não encontrado!", parent=self.root)
                    return
                
                self.var_bairro.set(dados.get("bairro", ""))
                self.var_cidade.set(dados.get("localidade", ""))
                self.var_uf.set(dados.get("uf", ""))
                self.var_pais.set("Brasil")
                
                Notificacao.sucesso("Sucesso", "Endereço preenchido com sucesso!", parent=self.root)
            else:
                Notificacao.erro("Erro", "Erro ao conectar com o serviço de CEP!", parent=self.root)
        except Exception as e:
            Notificacao.erro("Erro", f"Erro ao buscar endereço: {str(e)}", parent=self.root)

    def show_message(self, msg):
        Notificacao.sucesso("Sucesso", msg, parent=self.root)

    def show_error(self, err):
        Notificacao.erro("Erro", err, parent=self.root)