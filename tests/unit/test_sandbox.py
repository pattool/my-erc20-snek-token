import boa
from eth_utils import to_wei

from script.deploy import INITIAL_SUPPLY

RANDOM_USER = boa.env.generate_address("random_user")

def test_token_supply(snek_token):
    """Test the supply is correct."""
    #snek_token = deploy() # -> see conftest
    assert snek_token.totalSupply() == INITIAL_SUPPLY 


def test_token_emits_event(snek_token):
    with boa.env.prank(snek_token.owner()):
        snek_token.transfer(RANDOM_USER, INITIAL_SUPPLY) # .transfer function on the erc20 / (to Random_User, amount)
        logs = snek_token.get_logs() # get_logs come from boa lib
        #log_owner = logs[0].sender    #-> for 0.4.1 version vyper 
        log_owner = logs[0].topics[0]  #-> for 0.4.0 version vyper 
        assert log_owner == snek_token.owner() 
    assert snek_token.balanceOf(RANDOM_USER) == INITIAL_SUPPLY



def test_super_mint(snek_token):
    """Test the super_mint function increases user balance correctly."""
    
    # Get initial balance
    initial_balance = snek_token.balanceOf(RANDOM_USER)
    
    # Call super_mint
    with boa.env.prank(RANDOM_USER):
        tx = snek_token.super_mint()
    
    # Verify balance increased by 100 ether (in wei)
    increase_amount = to_wei(100, "ether")
    assert snek_token.balanceOf(RANDOM_USER) == initial_balance + increase_amount