from fastapi import FastAPI
from pydantic import BaseModel
import time, uuid

app = FastAPI()

trials = {}
licenses = {}
payments = {}

# =========================
# MODELOS
# =========================
class Trial(BaseModel):
    machine: str

class Payment(BaseModel):
    email: str

class Validate(BaseModel):
    key: str
    machine: str

# =========================
# HOME
# =========================
@app.get("/")
def home():
    return {"status": "online"}

# =========================
# TESTE 1H
# =========================
@app.post("/trial")
def trial(data: Trial):
    now = time.time()

    if data.machine not in trials:
        trials[data.machine] = now
        return {"status": "active", "restante": 3600}

    inicio = trials[data.machine]

    if now - inicio <= 3600:
        restante = int(3600 - (now - inicio))
        return {"status": "active", "restante": restante}

    return {"status": "expired"}

# =========================
# CRIAR PAGAMENTO (SIMULADO)
# =========================
@app.post("/create-payment")
def create_payment(data: Payment):
    payments[data.email] = {"status": "pending"}

    return {
        "payment_url": "https://google.com",  # troca depois
        "status": "pending"
    }

# =========================
# SIMULAR PAGAMENTO (TESTE)
# =========================
@app.get("/approve/{email}")
def approve(email: str):
    payments[email] = {"status": "paid"}
    return {"status": "aprovado"}

# =========================
# VERIFICAR PAGAMENTO
# =========================
@app.post("/check-payment")
def check_payment(data: Payment):

    if payments.get(data.email, {}).get("status") == "paid":

        key = str(uuid.uuid4())[:10].upper()

        licenses[key] = {
            "machine": None,
            "active": True
        }

        return {"status": "paid", "key": key}

    return {"status": "pending"}

# =========================
# VALIDAR LICENÇA
# =========================
@app.post("/license/validate")
def validate(data: Validate):

    lic = licenses.get(data.key)

    if not lic:
        return {"status": "invalid"}

    if lic["machine"] is None:
        lic["machine"] = data.machine
        return {"status": "ok"}

    if lic["machine"] != data.machine:
        return {"status": "blocked"}

    return {"status": "ok"}