import customtkinter as ctk
from view.cores_padrao import Cores_Padrao

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


class Main_View:
    def __init__(self):
        self.controller = None
        self.root = ctk.CTk()
        self.root.title("Sistema IDK WMS")
        self.root.geometry("1600x800")
        self.root.state('zoomed')
        
        self.main_container = ctk.CTkFrame(self.root, fg_color="#1A2B44")
        self.main_container.pack(fill="both", expand=True)
        
        self.right_panel = ctk.CTkFrame(
            self.main_container,
            fg_color=Cores_Padrao.COR_FUNDO,
        )
        self.right_panel.pack(fill="both", expand=True, padx=10, pady=10)

        self.right_panel_label = ctk.CTkLabel(
            self.right_panel,
            text="Login",
            font=("Arial", 14, "bold"),
            text_color="#000000",
            anchor="w"
        )
        self.right_panel_label.pack(fill="x", padx=10, pady=(10, 0))

        self.right_panel_content = ctk.CTkFrame(self.right_panel, fg_color=Cores_Padrao.COR_FUNDO, border_width=0)
        self.right_panel_content.pack(expand=True, fill="both", padx=10, pady=10)

        self.current_frame = None
        self.usuario = None

        self._setup_initial_content()

    def _setup_menu(self):
        self.menu_buttons = {}

        titulo = ctk.CTkLabel(
            self.left_panel,
            text="Menu Principal",
            font=("Arial", 16, "bold"),
            text_color="#FFFFFF"
        )
        titulo.pack(pady=20)

        if self.usuario._cargo in [1, 2]: # Diretor ou Supervisor
            botoes = [
                ("Produtos", self._show_produto),
                ("Armazéns", self._show_armazem),
                ("Funcionários", self._show_funcionario),
                ("Sair", self._logout),
                #("Cargos", self._show_cargo)
            ]
        else:
            botoes = [
                ("Produtos", self._show_produto),
                ("Armazéns", self._show_armazem),
                ("Sair", self._logout),
                #("Cargos", self._show_cargo)
            ]

        

        for texto, func in botoes:
            btn = ctk.CTkButton(
                self.left_panel,
                text=texto,
                font=("Arial", 12, "bold"),
                height=45,
                fg_color="#D9E7FF",
                text_color="#000000",
                hover_color="#A2C6FF",
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
        self.right_panel.configure(fg_color="#1A2B44")
        self.right_panel_content.configure(fg_color="#1A2B44")
        
        self._clear_right_panel()
        self._set_active_menu("Login")

        frame = ctk.CTkFrame(self.right_panel_content, fg_color="#1A2B44")
        frame.pack(expand=True, fill="both")

        ctk.CTkLabel(
            frame,
            text="Login",
            font=("Arial", 24, "bold"),
            text_color="#FFFFFF"
        ).pack(pady=20)

        self.login_email_var = ctk.StringVar()
        self.login_password_var = ctk.StringVar()

        ctk.CTkLabel(frame, text="Email", font=("Arial", 12), text_color="#FFFFFF").pack(anchor="center", pady=(5, 0))
        ctk.CTkEntry(
            frame,
            textvariable=self.login_email_var,
            width=360,
            height=50,
            corner_radius=0,
            placeholder_text="Digite seu email"
        ).pack(pady=5)

        ctk.CTkLabel(frame, text="Senha", font=("Arial", 12), text_color="#FFFFFF").pack(anchor="center", pady=(10, 0))
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
            command=self._attempt_login,
            width=360,
            height=50,
            corner_radius=0
        ).pack(pady=20)

        self.login_error_label = ctk.CTkLabel(frame, text="", font=("Arial", 12, "bold"), text_color="#FF5555")
        self.login_error_label.pack(pady=(5, 0))
        self.login_error_ok_button = ctk.CTkButton(frame, text="OK", command=self._hide_login_error, width=80)
        self.login_error_ok_button.pack(pady=(5, 0))
        self.login_error_label.pack_forget()
        self.login_error_ok_button.pack_forget()

        self.current_frame = frame

    def _set_active_menu(self, menu_name):
        self.active_screen = menu_name
        if hasattr(self, 'menu_buttons'):
            for name, btn in self.menu_buttons.items():
                if name == menu_name:
                    btn.configure(fg_color="#2D7FB6", text_color="#FFFFFF", hover_color="#1C5C94")
                else:
                    btn.configure(fg_color="#F0F0F0", text_color="#000000", hover_color="#E0E0E0")

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
        
        self.left_panel = ctk.CTkFrame(self.main_container, fg_color="#1A2B44", width=250)
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

    def _show_funcionario(self):
        if self.controller:
            self.controller.exibir_funcionario(self.right_panel_content)

    def _show_cargo(self):
        if self.controller:
            self.controller.exibir_cargo(self.right_panel_content)

    def run(self):
        self.root.mainloop()