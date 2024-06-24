# https://www.soldev.app/course/token-program
# https://solana.stackexchange.com/questions/7550/how-to-create-a-metadata-account-with-python

# 2. Make some token metadata

import os

from solders.pubkey import Pubkey
from solders.message import MessageV0
from solana.transaction import AccountMeta, Instruction

from solana.rpc.api import Client
from solana.constants import SYSTEM_PROGRAM_ID

from solders.transaction import VersionedTransaction

from borsh_construct import CStruct, String, U8, U16, U64, Vec, Option, Bool, Enum
from construct import Bytes

from my_sol_functions import clusterApiUrl, getKeypairFromEnvironment, getExplorerLink


system_rent = Pubkey.from_string('SysvarRent111111111111111111111111111111111')

cluster = "devnet"
# print(os.getenv("SECRET_KEY"))
payer = getKeypairFromEnvironment("SECRET_KEY")
solana_client = Client(clusterApiUrl("devnet"))

print(f"`🔑 We've loaded our keypair securely, using an env file! Our public key is: {payer.pubkey()}")

TOKEN_METADATA_PROGRAM_ID = Pubkey.from_string(
  "metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s"
)

# Subtitute in your token mint account
tokenMintAccount = Pubkey.from_string(os.environ.get("MINT_ADDRESS_2"))

tokenMintLink = getExplorerLink(
  "address",
  str(tokenMintAccount),
  "devnet"
)

print(f"✅ Look at the token mint before adding metadata: {tokenMintLink} !")

# metadataData = {
#   "name": "Solana Training Token",
#   "symbol": "TRAINING",
# #   Arweave / IPFS / Pinata etc link using metaplex standard for off-chain data
#   "uri": "https://arweave.net/1234",
#   "sellerFeeBasisPoints": 0,
#   "creators": None,
#   "collection": None,
#   "uses": None
# }


# structure of the instruction
instruction_structure = CStruct(
    "instructionDiscriminator" / U8,
    "createMetadataAccountArgsV3" / CStruct(
        "data" / CStruct(
            "name" / String,
            "symbol" / String,
            "uri" / String,
            "sellerFeeBasisPoints" / U16,
            "creators" / Option(Vec(CStruct(
                "address" / Bytes(32),
                "verified" / Bool,
                "share" / U8
            ))),
            "collection" / Option(CStruct(
                "verified" / Bool,
                "key" / String
            )),
            "uses" / Option(CStruct(
                "useMethod" / Enum(
                    "Burn",
                    "Multiple",
                    "Single",
                    enum_name="UseMethod"
                ),
                "remaining" / U64,
                "total" / U64
            ))
        ),
        "isMutable" / Bool,
        "collectionDetails" / Option(String) # fixme: string is not correct, insert correct type
    )
)

# data for the instruction
instruction_data = {
    "instructionDiscriminator": 33,
    "createMetadataAccountArgsV3": {
        "data": {
            "name": "My Super Token Name",
            "symbol": "SUPER",
            "uri": "https://arweave.net/somewhere",
            "sellerFeeBasisPoints": 500,
            "creators": [
                {
                    "address": bytes(payer.pubkey()),
                    "verified": 1,
                    "share": 100
                }
            ],
            "collection": None,
            "uses": None
        },
        "isMutable": 1,
        "collectionDetails": None
    }
}

metadataPDAAndBump = Pubkey.find_program_address(
    [
        b"metadata",
        bytes(TOKEN_METADATA_PROGRAM_ID),
        bytes(tokenMintAccount),
        ],
        TOKEN_METADATA_PROGRAM_ID
        )

metadataPDA = metadataPDAAndBump[0]


accounts = [\
        AccountMeta(pubkey=metadataPDA, is_signer=False, is_writable=True), # metadata
        AccountMeta(pubkey=tokenMintAccount, is_signer=False, is_writable=False), # mint
        AccountMeta(pubkey=payer.pubkey(), is_signer=True, is_writable=False), # mint authority
        AccountMeta(pubkey=payer.pubkey(), is_signer=True, is_writable=True), # payer
        AccountMeta(pubkey=payer.pubkey(), is_signer=True, is_writable=False), # update authority
        AccountMeta(pubkey=SYSTEM_PROGRAM_ID, is_signer=False, is_writable=False), # system program
        AccountMeta(pubkey=system_rent, is_signer=False, is_writable=False) # rent
]

# create instruction
instruction = Instruction(TOKEN_METADATA_PROGRAM_ID, instruction_structure.build(instruction_data), accounts)

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

tokenMintLink = getExplorerLink(
  "address",
  str(tokenMintAccount),
  "devnet"
)

print(f"✅ Look at the token mint again: {tokenMintLink} !")