# https://www.soldev.app/course/intro-to-writing-data

import sys
import requests

from solders.pubkey import Pubkey
from solders.message import MessageV0

from solana.rpc.api import Client

from solders.transaction import VersionedTransaction

from solders.system_program import TransferParams, transfer
from solana.transaction import Transaction

from my_sol_functions import clusterApiUrl, getKeypairFromEnvironment


cluster = "devnet"

sender = getKeypairFromEnvironment("SECRET_KEY")

if len(sys.argv) >=2:
    suppliedToPubkey = sys.argv[1]
    if suppliedToPubkey.lower().endswith(".sol"):
        r = requests.get(f'https://sns-sdk-proxy.bonfida.workers.dev/resolve/{suppliedToPubkey}')

        if r.status_code == 200:
            # Get the serialized transactions to perform the swap
            # Once we have the quote, we need to serialize the quote into a swap transaction that can be submitted on chain.
            suppliedToPubkey = r.json()['result']
    
else:
    print("Please provide a public key to send SOL to!")
    exit(1)

try:
    receiver = Pubkey.from_string(suppliedToPubkey)
    print(f"suppliedToPubkey: {suppliedToPubkey}")
except Exception as e:
    print(f"Invalid public key: {e}")
    print("Please provide a public key to send SOL to!")
    exit(1)


solana_client = Client(clusterApiUrl(cluster))
print("✅ Loaded our own keypair, the destination public key, and connected to Solana")

LAMPORTS_TO_SEND = 5000

instruction = transfer(
    TransferParams(
    from_pubkey=sender.pubkey(), 
    to_pubkey=receiver, 
    lamports=LAMPORTS_TO_SEND))

txn = Transaction().add(instruction)
solana_client = Client(clusterApiUrl("devnet"))
# sent_tx = solana_client.send_transaction(txn, sender)
# print(sent_tx)
# print(sent_tx.value)
# print("\nFee:",solana_client.get_fee_for_message(txn.compile_message()))

# blockhash = Hash.default()
blockhash = solana_client.get_latest_blockhash().value.blockhash

msg = MessageV0.try_compile(
    payer=sender.pubkey(),
    instructions=[instruction],
    address_lookup_table_accounts=[],
    recent_blockhash=blockhash,
)

# Sign the transaction with the required `Signers`
tx = VersionedTransaction(msg, [sender])
print(tx)

# Send the v0 transaction to the cluster
# NOTE: Unlike legacy transactions, sending a VersionedTransaction via sendTransaction 
# does NOT support transaction signing via passing in an array of Signers as the second parameter. 
# That is why we needed to sign the transaction before calling solana_client.sendTransaction().
sent_versioned_tx = solana_client.send_transaction(tx)
print(sent_versioned_tx)
print(sent_versioned_tx.value)
print(f"You can view it here: https://explorer.solana.com/tx/{sent_versioned_tx.value}?cluster={cluster}")
print("\nFee:",solana_client.get_fee_for_message(msg).value, "lamports")