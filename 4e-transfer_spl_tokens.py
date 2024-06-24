# https://www.soldev.app/course/token-program

# 5. Transfer Tokens

from my_sol_functions import clusterApiUrl, getKeypairFromEnvironment, getExplorerLink, getOrCreateAssociatedTokenAccount

import os
from solana.rpc.api import Client
from solders.pubkey import Pubkey

from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID



cluster = "devnet"

solana_client = Client(clusterApiUrl(cluster))

sender = getKeypairFromEnvironment("SECRET_KEY")
payer = sender
mint_authority = sender.pubkey()
multi_signers = [sender]

recipient = getKeypairFromEnvironment("SECRET_KEY_2")

# Our token has two decimal places
MINOR_UNITS_PER_MAJOR_UNITS = 10 ** 2
amount = 1 * MINOR_UNITS_PER_MAJOR_UNITS

# Subtitute in your token mint account from create-token-mint.ts
tokenMintAccount = Pubkey.from_string(os.environ.get("MINT_ADDRESS_2"))

token_client = Token(solana_client, tokenMintAccount, TOKEN_PROGRAM_ID, payer)

print(f"💸 Attempting to send 1 token to {recipient}...")

# Get or create the source and destination token accounts to store this token
sourceTokenAccount = getOrCreateAssociatedTokenAccount(
  payer,
  sender,
  token_client
)

destinationTokenAccount = getOrCreateAssociatedTokenAccount(
  payer,
  recipient,
  token_client
)

# Transfer the tokens
transactionSignature = token_client.transfer(
  source = sourceTokenAccount,
  dest = destinationTokenAccount,
  owner = sender,
  amount = amount,
  multi_signers=multi_signers
).value

link = getExplorerLink("transaction", transactionSignature, "devnet")

print(f"✅ Transaction confirmed, explorer link is: {link}")