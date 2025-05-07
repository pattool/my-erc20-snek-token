## ------------------------------------------------------------------
##                             IMPORTS
## ------------------------------------------------------------------
#from hypothesis.stateful import RuleBasedStateMachine, rule
#from contracts.sub_lesson import stateful_fuzz_solvable
#from boa.test.strategies import strategy
#from hypothesis import settings
#
#
## ------------------------------------------------------------------
##                              CLASS
## ------------------------------------------------------------------
#class StatefulFuzzer(RuleBasedStateMachine):
#    def __init__(self):
#        super().__init__()
#        self.contract = stateful_fuzz_solvable.deploy()
#        print("Deployed contract!")
#
#
#    # Need to give - "Rules" -> Actions, can have properties / invariants
#    #              - "Invariants" -> Properties that should always hold true
#    
#    @rule(new_number=strategy("uint256")) # Range between 0 and MaxUINT256
#    def change_number(self, new_number):
#        self.contract.change_number(new_number)                     # Action
#        print(f"    Called change_number with {new_number}")
#
#    
#    @rule(input=strategy("uint256")) # Range between 0 and MaxUINT256
#    def input_number_returns_itself(self, input):
#        response = self.contract.always_returns_input_number(input) # Action
#        print(f"    Called always returns with {input}")
#        assert response == input, f"Expected {input}, got {response}" # Invariant
#
#
## ------------------------------------------------------------------
##                            CALL CLASS
## ------------------------------------------------------------------
#TestStatefulFuzzing = StatefulFuzzer.TestCase
#
#TestStatefulFuzzing.settings = settings(max_examples=10000, stateful_step_count=50)