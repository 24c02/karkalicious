from api.models import Person, ShopAddress, MarketingShipmentRequest

shop_orderers = Person.all(formula="AND({orders},{first_name})")
print(len(shop_orderers))
j=0
for person in shop_orderers:
    title = "Low Skies stickers courtesy of the raccoon!"
    ref = "low skies heidi campaign - ordered an item in the shop"
    skus = [("Sti/LS/Dra/1st", 1), ("Sti/LS/Dra/2nd", 1)]
    if "item_donate_your_scales_to_heidi_36" in person.orders_items:
        ref = "low skies heidi campaign - donated to heidi"
        title = "a token of heidi's gratitude!"
        skus += [("Sti/Bra/Hak/Fin", 1), ("Sti/Bra/Hei/Pls", 1)]
        j+=1

    addy:ShopAddress = person.address[0]
    print(person.full_name,title, skus)
    print(addy.formatted)

    msr = MarketingShipmentRequest(
        first_name=addy.first_name,
        last_name=addy.last_name,
        email=person.email,
        address_line_1=addy.line_1,
        address_line_2=addy.line_2,
        city=addy.city,
        state_province=addy.state_province,
        zip_postal_code=addy.postal_code,
        country=addy.country,
        custom_instructions=", ".join([f"{qty}x {item}" for item, qty in skus]),
        internal_notes=ref,
        mailer="agh_fulfillment",
        request_type=["low_skies"],
        send_to_warehouse=False,
        state="ready",
        user_facing_title=title,
        phone_number=addy.phone
    )

    msr.save()


print(j)