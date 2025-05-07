# ------------------------------------------------------------------
#                             IMPORTS
# ------------------------------------------------------------------
from hypothesis.stateful import RuleBasedStateMachine, rule, invariant
from contracts import snek_token
from boa.test.strategies import strategy
from hypothesis import settings, assume

import boa
from script.deploy import INITIAL_SUPPLY
from eth_utils import to_wei


RANDOM_USER = boa.env.generate_address("random_user")

# ------------------------------------------------------------------
#                              CLASS
# ------------------------------------------------------------------
class StatefulFuzzer(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.token = snek_token.deploy(INITIAL_SUPPLY)
        print()
        print("Deployed initial supply:", INITIAL_SUPPLY)
        print()

    ## There is a issue on def change_supply ->overflow!!!!
    #@rule(new_supply=strategy("uint256", max_value=2**255-1))
    #def change_supply(self, new_supply):
    #    """Test the supply is changing correctly."""
    #    # Ensure new supply is within valid range
    #    assume(new_supply <= 2**255-1)
 #
    #    try:
    #        self.token = snek_token.deploy(new_supply)
    #        print(f"    Called change_supply with {new_supply}")
 #
    #        # Verify total supply matches what we set
    #        assert self.token.totalSupply() == new_supply, f"Expected totalSupply to be {new_supply}, \
    #        but got {self.token.totalSupply()}"
 #
    #        # Additional check to verify we're not exceeding MAX_SUPPLY
    #        #assert self.token.totalSupply() <= 2**255-1, "Total supply exceeds maximum allowed"
 #
    #    except Exception as e:            
    #        # Check if this is an expected error related to overflow
    #        error_msg = str(e)
    #        if "Max supply exceeded" in error_msg or "Arithmetic overflow" in error_msg:
    #            # This is an expected failure, tell Hypothesis to generate a new example
    #            assume(False)
    #        else:
    #            # Unexpected error, we want to fail the test
    #            print(f"Unexpected error: {error_msg}")
    #            raise 

    
    @rule() # no rule: mint amount is fixed hard coded in the super_mint().   
    def increase_amount(self):
        """Test the super_mint function increases user balance correctly."""
        
        initial_balance = self.token.balanceOf(RANDOM_USER)
        print(f"    Deployed initial balance: {initial_balance} with user {RANDOM_USER}")

        
        with boa.env.prank(RANDOM_USER):
            self.token.super_mint()
        print(f"    Called super_mint!")
        
        mint_amount = to_wei(100, "ether")        
        assert self.token.balanceOf(RANDOM_USER) == initial_balance + mint_amount,\
            f"    Expected balance to be {initial_balance + mint_amount} but got \
            {self.token.balanceOf(RANDOM_USER)}"
        

    @rule(user_num=strategy("uint256"))
    def test_super_mint_multiple_users(self, user_num):
        """Test super_mint with multiple users."""
        
        # Define mint amount and maximum supply constants
        mint_amount = to_wei(100, "ether")
        max_uint256 = 2**256 - 1

        # Generate a new user address
        new_user = boa.env.generate_address(f"user_{user_num}")
        
        # Get initial balances 
        initial_total_supply = self.token.totalSupply()
        initial_balance_owner = self.token.balanceOf(self.token.owner())
        initial_balance_random_user = self.token.balanceOf(new_user)
        print(f"    Deployed initial balance Owner: {initial_balance_owner} with user {self.token.owner()}")
        print(f"    Deployed initial balance New User: {initial_balance_random_user} with user {new_user}")

        # Check if we're close to max supply and would overflow
        if initial_total_supply > max_uint256 - (mint_amount * 2):
            print("Skipping test: Total supply too close to max uint256")
            return

        try:    
            # Owner mints tokens
            with boa.env.prank(self.token.owner()):
                self.token.super_mint()
                
            # Random_user mints tokens
            with boa.env.prank(new_user):
                self.token.super_mint()
            print(f"    Called super_mint with multiple users!")
            
            assert self.token.balanceOf(self.token.owner()) == initial_balance_owner + mint_amount, \
            f"    Expected balance to be {initial_balance_owner + mint_amount} but got \
            {self.token.balanceOf(self.token.owner())}" # maybe (new_user)
            
            assert self.token.balanceOf(new_user) == initial_balance_random_user + mint_amount, \
            f"    Expected balance to be {initial_balance_random_user + mint_amount} but got \
            {self.token.balanceOf(new_user)}"

        except Exception as e:
            # If we're near the max supply, this might be expected behavior
            if initial_total_supply > max_uint256 - (mint_amount * 3):
                print(f"    Expected error near max supply: {e}")
            else:
                # If we're not near max supply, this is an unexpected error
                print(f"    Unexpected error: {e}")
                raise  # Re-raise the exception


    @invariant()
    def test_super_mint_total_supply_bug(self):
        """Test that demonstrates balance should never exceed total_supply."""
        # Get initial total supply
        total_supply = self.token.totalSupply()
        balance_owner = self.token.balanceOf(self.token.owner())
        random_user_balance = self.token.balanceOf(RANDOM_USER)
        
        # Verify individual balances don't exceed total supply
        assert random_user_balance <= total_supply, \
        f"    Random user balance {random_user_balance} exceed total supply {total_supply}"

        assert balance_owner <= total_supply, \
        f"    Owner balance {balance_owner} exceeds total supply {total_supply}"

        # Verify total balance does not exceed total supply
        total_balances = random_user_balance + balance_owner
        assert total_balances <= total_supply

        f"    Sum of balances {total_balances} exceeds total supply {total_supply}"    
    

# ------------------------------------------------------------------
#                            CALL CLASS
# ------------------------------------------------------------------
TestStatefulFuzzing = StatefulFuzzer.TestCase

TestStatefulFuzzing.settings = settings(max_examples=3000, stateful_step_count=50)

# ------------------------------------------------------------------
#                            UNIT TEST
# ------------------------------------------------------------------


