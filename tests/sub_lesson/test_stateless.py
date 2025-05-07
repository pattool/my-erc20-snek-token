# ------------------------------------------------------------------
#                             IMPORTS
# ------------------------------------------------------------------
import pytest
from contracts.sub_lesson import stateless_fuzz_solvable
from hypothesis import given, HealthCheck, settings # given: define a range of number for an input
from boa.test.strategies import strategy # let you define a type for the input


# ------------------------------------------------------------------
#                             FIXTURES
# ------------------------------------------------------------------
@pytest.fixture(scope="session")
def contract():
    return stateless_fuzz_solvable.deploy()

# Note: hypothesis lib does not like fixtures!!!


# ------------------------------------------------------------------
#            FUNCTIONS: STATELESS FUZZING TEST WITH HYPOTHESIS 
# ------------------------------------------------------------------
@settings(
    max_examples=1000, suppress_health_check=[HealthCheck.function_scoped_fixture]
)
@given(input=strategy("uint256")) # Any number between 0 and MaxUINT256
def test_always_returns_input(contract, input):
    print(input)
    assert contract.always_returns_input_number(input) == input


# ------------------------------------------------------------------
#                         SIMPLE UNITTEST
# ------------------------------------------------------------------
#def test_always_returns_input(contract):
#    input = 0
#    assert contract.always_returns_input_number(input) == input