import os
import pytz
import datetime

from witnesschain import api

tz = os.getenv("TZ")
if tz == None or tz == "":
	tz = "UTC"

timezone	= pytz.timezone(tz)
now		= datetime.datetime.now(timezone)

create_campaign_data = {

	"campaign"		: "my-campaign",
	"description"		: "my-campaign-description",

	"type"			: "individual",

	"tags"			: [
		"campaign",
		"tags"
	],

	# images shown on phone
	"banner_url"		: "https://www.google.com/x.png",
	"poster_url"		: "https://www.google.com/x.png",

	"currency"		: "POINTS",	# What currency will be rewarded to participants
	"total_rewards"		: 10.0,		# The total rewards the campaign can give
	"reward_per_task"	: 2.0,		# rewards per task
	"fuel_required"		: 1.0,		# Fuel that will be spent by the user for this task

	"starts_at"		: now.isoformat(), # When campaign starts and ends
	"ends_at"		: (now + datetime.timedelta(days=10)).isoformat(),

	"max_submissions"	: 10000,	# Max submissions that this campaign can accept

	"is_active"		: False		# if true, makes it immediately available to all users
}

wc_api = api()

wc_api.login()

wc_api.create_campaign(create_campaign_data)

