import sys
sys.path.append("../../")
import json
from script.utils.cdv_tool import CdvTool

if __name__ == "__main__":
    config_file_path = sys.argv[1]
    config_file = open(config_file_path, "r")
    config = json.load(config_file)
    config_file.close()

    sign = config["sign"]
    items = config["items"]
    out_path = config["out_path"]

    cdv = CdvTool()
    result = cdv.coin_tree_upward_find(sign, items)

    out_file = open(out_path, "w")
    json.dump(result, out_file)
    out_file.close()

