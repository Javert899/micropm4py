from micropm4py.log import xes_import_traces_file_standard


def main():
    variants = xes_import_traces_file_standard.imp_variants_from_file("../micro_tests/running-example.xes")
    print(variants)


if __name__ == "__main__":
    main()
