from micropm4py.conversion.pm4py import dfg as dfg_conv
from micropm4py.log import xes_import_traces_file


def main():
    dfg_mp = xes_import_traces_file.imp_dfg_file("../micro_tests/running-example.xes")
    print(dfg_mp)
    dfg_pm4, acti_count, start_activities, end_activities = dfg_conv.to(dfg_mp)
    print(dfg_pm4)
    print(acti_count)
    print(start_activities)
    print(end_activities)


if __name__ == "__main__":
    main()
