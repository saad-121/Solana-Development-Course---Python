def clusterApiUrl(cluster: str = "mainnet-beta", websocket = False):
    if cluster in ["devnet", "mainnet-beta", "testnet"]:
        return f'{"https" if not websocket else "wss"}://api.{cluster}.solana.com'
    
LAMPORTS_PER_SOL = 10 ** 9


def getKeypairFromEnvironment(secret_key_variable_name_in_env:str):
    from solders.keypair import Keypair

    import json

    import os

    # Import secret key from environment
    secret_key = json.loads(os.environ.get(secret_key_variable_name_in_env))

    # Return keypair
    return Keypair.from_bytes(secret_key)

def getExplorerLink(type_of_lookup, specific_path, cluster: str = "mainnet-beta"):
    if type_of_lookup == "transaction":
        type_of_lookup = "tx"
    if type_of_lookup in ["address", "tx"] and cluster in ["devnet", "mainnet-beta", "testnet"]:
        return f"https://explorer.solana.com/{type_of_lookup}/{specific_path}?cluster={cluster}"
    

def get_latest_blockhash_value():
    return solana_client.get_latest_blockhash().value.blockhash

def getOrCreateAssociatedTokenAccount(payer, owner, token_client):
    # https://www.soldev.app/course/token-program

    # 3. Create an Associated Token Account to store the tokens
    import os
    from solana.rpc.api import Client
    from solders.pubkey import Pubkey
    from spl.token.instructions import create_associated_token_account
    from solana.transaction import Transaction


    try:
    
        get_accounts_by_owner_resp = token_client.get_accounts_by_owner(owner.pubkey())

        if "value" in dir(get_accounts_by_owner_resp):
            if len(get_accounts_by_owner_resp.value):
                existing_associated_token_account = get_accounts_by_owner_resp.value[0].pubkey
                print(f"OWner already has an associated token account. Its pubkey is: {existing_associated_token_account}")
                return existing_associated_token_account
            else:
                created_associated_token_account = token_client.create_associated_token_account(owner.pubkey())
                print(f"Createed a new associated token account: {created_associated_token_account}")
                return created_associated_token_account
        elif "message" in dir(get_accounts_by_owner_resp):
            if get_accounts_by_owner_resp.message == "Invalid param: Token mint could not be unpacked":
                # # Create a new transaction
                created_associated_token_account = token_client.create_associated_token_account(owner.pubkey())
                print(f"Createed a new associated token account: {created_associated_token_account}")
                return created_associated_token_account
        else:
            print(f"Received an unusual response. get_accounts_by_owner_resp: {get_accounts_by_owner_resp}")

    except Exception as e:
        print(f"Error getting owner_associated_token_account: {e}")
        
    



