"""
    author: Anthony Speicher
    date: 11/19/2025
    brief: takes xls file of NOTAM data, converts it into
           NOTAM.txt, parses that file and automatically labels
    usage: python annotator.py fnsx12345.xl
"""

import json
import sys
import pandas as pd

# convert xls to NOTAM.txt
# input xls file on commandline
df = pd.read_excel(sys.argv[1])
with open("NOTAM.txt", "w") as file:
    for i in range(4, len(df['Unnamed: 6'])):
        current = df['Unnamed: 6'][i]

        # remove whitespace and write
        if i < len(df['Unnamed: 6']) - 1:
            file.write("".join(current.splitlines()) + "\n")
        else:
            file.write("".join(current.splitlines()))

# parse text file
with open("NOTAM.txt", "r") as file:
    # standard json tags
    data = {"classes":["ACCOUNTABILITY","LOCATION_IDENT","LOCATION_EXACT","LOCATION_REL","HEIGHT_EXACT","HEIGHT_REL","OBST_INFO","TIME_PERIOD","OBST_TYPE","TIMEOFDAY"]}

    # full list of annotations, each in brackets
    annotations = []

    input = file.read()
    for line in input.splitlines():
        # current data and labels to be added to annotations
        #
        current = [line]
        # entities list with actual labels
        entities = []

        # parse line
        # ACCOUNTABILITY
        entities.append([1, line.find(" ") - 1, "ACCOUNTABILITY"])

        # LOCATION_IDENT
        count = line.find(" ") + 1
        while line[count] != " ":
            count += 1
        count += 1

        entities.append([count, line.find(" ", count) - 1, "LOCATION_IDENT"])

        # OBST_TYPE
        count = line.find(" ", count) + 1
        while line[count] != " ":
            count += 1
        count += 1

        entities.append([count, line.find("(", count) - 2, "OBST_TYPE"])

        # LOCATION_EXACT,
        count = line.find("(", count) + 1
        while line[count] != ")":
            count += 1
        count += 2

        entities.append([count, line.find(" ", count) - 1, "LOCATION_EXACT"])

        # LOCATION_REL
        count = line.find("(", count) + 1

        entities.append([count, line.find(")", count) - 1, "LOCATION_REL"])
        count = line.find(")", count) + 2

        # HEIGHT_EXACT
        entities.append([count, line.find("(", count) - 2, "HEIGHT_EXACT"])

        # HEIGHT_REL
        count = line.find("(", count) + 1

        entities.append([count, line.find(")", count) - 1, "HEIGHT_REL"])
        count = line.find(")", count) + 2

        # OBST_INFO
        end = line.rfind(" ")
        entities.append([count, end - 1, "OBST_INFO"])

        # TIME_PERIOD
        entities.append([end + 1, len(line) - 1, "TIME_PERIOD"])


        current.append({"entities":entities})
        annotations.append(current)


data["annotations"] = annotations

# write results
with open("finalannotations.json", "w") as file:
    json.dump(data, file)
