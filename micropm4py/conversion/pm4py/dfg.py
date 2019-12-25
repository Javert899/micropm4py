def to(dfg0):
    acti_count = {}
    dfg = {}

    for act in dfg0[1]:
        acti_count[dfg0[0][act]] = dfg0[1][act]

    for tup in dfg0[4]:
        new_tup = (dfg0[0][tup[0]], dfg0[0][tup[1]])
        dfg[new_tup] = dfg0[4][tup]

    return acti_count, dfg
