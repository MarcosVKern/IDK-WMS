import tkinter as tk
from view.cores_padrao import Cores_Padrao

class Main_View:
    def __init__(self):
        self.controller = None
        self.root = tk.Tk()
        self.root.title("Sistema WMS")
        self.root.geometry("1280x720")
        self.root.state('zoomed')
        
        self._setup_menu()

    def _setup_menu(self):
        topo_frame = tk.Frame(self.root)
        topo_frame.pack(pady=50)

        tk.Label(topo_frame, text="Bem-vindo ao Sistema WMS IDK.", font=("Arial", 24, "bold")).pack(pady=10)

        centro_frame = tk.Frame(self.root)
        centro_frame.pack(expand=True)

        botoes = [
            ("Produtos", self._abrir_produto),
            ("Armazéns", self._abrir_armazem),
            ("Funcionários", self._abrir_funcionario),
            ("Cargos", self._abrir_cargo)
        ]

        for texto, func in botoes:
            tk.Button(centro_frame, text=texto, font=("Arial", 14, "bold"), width=20, height=2, command=func, bg=Cores_Padrao.COR_BOTAO_MENU).pack(pady=10)

    def _abrir_produto(self):
        if self.controller:
            self.controller.exibir_produto()

    def _abrir_armazem(self):
        if self.controller:
            self.controller.exibir_armazem()

    def _abrir_funcionario(self):
        if self.controller:
            self.controller.exibir_funcionario()

    def _abrir_cargo(self):
        if self.controller:
            self.controller.exibir_cargo()

    def run(self):
        self.root.mainloop()