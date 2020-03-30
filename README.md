# Game theory project - CentraleSupélec
 
Author - Gabriel Pellegrino da Silva
Contributor - Guilherme Lubk do Prado

## Scripts

### create_graphs.py

Run this script to create n random graphs and save it on a specific folder. This number n
and this specific folder are hard-coded on this script.

### generate_graph.py

This script is called multiple times by create_graphs.py to really create the graph and save it
in a file.

### test.py

Run this script to call two solvers: the one developped by https://github.com/tcsprojects/pgsolver
Note that you need to follow the instructions present there to be able to use it.
The second solver is ours, fait maison.

### zielonka.py

This is our solver for a parity game, based on https://arxiv.org/abs/1904.12446 

## Library

### tools.py

This file contains classes to create a Graph and a Node



