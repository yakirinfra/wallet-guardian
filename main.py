from fastapi import FastAPI, HTTPException
from uuid import uuid4
from datetime import datetime

from models import CreateWalletRequest, TransactionRequest
from policy import evaluate_transaction

app = FastAPI(title="Wallet Guardian - Custody Policy Engine")

wallets = {}
audit_log = []


@app.get("/")
def health_check():
    return {
        "project": "Wallet Guardian",
        "status": "running",
        "description": "Policy-based wallet management simulator for BILS custody flows"
    }


@app.post("/wallet/create")
def create_wallet(request: CreateWalletRequest):
    wallet_id = str(uuid4())

    wallet = {
        "wallet_id": wallet_id,
        "name": request.name,
        "role": request.role,
        "address": f"SOL_{uuid4().hex[:12].upper()}",
        "asset": request.asset,
        "balance": request.initial_balance,
        "created_at": datetime.utcnow().isoformat()
    }

    wallets[wallet_id] = wallet

    audit_log.append({
        "timestamp": datetime.utcnow().isoformat(),
        "action": "WALLET_CREATED",
        "wallet_id": wallet_id,
        "wallet_name": request.name,
        "role": request.role
    })

    return wallet


@app.get("/wallets")
def get_wallets():
    return wallets


@app.post("/tx/request")
def request_transaction(tx: TransactionRequest):
    wallet = wallets.get(tx.from_wallet_id)

    if not wallet:
        raise HTTPException(status_code=404, detail="Source wallet not found")

    decision = evaluate_transaction(tx, wallet)

    record = {
        "timestamp": datetime.utcnow().isoformat(),
        "from_wallet_id": tx.from_wallet_id,
        "from_wallet_name": wallet["name"],
        "to_address": tx.to_address,
        "amount": tx.amount,
        "asset": tx.asset,
        "decision": decision["decision"],
        "reason": decision["reason"]
    }

    if decision["decision"] == "APPROVED":
        wallet["balance"] -= tx.amount
        record["execution_status"] = "SIMULATED_EXECUTED"
    elif decision["decision"] == "PENDING_APPROVAL":
        record["execution_status"] = "WAITING_FOR_APPROVAL"
    else:
        record["execution_status"] = "NOT_EXECUTED"

    audit_log.append(record)

    return record


@app.get("/audit-log")
def get_audit_log():
    return audit_log