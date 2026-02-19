import time

from eth_utils import to_wei
from moccasin.boa_tools import VyperContract
from moccasin.config import get_active_network

from contracts import snek_token

INITIAL_SUPPLY = to_wei(1000, "ether") # or int(1000e18) gives 18 decimals to 1000

def deploy() -> VyperContract:
    snek_contract = snek_token.deploy(INITIAL_SUPPLY)
    print(f"\nDeployed Snektoken at {snek_contract.address}")
    
    active_network = get_active_network()
    print(f"\nActive network: {active_network.name}")
    print(f"Explorer URI: {active_network.explorer_uri}")
    print(f"Explorer type: {active_network.explorer_type}")
    print(f"Network has explorer: {active_network.has_explorer}\n")
    

    if active_network.has_explorer() and active_network.is_local_or_forked_network() is False:
        print(f"Waiting 20 seconds for contract to be indexed by {active_network.explorer_type} ...\n")
        time.sleep(20)

        print(f"Starting {active_network.explorer_type} verification...")
        try:
            result = active_network.moccasin_verify(snek_contract)
            print(f"Verification request submitted to {active_network.explorer_type}")
            result.wait_for_verification()
            print("Verification completed succesfully!\n")
        except Exception as e:
            print(f"Verification failed with error: {e}")
            print(f"Error type: {type(e).__name__}")
            print()

    return snek_contract


def moccasin_main() -> VyperContract:
    return deploy()