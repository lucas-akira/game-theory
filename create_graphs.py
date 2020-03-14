import os

num_graphs = 1000
folder = 'tests/'
base_name = 'test'

for i in range(num_graphs):
    os.system("python3 generate_graph.py --fname " + folder + base_name + str(i).zfill(4) + '.gm')
