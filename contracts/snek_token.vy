# pragma version 0.4.0

# ------------------------------------------------------------------
#                            NATSPEC META DATA
# ------------------------------------------------------------------
"""
@license MIT
@title snek_token
@author Patrick!
@notice This is my ERC20 token!
"""


# ------------------------------------------------------------------
#                BUILT-IN INTERFACE OF THE VYPER COMPILER
# ------------------------------------------------------------------
# @dev We import and implement the `IERC20` interface,
# which is a built-in interface of the Vyper compiler.
from ethereum.ercs import IERC20
implements: IERC20  # Does not compile before it Ads all the function of an interface!


# ------------------------------------------------------------------
#                             IMPORTS
# ------------------------------------------------------------------
from snekmate.auth import ownable as ow  # example how to import this ownable vyper contract
from snekmate.tokens import erc20

### OR

#from lib.pypi.snekmate.auth import ownable as ow # example how to import this ownable vyper contract
#from lib.pypi.snekmate.tokens import erc20


# ------------------------------------------------------------------
#                      IMPORT STORAGE VARIABLES
# ------------------------------------------------------------------
initializes: ow
initializes: erc20[ownable := ow] # uses the exactly ownable as we imported as ow


# ------------------------------------------------------------------
#                         EXPORT FUNCTIONS
# ------------------------------------------------------------------
# exports functions (check json_file, to have the erc20 functions in the abi.)
exports: erc20.__interface__


# ------------------------------------------------------------------
#                         Constants VARIABLES
# ------------------------------------------------------------------
NAME: constant(String[25]) = "snek_token"
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
#@external
#def super_mint():
#    # We forget to update the total supply!
#    # self.totalSupply += amount # <- error self should be erc20
#    amount: uint256 = as_wei_value(100, "ether")
#    erc20.balanceOf[msg.sender] = erc20.balanceOf[msg.sender] + amount
#    log IERC20.Transfer(empty(address), msg.sender, amount)

@external
def super_mint():
    amount: uint256 = as_wei_value(100, "ether")

    # Overflow protection
    assert erc20.totalSupply + amount >= erc20.totalSupply, "Arithmetic overflow"
    # maximum cap against overflow attack   
    assert erc20.totalSupply + amount <= MAX_SUPPLY, "Max supply exceeded"
    

    erc20.balanceOf[msg.sender] +=  amount
    erc20.totalSupply += amount
    log IERC20.Transfer(empty(address), msg.sender, amount)

# ------------------------------------------------------------------
#                               END
# ------------------------------------------------------------------