# Sistema Bancário - Depósito | Saque | Extrato
# Com monetização: taxa por saque e limite de saques por dia

from decimal import Decimal, ROUND_HALF_UP
from datetime import datetime, date

TAXA_SAQUE = Decimal("1.50")           # taxa fixa por saque
LIMITE_SAQUES_DIA = 3                  # número máximo de saques por dia
LIMITE_POR_SAQUE = Decimal("1000.00")  # valor máximo por saque

# Estado do sistema
saldo = Decimal("0.00")
transacoes = []  # cada item: dict com tipo, valor, datahora, info extra
saques_hoje = 0
dia_referencia = date.today()

def dinheiro(valor: Decimal) -> str:
    """Formata Decimal em moeda com 2 casas."""
    return f"R$ {valor.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)}"

def resetar_contagem_se_virou_o_dia():
    global saques_hoje, dia_referencia
    hoje = date.today()
    if hoje != dia_referencia:
        saques_hoje = 0
        dia_referencia = hoje

def depositar():
    global saldo
    try:
        valor = Decimal(input("Valor do depósito: ").replace(",", "."))
    except Exception:
        print("❌ Valor inválido.")
        return
    if valor <= 0:
        print("❌ O depósito deve ser maior que zero.")
        return

    saldo += valor
    transacoes.append({
        "tipo": "DEPÓSITO",
        "valor": valor,
        "taxa": Decimal("0.00"),
        "data": datetime.now()
    })
    print(f"✅ Depósito realizado: {dinheiro(valor)} | Saldo: {dinheiro(saldo)}")

def sacar():
    global saldo, saques_hoje
    resetar_contagem_se_virou_o_dia()

    if saques_hoje >= LIMITE_SAQUES_DIA:
        print(f"❌ Limite diário de {LIMITE_SAQUES_DIA} saques atingido.")
        return

    try:
        valor = Decimal(input("Valor do saque: ").replace(",", "."))
    except Exception:
        print("❌ Valor inválido.")
        return

    if valor <= 0:
        print("❌ O saque deve ser maior que zero.")
        return
    if valor > LIMITE_POR_SAQUE:
        print(f"❌ Limite por saque: {dinheiro(LIMITE_POR_SAQUE)}.")
        return

    custo_total = valor + TAXA_SAQUE
    if custo_total > saldo:
        print(f"❌ Saldo insuficiente (precisa cobrir o valor + taxa de {dinheiro(TAXA_SAQUE)}).")
        return

    saldo -= custo_total
    saques_hoje += 1
    transacoes.append({
        "tipo": "SAQUE",
        "valor": -valor,  # negativo para facilitar somatórios
        "taxa": TAXA_SAQUE,
        "data": datetime.now()
    })
    print(f"✅ Saque de {dinheiro(valor)} realizado (taxa {dinheiro(TAXA_SAQUE)}). Saldo: {dinheiro(saldo)}")

def extrato():
    print("\n" + "="*42)
    print("EXTRATO".center(42))
    print("="*42)

    if not transacoes:
        print("Nenhuma movimentação.")
    else:
        total_depositos = Decimal("0.00")
        total_saques = Decimal("0.00")
        total_taxas = Decimal("0.00")

        for t in transacoes:
            data_fmt = t["data"].strftime("%d/%m/%Y %H:%M:%S")
            tipo = t["tipo"]
            valor = t["valor"]
            taxa = t.get("taxa", Decimal("0.00"))

            if tipo == "DEPÓSITO":
                total_depositos += valor
                print(f"[{data_fmt}] {tipo:<10} +{dinheiro(valor)}")
            elif tipo == "SAQUE":
                total_saques += -valor  # valor armazenado negativo
                total_taxas += taxa
                print(f"[{data_fmt}] {tipo:<10} -{dinheiro(-valor)}  (taxa {dinheiro(taxa)})")

        print("-"*42)
        print(f"Total de depósitos : {dinheiro(total_depositos)}")
        print(f"Total de saques    : {dinheiro(total_saques)}")
        print(f"Taxas cobradas     : {dinheiro(total_taxas)}")
        print("-"*42)
        print(f"SALDO ATUAL        : {dinheiro(saldo)}")
    print("="*42 + "\n")

def menu():
    print("""
=========== BANCO JEY ============
[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair
=================================
""")

def main():
    while True:
        resetar_contagem_se_virou_o_dia()
        menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            depositar()
        elif opcao == "2":
            sacar()
        elif opcao == "3":
            extrato()
        elif opcao == "0":
            print("👋 Obrigado por usar o Banco JEY! Até mais.")
            break
        else:
            print("❌ Opção inválida.")

if __name__ == "__main__":
    main()
