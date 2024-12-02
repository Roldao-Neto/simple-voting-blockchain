import tkinter as tk
from tkinter import messagebox
import requests
import json

# URL base do servidor Flask
SERVER_URL = "http://127.0.0.1:5000"

# Função para votar
def votar():
    def enviar_voto():
        voter_id = entry_voter_id.get()
        candidate = entry_candidate.get()
        if not voter_id or not candidate:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
        try:
            response = requests.post(f"{SERVER_URL}/vote", json={"voter_id": voter_id, "candidate": candidate})
            if response.status_code == 201:
                messagebox.showinfo("Sucesso", response.json()["message"])
                voto_window.destroy()
            else:
                messagebox.showerror("Erro", response.text)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao se conectar ao servidor: {e}")

    voto_window = tk.Toplevel(root)
    voto_window.title("Votar")
    tk.Label(voto_window, text="Voter ID:").pack(pady=5)
    entry_voter_id = tk.Entry(voto_window)
    entry_voter_id.pack(pady=5)
    tk.Label(voto_window, text="Candidato:").pack(pady=5)
    entry_candidate = tk.Entry(voto_window)
    entry_candidate.pack(pady=5)
    tk.Button(voto_window, text="Enviar Voto", command=enviar_voto).pack(pady=10)

# Função para minerar
def minerar():
    try:
        response = requests.get(f"{SERVER_URL}/mine")
        if response.status_code == 200:
            info = response.json()
            messagebox.showinfo("Sucesso", f"Novo bloco minerado!\nÍndice: {info['index']}\nProva: {info['proof']}")
        else:
            messagebox.showerror("Erro", response.text)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao se conectar ao servidor: {e}")

# Função para visualizar a blockchain
def ver_blockchain():
    try:
        response = requests.get(f"{SERVER_URL}/chain")
        if response.status_code == 200:
            blockchain = response.json()["chain"]
            blockchain_window = tk.Toplevel(root)
            blockchain_window.title("Blockchain")
            text = tk.Text(blockchain_window, wrap="word")
            text.insert("1.0", json.dumps(blockchain, indent=4))
            text.pack(expand=True, fill="both")
        else:
            messagebox.showerror("Erro", response.text)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao se conectar ao servidor: {e}")

def encerrar_votacao():
    try:
        response = requests.get(f"{SERVER_URL}/chain")
        if response.status_code == 200:
            blockchain = response.json()["chain"]
            if not blockchain:
                messagebox.showinfo("Resultado", "Ninguém quis votar.")
                return
            
            # Compilando todos os votos na blockchain
            votos = []
            for bloco in blockchain:
                votos.extend(bloco.get("votes", []))

            if not votos:
                messagebox.showinfo("Resultado", "Ninguém quis votar.")
                return

            # Contando votos
            resultados = {}
            for voto in votos:
                candidato = voto["candidate"]
                resultados[candidato] = resultados.get(candidato, 0) + 1

            # Exibindo resultados
            resultados_window = tk.Toplevel(root)
            resultados_window.title("Resultados da Votação")
            for candidato, total_votos in resultados.items():
                tk.Label(resultados_window, text=f"{candidato}: {total_votos} votos").pack(pady=2)

        else:
            messagebox.showerror("Erro", response.text)
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Erro", f"Erro ao se conectar ao servidor: {e}")

# Configuração da interface principal
root = tk.Tk()
root.title("Sistema de Votação Blockchain")
root.geometry("300x200")

tk.Button(root, text="Votar", command=votar).pack(pady=10)
tk.Button(root, text="Minerar", command=minerar).pack(pady=10)
tk.Button(root, text="Ver Blockchain", command=ver_blockchain).pack(pady=10)
tk.Button(root, text="Encerrar Votação", command=encerrar_votacao).pack(pady=10)

root.mainloop()
