# Game theory project - CentraleSupélec
 
Author - Gabriel Pellegrino da Silva

Contributor - Guilherme Lubk do Prado
	      Lucas Akira Morishita

## Graph Creation

### create\_graphs.py

Run this script to create n random graphs and save it on a specific folder. This number n
and this specific folder are hard-coded on this script.

### generate\_graph.py

This script is called multiple times by create\_graphs.py to really create the graph and save it
in a file.

### tools.py

This file contains classes to create a Graph and a Node

## Result Analysis

### test.py

Run this script to call two solvers: the one developped by https://github.com/tcsprojects/pgsolver
Note that you need to follow the instructions present there to be able to use it.
The second solver is ours, fait maison.


## Solvers

### zielonka.py

This is our solver for a parity game, based on https://arxiv.org/abs/1904.12446 

### pawel\_parys.py

Pawel Parys improvements over the zielonka's algorithm, a Quasi-polynomial approach.
https://www.mimuw.edu.pl/~parys/publications/2018-parity-algorithm.pdf

## Solvers improvements

On the conclusion of his paper, https://www.mimuw.edu.pl/~parys/publications/2018-parity-algorithm.pdf, Pawel Parys commented
another five possible optimization. Some of them are implemented below, note that they are incremental, that said, op4 contain
the improvements 1, 2, 3 and 4 and the pawel\_parys.py initial improvement described on his paper.

### op1\_pawel.py
Over the years, some optimizations to Zielonka’s algorithm were proposed. Replace the loopguard WO=∅ by WO=AtrO(G,WO) (which ensures that WO will be empty in the next iteration of the loop). 

### op2\_pawel.py
check whether AtrE(G,Nh) contains all nodes of priority h−1, and if so, to extend Nh by nodes of the next highest Even priority (i.e., h−2).
It seems that these optimizations can be applied to our algorithm as well.

### op3\_pawel.py
A straightforward optimization is to decrease pO and pE to |G| at the beginning of every recursive call.

### op4\_pawel.py
One can also observe that the call to SolveO in line 13 (with the full precision) gets the same subgame H as the last call to SolveO in line 8 (with decreased precision). 
A very rough idea is to make someuse of the computations performed by the decreased-precision call during the full-precision call.

### zielonka\_1.py

Zielonka standard implementation with the same improvement as op1.

### zielonka\_2.py

Zielonka standard implementation with the same improvement as op2.
