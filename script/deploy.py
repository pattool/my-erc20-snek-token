from contracts import snek_token
from eth_utils import to_wei
from moccasin.boa_tools import VyperContract

INITIAL_SUPPLY = to_wei(1000, "ether") # gives 18 decimals to 100

def deploy() -> VyperContract:
    snek_contract = snek_token.deploy(INITIAL_SUPPLY)
    print(f"Deployed to {snek_contract.address}")
    return snek_contract



def moccasin_main() -> VyperContract:
    return deploy()