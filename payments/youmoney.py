from yoomoney import Authorize, Client, Quickpay
from datetime import datetime
import yaml
import json

# Authorize(
#     client_id='AF99CAB0CB4E190ED904B1C1BC8733DC1899248B716BA3DD273FD349B8DFE74D',
#     redirect_uri='https://t.me/test_work_upco_bot',
#     scope=[
#         'account-info',
#         'operation-history',
#         'operation-details',
#         'incoming-transfers',
#         'payment-p2p',
#         'payment-shop'
#     ]
# )

with open('../config.yaml', 'r') as stream:
    token = yaml.load(stream, yaml.FullLoader)['yoomoney_token']

client = Client(token)
print()

quickpay = Quickpay(
    receiver=str(client.account_info().account),
    quickpay_form='shop',
    targets='Gimmik',
    paymentType='SB',
    sum=2,
    label='fdsagdsa32432fds'
)

print(quickpay.base_url, quickpay.redirected_url, sep='\n')

history = client.operation_history(label='qwerty123')
print(datetime.tzinfo.fget)
for op in history.operations:
    print(op.datetime.strftime('%H:%M'), op.datetime.tzinfo())

# user = client.account_info()
# print("Account number:", user.account)
# print("Account balance:", user.balance)
# print("Account currency code in ISO 4217 format:", user.currency)
# print("Account status:", user.account_status)
# print("Account type:", user.account_type)
# print("Extended balance information:")
# for pair in vars(user.balance_details):
#     print("\t-->", pair, ":", vars(user.balance_details).get(pair))
# print("Information about linked bank cards:")
# cards = user.cards_linked
# if len(cards) != 0:
#     for card in cards:
#         print(card.pan_fragment, " - ", card.type)
# else:
#     print("No card is linked to the account")
