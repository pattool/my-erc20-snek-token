# ------------------------------------------------------------------
#                             IMPORTS
# ------------------------------------------------------------------
from hypothesis.stateful import RuleBasedStateMachine, rule
from contracts.sub_lesson import stateful_fuzz_solvable
from boa.test.strategies import strategy
from hypothesis import settings


# ------------------------------------------------------------------
#                              CLASS
# ------------------------------------------------------------------
class StatefulFuzzer(RuleBasedStateMachine):
    def __init__(self):
        super().__init__()
        self.contract = stateful_fuzz_solvable.deploy()
        print()
        print("Deployed contract!")
        print()

        
    @rule(new_number=strategy("uint256"))
    def change_number(self, new_number):
        self.contract.change_number(new_number)
        print(f"    Called change_number with {new_number}")


    @rule(input=strategy("uint256"))
    def input_number_returns_itself(self, input):
        response = self.contract.always_returns_input_number(input)
        print(f"    Called always returns with {input}")
        assert response == input, f"Expected {input}, got {response}"


# ------------------------------------------------------------------
#                            CALL CLASS
# ------------------------------------------------------------------
TestStatefulFuzzing = StatefulFuzzer.TestCase

TestStatefulFuzzing.settings = settings(max_examples=20, stateful_step_count=10)