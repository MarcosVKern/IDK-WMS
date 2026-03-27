import tkinter as tk

class Main_view:
    def __init__(self):
        self.controller = None
        self.root = tk.Tk()
        self.root.title("Sistema de Pizzas")
        self.root.geometry("1280x720")
        self.root.state('zoomed')
        
        self._setup_menu()

    def _setup_menu(self):
        topo_frame = tk.Frame(self.root)
        topo_frame.pack(pady=50)

        tk.Label(topo_frame, text="Bem-vindo Sistema.", font=("Comic Sans MS", 24, "bold")).pack(pady=10)

        centro_frame = tk.Frame(self.root)
        centro_frame.pack(expand=True)

        botoes = [
            ("Produtos", self._abrir_produto)
        ]

        for texto, func in botoes:
            tk.Button(centro_frame, text=texto, font=("Arial", 14, "bold"), width=20, height=2, command=func, bg="#ddbef1").pack(pady=10)

    def _abrir_produto(self):
        if self.controller:
            self.controller.exibir_produto()

    def run(self):
        self.root.mainloop()