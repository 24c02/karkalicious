import os
from .util import post_to_ops
from pyairtable import Api
from pyairtable.orm import fields as F
from pyairtable.orm import Model
from functools import cached_property

Model.at_url = lambda self: f"https://airtable.com/{self.Meta.base_id}/{self.Meta.table_name}/{self.id}"
Model.slack_url = lambda self: f"<{self.at_url()}|{type(self).__name__} {self.id}>"

# deadly work:
original_Api_init = Api.__init__
def swizzled_Api_init(
        self,
        api_key: str,
        timeout = None,
        retry_strategy = True,
        endpoint_url: str = "https://api.airtable.com",
        use_field_ids: bool = False
    ):
    original_Api_init(
        self,
        api_key,
        timeout=timeout,
        retry_strategy=retry_strategy,
        endpoint_url=os.environ.get("AIRTABLE_ENDPOINT_URL", "https://api.airtable.com")
    )
Api.__init__ = swizzled_Api_init
class BaseMeta:
    base_id = "appTeNFYcUiYfGcR6"
    api_key = os.environ.get("AIRTABLE_PAT")

class Person(Model):
    class Meta(BaseMeta):
        table_name = 'tblfTzYVqvDJlIYUB' # 'people'

    def invalidate_otp(self):
        self.shop_otp = self.shop_otp_expires_at = None
        self.save()

    identifier = F.TextField('identifier', readonly=True)
    full_name = F.TextField('full_name', readonly=True)
    first_name = F.TextField('first_name', readonly=True)
    last_name = F.TextField('last_name', readonly=True)
    slack_id = F.TextField('slack_id', readonly=True)
    github_username = F.TextField('github_username', readonly=True)
    # ships = F.LinkField['Ship']('ships', model='Ship')
    # battles = F.LinkField['Battle']('battles', model='Battle')
    # event_rsvps = F.LinkField['Event']('event_rsvps', model='Event')
    # host_events = F.LinkField['Event']('host_events', model='Event')
    autonumber = F.AutoNumberField('autonumber', readonly=True)
    # slack_invite_sent = F.CheckboxField('slack_invite_sent')
    # slack_has_signed_in = F.CheckboxField('slack_has_signed_in')
    # user_referred_to_harbor = F.CheckboxField('user_referred_to_harbor')
    # slack_has_been_promoted = F.CheckboxField('slack_has_been_promoted')
    # academy_completed = F.CheckboxField('academy_completed')
    # user_has_graduated = F.NumberField('user_has_graduated', readonly=True)
    settled_tickets = F.NumberField('settled_tickets', readonly=True)
    # shop_true = F.CheckboxField('shop_true')
    shop_customs_acked = F.CheckboxField('shop_customs_acked')
    # help_requests = F.LinkField['Help']('help_requests', model='Help')
    # resolved_help_requests = F.LinkField['Help']('resolved_help_requests', model='Help')
    shop_black_market_enabled = F.CheckboxField('shop_black_market_enabled', readonly=True)
    email = F.EmailField('email', readonly=True)
    orders = F.LinkField['ShopOrder']('orders', model='ShopOrder')
    orders_items = F.TextField('orders__items', readonly=True)
    # ip_address = F.TextField('ip_address')
    address = F.LinkField['ShopAddress']('address', model='ShopAddress')
    shop_otp = F.TextField('shop_otp')
    doubloons_paid = F.NumberField('doubloons_paid', readonly=True)
    doubloons_spent = F.NumberField('doubloons_spent', readonly=True)
    doubloons_balance = F.NumberField('doubloons_balance', readonly=True)
    doubloons_granted = F.NumberField('doubloons_granted', readonly=True)
    shop_dev = F.CheckboxField('shop_dev', readonly=True)
    created_at = F.CreatedTimeField('created_at', readonly=True)
    shop_otp_expires_at = F.DatetimeField('shop_otp_expires_at')
    # doubloon_grants = F.LinkField['DoubloonAdjustment']('doubloon_grants', model='DoubloonAdjustment')
    # vote_balance = F.NumberField('vote_balance', readonly=True)
    # shipped_ship_count = F.CountField('shipped_ship_count')
    # vote_count = F.CountField('vote_count')
    # ships_awaiting_vote_requirement_count = F.CountField('ships_awaiting_vote_requirement_count')
    # ships_with_vote_requirement_met_count = F.CountField('ships_with_vote_requirement_met_count')
    # votes_expended = F.NumberField('votes_expended', readonly=True)
    # minimum_pending_vote_requirement = F.NumberField('minimum_pending_vote_requirement', readonly=True)
    # vote_balance_minus_minimum_pending_requirement = F.NumberField('vote_balance_minus_minimum_pending_requirement', readonly=True)
    ysws_verification_user = F.LinkField['YswsVerification']('YSWS Verification User', model='YswsVerification')
    verification_status = F.LookupField[str]('verification_status')
    # votes_remaining_for_next_pending_ship = F.NumberField('votes_remaining_for_next_pending_ship', readonly=True)
    # votes_required_for_all_pending_ships = F.NumberField('votes_required_for_all_pending_ships', readonly=True)
    # votes_remaining_for_all_pending_ships = F.NumberField('votes_remaining_for_all_pending_ships', readonly=True)
    # unique_vote_count = F.NumberField('unique_vote_count', readonly=True)
    # duplicate_vote_count = F.NumberField('duplicate_vote_count', readonly=True)
    # unique_vote_explanation_count = F.NumberField('unique_vote_explanation_count', readonly=True)
    # duplicate_vote_explanation_count = F.NumberField('duplicate_vote_explanation_count', readonly=True)
    # battles_uniqueness_enforcement_string = F.LookupField[str]('battles__uniqueness_enforcement_string')
    # agggregated_battle_explanations = F.TextField('agggregated_battle_explanations', readonly=True)
    record_id = F.TextField('record_id', readonly=True)
    # aggregated_battle_explanations_length = F.NumberField('aggregated_battle_explanations_length', readonly=True)
    # battles_explanation = F.LookupField[str]('battles__explanation')
    # aggregate_discordance = F.NumberField('aggregate_discordance', readonly=True)
    # trust_factor = F.PercentField('trust_factor', readonly=True)
    # mean_discordance = F.NumberField('mean_discordance', readonly=True)
    # slack_promotion_requested = F.CheckboxField('slack_promotion_requested')
    # eligible_to_vote = F.NumberFixeld('eligible_to_vote', readonly=True)
    verification_alum = F.LookupField[bool]('verification_alum')
    # has_ordered_free_stickers = F.CheckboxField('has_ordered_free_stickers', readonly=True)
    free_stickers_dupe_check = F.CheckboxField('free_stickers_dupe_check', readonly=True)

class ShopItem(Model):
    class Meta(BaseMeta):
        table_name = 'tblGChU9vC3QvswAV' # 'shop_items'

    identifier = F.TextField('identifier', readonly=True)
    name = F.TextField('name')
    subtitle = F.TextField('subtitle')
    description = F.TextField('description')
    image_url = F.TextField('image_url')
    tickets_us = F.NumberField('tickets_us')
    tickets_global = F.NumberField('tickets_global')
    doubloons_estimated = F.NumberField('doubloons_estimated', readonly=True)
    unit_cost = F.CurrencyField('unit_cost')
    fair_market_value = F.CurrencyField('fair_market_value')
    hacker_score = F.PercentField('hacker_score')
    fulfillment_type = F.SelectField('fulfillment_type')
    orders = F.LinkField['ShopOrder']('orders', model='ShopOrder')
    autonumber = F.AutoNumberField('autonumber')
    needs_addy = F.CheckboxField('needs_addy', readonly=True)
    agh_skus = F.TextField('agh_skus')
    hcb_grant_merchants = F.TextField('hcb_grant_merchants')
    hq_mail_item_description = F.TextField('hq_mail_item_description')
    enabled = F.CheckboxField('enabled')
    enabled_us = F.CheckboxField('enabled_us')
    enabled_eu = F.CheckboxField('enabled_eu')
    enabled_in = F.CheckboxField('enabled_in')
    enabled_xx = F.CheckboxField('enabled_xx')
    enabled_ca = F.CheckboxField('enabled_ca')
    fillout_key = F.TextField('fillout_key')
    additional_question = F.TextField('additional_question')
    customs_likely = F.CheckboxField('customs_likely')
    max_qty_per_order = F.NumberField('max_qty_per_order')
    requires_black_market = F.CheckboxField('requires_black_market')
    third_party_link_us = F.TextField('third_party_link_us')
    third_party_link_in = F.TextField('third_party_link_in')
    third_party_link_eu = F.TextField('third_party_link_eu')
    hcb_grant_amount_cents = F.NumberField('hcb_grant_amount_cents')
    fillout_base_url = F.TextField('fillout_base_url', readonly=True)
    fulfilled_at_end = F.CheckboxField('fulfilled_at_end', readonly=True)
    no_no_countries = F.TextField('no-no_countries')
    additional_text = F.RichTextField('additional_text')
    enabled_high_seas = F.CheckboxField('enabled_high_seas')
    skip_manual_validation = F.CheckboxField('skip_manual_validation')
    agh_random_sticker_count = F.NumberField('agh_random_sticker_count')
    coming_soon = F.CheckboxField('coming_soon')





class ShopOrder(Model):
    class Meta(BaseMeta):
        table_name = 'tbl7Dj23N5tjLanM4' # 'shop_orders'

    identifier = F.TextField('identifier', readonly=True)
    shop_item = F.LinkField['ShopItem']('shop_item', model='ShopItem')
    shop_item_name = F.LookupField[str]('shop_item:name')
    recipient = F.LinkField['Person']('recipient', model='Person')
    recipient_full_name = F.LookupField[str]('recipient:full_name')
    recipient_email = F.LookupField[str]('recipient:email')
    hcb_email = F.LookupField[str]('hcb_email')
    autonumber = F.AutoNumberField('autonumber')
    status = F.SelectField('status')
    addr_first_name = F.TextField('addr_first_name')
    addr_last_name = F.TextField('addr_last_name')
    addr_line1 = F.TextField('addr_line1')
    addr_line2 = F.TextField('addr_line2')
    addr_line3 = F.TextField('addr_line3')
    addr_city = F.TextField('addr_city')
    addr_state_province = F.TextField('addr_state_province')
    addr_postal_code = F.TextField('addr_postal_code')
    addr_country = F.TextField('addr_country')
    addr_phone = F.TextField('addr_phone')
    addr_seq = F.NumberField('addr_seq')
    tickets_paid = F.NumberField('tickets_paid', readonly=True)
    quantity = F.NumberField('quantity')
    additional_q_resp = F.TextField('additional_q_resp')
    customs_acked = F.CheckboxField('customs_acked')
    unit_price_paid = F.NumberField('unit_price_paid')
    record_id = F.TextField('record_id', readonly=True)
    rejection_reason = F.TextField('rejection_reason')
    huh = F.CheckboxField('huh')
    recipient_slack_id = F.LookupField[str]('recipient:slack_id')
    external_ref = F.TextField('external_ref')
    error = F.TextField('error')
    dev = F.CheckboxField('dev')


    def reject(self, rejection_reason: str):
        self.status = "REJECTED"
        self.rejection_reason = rejection_reason
        self.save()
        post_to_ops(f"{self.recipient_full_name[0]}'s {self.slack_url()} was rejected!\nreason: {rejection_reason}")
        return "rejected"

    def mark_fulfilled(self, ref, custom_message=None):
        self.status = "fulfilled"
        self.external_ref = str(ref)
        self.save()
        if(isinstance(ref, Model)):
            ref = ref.slack_url()
        post_to_ops(custom_message or f"{self.recipient_full_name[0]}'s {self.slack_url()} for {self.shop_item_name[0]} was automatically fulfilled! (ref {ref})")


# THIS IS FUCKING GROSS
setattr(ShopOrder, "at_url", lambda self: f"https://airtable.com/{self.Meta.base_id}/{self.Meta.table_name}/viwTVymHDzpUIlkIK/{self.id}")

class YswsVerification(Model):
    class Meta(BaseMeta):
        table_name = 'tblM3cGY2vCzNaJO7' # 'YSWS Verification'

class ShopAddress(Model):
    class Meta(BaseMeta):
        table_name = 'tblYxntrYxcTewLJW' # 'shop_addresses'

    identifier = F.TextField('identifier', readonly=True)
    person = F.LinkField['Person']('person', model='Person')
    person_identifier = F.LookupField[str]('person:identifier')
    person_shop_otp = F.LookupField[str]('person:shop_otp')
    first_name = F.TextField('first_name')
    last_name = F.TextField('last_name')
    line_1 = F.TextField('line_1')
    line_2 = F.TextField('line_2')
    line_3 = F.TextField('line_3')
    city = F.TextField('city')
    state_province = F.TextField('state_province')
    postal_code = F.TextField('postal_code')
    country = F.TextField('country')
    phone = F.PhoneNumberField('phone')
    formatted = F.TextField('formatted', readonly=True)
    sequence_number = F.NumberField('sequence_number')

class MarketingShipmentRequest(Model):
    class Meta:
        table_name = 'tbltnDSvmiUH0grQo' # 'Shipment Requests'
        base_id = "appK53aN0fz3sgJ4w"
        api_key = os.environ.get("AIRTABLE_PAT")

    ident = F.TextField('ID', readonly=True)
    first_name = F.TextField('First Name')
    last_name = F.TextField('Last Name')
    email = F.TextField('Email')
    address_line_1 = F.TextField('Address (Line 1)')
    address_line_2 = F.TextField('Address (Line 2)')
    city = F.TextField('City')
    state_province = F.TextField('State / Province')
    zip_postal_code = F.TextField('ZIP / Postal Code')
    country = F.TextField('Country')
    copy_paste = F.TextField('Copy & Paste', readonly=True)
    type = F.SelectField('Type')
    date_fulfilled = F.DateField('Date Fulfilled')
    send_to_warehouse = F.CheckboxField('Send To Warehouse')
    request_type = F.MultipleSelectField('Request Type')
    date_requested = F.CreatedTimeField('Date Requested')
    custom_instructions = F.TextField('Custom Instructions')
    internal_notes = F.RichTextField('Internal Notes')
    warehouse_postage_cost = F.CurrencyField('Warehouse–Postage Cost')
    warehouse_labor_cost = F.CurrencyField('Warehouse–Labor Cost')
    warehouse_total_cost = F.CurrencyField('Warehouse–Total Cost', readonly=True)
    warehouse_service = F.TextField('Warehouse–Service')
    warehouse_tracking_url = F.UrlField('Warehouse–Tracking URL')
    warehouse_tracking_number = F.TextField('Warehouse–Tracking Number')
    warehouse_items_shipped_json = F.TextField('Warehouse–Items Shipped JSON')
    confirmation_email_sent_automation = F.DatetimeField('Confirmation Email Sent (Automation)')
    sort_automation = F.DateField('Sort (Automation)', readonly=True)
    airtable_id_automation = F.TextField('Airtable ID (Automation)', readonly=True)
    tracking_number_email_sent_automation = F.DatetimeField('Tracking Number Email Sent (Automation)')
    created_by = F.CreatedByField('Created By')
    autonumber = F.AutoNumberField('autonumber')
    surprise = F.CheckboxField('surprise')
    state = F.SelectField('state')
    mailer = F.SelectField('mailer')
    warehouse_contents_json = F.TextField('warehouse_contents_json')
    applied_fixups = F.TextField('applied_fixups')
    rejection_reason = F.TextField('rejection_reason')
    phone_number = F.TextField('phone_number')
    user_facing_title = F.TextField('user_facing_title')


class ArrpheusMessageRequest(Model):
    class Meta(BaseMeta):
        table_name = 'tblryPue7qfuQnfeJ' # 'arrpheus_message_requests'

    autonumber = F.AutoNumberField('autonumber')
    created_at = F.CreatedTimeField('created_at')
    requester_identifier = F.TextField('requester_identifier')
    target_slack_id = F.TextField('target_slack_id')
    message_text = F.TextField('message_text')
    message_blocks = F.TextField('message_blocks')
    send_success = F.CheckboxField('send_success')
    send_failure = F.CheckboxField('send_failure')
    failure_reason = F.TextField('failure_reason')