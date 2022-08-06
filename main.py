from datetime import *
from keep_alive import keep_alive
from pytz import timezone

import discord
import json
import os
import requests



# Variables

intents = discord.Intents.default()
intents.members = True

channel_holidays = 000000000000000000 # put your notification channel ID here
client = discord.Client(intents = intents)

test_json = \
'''
[
  {
    "name": "Assumption of Mary",
    "name_local": "",
    "language": "",
    "description": "",
    "country": "LB",
    "location": "Lebanon",
    "type": "National",
    "date": "08/15/2020",
    "date_year": "2020",
    "date_month": "08",
    "date_day": "15",
    "week_day": "Saturday"
  }
]
'''



# Defined Method - On Ready

@client.event
async def on_ready():
	print("We have logged in as {0.user}".format(client))
	await infinite_timer()



# Defined Methods

def get_holidays(date: datetime):
	day = date.strftime("%d")
	month = date.strftime("%m")
	year = date.strftime("%Y")
	request = requests.get("https://holidays.abstractapi.com/v1/?api_key=" + os.environ["API_KEY"] + "&country=LB&year=" + year + "&month=" + month + "&day=" + day)
	return json.loads(request.text)


async def infinite_timer():
	has_sent_message = False
	while True:
		now = datetime.now(timezone("Asia/Beirut"))
		if now.strftime("%H:%M") == "06:00" and not has_sent_message:
			holidays = get_holidays(now)
			await send_holidays(holidays)
			has_sent_message = True
		elif not has_sent_message:
			has_sent_message = False

async def send_holidays(holidays: list):
	channel = client.get_channel(channel_holidays)
	for holiday in holidays:
		country = "in Lebanon"
		date = holiday["date_year"] + "-" + holiday["date_month"] + "-" + holiday["date_day"]
		name = holiday["name"]
		is_day_off = False
		if holiday["country"] != "LB": country = "throughout the world"
		await channel.send("🎉 **" + name + "**\nToday, __" + date + "__, let's celebrate this special day " + country + "!")
		if holiday["country"] != "LB": await channel.send("Let's make the most of this day off together!")



# Called Methods

keep_alive()
client.run(os.environ["TOKEN"])
