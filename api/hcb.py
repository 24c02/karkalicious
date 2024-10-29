import requests
import os

def create_card_grant(email: str, amount_cents: int, allowed_merchants = None, category_lock = None):
    hcb_api_token = os.environ.get("HCB_API_TOKEN")
    hcb_base_url = os.environ.get("HCB_BASE_URL")
    hcb_org_slug = os.environ.get("HCB_ORG_SLUG")

    if not hcb_api_token:
        raise Exception("missing HCB_API_TOKEN >:-/")
    try:
        response = requests.post(
            f"{hcb_base_url}/api/v4/organizations/{hcb_org_slug}/card_grants",
            headers={
                "Authorization": f"Bearer {hcb_api_token}"
            },
            json={
                "email": email,
                "amount_cents": amount_cents,
                "merchant_lock": allowed_merchants,
                "category_lock": category_lock
            }
        )
    except Exception as e:
        raise

    if response.status_code != 200: raise Exception(f"HCB returned error: {response.json()}")
    print(response.json())
    return f"{hcb_base_url}/grants/{response.json()['id'][4:]}"

def update_transaction_memo(tx_id: str, new_memo: str):
    pass