import os
import sys
from argparse import ArgumentParser
import pandas as pd

parser = ArgumentParser()
parser.add_argument("--folder", help="folder with all the tests", nargs='+', required=True)

try:
    args = parser.parse_args()
except:
    parser.print_help(sys.stderr)
    exit(1)

folder = args.folder[0]

tests = os.listdir(folder)

for test in tests:
    os.system("pgsolver -global recursive --printsolonly " + folder + "/" + test + " > output/" + test[:-3] + "_pg.gm")
    os.system("python3 main.py --input " + folder + "/" + test + " --output output/" + test[:-3] + "_CS.gm")
    data1 = pd.read_csv("output/" + test[:-3] + "_pg.gm")
    data2 = pd.read_csv("output/" + test[:-3] + "_CS.gm")

    data1 = data1.fillna(method='ffill')
    data2 = data2.fillna(method='ffill')

    #data1 = data1.to_csv(header=None, index=False)
    #data2 = data2.to_csv(header=None, index=False)


    print(data1)
    print(data2)






