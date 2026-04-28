WHITELIST = [
    "SOL_APPROVED_VENDOR",
    "SOL_COMPANY_WALLET",
    "SOL_ETORO_DEMO"
]

MAX_SINGLE_TX = 5000


def evaluate_transaction(tx, wallet):
    if tx.asset != wallet["asset"]:
        return {
            "decision": "BLOCKED",
            "reason": "Asset mismatch"
        }

    if tx.amount > wallet["balance"]:
        return {
            "decision": "BLOCKED",
            "reason": "Insufficient balance"
        }

    if tx.to_address not in WHITELIST:
        return {
            "decision": "BLOCKED",
            "reason": "Destination address is not whitelisted"
        }

    if tx.amount > MAX_SINGLE_TX:
        return {
            "decision": "PENDING_APPROVAL",
            "reason": "Amount exceeds single transaction limit"
        }

    return {
        "decision": "APPROVED",
        "reason": "Transaction passed all custody policy checks"
    }