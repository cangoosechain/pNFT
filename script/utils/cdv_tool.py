import os
import json
import hashlib
from script.utils.log import Log


class CdvTool(object):
    def __init__(self):
        log = Log("coin_maker_log")
        self.log = log.logger

    @staticmethod
    def sha256(data_sha256):
        return hashlib.sha256(data_sha256.encode(encoding='UTF-8')).hexdigest()

    def build(self, coin_file):
        build_cmd = "cdv clsp build %s" % coin_file
        self.log.info(build_cmd)
        build_result = os.popen(build_cmd).read().strip()
        return build_result

    def curry(self, hex_file_name, param_list):
        for i in range(len(param_list)):
            param_list[i] = "-a %s" % param_list[i]
        param_list_merge_str = " ".join(param_list)
        curry_cmd = "cdv clsp curry %s %s" % (hex_file_name, param_list_merge_str)
        curry_cmd_treehash = "%s --treehash" % curry_cmd
        curry_cmd_x = "%s -x" % curry_cmd
        self.log.info(curry_cmd_treehash)
        puzzle_hash = os.popen(curry_cmd_treehash).read().strip()
        self.log.info(curry_cmd_x)
        puzzle_reveal = os.popen(curry_cmd_x).read().strip()
        return puzzle_hash, puzzle_reveal, curry_cmd

    def encode(self, puzzle_hash, prefix):
        encode_cmd = "cdv encode %s --prefix %s" % (puzzle_hash, prefix)
        self.log.info(encode_cmd)
        address = os.popen(encode_cmd).read().strip()
        return address
    
    def chia_wallet_send(self, amount_for_wallet_send, address):
        chia_wallet_send_cmd = "chia wallet send -a %s -t %s" % (
            amount_for_wallet_send, address)
        self.log.info(chia_wallet_send_cmd)
        result = os.popen(chia_wallet_send_cmd).read().strip()
        return result

    def coinrecords(self, sign, items):
        coinrecords_cmd = "cdv rpc coinrecords --by %s %s " % (
            sign, " ".join(items))
        coins = os.popen(coinrecords_cmd).read().strip()
        coins = coins.replace("'", '"')
        coins = coins.replace("True", "true").replace("False", "false")
        coins = json.loads(coins)
        return coins

    def opc(self, params_list):
        solution_list = []
        for params in params_list:
            opc_cmd = "opc '(%s)'" % (" ".join(params))
            self.log.info(opc_cmd)
            solution = os.popen(opc_cmd).read().strip()
            self.log.info(solution)
            solution_list.append(solution)
        return solution_list

    def coin_info(self, amount, parent_coin_info, puzzle_hash, puzzle_reveal, solution):
        coin_json = {
            "coin": {
                "amount": amount,
                "parent_coin_info": parent_coin_info,
                "puzzle_hash": puzzle_hash
            },
            "puzzle_reveal": puzzle_reveal,
            "solution": solution
        }
        return coin_json

    def spend_bundle(self, coin_spends, aggregated_signature):
        spend_bundle_file = open("temp_spend_bundle.json", "w")
        spend_bundle_json = {
            "coin_spends": coin_spends,
            "aggregated_signature": aggregated_signature
        }
        json.dump(spend_bundle_json, spend_bundle_file)
        spend_bundle_file.close()
        self.log.info("make temp_spend_bundle.json finish")

    def get_parent_coin_info(self, coins):
        coins_parent_coin_info = []
        for each_coin in coins:
            parent_coin_info = each_coin["coin"]["parent_coin_info"]
            coins_parent_coin_info.append(parent_coin_info)
        coins_parent_coin_info = list(set(coins_parent_coin_info))
        self.log.info("get coins_parent_coin_info: %s" %
                      coins_parent_coin_info)
        return coins_parent_coin_info

    def coin_tree_upward_find(self, sign, items, all_tree_coins=[]):
        coins = self.coinrecords(sign, items)
        all_tree_coins.extend(coins)
        self.log.info("get coins: %s" % json.dumps(coins))
        coins_parent_coin_info = self.get_parent_coin_info(coins)

        if len(coins_parent_coin_info) > 0:
            self.coin_tree_upward_find(
                "id", coins_parent_coin_info, all_tree_coins)
        else:
            self.log.info("get coins_tree: %s" % json.dumps(all_tree_coins))
