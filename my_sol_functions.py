def clusterApiUrl(rpc: str, websocket = False):
    if rpc in ["devnet", "mainnet-beta", "testnet"]:
        return f'{"https" if not websocket else "wss"}://api.{rpc}.solana.com'
    
LAMPORTS_PER_SOL = 10 ** 9