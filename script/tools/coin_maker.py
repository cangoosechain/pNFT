import re
from script.utils.cdv_tool import CdvTool


class CoinMaker(CdvTool):
    def __init__(self):
        super(CoinMaker, self).__init__()

    def make_one_coin(self, coin_file, curry_param_list, amount, prefix="txch", mojo=0.000000000001):
        self.build(coin_file)
        puzzle_hash, puzzle_reveal, curry_cmd = self.curry(
            "%s.hex" % coin_file, curry_param_list)
        address = self.encode(puzzle_hash, prefix)
        result = self.chia_wallet_send("%.12f" % (amount * mojo), address)
        sub_result = re.findall(r"Do(.+?)to", result)
        if sub_result:
            self.log.info(sub_result[0].strip())
        else:
            self.log.info(result)
        coin_info = {
            "amount": amount,
            "puzzle_hash": puzzle_hash,
            "puzzle_reveal": puzzle_reveal,
            "address": address,
            "curry_cmd": curry_cmd,
        }
        return coin_info

    def make_coins(self, coin_file, accounts_info, total_amount, prefix="txch", mojo=0.000000000001):
        self.build(coin_file)
        self.log.info("start make coin curry cmd list")
        curry_dic = {}
        for each in accounts_info:
            account_hash_list = []
            account_list = accounts_info[each]["operator"]
            for account in account_list:
                plaintext = "%s_%s" % (each, account)
                account_hash_list.append(self.sha256(plaintext))
            param = ["'(%s)'" % " ".join(account_hash_list)]
            hex_file_name = "%s.hex" % coin_file

            self.log.info("start curry %s" % hex_file_name)
            puzzle_hash, puzzle_reveal, curry_cmd = self.curry(
                hex_file_name, param)
            address = self.encode(puzzle_hash, prefix)
            amount = accounts_info[each]["amount"]
            if amount == -1 or amount == "-1":
                amount = total_amount * accounts_info[each]["ratio"]
            amount_for_wallet_send = "%.12f" % (mojo * amount)
            amount = str(int(amount))

            self.log.info("%s puzzle_hash: %s" % (hex_file_name, puzzle_hash))

            create_info = self.chia_wallet_send(
                amount_for_wallet_send, address)
            self.log.info("%s create_info: %s" % (hex_file_name, create_info))

            curry_dic[each] = {
                "operator": account_hash_list,
                "address": address,
                "amount_for_wallet_send": amount_for_wallet_send,
                "amount": amount,
                "puzzle_hash": puzzle_hash,
                "puzzle_reveal": puzzle_reveal,
                "curry_cmd": curry_cmd
            }
        self.log.info("finish make coin curry cmd list")
        return curry_dic
