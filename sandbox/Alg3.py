import copy

from igraph import *

def algorithm_3(graph, source, target):

    # initialization
    pointer = 0
    num = 1
    # tags is an array of integers, python starts counting from 0
    tags = [0]
    flag = False

    net = graph.get_adjlist(mode='in')
    all_MFRs = [[[target, net[target]]]]

    # while some partial MFRs remain
    while pointer < num:
        flag = False
        c_MFR = all_MFRs[pointer]
        c_tag = tags[pointer]
        # while the current MFR is incomplete
        while not flag:
            c_node = c_MFR[c_tag][0]
            # c_preds is a list of integers
            c_preds = c_MFR[c_tag][1]

            # if no predecessors remain
            # python uses implicit booleans for lists
            if not c_preds:
                if c_tag == len(c_MFR) - 1:
                    flag = True
                else:
                    c_tag = c_tag + 1

            else:
                if True:
                # placeholder;
                # actually need to check that c_node is not a composite node
                    m = len(c_preds)
                    c_MFR[c_tag][1] = c_preds[0]

                    # allots memory to new partial MFRs
                    i = 0
                    while i < m - 1:
                        # Python doesn't reassign the actual list otherwise
                        temp1 = copy.deepcopy(c_MFR)
                        # deepcopy is very memory-intensive
                        temp1[c_tag][1] = [c_preds[i + 1]]
                        # current MFR is replaced by first copy
                        all_MFRs.append(temp1)
                        tags.append(c_tag)
                        i = i + 1
                    num = num + m - 1
                c_preds = [c_MFR[c_tag][1]]

                # returns list of entries in MFR's first "column"
                stems = [mfr[0] for mfr in c_MFR]

                # checks that all c_preds are in c_MFR
                if not set(c_preds).difference(set(stems)):
                    # same as line 35
                    if c_tag == len(c_MFR) - 1:
                        flag = True
                    else:
                        c_tag = c_tag + 1
                # appends new rows to current partial MFR
                else:
                    for v in c_preds:
                        temp2 = net[v]
                        c_MFR.append([v, temp2])

                c_tag = c_tag + 1

        pointer = pointer + 1

    # removes "extra" MFRs, those that result from cycles in graph
    # BUG: it removes all but one extra MFR
    for mfr in all_MFRs:
        if not mfr[len(mfr)-1][0] == 0:
            all_MFRs.remove(mfr)

    print("Final MFRs:")
    for mfr in all_MFRs:
        print(mfr)
    print("Number of MFRs:", len(all_MFRs))
