from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime

app = FastAPI()

# =========================
# BANCO
# =========================
conn = sqlite3.connect("licencas.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS licencas (
    chave TEXT PRIMARY KEY,
    expira TEXT,
    maquina TEXT
)
""")
conn.commit()

# =========================
# MODELO
# =========================
class Licenca(BaseModel):
    chave: str
    maquina: str

# =========================
# VALIDAR
# =========================
@app.post("/validar")
def validar(licenca: Licenca):

    cursor.execute("SELECT * FROM licencas WHERE chave=?", (licenca.chave,))
    dados = cursor.fetchone()

    if not dados:
        return {"status": "invalida"}

    chave, expira, maquina = dados

    # expiração
    if datetime.now() > datetime.strptime(expira, "%Y-%m-%d"):
        return {"status": "expirada"}

    # vincular máquina
    if maquina == "":
        cursor.execute("UPDATE licencas SET maquina=? WHERE chave=?", (licenca.maquina, chave))
        conn.commit()
        return {"status": "ok"}

    elif maquina != licenca.maquina:
        return {"status": "bloqueado"}

    return {"status": "ok"}

# =========================
# CRIAR LICENÇA (ADMIN)
# =========================
@app.post("/criar")
def criar(chave: str, expira: str):
    try:
        cursor.execute("INSERT INTO licencas VALUES (?, ?, '')", (chave, expira))
        conn.commit()
        return {"status": "criada"}
    except:
        return {"status": "erro"}

# =========================
# LISTAR (ADMIN)
# =========================
@app.get("/listar")
def listar():
    cursor.execute("SELECT * FROM licencas")
    dados = cursor.fetchall()
    return {"licencas": dados}