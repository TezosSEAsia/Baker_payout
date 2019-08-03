# /usr/bin/python3 payout.py 
import json
from urllib.request import urlopen

# set address
baker_address = "tz1R6Ej25VSerE3MkSoEEeBjKHCDTFbpKuSX"
fee_percent = 9.50  # delegation service fee
cycle = 136
#increase the page number if too many delegates
page = 4


totalpayout = 0

for i in range(page):
    with urlopen("https://api1.tzscan.io/v2/rewards_split/" + baker_address + "?cycle=" + str(cycle) +"&p=" + str(i) + "&number=50") as url:
        response = url.read()

    data = json.loads(response.decode("utf-8"))

    total_staking_balance = float(data['delegate_staking_balance'])
    total_rewards = float(data['blocks_rewards']) + float(data['endorsements_rewards']) + float (data['fees']) + float(data['gain_from_denounciation']) - float(data['lost_deposit_from_denounciation']) - float(data['lost_fees_denounciation']) - float(data['lost_rewards_denounciation'])

    for del_balance in data['delegators_balance']:
        delegator_address = del_balance[0]['tz']
        payout = (float(del_balance[1]) / total_staking_balance) * total_rewards
        payout = (payout * (100 - fee_percent)) / 100  # subtract fee
        payout = round(payout / 1000000, 3)  # convert to XTZ
        totalpayout = totalpayout + payout
        print("./tezos-client transfer " + str(payout) + " from " + baker_address + " to "+ delegator_address + " --fee 0.0013" )


print("Total payout for cycle " + str(cycle) + " " + str(totalpayout))
