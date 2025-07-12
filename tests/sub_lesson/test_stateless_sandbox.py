# ------------------------------------------------------------------
#                             IMPORTS
# ------------------------------------------------------------------
import pytest
from boa.test.strategies import strategy  # let you define a type for the input
from hypothesis import given, settings


from contracts.sub_lesson import stateless_fuzz_solvable





# ------------------------------------------------------------------
#                             FIXTURES
# ------------------------------------------------------------------
@pytest.fixture(scope="session")
def contract():
    return stateless_fuzz_solvable.deploy()
    
# Note: hypothesis lib does not like fixtures!!!


# ------------------------------------------------------------------
#                   FUNCTIONS: STATELESS FUZZING
# ------------------------------------------------------------------

@settings(max_examples=3000)
@given(input=strategy("uint256")) # Any number between 0 and MaxUINT256
def test_always_returns_input(contract, input):
    print(input)
    assert contract.always_returns_input_number(input) == input

    
# ------------------------------------------------------------------
#                          SIMPLE UNITEST
# ------------------------------------------------------------------
#def test_always_returns_input(contract):
#    input = 0
#    assert contract.always_returns_input_number(input) == input