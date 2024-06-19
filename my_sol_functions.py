def clusterApiUrl(rpc: str, websocket = False):
    if rpc in ["devnet", "mainnet-beta", "testnet"]:
        return f'{"https" if not websocket else "wss"}://api.{rpc}.solana.com'
    
LAMPORTS_PER_SOL = 10 ** 9

def getKeypairFromEnvironment(secret_key_variable_name_in_env:str):
    from solders.keypair import Keypair

    import json

    import os

    # Import secret key from environment
    secret_key = json.loads(os.environ.get(secret_key_variable_name_in_env))

    # Return keypair
    return Keypair.from_bytes(secret_key)