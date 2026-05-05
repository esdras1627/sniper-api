import requests
import time
import uuid
import webbrowser

API = "https://sniper-api-kypc.onrender.com"  # sua URL

maquina = str(uuid.getnode())

# =========================
# TESTE 1H
# =========================
resp = requests.post(API + "/trial", json={
    "machine": maquina
})

data = resp.json()

if data.get("status") == "active":
    print(f"🟢 Teste ativo ({data['restante']}s restantes)")

else:
    print("🔒 Teste expirado!")

    print("1 - Comprar acesso")
    print("2 - Inserir licença")

    op = input("Escolha: ")

    if op == "1":
        email = input("Digite seu email: ")

        resp = requests.post(API + "/create-payment", json={
            "email": email
        }).json()

        print("💰 Abra o link:")
        print(resp["payment_url"])

        webbrowser.open(resp["payment_url"])

        print("\n⚠️ PARA TESTE:")
        print(f"Acesse: {API}/approve/{email}")

        print("⏳ Aguardando pagamento...")

        while True:
            check = requests.post(API + "/check-payment", json={
                "email": email
            }).json()

            if check["status"] == "paid":
                licenca = check["key"]
                print("✅ Pago!")
                print("🔑 Licença:", licenca)
                break

            time.sleep(5)

    else:
        licenca = input("🔑 Licença: ")

    # VALIDAR
    resp = requests.post(API + "/license/validate", json={
        "key": licenca,
        "machine": maquina
    }).json()

    if resp["status"] != "ok":
        print("❌ Licença inválida")
        exit()

    print("✅ Acesso liberado!")

# =========================
# AQUI ENTRA SEU ROBÔ REAL
# =========================
print("🚀 ROBÔ RODANDO...")