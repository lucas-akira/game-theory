import os

num_graphs = 100
folder = 'tests/'
base_name = 'test'

if not os.path.exists(folder):
    os.makedirs(folder)

for i in range(num_graphs):
    print("Created", str(i).zfill(4), "of", num_graphs)
    os.system("python3 generate_graph.py --fname " + folder + base_name + str(i).zfill(4) + '.gm')
