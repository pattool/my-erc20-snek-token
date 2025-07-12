import boa
from eth_utils import to_wei

from script.deploy import INITIAL_SUPPLY

RANDOM_USER = boa.env.generate_address("random_user")

def test_token_supply(snek_token):
    """Test the supply is correct."""
    #snek_token = deploy() # -> see conftest
    assert snek_token.totalSupply() == INITIAL_SUPPLY # function .totalSupply is exported from erc20.vy


def test_token_emits_event(snek_token):
    #snek_token = deploy() # -> see conftest
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


def test_super_mint_multiple_users(snek_token):
    """Test super_mint with multiple users."""
    
    # Get initial balances
    initial_balance_owner = snek_token.balanceOf(snek_token.owner())
    initial_balance_random_user = snek_token.balanceOf(RANDOM_USER)
    
    
    # Owner mints tokens
    with boa.env.prank(snek_token.owner()):
        snek_token.super_mint()
    
    # Random_user mints tokens
    with boa.env.prank(RANDOM_USER):
        snek_token.super_mint()
    
    # Verify balances increased correctly
    mint_amount = to_wei(100, "ether")
    assert snek_token.balanceOf(snek_token.owner()) == initial_balance_owner + mint_amount
    assert snek_token.balanceOf(RANDOM_USER) == initial_balance_random_user + mint_amount 


def test_super_mint_total_supply_bug(snek_token):
    """Test that demonstrates the bug in super_mint (totalSupply updated)."""
    # Get initial total supply
    initial_total_supply = snek_token.totalSupply()
    
    # Call super_mint
    with boa.env.prank(snek_token.owner()):
        snek_token.super_mint()
    
    # Verify total supply did change (this is the bug)
    assert snek_token.totalSupply() > initial_total_supply




    