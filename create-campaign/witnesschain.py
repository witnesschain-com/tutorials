import os
import sys
import json
import requests

from eth_account.messages import encode_defunct
from eth_account import Account

BASE_URL = "https://mainnet.witnesschain.com/proof/v1/pol"

class api:
#
	def __init__(self):
	#
		self.session = requests.Session()

		if "PRIVATE_KEY" not in os.environ:
			print("===> \033[91mPRIVATE_KEY\033[0m environment variable not found")
			sys.exit(-1)

		self.private_key = os.environ["PRIVATE_KEY"] 

		try:
			self.address = Account.from_key(self.private_key).address
		except:
			print("===> Invalid \033[91mPRIVATE_KEY\033[0m")
			sys.exit(-1)
	#

	def sign(self,msg):
	#
		# Create the message hash
		msghash = encode_defunct(text=msg)

		# Sign the message
		signed_message = Account.sign_message(msghash, self.private_key)

		s = signed_message.signature.hex()

		if s.startswith("0x"):
			return signed_message.signature.hex()
		else:
			return "0x" + signed_message.signature.hex()
	#

	def do_post(self,api,body):
	#
		r = self.session.post (
			url	= BASE_URL + "/" + api,
			data	= body,
			headers = {
				"content-type" : "application/json"
			}
		)

		if r.status_code == 200:
			print("\033[92mSUCCESS\033[0m",r.url)
			print(r.text)
		else:
			print("\033[91mFAILURE\033[0m",r.status_code,r.url)
			print(r.text)
			return None


		j	= json.loads(r.text.encode())
		result	= j["result"]

		return result
	#

	def login (self): 
	#
		r = self.do_post (
			"pre-login",
			json.dumps({
				"role"			: "payer",
				"keyType"		: "ethereum",
				"publicKey"		: self.address,
				"clientVersion"		: "9999999999",
				"walletPublicKey"	: {
					"ethereum" : self.address
				}
			})
		)

		signature = self.sign(r["message"])

		r = self.do_post (
			"login",
			json.dumps({
				"signature" : signature
			})
		)
	#

	def get_balance (self):
	#
		r = self.do_post (
			"my-balance",
			json.dumps({})
		)
	#

	def get_campaigns (self):
	#
		r = self.do_post (
			"campaigns",
			json.dumps({})
		)
	#

	def create_campaign (self,campaign_data):
	#
		r = self.do_post (
			"create-campaign",
			json.dumps(campaign_data)
		)
	#
#
