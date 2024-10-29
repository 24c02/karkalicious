from .models import MarketingShipmentRequest, ShopOrder, ShopItem, Person

ALWAYS_INCLUDED_ITEMS = [
    # ("Pri/Arc/4x6/Wel", 1)
]

def create_msr(order: ShopOrder, contents, user_facing_title, ref=None):
    if ref is None: ref = str(order)
    item: ShopItem = order.shop_item[0]
    person: Person = order.recipient[0]
    contents = [*ALWAYS_INCLUDED_ITEMS, *contents]

    msr = MarketingShipmentRequest(
        first_name=order.addr_first_name,
        last_name=order.addr_last_name,
        email=person.email,
        address_line_1=order.addr_line1,
        address_line_2=order.addr_line2,
        city=order.addr_city,
        state_province=order.addr_state_province,
        zip_postal_code=order.addr_postal_code,
        country=order.addr_country,
        custom_instructions=", ".join([f"{qty}x {item}" for item, qty in contents]),
        internal_notes=ref,
        mailer="agh_fulfillment",
        request_type=["low_skies"],
        send_to_warehouse=True,
        state="ready",
        user_facing_title=user_facing_title,
        phone_number=order.addr_phone
    )

    msr.save()
    return msr

