# ------------------------------------------------------------------
#                            META DATA
# ------------------------------------------------------------------
# pragma version 0.4.0
"""
@title always_return_input_two
@license MIT
@notice INVARIANT: always_returns_input_number should always return the input number
"""


# ------------------------------------------------------------------
#                         STATE VARIABLES
# ------------------------------------------------------------------
some_number: public(uint256)


# ------------------------------------------------------------------
#                             FUNCTION
# ------------------------------------------------------------------
@external
def always_returns_input_number(input_number: uint256) -> uint256:
    """
    @param input_number The input number to check
    """
    #if self.some_number == 2:
    #    return 0
    return input_number


@external
def change_number(new_number: uint256):
    self.some_number = new_number
