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

expected_outcomes = []
for test in tests:
    os.system("pgsolver -global recursive --printsolonly " + folder + "/" + test + " > " + output_folder + test[:-3] + "_pg.gm")
    expected_outcomes.append(get_text("output/" + test[:-3] + "_pg.gm", True))


failed = [[] for j in range(len(methods))]
times = [[] for j in range(len(methods))]
avg_times = []
total_times = []
j = 0
print("------------------------------------")
for method in methods:
    print("METHOD: " + method)
    i = 0
    total_time = 0
    for test in tests:

        start_time = time.time()
        os.system("python3 " + method + ".py" + " --input " + folder + "/" + test + " --output " + output_folder + test[:-3] + "_pp.gm")
        elapsed_time = time.time() - start_time
        times[j].append(elapsed_time)
        actual_outcome = get_text("output/" + test[:-3] + "_pp.gm")

        equal = (expected_outcomes[i] == actual_outcome)
        result = "PASSED" if equal else "FAILED"

        print("TEST #" + str(i).zfill(4) + " - " + result + " - Elapsed time in seconds: " + str(elapsed_time))
        total_time += elapsed_time
        if result == "FAILED":
            failed[j].append(i)
        i+=1

    j+=1
    #print("Total execution time: " + str(total_time))
    #print("Average time: " + str(total_time/len(tests)))
    total_times.append(total_time)
    avg_times.append(total_time/len(tests))
    print("------------------------------------")

j = 0
print("RESULTS:")
for method in methods:
    print(method + ": Avg. Time: " + str(avg_times[j]) + " | Total time: " + str(total_times[j]))
    j+=1
print("------------------------------------")


j = 0
print("FAILED: ")
for method in methods:
    if len(failed[j]) == 0:
        print(method + ": None")
    else:
        print(method + ": " + ''.join(failed[j]))
    j+=1
print("------------------------------------")

# Find the best performing algorithm for each test

best_methods = []
print("BEST PERFORMANCE:")
for i in range(len(tests)):
    j = 0
    best_time = -1
    for method in methods:
        if best_time == -1 or times[j][i] < best_time:
            best_time = times[j][i]
            best_method = method
        j+=1
    print("TEST #" + str(i).zfill(4) + ": " + best_method + " with a time of " + str(best_time) + " seconds")
    best_methods.append(best_method)
print("------------------------------------")
print("OVERALL BEST METHOD:")
number_method = {method: 0 for method in methods}
for i in best_methods:
    number_method[i] += 1

best = max(number_method, key=lambda key: number_method[key])
print(best + ", best in " + str(100*number_method[best]/len(best_methods)) + "% of the tests")
print("NUMBER OF BEST PERFORMANCES FOR EACH METHOD:")
print(number_method)
