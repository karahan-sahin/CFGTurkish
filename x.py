import re

with open("propbank.csv") as f:
    lines = f.read().split("\n")
    ones = []
    for line in lines:
        if re.findall("TUR10-\d+,[A-Za-zçığü]+,.+?$",line):
            ones.append(line)

print(ones[0])

with open("propbank_update.csv","w+") as f_out:
    for line in ones:
        f_out.write(f"{line}\n")