# https://www.soldev.app/course/token-program

# 4. Mint Tokens

import os
from solana.rpc.api import Client
from my_sol_functions import clusterApiUrl, getKeypairFromEnvironment, getExplorerLink
from solders.pubkey import Pubkey

from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID

cluster = "devnet"

solana_client = Client(clusterApiUrl(cluster))

payer = getKeypairFromEnvironment("SECRET_KEY")
mint_authority = payer.pubkey()
multi_signers = [payer]

# Our token has two decimal places
MINOR_UNITS_PER_MAJOR_UNITS = 10 ** 2
amount = 10 * MINOR_UNITS_PER_MAJOR_UNITS

# Subtitute in your token mint account from create-token-mint.ts
tokenMintAccount = Pubkey.from_string(os.environ.get("MINT_ADDRESS_2"))

# Substitute in your own, or a friend's token account address, based on the previous step.
dest = Pubkey.from_string(os.environ.get("Associated_Token_Account_2"))

token_client = Token(solana_client, tokenMintAccount, TOKEN_PROGRAM_ID, payer)

transactionSignature = token_client.mint_to(
  dest=dest,
  mint_authority=mint_authority,
  amount=amount,
  multi_signers=multi_signers
).value

link = getExplorerLink("transaction", transactionSignature, "devnet");

print(f"✅ Success! Mint Token Transaction: {link}")