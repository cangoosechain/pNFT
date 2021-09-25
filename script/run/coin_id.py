import sys
sys.path.append("../../")
import json
from script.utils.cdv_tool import CdvTool

if __name__ == "__main__":
    parent_id = "a7c8d15032a16dedf588c982465ebc91eabef57e57c3b6664c65dec417b09261"
    puzzlehash = "3c0171378604a01ffd188af6e1fb188437f10f7f8ab374f9a20188fabd7164ae"
    amount = "1749999999930"
    real_coin_id = "0bc218854ea58ddb8dfb302349b7d37359d39ae404375b5b2a4e4b0be24197fe"

    str = parent_id + puzzlehash + amount

    cdv = CdvTool()
    coin_id = cdv.sha256(str)
    print("real_coin_id:\t%s" % real_coin_id)
    print("my_coin_id:\t%s" % coin_id)
    

