# https://www.soldev.app/course/intro-to-reading-data
# https://github.com/Bonfida/sns-sdk/tree/main

from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.keypair import Keypair

import json

import os
from my_sol_functions import clusterApiUrl, LAMPORTS_PER_SOL

import sys

import requests

solana_client = Client(clusterApiUrl("devnet"))

# address = Pubkey.from_string('CenYq6bDRB7p73EjsPEpiYN7uveyPUTdXkDkgUduboaN')

# You can also import your address by using the secret key
secret_key = json.loads(os.environ.get("SECRET_KEY"))

address = Keypair.from_bytes(secret_key).pubkey()

# lamps = 1 * LAMPORTS_PER_SOL
# # Request an airdrop (in lamports, 1 SOL = 1,000,000,000 lamports)
# airdrop_signature = solana_client.request_airdrop(address, 1000000000)

# # Confirm the airdrop transaction
# confirmation = solana_client.confirm_transaction(airdrop_signature['result'])
# print(confirmation)

balance = solana_client.get_balance(address).value
print(f"The balance of the account at {address} is {balance} lamports.")

balanceInSol = balance / LAMPORTS_PER_SOL
print(f"The balance of the account at {address} is {balanceInSol} SOL.")

# Check other student's balances
# You can modify the script to check balances on any wallet.

if len(sys.argv) >=2:
    suppliedPublicKey = sys.argv[1]
    if suppliedPublicKey.lower().endswith(".sol"):
        r = requests.get(f'https://sns-sdk-proxy.bonfida.workers.dev/resolve/{suppliedPublicKey}')

        if r.status_code == 200:
            # Get the serialized transactions to perform the swap
            # Once we have the quote, we need to serialize the quote into a swap transaction that can be submitted on chain.
            suppliedPublicKey = r.json()['result']
    
else:
    print("Provide a public key to check the balance of!")
    exit()

try:
    publicKey = Pubkey.from_string(suppliedPublicKey)
except Exception as e:
    print(f"Invalid public key: {e}")
    print("Provide a public key to check the balance of!")
    exit()

balanceInLamports = solana_client.get_balance(publicKey).value

balanceInSOL = balanceInLamports / LAMPORTS_PER_SOL

print(
  f"✅ Finished! The balance for the wallet at address {publicKey} is {balanceInSOL} SOL!"
)