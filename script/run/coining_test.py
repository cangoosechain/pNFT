import sys
sys.path.append("../../")
import time
from script.utils.cdv_tool import CdvTool

if __name__ == "__main__":
    # address = "txch18ddsuq5zpdrqdk99jwc989275nk590sh0gel4z256mar2eqc8l9qlskx65"
    # amount = "0.000000000001"
    address = sys.argv[1]
    amount = sys.argv[2]
    start_time = time.time()
    print(start_time)
    cdv = CdvTool()
    last_time = time.time()
    success_count = 0
    success_cost_time = 0
    for i in range(60000):
        result = cdv.chia_wallet_send(amount, address)
        print(result)

        total_count = i + 1
        cost_time = time.time() - start_time
        avg_time = cost_time / total_count
        this_one_cost_time = time.time() - last_time

        if "Exception" not in result:
            success_count = success_count + 1
            success_cost_time = success_cost_time + this_one_cost_time
        avg_success_time = success_cost_time / success_count

        print("total_count: %s\tcost_time: %.3f\tavg_time: %.3f\tthis_one_cost_time: %.3f" %
              (total_count, cost_time, avg_time, this_one_cost_time))
        print("success_count: %s\tsuccess_cost_time: %.3f\tavg_success_time: %.3f" % (
            success_count, success_cost_time, avg_success_time))
        last_time = time.time()
    print(time.time() - start_time)
