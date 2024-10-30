import os

from .models import Person, ShopOrder, ShopAddress, ShopItem
from .util import post_to_ops, post_to_noise
COUNTRY_US = "United States"
COUNTRY_INDIA = "India"
COUNTRY_CANADA = "Canada"
EU_COUNTRIES = [
    "Austria",
    "Belgium",
    "Bulgaria",
    "Croatia",
    "Cyprus"
    "Czech Republic",
    "Denmark",
    "Estonia",
    "Finland",
    "France",
    "Germany",
    "Greece",
    "Hungary",
    "Ireland",
    "Italy",
    "Latvia",
    "Lithuania",
    "Luxembourg",
    "Malta",
    "Netherlands",
    "Poland",
    "Portugal",
    "Romania",
    "Slovakia",
    "Spain",
    "Sweden"
]

def freeze_address(order: ShopOrder, person: Person):
    address: ShopAddress = person.address[0]

    order.addr_first_name = address.first_name
    order.addr_last_name = address.last_name
    order.addr_line1 = address.line_1
    order.addr_line2 = address.line_2
    order.addr_line3 = address.line_3
    order.addr_city = address.city
    order.addr_state_province = address.state_province
    order.addr_postal_code = address.postal_code
    order.addr_country = address.country
    order.addr_phone = address.phone
    order.addr_seq = address.sequence_number

    order.save()

def validate_and_freeze_order(order: ShopOrder, save=True):
    post_to_noise(f"doing initial processing on {order.slack_url()}")
    item: ShopItem = order.shop_item[0]
    person: Person = order.recipient[0]
    freeze_address(order, person)
    person.invalidate_otp()

    item_is_free_stickers = item.id == "recHByvKaaeXaGsPq"

    if item_is_free_stickers and person.has_ordered_free_stickers:
        return order.reject("you've already ordered some!")
    #
    # if item.coming_soon:
    #     return order.reject("this item isn't available yet!")
    if not order.quantity: order.quantity = 1
    if order.quantity < 0: return order.reject("ya gotta order at least one :-P")
    order.save()
    person.fetch()
    # rejected unless free sticekrs

    if person.verification_alum[0]:
        return order.reject("you've ascended past eligibility for this program...")
    if person.verification_status[0] == "Ineligible":
        return order.reject("you're marked as ineligible for this program :-(")

    if person.verification_status[0] not in ["Eligible L1", "Eligible L2"]:
        if not item_is_free_stickers:
            return order.reject(f"you need to <https://forms.hackclub.com/eligibility?program={os.environ.get('CONTEST', 'Low Skies')}&slack_id={person.slack_id}|verify your identity> first.")
        order.status = "AWAITING_YSWS_VERIFICATION"
        return order.save()
        # return order.reject("you need to verify your identity first.")


    if not item.enabled and not person.shop_dev and not item_is_free_stickers: return order.reject("this item isn't available.")

    expected_price = item.tickets_us

    if item.needs_addy:
        # freeze_address(order, person)
        if order.customs_acked:
            person.shop_customs_acked = True
            person.save()

        if order.addr_country == COUNTRY_US: regional_enable = item.enabled_us
        elif order.addr_country == COUNTRY_INDIA: regional_enable = item.enabled_in
        elif order.addr_country in EU_COUNTRIES: regional_enable = item.enabled_eu
        elif order.addr_country == COUNTRY_CANADA: regional_enable = item.enabled_ca
        else: regional_enable = item.enabled_xx

        if not regional_enable: return order.reject("this item isn't available in your region.")

        if item.no_no_countries:
            nnc = item.no_no_countries.split("|")
            if order.addr_country in nnc:
                return order.reject(f"we can't ship that to {order.addr_country}!")

        expected_price = item.tickets_us if order.addr_country == COUNTRY_US else item.tickets_global

    if order.unit_price_paid != expected_price: return order.reject("there was a pricing error? this shouldn't ever happen, please DM <@U06QK6AG3RD>.")

    if order.tickets_paid > person.settled_tickets: return order.reject("you can't afford it :-(")

    if os.environ["FOR_REALZ"] == "yeah!" or item.skip_manual_validation:
        order.status = "in_flight"
        post_to_noise(f"{order.slack_url()} is good, now in flight!")
    else:
        order.status = "PENDING_MANUAL_REVIEW"
        post_to_ops(f"hey <!subteam^S07PYE7FXPT>, {order.slack_url()} is waiting for you! set it to in_flight if it's good to go :3")
    order.save()

    return "in_flight"
