# https://www.soldev.app/course/intro-to-custom-on-chain-programs

from my_sol_functions import clusterApiUrl, getKeypairFromEnvironment, getExplorerLink

import os
from solana.rpc.api import Client
from solders.pubkey import Pubkey
from solders.transaction import VersionedTransaction
# from solders.instruction import Instruction
from solana.transaction import AccountMeta, Instruction
from solders.message import MessageV0


# 1. Basic scaffolding

cluster = "devnet"

solana_client = Client(clusterApiUrl(cluster))

payer = getKeypairFromEnvironment("SECRET_KEY")

# newBalance = solana_client.request_airdrop(
#   payer.pubkey(),
#   10000
# )

# print(newBalance)

# 2. Ping program

PING_PROGRAM_ADDRESS = Pubkey.from_string('ChT1B39WKLS8qUrkLvFDXMhEJ4F1XZzwUNHUt4AU9aVa')
PING_PROGRAM_DATA_ADDRESS =  Pubkey.from_string('Ah9K7dQ8EHaZqcAsgBW8w37yN2eAy3koFmUn4x3CJtod')

# transaction = Transaction()
program_id = PING_PROGRAM_ADDRESS
pingProgramDataId = PING_PROGRAM_DATA_ADDRESS

# create instruction
instruction = Instruction(
    program_id = program_id, 
    data = b"", 
    accounts = [
        AccountMeta(pubkey=pingProgramDataId, is_signer=False, is_writable=True)
        ]
  )

# Create and sign the transaction

blockhash = solana_client.get_latest_blockhash().value.blockhash

msg = MessageV0.try_compile(
    payer=payer.pubkey(),
    instructions=[instruction],
    address_lookup_table_accounts=[],
    recent_blockhash=blockhash,
)

# Sign the transaction with the required `Signers`
tx = VersionedTransaction(msg, [payer])

# Send the v0 transaction to the cluster
# NOTE: Unlike legacy transactions, sending a VersionedTransaction via sendTransaction 
# does NOT support transaction signing via passing in an array of Signers as the second parameter. 
# That is why we needed to sign the transaction before calling solana_client.sendTransaction().
sent_versioned_tx = solana_client.send_transaction(tx)
print(sent_versioned_tx)
print(sent_versioned_tx.value)

transactionLink = getExplorerLink(
  "tx",
  sent_versioned_tx.value,
  "devnet"
)

print(f"✅ Transaction confirmed, explorer link is: {transactionLink} !")