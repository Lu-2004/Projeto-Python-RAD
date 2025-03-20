import customtkinter as ctk
from tkinter import messagebox
import sqlite3

# Definindo o tema escuro globalmente
ctk.set_appearance_mode("dark")  # Tema escuro
ctk.set_default_color_theme("dark-blue")  # Esquema de cores

# Conexão com o banco de dados SQLite
conn = sqlite3.connect("usuarios.db")
cursor = conn.cursor()

# Criando a tabela de usuários se não existir
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    email TEXT PRIMARY KEY,
    senha TEXT
)
""")
conn.commit()

# Função de login
def verificar_login():
    email = entry_usuario.get()
    senha = entry_senha.get()

    # Consultar o banco de dados
    cursor.execute("SELECT * FROM usuarios WHERE email = ? AND senha = ?", (email, senha))
    usuario = cursor.fetchone()

    if usuario:
        messagebox.showinfo("Login Bem-sucedido", f"Bem-vindo, {email}!")
        abrir_menu(email)
        root.destroy()  # Fecha a tela de login
    else:
        messagebox.showerror("Erro", "E-mail ou senha incorretos!")

# Função para abrir o menu principal
def abrir_menu(email):
    menu_window = ctk.CTk()
    menu_window.title(f"Menu - {email}")
    menu_window.geometry("350x210")
    menu_window.resizable(width=False, height=False)

    def mostrar_dados_financeiros(tipo):
        if tipo == "receitas":
            messagebox.showinfo("Dashboard de Receitas", "Aqui você pode visualizar suas receitas.")
        elif tipo == "despesas":
            messagebox.showinfo("Dashboard de Despesas", "Aqui você pode visualizar suas despesas.")
        elif tipo == "geral":
            messagebox.showinfo("Dashboard Geral", "Aqui você pode ver o controle geral de finanças.")
    
    welcome_label = ctk.CTkLabel(menu_window, text=f"Bem-vindo ao sistema, {email}!", font=("Arial", 14))
    welcome_label.pack(pady=10)

    btn_receitas = ctk.CTkButton(menu_window, text="Dashboard de Receitas", width=200, command=lambda: mostrar_dados_financeiros("receitas"))
    btn_receitas.pack(pady=10)

    btn_despesas = ctk.CTkButton(menu_window, text="Dashboard de Despesas", width=200, command=lambda: mostrar_dados_financeiros("despesas"))
    btn_despesas.pack(pady=10)

    btn_geral = ctk.CTkButton(menu_window, text="Dashboard Geral", width=200, command=lambda: mostrar_dados_financeiros("geral"))
    btn_geral.pack(pady=10)

    menu_window.mainloop()

# Função para abrir a janela de criar conta
def abrir_criar_conta():
    criar_conta_janela = ctk.CTkToplevel()
    criar_conta_janela.title("Criar Conta")
    criar_conta_janela.geometry("300x300")
    criar_conta_janela.resizable(width=False, height=False)

    def criar_conta():
        email = novo_email_entry.get()
        senha = nova_senha_entry.get()
        confirmacao = confirmacao_senha_entry.get()

        if senha != confirmacao:
            messagebox.showerror("Erro", "As senhas não coincidem!")
        elif not email or not senha:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos!")
        else:
            try:
                cursor.execute("INSERT INTO usuarios (email, senha) VALUES (?, ?)", (email, senha))
                conn.commit()
                messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
                criar_conta_janela.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Erro", "E-mail já cadastrado!")

    ctk.CTkLabel(criar_conta_janela, text="E-mail:").pack(pady=5)
    novo_email_entry = ctk.CTkEntry(criar_conta_janela)
    novo_email_entry.pack(pady=5)

    ctk.CTkLabel(criar_conta_janela, text="Senha:").pack(pady=5)
    nova_senha_entry = ctk.CTkEntry(criar_conta_janela, show="*")
    nova_senha_entry.pack(pady=5)

    ctk.CTkLabel(criar_conta_janela, text="Confirmar Senha:").pack(pady=5)
    confirmacao_senha_entry = ctk.CTkEntry(criar_conta_janela, show="*")
    confirmacao_senha_entry.pack(pady=5)

    ctk.CTkButton(criar_conta_janela, text="Criar Conta", command=criar_conta).pack(pady=10)

# Criar a janela principal de login
root = ctk.CTk()
root.title("Tela de Login")
root.geometry("300x300")
root.resizable(width=False, height=False)

ctk.CTkLabel(root, text="E-mail:").pack(pady=5)
entry_usuario = ctk.CTkEntry(root)
entry_usuario.pack(pady=5)

ctk.CTkLabel(root, text="Senha:").pack(pady=5)
entry_senha = ctk.CTkEntry(root, show="*")
entry_senha.pack(pady=5)

btn_login = ctk.CTkButton(root, text="Login", command=verificar_login)
btn_login.pack(pady=10)

btn_criar_conta = ctk.CTkButton(root, text="Criar Conta", command=abrir_criar_conta)
btn_criar_conta.pack(pady=10)

root.mainloop()

# Fechar a conexão com o banco de dados ao encerrar o programa
conn.close()
