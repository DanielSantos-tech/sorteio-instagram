import csv
import re
import random
from collections import Counter
import tkinter as tk
from tkinter import filedialog, messagebox

MIN_MENTIONS = 3  # regra: exatamente 3 amigos diferentes


def extract_mentions(text: str) -> list[str]:
    return re.findall(r"@([A-Za-z0-9._]+)", text)


def is_valid_comment(text: str) -> bool:
    mentions = [m.lower() for m in extract_mentions(text)]

    # exatamente 3 marcações
    if len(mentions) != MIN_MENTIONS:
        return False

    # as 3 precisam ser diferentes
    if len(set(mentions)) != MIN_MENTIONS:
        return False

    return True


class SorteioApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Gerador de Nomes — Danieltech")
        self.root.geometry("720x520")
        self.root.minsize(720, 520)

        self.csv_path = None
        self.comments = []
        self.tickets = []

        # ===== Topo =====
        title = tk.Label(
            root,
            text="Sorteio Farmácia Santos (3 amigos diferentes)",
            font=("Segoe UI", 18, "bold")
        )
        title.pack(pady=(18, 6))

        subtitle = tk.Label(
            root,
            text="Carregue o CSV de comentários e clique em Sortear.",
            font=("Segoe UI", 11)
        )
        subtitle.pack(pady=(0, 14))

        # ===== Área de botões =====
        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=8)

        self.btn_load = tk.Button(
            btn_frame,
            text="1) Carregar CSV",
            width=18,
            command=self.load_csv
        )
        self.btn_load.grid(row=0, column=0, padx=8)

        self.btn_validate = tk.Button(
            btn_frame,
            text="2) Validar",
            width=18,
            command=self.validate_comments,
            state="disabled"
        )
        self.btn_validate.grid(row=0, column=1, padx=8)

        self.btn_draw = tk.Button(
            btn_frame,
            text="3) Sortear 🎁",
            width=18,
            command=self.draw_winner,
            state="disabled"
        )
        self.btn_draw.grid(row=0, column=2, padx=8)

        # ===== Status do arquivo =====
        self.lbl_file = tk.Label(root, text="CSV: (nenhum carregado)", font=("Segoe UI", 10, "italic"))
        self.lbl_file.pack(pady=(10, 6))

        # ===== Caixa de saída =====
        self.output = tk.Text(root, height=16, width=90)
        self.output.pack(padx=14, pady=10)
        self.output.insert("end", "➡️ Dica: O CSV deve ter colunas: username,text\n\n")
        self.output.config(state="disabled")

        btn_frame.pack(pady=8)

        # ===== Créditos (posição superior) =====
        credits = tk.Frame(root)
        credits.pack(pady=(4, 10))

        tk.Label(
            credits,
            text="Colaboradores: @terekids  |  @farmacia_santoos",
            font=("Segoe UI", 11)
        ).pack(pady=(0, 3))

        tk.Label(
            credits,
            text="Criado por: Danieltech",
            font=("Segoe UI", 11, "bold")
        ).pack()

        tk.Label(
            credits,
            text="Criado por: Danieltech",
            font=("Segoe UI", 11, "bold")
        ).pack()

    def log(self, msg: str):
        self.output.config(state="normal")
        self.output.insert("end", msg + "\n")
        self.output.see("end")
        self.output.config(state="disabled")

    def clear_output(self):
        self.output.config(state="normal")
        self.output.delete("1.0", "end")
        self.output.config(state="disabled")

    def load_csv(self):
        path = filedialog.askopenfilename(
            title="Selecione o comentarios.csv",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not path:
            return

        try:
            comments = []
            with open(path, "r", encoding="utf-8", newline="") as f:
                reader = csv.DictReader(f)
                if "username" not in reader.fieldnames or "text" not in reader.fieldnames:
                    raise ValueError("CSV precisa ter colunas: username,text")

                for row in reader:
                    user = (row.get("username") or "").strip()
                    text = (row.get("text") or "").strip()
                    if user and text:
                        comments.append({"username": user, "text": text})

            self.csv_path = path
            self.comments = comments
            self.tickets = []

            self.lbl_file.config(text=f"CSV: {path}")
            self.btn_validate.config(state="normal")
            self.btn_draw.config(state="disabled")

            self.clear_output()
            self.log("✅ CSV carregado com sucesso!")
            self.log(f"Total de comentários lidos: {len(self.comments)}")
            self.log("\nClique em 'Validar' para aplicar a regra (3 amigos diferentes).")

        except Exception as e:
            messagebox.showerror("Erro ao carregar CSV", str(e))

    def validate_comments(self):
        if not self.comments:
            messagebox.showwarning("Atenção", "Carregue um CSV primeiro.")
            return

        tickets = []
        invalid = 0

        for c in self.comments:
            if is_valid_comment(c["text"]):
                tickets.append(c["username"])
            else:
                invalid += 1

        self.tickets = tickets

        self.log("\n=== RELATÓRIO DE VALIDAÇÃO ===")
        self.log(f"Válidos (3 amigos diferentes): {len(tickets)}")
        self.log(f"Inválidos: {invalid}")

        if len(tickets) == 0:
            self.btn_draw.config(state="disabled")
            self.log("\n⚠️ Nenhum comentário válido. Confira as marcações com @.")
        else:
            self.btn_draw.config(state="normal")
            self.log("\n✅ Pronto! Agora clique em 'Sortear 🎁'.")

    def draw_winner(self):
        if not self.tickets:
            messagebox.showwarning("Atenção", "Valide primeiro (ou não há bilhetes).")
            return

        winner = random.choice(self.tickets)
        chances = Counter(self.tickets)

        self.log("\n=== SORTEIO ===")
        self.log(f"🏆 VENCEDOR(A): @{winner}")

        self.log("\n=== CHANCES POR USUÁRIO ===")
        for user, qty in chances.most_common():
            self.log(f"@{user}: {qty} bilhete(s)")


if __name__ == "__main__":
    root = tk.Tk()
    app = SorteioApp(root)
    root.mainloop()
