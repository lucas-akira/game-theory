import os
import sys
from argparse import ArgumentParser
import pandas as pd

def get_text(name, remove=False):

    f = []
    with open(name, 'r') as file:
        for line in file.readlines()[1:]:
            line = line.replace(";", "")
            line = line.replace("\n", "")
            line = line.split(" ")
            if remove and len(line) == 3:
                line = line[:-1]
            f.append(line)

    return f


parser = ArgumentParser()
parser.add_argument("--folder", help="test folder", nargs='+', required=True)

try:
    args = parser.parse_args()
except:
    parser.print_help(sys.stderr)
    exit(1)

folder = args.folder[0]

tests = os.listdir(folder)

output_folder = "output/"

if not os.path.exists(output_folder):
    os.makedirs(output_folder)


i = 0
failed = []
for test in tests:
    os.system("pgsolver -global recursive --printsolonly " + folder + "/" + test + " > " + output_folder + test[:-3] + "_pg.gm")
    os.system("python3 zielonka.py --input " + folder + "/" + test + " --output " + output_folder + test[:-3] + "_CS.gm")


    f1 = get_text("output/" + test[:-3] + "_pg.gm", True)
    f2 = get_text("output/" + test[:-3] + "_CS.gm")


    equal = f1 == f2
    result = "PASSED" if equal else "FAILED"

    print("TEST #" + str(i).zfill(4) + " - " + result)

    if result == "FAILED":
        failed.append(i)
    i+=1

print("FAILED: ", failed)
