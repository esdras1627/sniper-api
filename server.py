from fastapi import FastAPI, Request
from pydantic import BaseModel
import time, uuid

app = FastAPI()

trials = {}
payments = {}
licenses = {}

# =========================
# MODELOS
# =========================
class Trial(BaseModel):
    machine: str

class CreatePayment(BaseModel):
    email: str

class CheckPayment(BaseModel):
    email: str

class Validate(BaseModel):
    key: str
    machine: str

# =========================
# TRIAL
# =========================
@app.post("/trial")
def trial(data: Trial):
    now = time.time()

    if data.machine not in trials:
        trials[data.machine] = now
        return {"status": "active", "restante": 3600}

    inicio = trials[data.machine]

    if now - inicio <= 3600:
        return {"status": "active", "restante": int(3600 - (now - inicio))}

    return {"status": "expired"}

# =========================
# CRIAR PAGAMENTO (REAL)
# =========================
@app.post("/create-payment")
def create_payment(data: CreatePayment):

    payment_id = str(uuid.uuid4())

    payments[data.email] = {
        "status": "pending",
        "id": payment_id
    }

    return {
        "payment_url": "https://link.mercadopago.com.br/snipertrader",
        "payment_id": payment_id
    }

# =========================
# WEBHOOK (MERCADO PAGO)
# =========================
@app.post("/webhook")
async def webhook(request: Request):
    data = await request.json()

    # Aqui você vai receber dados do pagamento
    # (estrutura depende do Mercado Pago real)

    # SIMPLIFICAÇÃO:
    email = data.get("email")

    if email in payments:
        payments[email]["status"] = "paid"

    return {"status": "ok"}

# =========================
# VERIFICAR PAGAMENTO
# =========================
@app.post("/check-payment")
def check_payment(data: CheckPayment):

    pagamento = payments.get(data.email)

    if pagamento and pagamento["status"] == "paid":

        # cria licença automática
        key = str(uuid.uuid4())[:10].upper()

        licenses[key] = {
            "machine": None
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