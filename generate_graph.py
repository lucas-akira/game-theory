from random import randrange
from uuid import uuid4
from argparse import ArgumentParser
import sys
import numpy as np



def main(fname, size, dist, lam):

    with open(fname, 'w') as fout:
        #Each graph have the same amount of nodes 
        size = int(size) - 1
        fout.write("parity " + str(size+1) + ";\n")
        for i in  range(size+1):
            fout.write(str(i) + ' ')
            priority = randrange(1, 100)
            fout.write(str(priority) + ' ')
            owner = randrange(0, 2)
            fout.write(str(owner) + ' ')
            #Number of edges
            if dist == "unif":
                number_of_edges = randrange(1, size+1)
            elif dist == "poisson":
                number_of_edges = np.random.poisson(lam) + 1
                if number_of_edges > size:
                    number_of_edges = 4
                print("Number of edges = " + str(number_of_edges))
            elif dist == "gaussian":
                number_of_edges = 10
            
            used = [0] * (size + 1)
            for j in range(number_of_edges):

                while True:
                    t = randrange(0, size + 1)
                    if t != i and used[t] == 0:
                        # only add edges to other vertexes, dont allow self loops
                        used[t] = 1
                        fout.write(str(t))
                        break

                if j == number_of_edges - 1:
                    fout.write(" ")
                else:
                    fout.write(",")

            
            uuid = uuid4()
            fout.write("\"" + str(uuid) + "\";\n")

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument("--fname", help="name of the file to be created", nargs=1, required=True)
    parser.add_argument("--size", help="max size of each graph. Default = 30", nargs=1, required=True)
    parser.add_argument("--dist", help="unif - poisson - gaussian - probability distribution of the degree of each node", nargs=1, required=True)

    try:
        args = parser.parse_args()
    except:
        parser.print_help(sys.stderr)
        exit(1)

    main(args.fname[0], args.size[0], args.dist[0], lam = 30)

