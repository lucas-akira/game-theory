from random import randrange
from uuid import uuid4
from argparse import ArgumentParser
import sys

max_size = 30

def main(fname):

    with open(fname, 'w') as fout:
        size = randrange(1, max_size)

        fout.write("parity " + str(size) + ";\n")
        for i in  range(size+1):
            fout.write(str(i) + ' ')
            priority = randrange(1, 100)
            fout.write(str(priority) + ' ')
            owner = randrange(1, 3)
            owner = owner % 2
            fout.write(str(owner) + ' ')

            number_of_edges = randrange(1, size+1)
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

    try:
        args = parser.parse_args()
    except:
        parser.print_help(sys.stderr)
        exit(1)

    main(args.fname[0])

