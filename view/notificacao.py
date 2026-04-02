import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from view.cores_padrao import Cores_Padrao


class Notificacao:
    @staticmethod
    def erro(titulo, mensagem, parent=None):
        janela = ctk.CTkToplevel()
        janela.title(titulo)
        janela.geometry("400x200")
        janela.resizable(False, False)

        if parent:
            janela.transient(parent)
            janela.grab_set()

        janela.configure(fg_color=Cores_Padrao.COR_FUNDO)

        frame_principal = ctk.CTkFrame(
            janela, fg_color="#f5e8e8", border_width=2, border_color="#d97ca1"
        )
        frame_principal.pack(fill="both", expand=True, padx=5, pady=5)

        frame_titulo = ctk.CTkFrame(frame_principal, fg_color="#f5e8e8")
        frame_titulo.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            frame_titulo,
            text="⚠ ERRO",
            font=("Arial", 14, "bold"),
            text_color="#d97ca1",
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame_principal,
            text=mensagem,
            font=("Arial", 11),
            text_color=Cores_Padrao.COR_TEXTO,
            wraplength=350,
            justify="left",
        ).pack(padx=15, pady=10, fill="both", expand=True)

        ctk.CTkButton(
            frame_principal,
            text="OK",
            fg_color="#d97ca1",
            hover_color="#c97bb8",
            text_color="white",
            command=janela.destroy,
        ).pack(pady=10, padx=15, fill="x")

        janela.focus()
        janela.wait_window()

    @staticmethod
    def aviso(titulo, mensagem, parent=None):
        janela = ctk.CTkToplevel()
        janela.title(titulo)
        janela.geometry("400x200")
        janela.resizable(False, False)

        if parent:
            janela.transient(parent)
            janela.grab_set()

        janela.configure(fg_color=Cores_Padrao.COR_FUNDO)

        frame_principal = ctk.CTkFrame(
            janela, fg_color="#f5f0e8", border_width=2, border_color="#d9a47c"
        )
        frame_principal.pack(fill="both", expand=True, padx=5, pady=5)

        frame_titulo = ctk.CTkFrame(frame_principal, fg_color="#f5f0e8")
        frame_titulo.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            frame_titulo,
            text="⚠ AVISO",
            font=("Arial", 14, "bold"),
            text_color="#d9a47c",
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame_principal,
            text=mensagem,
            font=("Arial", 11),
            text_color=Cores_Padrao.COR_TEXTO,
            wraplength=350,
            justify="left",
        ).pack(padx=15, pady=10, fill="both", expand=True)

        ctk.CTkButton(
            frame_principal,
            text="OK",
            fg_color="#d9a47c",
            hover_color="#c99470",
            text_color="white",
            command=janela.destroy,
        ).pack(pady=10, padx=15, fill="x")

        janela.focus()
        janela.wait_window()

    @staticmethod
    def sucesso(titulo, mensagem, parent=None):
        """Exibe notificação de sucesso"""
        janela = ctk.CTkToplevel()
        janela.title(titulo)
        janela.geometry("400x200")
        janela.resizable(False, False)

        if parent:
            janela.transient(parent)
            janela.grab_set()

        janela.configure(fg_color=Cores_Padrao.COR_FUNDO)

        frame_principal = ctk.CTkFrame(
            janela, fg_color="#e8f5e8", border_width=2, border_color="#7cd97c"
        )
        frame_principal.pack(fill="both", expand=True, padx=5, pady=5)

        frame_titulo = ctk.CTkFrame(frame_principal, fg_color="#e8f5e8")
        frame_titulo.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            frame_titulo,
            text="✓ SUCESSO",
            font=("Arial", 14, "bold"),
            text_color="#7cd97c",
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame_principal,
            text=mensagem,
            font=("Arial", 11),
            text_color=Cores_Padrao.COR_TEXTO,
            wraplength=350,
            justify="left",
        ).pack(padx=15, pady=10, fill="both", expand=True)

        ctk.CTkButton(
            frame_principal,
            text="OK",
            fg_color="#7cd97c",
            hover_color="#6cc96c",
            text_color="white",
            command=janela.destroy,
        ).pack(pady=10, padx=15, fill="x")

        janela.focus()
        janela.wait_window()

    @staticmethod
    def confirmacao(titulo, mensagem, parent=None):
        """Exibe caixa de confirmação e retorna True/False"""
        janela = ctk.CTkToplevel()
        janela.title(titulo)
        janela.geometry("400x220")
        janela.resizable(False, False)

        if parent:
            janela.transient(parent)
            janela.grab_set()

        janela.configure(fg_color=Cores_Padrao.COR_FUNDO)

        frame_principal = ctk.CTkFrame(
            janela, fg_color="#e8f0f5", border_width=2, border_color="#7ca1d9"
        )
        frame_principal.pack(fill="both", expand=True, padx=5, pady=5)

        frame_titulo = ctk.CTkFrame(frame_principal, fg_color="#e8f0f5")
        frame_titulo.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            frame_titulo,
            text="? CONFIRMAÇÃO",
            font=("Arial", 14, "bold"),
            text_color="#7ca1d9",
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame_principal,
            text=mensagem,
            font=("Arial", 11),
            text_color=Cores_Padrao.COR_TEXTO,
            wraplength=350,
            justify="left",
        ).pack(padx=15, pady=10, fill="both", expand=True)

        resultado = {"resposta": False}

        def confirmar():
            resultado["resposta"] = True
            janela.destroy()

        def cancelar():
            resultado["resposta"] = False
            janela.destroy()

        frame_botoes = ctk.CTkFrame(frame_principal, fg_color="#e8f0f5")
        frame_botoes.pack(pady=10, padx=15, fill="x")

        ctk.CTkButton(
            frame_botoes,
            text="Sim",
            fg_color="#7cd97c",
            hover_color="#6cc96c",
            text_color="white",
            command=confirmar,
        ).pack(side="left", padx=5, fill="x", expand=True)

        ctk.CTkButton(
            frame_botoes,
            text="Não",
            fg_color="#d97ca1",
            hover_color="#c97bb8",
            text_color="white",
            command=cancelar,
        ).pack(side="left", padx=5, fill="x", expand=True)

        janela.focus()
        janela.wait_window()

        return resultado["resposta"]

    @staticmethod
    def info(titulo, mensagem, parent=None):
        """Exibe notificação informativa"""
        janela = ctk.CTkToplevel()
        janela.title(titulo)
        janela.geometry("400x200")
        janela.resizable(False, False)

        if parent:
            janela.transient(parent)
            janela.grab_set()

        janela.configure(fg_color=Cores_Padrao.COR_FUNDO)

        frame_principal = ctk.CTkFrame(
            janela, fg_color="#e8f0f5", border_width=2, border_color="#7ca1d9"
        )
        frame_principal.pack(fill="both", expand=True, padx=5, pady=5)

        frame_titulo = ctk.CTkFrame(frame_principal, fg_color="#e8f0f5")
        frame_titulo.pack(fill="x", padx=15, pady=(15, 5))

        ctk.CTkLabel(
            frame_titulo,
            text="ℹ INFORMAÇÃO",
            font=("Arial", 14, "bold"),
            text_color="#7ca1d9",
        ).pack(anchor="w")

        ctk.CTkLabel(
            frame_principal,
            text=mensagem,
            font=("Arial", 11),
            text_color=Cores_Padrao.COR_TEXTO,
            wraplength=350,
            justify="left",
        ).pack(padx=15, pady=10, fill="both", expand=True)

        ctk.CTkButton(
            frame_principal,
            text="OK",
            fg_color="#7ca1d9",
            hover_color="#6c91c9",
            text_color="white",
            command=janela.destroy,
        ).pack(pady=10, padx=15, fill="x")

        janela.focus()
        janela.wait_window()
