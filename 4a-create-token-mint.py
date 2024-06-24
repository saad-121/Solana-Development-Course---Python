# https://www.soldev.app/course/token-program
# https://michaelhly.com/solana-py/spl/token/client/#spl.token.client.Token.create_mint

# 1. Create the Token Mint

from solana.rpc.api import Client
from spl.token.client import Token
from spl.token.constants import TOKEN_PROGRAM_ID

from my_sol_functions import clusterApiUrl, getKeypairFromEnvironment, get_latest_blockhash_value, getExplorerLink

cluster = "devnet"

solana_client = Client(clusterApiUrl(cluster))


user = getKeypairFromEnvironment("SECRET_KEY")
print(f"🔑 Loaded our keypair securely, using an env file! Our public key is: {user.pubkey()}")

blockhash = get_latest_blockhash_value()
token_client = Token(solana_client, user.pubkey(), TOKEN_PROGRAM_ID, user)
tokenMint = token_client.create_mint( # Create and initialize a token.
    conn=solana_client, # RPC connection to a solana cluster.
    payer = user, # Fee payer for transaction.
    mint_authority = user.pubkey(), # Account or multisig that will control minting.
    decimals = 2, # Location of the decimal place.
    program_id = TOKEN_PROGRAM_ID, # SPL Token program account.
    freeze_authority = None, # (optional) Account or multisig that can freeze token accounts.
    skip_confirmation = False, # (optional) Option to skip transaction confirmation. 
    # If skip confirmation is set to False, this method will block for at most 30 seconds or until the transaction is confirmed.
    recent_blockhash = blockhash # (optional) a prefetched Blockhash for the transaction.
    )

print(tokenMint.pubkey)

link = getExplorerLink("address", tokenMint.pubkey, "devnet")
print(f"✅ Finished! Created token mint: {link}")