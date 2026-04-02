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
        self.pasta_imagens = os.path.join("imagens", "produtos")  # Pasta dinâmica

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
            pady=5,
            bg=Cores_Padrao.COR_FUNDO,
        )
        frame_form.pack(side="left", fill="both", expand=True, padx=(0, 10))
        frame_form.pack_propagate(False)
        frame_form.configure(width=500)

        tk.Label(frame_form, text="ID:", bg=Cores_Padrao.COR_FUNDO).grid(
            row=0, column=0, sticky="w", pady=(0, 2)
        )
        tk.Entry(
            frame_form,
            textvariable=self.var_id,
            state="readonly",
            width=15,
            bg=Cores_Padrao.COR_INPUT_BG,
            fg=Cores_Padrao.COR_INPUT_FG,
            readonlybackground=Cores_Padrao.COR_INPUT_BG,
        ).grid(row=1, column=0, padx=5, pady=(0, 10), sticky="w")

        tk.Label(frame_form, text="Nome:", bg=Cores_Padrao.COR_FUNDO).grid(
            row=2, column=0, sticky="w", pady=(0, 2)
        )
        tk.Entry(
            frame_form,
            textvariable=self.var_nome,
            width=30,
            bg=Cores_Padrao.COR_INPUT_BG,
            fg=Cores_Padrao.COR_INPUT_FG,
        ).grid(row=3, column=0, padx=5, pady=(0, 10), sticky="w")

        tk.Label(frame_form, text="Descrição:", bg=Cores_Padrao.COR_FUNDO).grid(
            row=4, column=0, sticky="w", pady=(0, 2)
        )
        tk.Entry(
            frame_form,
            textvariable=self.var_descricao,
            width=30,
            bg=Cores_Padrao.COR_INPUT_BG,
            fg=Cores_Padrao.COR_INPUT_FG,
        ).grid(row=5, column=0, padx=5, pady=(0, 10), sticky="w")

        tk.Label(frame_form, text="Imagem:", bg=Cores_Padrao.COR_FUNDO).grid(
            row=6, column=0, sticky="w", pady=(0, 2)
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
        """Cria a estrutura de pastas para armazenar imagens e placeholder"""
        pasta = "imagens/produtos"
        caminho_absoluto = self._get_caminho_absoluto(pasta)
        if not os.path.exists(caminho_absoluto):
            os.makedirs(caminho_absoluto)
        
        # Criar placeholder.png se não existir
        placeholder_path = os.path.join(caminho_absoluto, "placeholder.png")
        if not os.path.exists(placeholder_path):
            try:
                # Criar imagem placeholder cinza
                img = Image.new('RGB', (300, 250), color=(200, 200, 200))
                img.save(placeholder_path)
            except Exception as e:
                print(f"Erro ao criar placeholder: {str(e)}")

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
    
    def _get_pasta_imagens_absoluta(self):
        """Retorna o caminho absoluto da pasta de imagens"""
        return self._get_caminho_absoluto(self.pasta_imagens)

    def _exibir_imagem(self, nome_arquivo):
        """Exibe a imagem no preview com redimensionamento automático. Recebe apenas o NOME do arquivo"""
        try:
            if not nome_arquivo:
                # Sem imagem, tenta carregar placeholder
                placeholder_path = os.path.join(self._get_pasta_imagens_absoluta(), "placeholder.png")
                
                if os.path.exists(placeholder_path):
                    self.imagem_pil = Image.open(placeholder_path)
                    self.imagem_pil.thumbnail((300, 250), Image.Resampling.LANCZOS)
                    self.foto = ctk.CTkImage(light_image=self.imagem_pil, size=(self.imagem_pil.width, self.imagem_pil.height))
                    self.label_preview_imagem.configure(image=self.foto, text="")
                else:
                    # Sem placeholder, mostra mensagem
                    self.foto = None
                    self.imagem_pil = None
                    self.label_preview_imagem.configure(text="Nenhuma imagem")
                return
            
            # Constrói caminho absoluto: pasta_imagens + nome_arquivo
            caminho_absoluto = os.path.join(self._get_pasta_imagens_absoluta(), nome_arquivo)
            
            # Verifica se o arquivo existe
            if not os.path.exists(caminho_absoluto):
                # Arquivo não encontrado, usa placeholder
                placeholder_path = os.path.join(self._get_pasta_imagens_absoluta(), "placeholder.png")
                
                if os.path.exists(placeholder_path):
                    # Carrega placeholder com PIL
                    self.imagem_pil = Image.open(placeholder_path)
                    self.imagem_pil.thumbnail((300, 250), Image.Resampling.LANCZOS)
                    self.foto = ctk.CTkImage(light_image=self.imagem_pil, size=(self.imagem_pil.width, self.imagem_pil.height))
                    self.label_preview_imagem.configure(image=self.foto, text="")
                    return
                else:
                    # Sem placeholder, mostra mensagem
                    self.foto = None
                    self.imagem_pil = None
                    self.label_preview_imagem.configure(text="Arquivo não encontrado")
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
            # Tenta carregar placeholder em caso de erro
            try:
                placeholder_path = os.path.join(self._get_pasta_imagens_absoluta(), "placeholder.png")
                if os.path.exists(placeholder_path):
                    self.imagem_pil = Image.open(placeholder_path)
                    self.imagem_pil.thumbnail((300, 250), Image.Resampling.LANCZOS)
                    self.foto = ctk.CTkImage(light_image=self.imagem_pil, size=(self.imagem_pil.width, self.imagem_pil.height))
                    self.label_preview_imagem.configure(image=self.foto, text="")
                    return
            except:
                pass
            
            # Limpa referências
            self.foto = None
            self.imagem_pil = None
            self.label_preview_imagem.configure(text="Erro ao carregar")

    def _resetar_preview(self):
        """Reseta o preview da imagem para estado original"""
        # Limpa referências PRIMEIRO para evitar conflitos
        self.foto = None
        self.imagem_pil = None
        self.label_preview_imagem.configure(text="Nenhuma imagem")

    def _selecionar_imagem(self):
        """Abre diálogo para selecionar imagem PNG ou JPG - NÃO copia até salvar"""
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
                    # Restaura preview anterior
                    imagem_atual = self.var_imagem.get()
                    if imagem_atual:
                        self._exibir_imagem(imagem_atual)
                        self.label_imagem_selecionada.config(text=f"Atual: {os.path.basename(imagem_atual)}")
                    else:
                        self._resetar_preview()
                        self.label_imagem_selecionada.config(text="Nenhuma imagem")
                    self.imagem_selecionada = None
                    return
                
                # APENAS armazena o caminho do arquivo selecionado (NÃO copia)
                self.imagem_selecionada = arquivo
                nome_selecionado = os.path.basename(arquivo)
                self.label_imagem_selecionada.config(text=f"📋 {nome_selecionado} (salve p/ confirmar)")
                
                # Exibe preview da imagem selecionada
                self._exibir_imagem_temporaria(arquivo)
                
                Notificacao.sucesso("Sucesso", "Imagem selecionada. Clique em 'Adicionar' ou 'Atualizar' para salvar!", parent=self.root)
            except Exception as e:
                Notificacao.erro("Erro", f"Erro ao processar imagem: {str(e)}", parent=self.root)
                # Restaura preview anterior
                imagem_atual = self.var_imagem.get()
                if imagem_atual:
                    self._exibir_imagem(imagem_atual)
                    self.label_imagem_selecionada.config(text=f"Atual: {os.path.basename(imagem_atual)}")
                else:
                    self._resetar_preview()
                    self.label_imagem_selecionada.config(text="Nenhuma imagem")
                self.imagem_selecionada = None
        else:
            # Usuário cancelou
            imagem_atual = self.var_imagem.get()
            if imagem_atual:
                self._exibir_imagem(imagem_atual)
                self.label_imagem_selecionada.config(text=f"Atual: {os.path.basename(imagem_atual)}")
            else:
                self._resetar_preview()
                self.label_imagem_selecionada.config(text="Nenhuma imagem")
            self.imagem_selecionada = None

    def display(self):
        """Exibir quando embutido em um frame"""
        self.root.pack(fill="both", expand=True)
        self.root.after(200, self._acao_listar)

    def run(self):
        """Executar como janela separada"""
        self.root.after(200, self._acao_listar)
        self.root.grab_set()
        self.root.mainloop()

    def _copiar_imagem_selecionada(self):
        """Copia a imagem selecionada para a pasta de produtos. Salva APENAS o NOME no banco"""
        if not self.imagem_selecionada:
            return  # Sem nova imagem, mantém a anterior
        
        try:
            # Cria nome único com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_")
            nome_arquivo = timestamp + os.path.basename(self.imagem_selecionada)
            
            # Caminho absoluto de destino na pasta de imagens
            pasta_destino = self._get_pasta_imagens_absoluta()
            caminho_absoluto = os.path.join(pasta_destino, nome_arquivo)
            
            # Copia o arquivo
            shutil.copy2(self.imagem_selecionada, caminho_absoluto)
            
            # Salva APENAS o NOME do arquivo (não o caminho) no var_imagem
            self.var_imagem.set(nome_arquivo)
            
            # Reseta indicador
            self.imagem_selecionada = None
            
            return nome_arquivo
        except Exception as e:
            Notificacao.erro("Erro", f"Erro ao salvar imagem: {str(e)}", parent=self.root)
            raise
    
    def _validar_e_usar_placeholder(self):
        """Valida a imagem salva. Se não existir, usa placeholder. Trabalha apenas com NOMES de arquivo"""
        nome_arquivo = self.var_imagem.get()
        
        if not nome_arquivo:
            return  # Sem imagem
        
        # Constrói caminho absoluto: pasta + nome
        caminho_arquivo = os.path.join(self._get_pasta_imagens_absoluta(), nome_arquivo)
        
        # Se arquivo não existe, usa placeholder
        if not os.path.exists(caminho_arquivo):
            self.var_imagem.set("placeholder.png")
    
    def _exibir_imagem_temporaria(self, caminho_arquivo):
        """Exibe preview de um arquivo que ainda não foi copiado"""
        try:
            if not os.path.exists(caminho_arquivo):
                self.foto = None
                self.imagem_pil = None
                self.label_preview_imagem.configure(text="Arquivo não existe")
                return
            
            self.imagem_pil = Image.open(caminho_arquivo)
            self.imagem_pil.thumbnail((300, 250), Image.Resampling.LANCZOS)
            self.foto = ctk.CTkImage(light_image=self.imagem_pil, size=(self.imagem_pil.width, self.imagem_pil.height))
            self.label_preview_imagem.configure(image=self.foto, text="")
        except Exception as e:
            print(f"Erro ao exibir preview: {str(e)}")
            self.foto = None
            self.imagem_pil = None
            self.label_preview_imagem.configure(text="Erro ao carregar")

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
        # Copia imagem selecionada antes de adicionar
        try:
            self._copiar_imagem_selecionada()
            self._validar_e_usar_placeholder()
        except:
            return  # Erro ao salvar imagem
        
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
        # Copia imagem selecionada antes de atualizar
        try:
            self._copiar_imagem_selecionada()
            self._validar_e_usar_placeholder()
        except:
            return  # Erro ao salvar imagem
        
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
            
            # Reseta o indicador de nova seleção
            self.imagem_selecionada = None
            
            # Atualiza label com imagem atual
            if v[3]:  # Se houver imagem (apenas NOME do arquivo)
                nome_arquivo = v[3]  # v[3] já é apenas o nome
                self.label_imagem_selecionada.config(text=f"Atual: {nome_arquivo}")
                self._exibir_imagem(nome_arquivo)  # Passa apenas o nome
            else:
                self.label_imagem_selecionada.config(text="Nenhuma imagem")
                self._resetar_preview()

    def show_message(self, msg):
        Notificacao.sucesso("Sucesso", msg, parent=self.root)

    def show_error(self, err):
        Notificacao.erro("Erro", err, parent=self.root)
