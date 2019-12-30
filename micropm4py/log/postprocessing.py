def add_art_st_end(log):
    i = 0
    while i < len(log):
        if len(log[i]) == 2 and type(log[i][1]) is list:
            log[i][1] = [">>"] + log[i][1] + ["[]"]
        i = i + 1
    return log
