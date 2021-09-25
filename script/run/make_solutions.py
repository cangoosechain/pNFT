import sys
sys.path.append("../../")
import json
from script.utils.cdv_tool import CdvTool



if __name__ == "__main__":
    config_file_path = sys.argv[1]
    config_file = open(config_file_path, "r")
    config = json.load(config_file)
    config_file.close()

    out_path = config["out_path"]
    solutions = config["solutions"]

    cdv = CdvTool()
    result = cdv.opc(solutions)
    # print(json.dumps(result))

    out_file = open(out_path, "w")
    json.dump(result, out_file)
    out_file.close()
