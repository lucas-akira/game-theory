import os
import math

num_graphs = 1
folder = 'tests/'
base_name = 'test'
#defining number of digits for name encoding
nDigits = math.trunc(math.log10(num_graphs)) + 1


if not os.path.exists(folder):
    os.makedirs(folder)


size = 30
dist = "poisson"

print("Creating graphs\n")
for i in range(num_graphs):
    print("Created", str(i).zfill(nDigits), "of", num_graphs)
    os.system("python3 generate_graph.py --fname " + folder + base_name + str(i).zfill(nDigits) + '.gm --size ' + str(size) + " --dist " + dist)

#File Structure
print("\nFile Structure:")
print("Header: purpose number_of_nodes")
print("Body: node_name color player neighbours id_code")