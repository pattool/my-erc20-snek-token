# ------------------------------------------------------------------
#                            META DATA
# ------------------------------------------------------------------
# pragma version 0.4.0
"""
@title always_return_input
@license MIT
@notice INVARIANT: always_returns_input_number should always return the input number
"""


# ------------------------------------------------------------------
#                             FUNCTION
# ------------------------------------------------------------------
@external
@pure
def always_returns_input_number(input_number: uint256) -> uint256:
    """
    @param input_number The input number to check
    """
    #if input_number == 2:
    #    return 0
    return input_number