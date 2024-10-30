import os, json

from fastapi import HTTPException

from .models import ShopOrder, Person, MarketingShipmentRequest, ShopItem
from .util import post_to_noise, post_to_ops
from .agh import create_msr
from .hcb import create_card_grant
CONTEST = os.environ.get('CONTEST', 'Low Skies')
import random
import traceback
class BaseFulfiller:
    pass

class QueueForNightlyFulfiller(BaseFulfiller):
    def __call__(self, order: ShopOrder):
        post_to_noise(f"queueing {order.slack_url()} for nightly {order.shop_item[0].fulfillment_type} run...")
        order.status = "pending_nightly"
        order.save()
class SlackFulfiller(BaseFulfiller):
    def __init__(self, template: str):
        self.template = template
    def __call__(self, order: ShopOrder):
        templated = eval(f"""f\"{self.template}\"""")
        post_to_ops(f"hey <!subteam^S07PYE7FXPT>!\n{templated}")

class SingleAGHFulfiller:
    def __call__(self, order: ShopOrder):
        item: ShopItem = order.shop_item[0]
        print(item.agh_skus)
        skus = json.loads(item.agh_skus)
        msr: MarketingShipmentRequest = create_msr(order, [(sku, order.quantity) for sku in skus], f"{CONTEST} – {item.name}")
        order.mark_fulfilled(msr)

class HCBCardGrantFulfiller:
    def __call__(self, order: ShopOrder):
        item: ShopItem = order.shop_item[0]
        print(order.hcb_email)
        hcb_grant = create_card_grant(order.hcb_email, item.hcb_grant_amount_cents * order.quantity, item.hcb_grant_merchants)
        order.mark_fulfilled(hcb_grant)

class AGHRandomStickersFulfiller:
    def __call__(self, order: ShopOrder):
        item: ShopItem = order.shop_item[0]
        skus = json.loads(item.agh_skus)

        shopping_list = {}

        for i in range(order.quantity):
            x = random.sample(skus, item.agh_random_sticker_count)
            for y in x:
                shopping_list[y] = shopping_list.get(y, 0) + 1
        stickers_to_buy = [(k, v) for k, v in shopping_list.items()]

        msr: MarketingShipmentRequest = create_msr(order, stickers_to_buy, f"{CONTEST} – {item.name}")
        order.mark_fulfilled(msr)

class DummyFulfiller:
    def __call__(self, order: ShopOrder):
        order.mark_fulfilled(":3")

TYPE_MAPPING = {
    "hq_mail": QueueForNightlyFulfiller(),
    "hcb_grant": HCBCardGrantFulfiller() if os.environ.get("HCB_USE_REAL_MONEY") else SlackFulfiller("please create a card grant for {order.slack_url()}!"),
    "agh": SingleAGHFulfiller(),
    "agh_random_stickers": AGHRandomStickersFulfiller(),
    "third_party_physical": QueueForNightlyFulfiller(),
    "third_party_virtual": SlackFulfiller("please do the {order.shop_item_name} thing for {order.slack_url()}!"),
    "dummy": DummyFulfiller(),
    "minuteman": QueueForNightlyFulfiller(),
    "special": QueueForNightlyFulfiller()
}

def fulfill(order: ShopOrder):
    try:
        fulfiller = TYPE_MAPPING[order.shop_item[0].fulfillment_type]
        post_to_noise(f"fulfilling {order.slack_url()} with {fulfiller.__class__.__name__}")
        fulfiller(order)
    except Exception as e:
        order.error = repr(e)
        order.status = "error_fulfilling"
        order.save()
        post_to_ops(f"<@U06QK6AG3RD>: error fulfilling {order.slack_url()}! error was {repr(e)} in {traceback.format_exc()}")
        raise
