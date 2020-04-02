import os
import sys
import time
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

methods = ["op1_pawel", "op2_pawel", "op3_pawel", "op4_pawel"]
i = 0
failed = []
for method in methods:
    print("METHOD: " + method)
    for test in tests:
        os.system("./pgsolver -global recursive --printsolonly " + folder + "/" + test + " > " + output_folder + test[:-3] + "_pg.gm")
        start_time = time.time()
        os.system("python3 " + method + ".py" + " --input " + folder + "/" + test + " --output " + output_folder + test[:-3] + "_pp.gm")
        elapsed_time = time.time() - start_time

        f1 = get_text("output/" + test[:-3] + "_pg.gm", True)
        f2 = get_text("output/" + test[:-3] + "_pp.gm")


        equal = f1 == f2
        result = "PASSED" if equal else "FAILED"

        print("TEST #" + str(i).zfill(4) + " - " + result + " - Elapsed time in seconds: " + str(elapsed_time))

        if result == "FAILED":
            failed.append(i)
        i+=1

print("FAILED: ", failed)
