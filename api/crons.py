from fastapi import APIRouter
from .models import ShopOrder, Person
from .tasks import validate_and_freeze_order
from pyairtable.formulas import match, AND, FIELD, GREATER_EQUAL, to_airtable_value
from .util import post_to_noise
from datetime import datetime
from os import environ

router = APIRouter(
    prefix="/cron"
)

@router.get("/process_fresh_orders")
def process_fresh_orders():
    # 10 mins to fix race condition where cron runs as on-demand processing is happening
    unprocessed_orders = ShopOrder.all(formula=f'AND({match({"status": "fresh", "dev": environ.get("ENV") == "DEV"})}, DATETIME_DIFF(NOW(), CREATED_TIME(), "minutes") > 10)')
    if not unprocessed_orders:
        return {"count":0}

    post_to_noise(f"hey <@U06QK6AG3RD> - :-/ fresh orders cron had {len(unprocessed_orders)} hits, what's up with that?")
    for order in unprocessed_orders:
        validate_and_freeze_order(order, save=False)
    return {'count': len(unprocessed_orders)}

@router.get("/expire_outstanding_otps")
def expire_outstanding_otps():
    post_to_noise("expiring outstanding otps...")
    people_with_outstanding_otps = Person.all(formula=f"AND(NOT({{shop_dev}}), {{shop_otp_expires_at}}, NOW() > {{shop_otp_expires_at}})")
    for person in people_with_outstanding_otps:
        person.shop_otp = person.shop_otp_expires_at = None
    Person.batch_save(people_with_outstanding_otps)

# @router.get("/agh_nightlies") # not a thing yet
# def agh_nightly_batch():
#     unprocessed_orders = ShopOrder.all(formula=match({"status": "fresh"}))
