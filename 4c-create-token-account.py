# https://www.soldev.app/course/token-program

# 3. Create an Associated Token Account to store the tokens
import os
from solana.rpc.api import Client
from my_sol_functions import clusterApiUrl, getKeypairFromEnvironment, getExplorerLink
from solders.pubkey import Pubkey

from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID



cluster = "devnet"

solana_client = Client(clusterApiUrl(cluster))

payer = getKeypairFromEnvironment("SECRET_KEY")
owner = payer

print(f"🔑 Loaded our keypair securely, using an env file! Our public key is: {payer.pubkey()}")


tokenMintAccount = Pubkey.from_string(os.environ.get("MINT_ADDRESS_2"))

# Here we are making an associated token account for our own address, but we can 
# make an ATA on any other wallet in devnet!
# recipient = Pubkey.from_string("SOMEONE_ELSES_DEVNET_ADDRESS");
recipient = payer.pubkey()

program_id = TOKEN_PROGRAM_ID

token_client = Token(solana_client, tokenMintAccount, program_id, payer)

created_token_account = token_client.create_associated_token_account(owner.pubkey())

print(f"\ncreated_token_account: {created_token_account}")

token_account_link = getExplorerLink(
  "address",
  str(created_token_account),
  cluster
)

print(f"\ntoken_account_link: {token_account_link}")

