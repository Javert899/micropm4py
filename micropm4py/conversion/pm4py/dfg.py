def to(dfg0):
    acti_count = {}
    dfg = {}
    start_activities = set()
    end_activities = set()

    for act in dfg0[1]:
        acti_count[dfg0[0][act]] = dfg0[1][act]

    for tup in dfg0[4]:
        new_tup = (dfg0[0][tup[0]], dfg0[0][tup[1]])
        dfg[new_tup] = dfg0[4][tup]

    for act in dfg0[2]:
        start_activities.add(dfg0[0][act])

    for act in dfg0[3]:
        end_activities.add(dfg0[0][act])

    return dfg, acti_count, start_activities, end_activities
