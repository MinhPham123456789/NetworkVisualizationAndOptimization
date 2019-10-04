import pandas as pd

def get_throughput_information(csv_table):
    # csv_test = pd.read_csv(csv_table)
    csv_result = pd.read_csv(csv_table, names=[i for i in range(24)])
    return csv_result