from logging import root

import customtkinter as ctk
from view.cores_padrao import Cores_Padrao
import tkinter as tk
from tkinter import ttk

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class Main_View:
    def __init__(self):
        self.controller = None
        self.root = ctk.CTk()
        self.root.title("Sistema IDK WMS")
        self.root.geometry("1920x1080")
        self.root.state('zoomed')
        
        # Maximizar a janela após criar
        self.root.after(100, self._maximize_window)
        
        self.main_container = ctk.CTkFrame(self.root, fg_color=Cores_Padrao.COR_FUNDO_MENU)
        self.main_container.pack(fill="both", expand=True)
        
        self.right_panel = ctk.CTkFrame(
            self.main_container,
            fg_color=Cores_Padrao.COR_FUNDO,
        )
        self.right_panel.pack(fill="both", expand=True, padx=10, pady=10)

        self.right_panel_label = ctk.CTkLabel(
            self.right_panel,
            text="",
            font=("Arial", 14, "bold"),
            text_color=Cores_Padrao.COR_TEXTO_MENU_ESCURO,
            anchor="w"
        )
        self.right_panel_label.pack(fill="x", padx=10, pady=(10, 0))

        self.right_panel_content = ctk.CTkFrame(self.right_panel, fg_color=Cores_Padrao.COR_FUNDO, border_width=0)
        self.right_panel_content.pack(expand=True, fill="both", padx=10, pady=10)

        self.current_frame = None
        self.usuario = None

        self._setup_initial_content()

        #Pink treeview style
        root = self.root
        root.title("Pink.TreeView")
        
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Pink.Treeview", 
            background=Cores_Padrao.COR_TABLE_BG, 
            fieldbackground=Cores_Padrao.COR_TABLE_BG, 
            foreground=Cores_Padrao.COR_TABLE_FG,
            rowheight=25
        )

        style.configure("TCombobox", 
                fieldbackground=Cores_Padrao.COR_FUNDO,    # Cor de fundo do campo
                background=Cores_Padrao.COR_INPUT_BG,    # Cor da área da seta
                foreground=Cores_Padrao.COR_TEXTO   # Cor texto
        )

        style.map('TCombobox',
          fieldbackground=[('readonly', Cores_Padrao.COR_FUNDO)],
          selectbackground=[('readonly', Cores_Padrao.COR_BOTAO_HOVER)],
          selectforeground=[('readonly', Cores_Padrao.COR_FUNDO)]
        )

        style.map('Pink.Treeview', background=[('selected', Cores_Padrao.COR_BOTAO_HOVER)])

        style.configure("Pink.Treeview.Heading",
            background=Cores_Padrao.COR_INPUT_BG,
            foreground=Cores_Padrao.COR_TEXTO,
            relief="flat"
        )


    def _setup_menu(self):
        self.menu_buttons = {}

        titulo = ctk.CTkLabel(
            self.left_panel,
            text="Menu Principal",
            font=("Arial", 16, "bold"),
            text_color=Cores_Padrao.COR_TEXTO_MENU
        )
        titulo.pack(pady=20)

        if self.usuario._cargo in [1, 2]: # Diretor ou Supervisor
            botoes = [
                ("Produtos", self._show_produto),
                ("Armazéns", self._show_armazem),
                ("Unidades de Armazenamento", self._show_unidade_armazenamento),
                ("Movimentos de Estoque", self._show_movimento_estoque),
                ("Consultar Estoque", self._show_estoque),
                ("Funcionários", self._show_funcionario),
                ("Sair", self._logout),
                #("Cargos", self._show_cargo)
            ]
        elif self.usuario._cargo in [3]: # Logística
            botoes = [
                ("Produtos", self._show_produto),
                ("Unidades de Armazenamento", self._show_unidade_armazenamento),
                ("Movimentos de Estoque", self._show_movimento_estoque),
                ("Consultar Estoque", self._show_estoque),
                ("Sair", self._logout),
            ]
        else: # Operador e outros
            botoes = [
                ("Produtos", self._show_produto),
                ("Movimentos de Estoque", self._show_movimento_estoque),
                ("Sair", self._logout),
            ]

        

        for texto, func in botoes:
            btn = ctk.CTkButton(
                self.left_panel,
                text=texto,
                font=("Arial", 12, "bold"),
                height=45,
                fg_color=Cores_Padrao.COR_BOTAO_MENU,
                text_color=Cores_Padrao.COR_TEXTO_MENU_ESCURO,
                hover_color=Cores_Padrao.COR_BOTAO_MENU_HOVER,
                corner_radius=0,
                command=lambda t=texto, f=func: self._menu_command(t, f)
            )
            btn.pack(fill="x", padx=0, pady=0)
            self.menu_buttons[texto] = btn

        self._set_menu_state("disabled")
        self.active_screen = None

    def _set_menu_state(self, state):
        for btn in self.menu_buttons.values():
            btn.configure(state=state)

    def _setup_initial_content(self):
        self._show_login()

    def _show_login(self):
        self.right_panel.configure(fg_color=Cores_Padrao.COR_FUNDO_MENU)
        self.right_panel_content.configure(fg_color=Cores_Padrao.COR_FUNDO_MENU)
        
        self._clear_right_panel()
        self._set_active_menu("Login")

        frame = ctk.CTkFrame(self.right_panel_content, fg_color=Cores_Padrao.COR_FUNDO_MENU)
        frame.pack(expand=True, fill="both")

        ctk.CTkLabel(
            frame,
            text="Login",
            font=("Arial", 24, "bold"),
            text_color=Cores_Padrao.COR_TEXTO_MENU
        ).pack(pady=20)

        self.login_email_var = ctk.StringVar()
        self.login_password_var = ctk.StringVar()

        ctk.CTkLabel(frame, text="Email", font=("Arial", 12), text_color=Cores_Padrao.COR_TEXTO_MENU).pack(anchor="center", pady=(5, 0))
        ctk.CTkEntry(
            frame,
            textvariable=self.login_email_var,
            width=360,
            height=50,
            corner_radius=0,
            placeholder_text="Digite seu email"
        ).pack(pady=5)

        ctk.CTkLabel(frame, text="Senha", font=("Arial", 12), text_color=Cores_Padrao.COR_TEXTO_MENU).pack(anchor="center", pady=(10, 0))
        ctk.CTkEntry(
            frame,
            textvariable=self.login_password_var,
            width=360,
            height=50,
            corner_radius=0,
            placeholder_text="Digite sua senha",
            show="*"
        ).pack(pady=5)

        ctk.CTkButton(
            frame,
            text="Entrar",
            text_color=Cores_Padrao.COR_TEXTO_MENU_ESCURO,
            fg_color=Cores_Padrao.COR_BOTAO_MENU_ATIVO,
            hover_color=Cores_Padrao.COR_BOTAO_MENU_HOVER,
            command=self._attempt_login,
            width=360,
            height=50,
            corner_radius=0
        ).pack(pady=20)

        self.login_error_label = ctk.CTkLabel(frame, text="", font=("Arial", 12, "bold"), text_color=Cores_Padrao.COR_TEXTO_ERROR)
        self.login_error_label.pack(pady=(5, 0))
        self.login_error_ok_button = ctk.CTkButton(frame, text="OK", command=self._hide_login_error, width=80, 
                                                    fg_color=Cores_Padrao.COR_BOTAO_MENU_ATIVO,
                                                    hover_color=Cores_Padrao.COR_BOTAO_MENU_HOVER,
                                                    text_color=Cores_Padrao.COR_TEXTO_MENU_ESCURO)
        self.login_error_ok_button.pack(pady=(5, 0))
        self.login_error_label.pack_forget()
        self.login_error_ok_button.pack_forget()

        self.current_frame = frame

    def _set_active_menu(self, menu_name):
        self.active_screen = menu_name
        if hasattr(self, 'menu_buttons'):
            for name, btn in self.menu_buttons.items():
                if name == menu_name:
                    btn.configure(fg_color=Cores_Padrao.COR_BOTAO_MENU_ATIVO, 
                                  text_color=Cores_Padrao.COR_TEXTO_MENU_ESCURO, 
                                  hover_color=Cores_Padrao.COR_BOTAO_MENU_HOVER)
                else:
                    btn.configure(fg_color=Cores_Padrao.COR_BOTAO_MENU, 
                                  text_color=Cores_Padrao.COR_TEXTO_MENU_ESCURO, 
                                  hover_color=Cores_Padrao.COR_BOTAO_MENU_HOVER)

        self.right_panel_label.configure(text=menu_name)

    def _clear_right_panel(self):
        """Limpar o painel direito"""
        for widget in self.right_panel_content.winfo_children():
            widget.destroy()

    def _menu_command(self, nome, action):
        self._set_active_menu(nome)
        self._clear_right_panel()
        action()

    def _attempt_login(self):
        email = self.login_email_var.get().strip()
        senha = self.login_password_var.get().strip()
        if not email or not senha:
            return self._display_login_error("Email ou senha inválidos")

        try:
            usuario = self.controller.login(email, senha)
            self.usuario = usuario
            self._show_welcome_content()
        except Exception:
            self._display_login_error("Email ou senha estão errados")

    def _display_login_error(self, mensagem):
        self.login_error_label.configure(text=mensagem)
        self.login_error_label.pack()
        self.login_error_ok_button.pack()

    def _hide_login_error(self):
        self.login_error_label.pack_forget()
        self.login_error_ok_button.pack_forget()

    def _logout(self):
        self.usuario = None
        
        self.menu_buttons.clear()
        
        self.left_panel.pack_forget()
        self.left_panel.destroy()
        
        self.right_panel.pack(fill="both", expand=True, padx=10, pady=10)
        
        self._show_login()

    def _show_welcome_content(self):
        self.right_panel.pack_forget()
        
        self.left_panel = ctk.CTkFrame(self.main_container, fg_color=Cores_Padrao.COR_FUNDO_MENU, width=250)
        self.left_panel.pack(side="left", fill="y", padx=10, pady=10)
        self.left_panel.pack_propagate(False)
        
        self.right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.right_panel.configure(fg_color=Cores_Padrao.COR_FUNDO)
        self.right_panel_content.configure(fg_color=Cores_Padrao.COR_FUNDO)
        
        self._setup_menu()
        self._set_menu_state("normal")
        
        self._clear_right_panel()
        self._set_active_menu("Bem-vindo")

        frame = ctk.CTkFrame(self.right_panel_content, fg_color=Cores_Padrao.COR_FUNDO)
        frame.pack(expand=True, fill="both")

        nome_usuario = self.usuario._nome if self.usuario else "Usuário"

        ctk.CTkLabel(
            frame,
            text=f"Bem-vindo, {nome_usuario}",
            font=("Arial", 28, "bold"),
            text_color=Cores_Padrao.COR_TEXTO
        ).pack(pady=20)

        ctk.CTkLabel(
            frame,
            text="Selecione uma opção no menu lateral",
            font=("Arial", 14),
            text_color=Cores_Padrao.COR_TEXTO
        ).pack(pady=10)

        self.current_frame = frame

    def _show_produto(self):
        if self.controller:
            self.controller.exibir_produto(self.right_panel_content)

    def _show_armazem(self):
        if self.controller:
            self.controller.exibir_armazem(self.right_panel_content)

    def _show_unidade_armazenamento(self):
        if self.controller:
            self.controller.exibir_unidade_armazenamento(self.right_panel_content)

    def _show_funcionario(self):
        if self.controller:
            self.controller.exibir_funcionario(self.right_panel_content)

    def _show_movimento_estoque(self):
        if self.controller:
            self.controller.exibir_movimento_estoque(self.right_panel_content, self.usuario)

    def _show_estoque(self):
        if self.controller:
            self.controller.exibir_estoque(self.right_panel_content)

    def _show_cargo(self):
        if self.controller:
            self.controller.exibir_cargo(self.right_panel_content)

    def run(self):
        self.root.mainloop()
    
    def _maximize_window(self):
        """Maximiza a janela para ocupar a tela inteira"""
        try:
            # Tenta usar a abordagem do Windows
            self.root.state('zoomed')
        except:
            try:
                # Se falhar, tenta a abordagem genérica
                self.root.attributes('-zoomed', True)
            except:
                # Se ainda falhar, obtém as dimensões da tela e redimensiona
                self.root.update_idletasks()
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                self.root.geometry(f"{screen_width}x{screen_height}+0+0")