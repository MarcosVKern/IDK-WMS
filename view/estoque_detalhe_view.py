import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
from PIL import Image
import os
from view.cores_padrao import Cores_Padrao
from view.notificacao import Notificacao


class EstoqueDetalhe_View:
    def __init__(self, estoque_info, produto_info=None, parent=None):
        """
        estoque_info: dict com {quantidade, nome_produto, id_produto, unidade, id_unidade, nome_armazem, id_armazem}
        produto_info: dict com {nome, descricao, imagem}
        parent: parent window para Toplevel
        """
        self.estoque_info = estoque_info
        self.produto_info = produto_info or {}
        self.parent = parent

        self.pasta_imagens = "imagens/produtos"
        self.foto = None
        self.imagem_pil = None

        if parent is None:
            self.root = tk.Toplevel()
            self.root.title(f"Detalhes do Estoque - {estoque_info['nome_produto']}")
            self.root.geometry("700x500")
            self.root.configure(bg=Cores_Padrao.COR_FUNDO)
            self.root.grab_set()
        else:
            self.root = tk.Frame(parent, bg=Cores_Padrao.COR_FUNDO)

        self._setup_ui()

    def _get_caminho_absoluto(self, caminho_relativo):
        """Converte caminho relativo para caminho absoluto baseado no diretório raiz do projeto"""
        diretorio_raiz = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        if os.path.isabs(caminho_relativo):
            return caminho_relativo

        caminho_absoluto = os.path.join(diretorio_raiz, caminho_relativo)
        return os.path.abspath(caminho_absoluto)

    def _get_pasta_imagens_absoluta(self):
        return self._get_caminho_absoluto(self.pasta_imagens)

    def _carregar_placeholder(self):
        """Carrega e exibe a imagem placeholder"""
        placeholder_path = os.path.join(
            self._get_pasta_imagens_absoluta(), "placeholder.png"
        )
        if os.path.exists(placeholder_path):
            try:
                self.imagem_pil = Image.open(placeholder_path)
                self.imagem_pil.thumbnail((300, 250), Image.Resampling.LANCZOS)
                self.foto = ctk.CTkImage(
                    light_image=self.imagem_pil,
                    size=(self.imagem_pil.width, self.imagem_pil.height),
                )
                self.label_imagem.configure(image=self.foto, text="")
                return True
            except Exception as e:
                print(f"Erro ao carregar placeholder: {str(e)}")
        return False

    def _exibir_imagem(self, nome_arquivo):
        """Exibe a imagem no preview. Se não encontrada, usa placeholder"""
        try:
            if not nome_arquivo:
                if not self._carregar_placeholder():
                    self.foto = None
                    self.imagem_pil = None
                    self.label_imagem.configure(text="Nenhuma imagem")
                return

            caminho_absoluto = os.path.join(
                self._get_pasta_imagens_absoluta(), nome_arquivo
            )

            if not os.path.exists(caminho_absoluto):
                if not self._carregar_placeholder():
                    self.foto = None
                    self.imagem_pil = None
                    self.label_imagem.configure(text="Arquivo não encontrado")
                return

            self.imagem_pil = Image.open(caminho_absoluto)
            self.imagem_pil.thumbnail((300, 250), Image.Resampling.LANCZOS)
            self.foto = ctk.CTkImage(
                light_image=self.imagem_pil,
                size=(self.imagem_pil.width, self.imagem_pil.height),
            )
            self.label_imagem.configure(image=self.foto, text="")

        except Exception as e:
            print(f"Erro ao carregar imagem: {str(e)}")
            if not self._carregar_placeholder():
                self.foto = None
                self.imagem_pil = None
                self.label_imagem.configure(text="Erro ao carregar")

    def _setup_ui(self):
        """Cria a interface de detalhes"""
        try:
            # Título
            tk.Label(
                self.root,
                text=f"Detalhes do Estoque",
                font=("Arial", 14, "bold"),
                pady=10,
                bg=Cores_Padrao.COR_FUNDO,
            ).pack(fill="x")

            # Frame principal com info e imagem
            frame_conteudo = tk.Frame(self.root, bg=Cores_Padrao.COR_FUNDO)
            frame_conteudo.pack(fill="both", expand=True, padx=15, pady=10)
            frame_info = tk.LabelFrame(
                frame_conteudo,
                text="Informações do Estoque",
                padx=15,
                pady=15,
                bg=Cores_Padrao.COR_FUNDO,
            )
            frame_info.pack(side="left", fill="both", expand=True, padx=(0, 10))

            # Produto
            tk.Label(
                frame_info,
                text="Produto:",
                font=("Arial", 10, "bold"),
                bg=Cores_Padrao.COR_FUNDO,
            ).grid(row=0, column=0, sticky="w", pady=5)
            tk.Label(
                frame_info,
                text=self.estoque_info["nome_produto"],
                font=("Arial", 10),
                bg=Cores_Padrao.COR_FUNDO,
            ).grid(row=0, column=1, sticky="w", pady=5, padx=10)

            # Descrição (se disponível)
            if self.produto_info.get("descricao"):
                tk.Label(
                    frame_info,
                    text="Descrição:",
                    font=("Arial", 10, "bold"),
                    bg=Cores_Padrao.COR_FUNDO,
                ).grid(row=1, column=0, sticky="nw", pady=5)
                frame_desc = tk.Frame(frame_info, bg=Cores_Padrao.COR_FUNDO)
                frame_desc.grid(row=1, column=1, sticky="nw", pady=5, padx=10)

                text_desc = tk.Text(
                    frame_desc,
                    height=4,
                    width=30,
                    wrap=tk.WORD,
                    bg=Cores_Padrao.COR_INPUT_BG,
                    fg=Cores_Padrao.COR_TEXTO,
                )
                text_desc.pack()
                text_desc.insert(1.0, self.produto_info.get("descricao", ""))
                text_desc.config(state="disabled")

                row_offset = 2
            else:
                row_offset = 1

            # Quantidade
            tk.Label(
                frame_info,
                text="Quantidade:",
                font=("Arial", 10, "bold"),
                bg=Cores_Padrao.COR_FUNDO,
            ).grid(row=row_offset, column=0, sticky="w", pady=5)
            tk.Label(
                frame_info,
                text=str(self.estoque_info["quantidade"]),
                font=("Arial", 10),
                bg=Cores_Padrao.COR_FUNDO,
            ).grid(row=row_offset, column=1, sticky="w", pady=5, padx=10)

            # Unidade de Armazenamento
            tk.Label(
                frame_info,
                text="Unidade:",
                font=("Arial", 10, "bold"),
                bg=Cores_Padrao.COR_FUNDO,
            ).grid(row=row_offset + 1, column=0, sticky="w", pady=5)
            tk.Label(
                frame_info,
                text=self.estoque_info["unidade"],
                font=("Arial", 10),
                bg=Cores_Padrao.COR_FUNDO,
            ).grid(row=row_offset + 1, column=1, sticky="w", pady=5, padx=10)

            # Armazém
            tk.Label(
                frame_info,
                text="Armazém:",
                font=("Arial", 10, "bold"),
                bg=Cores_Padrao.COR_FUNDO,
            ).grid(row=row_offset + 2, column=0, sticky="w", pady=5)
            tk.Label(
                frame_info,
                text=self.estoque_info["nome_armazem"],
                font=("Arial", 10),
                bg=Cores_Padrao.COR_FUNDO,
            ).grid(row=row_offset + 2, column=1, sticky="w", pady=5, padx=10)

            # Frame direito - Imagem
            frame_imagem = tk.LabelFrame(
                frame_conteudo,
                text="Imagem do Produto",
                padx=10,
                pady=10,
                bg=Cores_Padrao.COR_FUNDO,
                width=350,
                height=300,
            )
            frame_imagem.pack(side="right", fill="both", padx=(10, 0))
            frame_imagem.pack_propagate(False)

            self.label_imagem = ctk.CTkLabel(
                frame_imagem,
                text="Carregando imagem...",
                bg_color=Cores_Padrao.COR_FUNDO,
                text_color=Cores_Padrao.COR_TEXTO,
            )
            self.label_imagem.pack(fill="both", expand=True)

            # Carregar imagem do produto
            nome_imagem = self.produto_info.get("imagem") or ""
            self._exibir_imagem(nome_imagem)

            # Frame botões
            frame_botoes = tk.Frame(self.root, pady=10, bg=Cores_Padrao.COR_FUNDO)
            frame_botoes.pack()

            ctk.CTkButton(
                frame_botoes,
                text="Fechar",
                command=self._acao_fechar,
                fg_color=Cores_Padrao.COR_BOTAO_LIMPAR,
                hover_color=Cores_Padrao.COR_BOTAO_LIMPAR_HOVER,
                text_color=Cores_Padrao.COR_TEXTO,
                width=150,
            ).pack()
            
        except Exception as e:
            pass

    def _acao_fechar(self):
        """Fecha a janela de detalhes"""
        if isinstance(self.root, tk.Toplevel):
            self.root.destroy()
        else:
            self.root.pack_forget()

    def display(self):
        """Exibir quando embutido em um frame"""
        self.root.pack(fill="both", expand=True)

    def run(self):
        """Executar como janela separada"""
        if isinstance(self.root, tk.Toplevel):
            self.root.mainloop()
        else:
            self.display()
