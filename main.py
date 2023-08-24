import os
import requests
import time
import json
import fgourl
import user
import coloredlogs
import logging

# User - Enviroments Variables
userIds = os.environ['userIds'].split(',')
authKeys = os.environ['authKeys'].split(',')
secretKeys = os.environ['secretKeys'].split(',')

# User Agen - Enviroments Variables
user_agent = os.environ['UserAgent']
if user_agent != 'nullvalue':
    fgourl.user_agent_ = user_agent

# Region - Enviroments Variables
fate_regions = os.environ['fateRegion'].split(',')
fate_region = NULL

# Webhook - Enviroments Variables
webhook_discord_url = os.environ['webhookDiscord']

# Keys
userNums = len(userIds)
authKeyNums = len(authKeys)
secretKeyNums = len(secretKeys)
fateRegionsNums = len(fate_regions)

# Logger
logger = logging.getLogger("FGO Daily Login")
coloredlogs.install(fmt='%(asctime)s %(name)s %(levelname)s %(message)s')

def get_latest_verCode():
    endpoint = ""

    if fate_region == "NA":
        endpoint += "https://raw.githubusercontent.com/O-Isaac/FGO-VerCode-extractor/NA/VerCode.json"
    else:
        endpoint += "https://raw.githubusercontent.com/O-Isaac/FGO-VerCode-extractor/JP/VerCode.json"

    response = requests.get(endpoint).text
    response_data = json.loads(response)

    return response_data['verCode']


def main():
    global fate_region

    if userNums == authKeyNums and userNums == secretKeyNums and userNums == fateRegionsNums:
        for i in range(userNums):
            fate_region = fate_regions[i]

            logger.info('Getting Lastest Assets Info')
            fgourl.set_latest_assets()
            
            try:
                instance = user.user(userIds[i], authKeys[i], secretKeys[i])
                time.sleep(3)
                logger.info('Loggin into account!')
                instance.topLogin()
                time.sleep(2)
                instance.topHome()
                time.sleep(2)
                logger.info('Throw daily friend summon!')
                instance.drawFP()
                time.sleep(2)
            except Exception as ex:
                logger.error(ex)
    else:
        logger.error("The environment variables are misconfigured.")

if __name__ == "__main__":
    main()
