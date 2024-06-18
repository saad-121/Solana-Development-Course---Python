# https://www.soldev.app/course/intro-to-cryptography
# https://kevinheavey.github.io/solders/tutorials/keypairs.html#generating-a-new-keypair


from solders.keypair import Keypair

import json

import os

# Generating a new keypair
keypair = Keypair()
print(f"\nCreated a new Keypair with public key: {keypair.pubkey()}")
print(f"\nHere is the private key: {keypair.to_bytes_array()}")

# Converting a keypair to raw bytes
# To get the raw bytes of a keypair object you just call bytes(keypair):
raw = bytes(keypair)
print(f"\nHere are the raw bytes of the new Keypair : {raw}")


# Restoring a keypair from a secret
# If you already have the 64-byte secret key, you can use Keypair.from_bytes:
secret_key = [
    174, 47, 154, 16, 202, 193, 206, 113,
    199, 190, 53, 133, 169, 175, 31, 56,
    222, 53, 138, 189, 224, 216, 117, 173,
    10, 149, 53, 45, 73, 251, 237, 246,
    15, 185, 186, 82, 177, 240, 148, 69,
    241, 227, 167, 80, 141, 89, 240, 121,
    121, 35, 172, 247, 68, 251, 226, 218,
    48, 63, 176, 109, 168, 89, 238, 135,
]

keypair = Keypair.from_bytes(secret_key)
print(f"\nCreated Keypair with public key: {keypair.pubkey()}")
print(f"\nHere is the private key: {keypair.to_bytes_array()}")


# You can also import it from environment
secret_key = json.loads(os.environ.get("SECRET_KEY"))
# print(f"\nsecret_key {secret_key}")

keypair = Keypair.from_bytes(secret_key)
print(f"\nImported Keypair from secret key in environment. The keypair has this public key: {keypair.pubkey()}")
