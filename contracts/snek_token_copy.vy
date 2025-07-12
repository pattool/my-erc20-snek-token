# pragma version 0.4.0

# ------------------------------------------------------------------
#                        NATSPEC META DATA
# ------------------------------------------------------------------
"""
@license MIT
@title snek_token_copy
@author Patrick!
@notice This is my ERC20 token copy!
"""

# ------------------------------------------------------------------
#             BUILT-IN INTERFACE OF THE VYPER COMPILER
# ------------------------------------------------------------------
# @dev We import and implement the `IERC20` interface,
# which is a built-in interface of the Vyper compiler.
from ethereum.ercs import IERC20
implements: IERC20  # Does not compile before it Ads all the function of an interface!


# ------------------------------------------------------------------
#                             IMPORTS
# ------------------------------------------------------------------
from snekmate.auth import ownable as ow
from snekmate.tokens import erc20







# ------------------------------------------------------------------
#                     IMPORT STORAGE VARIABLES
# ------------------------------------------------------------------
initializes: ow
initializes: erc20[ownable := ow]


# ------------------------------------------------------------------
#                             EXPORTS
# ------------------------------------------------------------------
# exports functions (check json_file, to have the erc20 functions in the abi.)
exports: erc20.__interface__


# ------------------------------------------------------------------
#                         Constants VARIABLES
# ------------------------------------------------------------------
NAME: constant(String[25]) = "snek_token_copy"
SYMBOL: constant(String[5]) = "SNEK"
DECIMALS: constant(uint8) = 18
EIP712_VERSION: constant(String[20]) = "1"

MAX_SUPPLY: constant(uint256) = 2**255


# ------------------------------------------------------------------
#                           CONSTRUCTOR
# ------------------------------------------------------------------
@deploy
def __init__(initial_supply: uint256):
    ow.__init__()
    erc20.__init__(NAME, SYMBOL, DECIMALS, NAME, EIP712_VERSION)
    erc20._mint(msg.sender, initial_supply)


# ------------------------------------------------------------------
#                            FUNCTIONS
# ------------------------------------------------------------------






















# ------------------------------------------------------------------
#                               END
# ------------------------------------------------------------------