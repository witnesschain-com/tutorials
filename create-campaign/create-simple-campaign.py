import os
import pytz
import datetime
import json
from dotenv import load_dotenv

from witnesschain import api

# Get timezone
tz = os.getenv("TZ")
if tz == None or tz == "":
    tz = "UTC"

timezone = pytz.timezone(tz)
now = datetime.datetime.now(timezone)
load_dotenv()

# Load campaign configuration from JSON file
config_file = './campaign_config.json'

try:
    with open(config_file, 'r') as f:
        campaign_config = json.load(f)
except FileNotFoundError:
    print(f"Error: Configuration file '{config_file}' not found.")
    exit(1)
except json.JSONDecodeError:
    print(f"Error: Invalid JSON in configuration file '{config_file}'.")
    exit(1)

# Add timestamp information
campaign_config["starts_at"] = now.isoformat()
campaign_config["ends_at"] = (now + datetime.timedelta(days=10)).isoformat()

# Initialize API and create campaign
try:
    wc_api = api()
    wc_api.login()
    result = wc_api.create_campaign(campaign_config)
    print(f"Campaign created successfully: {result}")
except Exception as e:
    print(f"Error creating campaign: {str(e)}")