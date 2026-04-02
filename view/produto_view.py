import tkinter as tk
from tkinter import ttk, filedialog
import customtkinter as ctk
from view.cores_padrao import Cores_Padrao
from view.notificacao import Notificacao
import os
import shutil
from datetime import datetime
from PIL import Image
import io


class Produto_View:
    def __init__(self, parent=None):
        self.controller = None
        self.parent = parent
        self.imagem_selecionada = None
        self.foto = None
        self.imagem_pil = None  # Mantém referência da imagem PIL

        if parent is None:
            self.root = tk.Toplevel()
            self.root.title("Gerenciamento de Produtos")
            self.root.geometry("1280x720")
            self.root.state("zoomed")
            self.is_embedded = False
        else:
            self.root = tk.Frame(parent, bg=Cores_Padrao.COR_FUNDO)
            self.is_embedded = True

        self.var_id = tk.StringVar()
        self.var_nome = tk.StringVar()
        self.var_descricao = tk.StringVar()
        self.var_imagem = tk.StringVar()

        self._criar_pasta_imagens()
        self._setup_ui()

    def _setup_ui(self):
        tk.Label(
            self.root,
            text="GERENCIAMENTO DE PRODUTOS",
            font=("Arial", 16, "bold"),
            pady=10,
            bg=Cores_Padrao.COR_FUNDO if self.is_embedded else None,
        ).pack()

        # Frame principal com formulário e preview de imagem
        frame_conteudo = tk.Frame(self.root, bg=Cores_Padrao.COR_FUNDO)
        frame_conteudo.pack(padx=20, pady=5, fill="x")

        frame_form = tk.LabelFrame(
            frame_conteudo,
            text="Detalhes do Produto",
            padx=10,
            pady=10,
            bg=Cores_Padrao.COR_FUNDO,
        )
        frame_form.pack(side="left", fill="both", expand=True, padx=(0, 10))
        frame_form.pack_propagate(False)
        frame_form.configure(width=500)

        tk.Label(frame_form, text="ID:", bg=Cores_Padrao.COR_FUNDO).grid(
            row=0, column=0, sticky="w"
        )
        tk.Entry(
            frame_form,
            textvariable=self.var_id,
            state="readonly",
            width=15,
            bg=Cores_Padrao.COR_INPUT_BG,
            fg=Cores_Padrao.COR_INPUT_FG,
            readonlybackground=Cores_Padrao.COR_INPUT_BG,
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")

        tk.Label(frame_form, text="Nome:", bg=Cores_Padrao.COR_FUNDO).grid(
            row=2, column=0, sticky="w"
        )
        tk.Entry(
            frame_form,
            textvariable=self.var_nome,
            width=30,
            bg=Cores_Padrao.COR_INPUT_BG,
            fg=Cores_Padrao.COR_INPUT_FG,
        ).grid(row=3,column=0, pady=5)

        tk.Label(frame_form, text="Descrição:", bg=Cores_Padrao.COR_FUNDO).grid(
            row=4, column=0, sticky="w"
        )
        tk.Entry(
            frame_form,
            textvariable=self.var_descricao,
            width=30,
            bg=Cores_Padrao.COR_INPUT_BG,
            fg=Cores_Padrao.COR_INPUT_FG,
        ).grid(row=5, column=0, pady=5)

        tk.Label(frame_form, text="Imagem:", bg=Cores_Padrao.COR_FUNDO).grid(
            row=6, column=0, sticky="w"
        )
        
        frame_imagem = tk.Frame(frame_form, bg=Cores_Padrao.COR_FUNDO)
        frame_imagem.grid(row=7, column=0, pady=5, sticky="ew")

        ctk.CTkButton(
            frame_imagem,
            text="Selecionar Imagem",
            command=self._selecionar_imagem,
            fg_color=Cores_Padrao.COR_BOTAO_ATUALIZAR,
            hover_color=Cores_Padrao.COR_BOTAO_ATUALIZAR_HOVER,
            text_color=Cores_Padrao.COR_TEXTO_BOTAO,
            width=150,
        ).pack(side="left", padx=5)

        self.label_imagem_selecionada = tk.Label(
            frame_imagem, 
            text="Nenhuma imagem selecionada", 
            bg=Cores_Padrao.COR_FUNDO,
            fg=Cores_Padrao.COR_TEXTO,
            font=("Arial", 9)
        )
        self.label_imagem_selecionada.pack(side="left", padx=10)

        # Frame de visualização de imagem
        frame_preview = ctk.CTkFrame(
            frame_conteudo,
            fg_color=Cores_Padrao.COR_FUNDO,
            border_width=2,
            border_color=Cores_Padrao.COR_TABLE_BG,
        )
        frame_preview.pack(side="right", fill="both", expand=True, padx=(10, 0))
        frame_preview.pack_propagate(False)
        frame_preview.configure(width=350, height=300)

        # Título do preview
        ctk.CTkLabel(
            frame_preview,
            text="Preview da Imagem",
            text_color=Cores_Padrao.COR_TEXTO,
            font=("Arial", 12, "bold"),
            bg_color=Cores_Padrao.COR_FUNDO,
        ).pack(pady=10)

        # Label para exibir a imagem com CTkLabel
        self.label_preview_imagem = ctk.CTkLabel(
            frame_preview,
            text="Nenhuma imagem",
            text_color=Cores_Padrao.COR_TEXTO,
            bg_color=Cores_Padrao.COR_TABLE_BG,
            fg_color=Cores_Padrao.COR_TABLE_BG,
            font=("Arial", 10),
            wraplength=300,
            image=None,
        )
        self.label_preview_imagem.pack(fill="both", expand=True, padx=10, pady=10)

        frame_botoes = tk.Frame(
            self.root, pady=10, bg=Cores_Padrao.COR_FUNDO if self.is_embedded else None
        )
        frame_botoes.pack()

        ctk.CTkButton(
            frame_botoes,
            text="Adicionar Produto",
            command=self._acao_adicionar,
            fg_color=Cores_Padrao.COR_BOTAO_SALVAR,
            hover_color=Cores_Padrao.COR_BOTAO_SALVAR_HOVER,
            text_color=Cores_Padrao.COR_TEXTO_BOTAO,
            width=150,
        ).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(
            frame_botoes,
            text="Atualizar Produto",
            command=self._acao_atualizar,
            fg_color=Cores_Padrao.COR_BOTAO_ATUALIZAR,
            hover_color=Cores_Padrao.COR_BOTAO_ATUALIZAR_HOVER,
            text_color=Cores_Padrao.COR_TEXTO_BOTAO,
            width=150,
        ).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(
            frame_botoes,
            text="Deletar Produto",
            command=self._acao_deletar,
            fg_color=Cores_Padrao.COR_BOTAO_DELETAR,
            hover_color=Cores_Padrao.COR_BOTAO_DELETAR_HOVER,
            text_color=Cores_Padrao.COR_TEXTO_BOTAO,
            width=150,
        ).pack(side=tk.LEFT, padx=5)
        ctk.CTkButton(
            frame_botoes,
            text="Limpar",
            command=self._limpar_campos,
            fg_color=Cores_Padrao.COR_BOTAO_LIMPAR,
            hover_color=Cores_Padrao.COR_BOTAO_LIMPAR_HOVER,
            text_color=Cores_Padrao.COR_TEXTO,
            width=150,
        ).pack(side=tk.LEFT, padx=5)

        frame_tabela = tk.Frame(self.root, padx=20, pady=10, bg=Cores_Padrao.COR_FUNDO)
        frame_tabela.pack(expand=True, fill="both")

        self.colunas = ("id", "nome", "descricao", "imagem")
        style = ttk.Style()
        style.configure(
            "Pink.Treeview",
            background=Cores_Padrao.COR_TABLE_BG,
            fieldbackground=Cores_Padrao.COR_TABLE_BG,
            foreground=Cores_Padrao.COR_TEXTO,
        )
        self.tree = ttk.Treeview(
            frame_tabela, columns=self.colunas, show="headings", style="Pink.Treeview"
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("nome", text="Nome")
        self.tree.heading("descricao", text="Descrição")
        self.tree.heading("imagem", text="URL da Imagem")

        for col in self.colunas:
            self.tree.column(col, anchor="center")

        self.tree.pack(side="left", expand=True, fill="both")
        self.tree.bind("<<TreeviewSelect>>", self._ao_selecionar_tabela)

        # Configurar efeito zebrado
        self.tree.tag_configure("evenrow", background=Cores_Padrao.COR_ZEBRADO_PAR)
        self.tree.tag_configure("oddrow", background=Cores_Padrao.COR_ZEBRADO_IMPAR)

    def _criar_pasta_imagens(self):
        """Cria a estrutura de pastas para armazenar imagens"""
        pasta = "imagens/produtos"
        caminho_absoluto = self._get_caminho_absoluto(pasta)
        if not os.path.exists(caminho_absoluto):
            os.makedirs(caminho_absoluto)

    def _get_caminho_absoluto(self, caminho_relativo):
        """Converte caminho relativo para caminho absoluto baseado no diretório raiz do projeto"""
        # Obtém o diretório do arquivo main.py (raiz do projeto)
        diretorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Se o caminho já é absoluto, retorna como está
        if os.path.isabs(caminho_relativo):
            return caminho_relativo
        
        # Constrói o caminho absoluto
        caminho_absoluto = os.path.join(diretorio_raiz, caminho_relativo)
        return os.path.abspath(caminho_absoluto)

    def _exibir_imagem(self, caminho_imagem):
        """Exibe a imagem no preview com redimensionamento automático"""
        try:
            if not caminho_imagem:
                # Limpa referências PRIMEIRO para evitar conflitos
                self.foto = None
                self.imagem_pil = None
                self.label_preview_imagem.configure(text="Nenhuma imagem")
                return
            
            # Obtém o caminho absoluto
            caminho_absoluto = self._get_caminho_absoluto(caminho_imagem)
            
            # Verifica se o arquivo existe
            if not os.path.exists(caminho_absoluto):
                # Limpa referências PRIMEIRO
                self.foto = None
                self.imagem_pil = None
                self.label_preview_imagem.configure(text="Imagem não encontrada")
                return
            
            # Carrega a imagem com PIL e mantém referência
            self.imagem_pil = Image.open(caminho_absoluto)
            
            # Redimensiona mantendo proporção
            self.imagem_pil.thumbnail((300, 250), Image.Resampling.LANCZOS)
            
            # Cria CTkImage e armazena a referência para evitar garbage collection
            self.foto = ctk.CTkImage(light_image=self.imagem_pil, size=(self.imagem_pil.width, self.imagem_pil.height))
            
            # Configura o label com a imagem (sem texto quando há imagem)
            self.label_preview_imagem.configure(image=self.foto, text="")
            
        except Exception as e:
            print(f"Erro ao carregar imagem: {str(e)}")
            # Limpa referências PRIMEIRO para evitar conflitos
            self.foto = None
            self.imagem_pil = None
            self.label_preview_imagem.configure(text="Erro ao carregar")
            self.foto = None
            self.imagem_pil = None

    def _resetar_preview(self):
        """Reseta o preview da imagem para estado original"""
        # Limpa referências PRIMEIRO para evitar conflitos
        self.foto = None
        self.imagem_pil = None
        self.label_preview_imagem.configure(text="Nenhuma imagem")

    def _selecionar_imagem(self):
        """Abre diálogo para selecionar imagem PNG ou JPG"""
        arquivo = filedialog.askopenfilename(
            title="Selecionar Imagem",
            filetypes=[("Imagens", "*.png *.jpg *.jpeg"), ("PNG", "*.png"), ("JPG", "*.jpg *.jpeg"), ("Todos", "*.*")],
            parent=self.root
        )
        
        if arquivo:
            try:
                # Verifica extensão
                extensao = os.path.splitext(arquivo)[1].lower()
                if extensao not in ['.png', '.jpg', '.jpeg']:
                    Notificacao.erro("Erro", "Apenas arquivos PNG e JPG são aceitos!", parent=self.root)
                    self._resetar_preview()
                    self.imagem_selecionada = None
                    self.label_imagem_selecionada.config(text="Nenhuma imagem selecionada")
                    self.var_imagem.set("")
                    return
                
                # Cria nome único com timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
                nome_arquivo = timestamp + os.path.basename(arquivo)
                
                # Caminho de destino (relativo)
                pasta_destino = os.path.join("imagens", "produtos")
                caminho_destino = os.path.join(pasta_destino, nome_arquivo)
                
                # Obtém caminho absoluto para copiar o arquivo
                caminho_absoluto = self._get_caminho_absoluto(caminho_destino)
                
                # Copia o arquivo
                shutil.copy2(arquivo, caminho_absoluto)
                
                # Armazena o caminho relativo
                self.imagem_selecionada = caminho_destino
                self.var_imagem.set(caminho_destino)
                self.label_imagem_selecionada.config(text=f"✓ {nome_arquivo}")
                
                # Exibe a imagem no preview
                self._exibir_imagem(caminho_destino)
                
                Notificacao.sucesso("Sucesso", "Imagem selecionada com sucesso!", parent=self.root)
            except Exception as e:
                Notificacao.erro("Erro", f"Erro ao copiar imagem: {str(e)}", parent=self.root)
                self._resetar_preview()
                self.imagem_selecionada = None
                self.label_imagem_selecionada.config(text="Nenhuma imagem selecionada")
                self.var_imagem.set("")
        else:
            # Usuário cancelou a seleção
            self._resetar_preview()
            self.imagem_selecionada = None
            self.label_imagem_selecionada.config(text="Nenhuma imagem selecionada")
            self.var_imagem.set("")

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
                "imagem": self.var_imagem.get(),
            }
        except Exception as e:
            Notificacao.erro(
                "Erro", f"Erro ao obter dados do produto: {e}", parent=self.root
            )
            return None

    def _acao_adicionar(self):
        self.controller.add_produto()
        self._acao_listar()

    def _acao_listar(self):
        if self.controller:
            self.controller.list_produtos()

    def show_produtos(self, lista):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for idx, p in enumerate(lista):
            tag = "evenrow" if idx % 2 == 0 else "oddrow"
            self.tree.insert(
                "", "end", values=(p._id, p._nome, p._descricao, p._imagem), tags=(tag,)
            )

    def _acao_atualizar(self):
        self.controller.update_produto()
        self._acao_listar()

    def get_id(self):
        val = self.var_id.get()
        return int(val) if val else None

    def _acao_deletar(self):
        if Notificacao.confirmacao(
            "Confirmação",
            "Tem certeza que deseja deletar este produto?",
            parent=self.root,
        ):
            self.controller.delete_produto()
            self._acao_listar()
            self._limpar_campos()

    def _limpar_campos(self):
        for val in [self.var_id, self.var_nome, self.var_descricao, self.var_imagem]:
            val.set("")
        self.imagem_selecionada = None
        self.label_imagem_selecionada.config(text="Nenhuma imagem selecionada")
        self._resetar_preview()

    def _ao_selecionar_tabela(self, event):
        item_sel = self.tree.selection()
        if item_sel:
            v = self.tree.item(item_sel)["values"]
            self.var_id.set(v[0])
            self.var_nome.set(v[1])
            self.var_descricao.set(v[2])
            self.var_imagem.set(v[3])
            
            # Reseta o status de seleção (sem nova imagem)
            self.imagem_selecionada = None
            self.label_imagem_selecionada.config(text="Nenhuma imagem selecionada")
            
            # Exibe a imagem do produto
            if v[3]:  # Se houver imagem
                self._exibir_imagem(v[3])
            else:
                self._resetar_preview()

    def show_message(self, msg):
        Notificacao.sucesso("Sucesso", msg, parent=self.root)

    def show_error(self, err):
        Notificacao.erro("Erro", err, parent=self.root)
