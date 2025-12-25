import csv
import re
import random
from collections import Counter

CSV_PATH = "comentarios.csv"
EXACT_MENTIONS = 3  # regra: exatamente 3 amigos

def extract_mentions(text: str) -> list[str]:
    # pega @username (Instagram aceita letras, números, _ e .)
    return re.findall(r"@([A-Za-z0-9._]+)", text)

def is_valid_comment(text: str) -> bool:
    mentions = extract_mentions(text)

    # normaliza (ignora diferença de maiúsculas/minúsculas)
    mentions_norm = [m.lower() for m in mentions]

    # tem que ser exatamente 3 marcações no comentário
    if len(mentions_norm) != EXACT_MENTIONS:
        return False

    # e as 3 têm que ser diferentes
    if len(set(mentions_norm)) != EXACT_MENTIONS:
        return False

    return True

def read_csv(path: str) -> list[dict]:
    rows = []
    with open(path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            user = (row.get("username") or "").strip()
            text = (row.get("text") or "").strip()
            if user and text:
                rows.append({"username": user, "text": text})
    return rows

def main() -> None:
    comments = read_csv(CSV_PATH)

    tickets = []
    invalid_count = 0

    for c in comments:
        if is_valid_comment(c["text"]):
            tickets.append(c["username"])  # 1 comentário válido = 1 bilhete
        else:
            invalid_count += 1

    print("=== RELATÓRIO ===")
    print(f"Total de comentários no CSV: {len(comments)}")
    print(f"Válidos (3 amigos diferentes): {len(tickets)}")
    print(f"Inválidos: {invalid_count}")

    if not tickets:
        print("\nNenhum comentário válido com 3 amigos diferentes.")
        return

    winner = random.choice(tickets)

    print("\n=== VENCEDOR ===")
    print(f"@{winner}")

    print("\n=== CHANCES POR USUÁRIO ===")
    for user, qty in Counter(tickets).most_common():
        print(f"@{user}: {qty} bilhete(s)")

if __name__ == "__main__":
    main()