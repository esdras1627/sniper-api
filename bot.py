import requests
import time
import uuid
import webbrowser

API = "https://sniper-api-kypc.onrender.com"

maquina = str(uuid.getnode())

# TESTE
trial = requests.post(API + "/trial", json={
    "machine": maquina
}).json()

if trial.get("status") == "active":
    print("🟢 Teste ativo")

else:
    print("🔒 Teste expirado")

    email = input("Digite seu email: ")

    pagamento = requests.post(API + "/create-payment", json={
        "email": email
    }).json()

    print("💰 Abra o link:")
    print(pagamento["payment_url"])

    webbrowser.open(pagamento["payment_url"])

    print("⏳ Aguardando pagamento automático...")

    while True:
        check = requests.post(API + "/check-payment", json={
            "email": email
        }).json()

        if check["status"] == "paid":

            key = check["key"]

            valid = requests.post(API + "/license/validate", json={
                "key": key,
                "machine": maquina
            }).json()

            if valid["status"] == "ok":
                print("✅ Acesso liberado automaticamente!")
                break

        time.sleep(5)

# SEU ROBÔ AQUI
print("🚀 ROBÔ ATIVO")