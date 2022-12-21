from Graph import Graph
from CRT import CRT
from functions import *


G = Graph()
G.create_graph(5, [(1, 2), (2, 3), (1, 4), (3, 5), (2, 3)])
# Graph depth-first search
print(G.dfs_order(1)) # [1, 2, 3, 5, 4], 1
print(G.dfs_order(2)) # [2, 1, 4, 3, 5], 2
print(G.dfs_order(3)) # [3, 2, 1, 4, 5], 3

# Graph breadth-first search
G = Graph()
G.create_graph(4, [(1, 3), (3, 1), (1, 2), (2, 3), (3, 4), (4, 4)], False)
print(G.bfs_order(3)) # [3, 4, 1, 2], 3

# 2-SAT solver
# on this example (a || c) && (!a || !d) && (b || !d) && (b || !e) && (c || d)
print(solve_2_sat([(1,  3), (-1,  -4), (2 , -4) , (2 , -5), (3, 4)])) #
# on this example (!a || !a)
print(solve_2_sat([(-1, -1)])) #


# prime factorization
print(factorization(452)) # [(2, 2), (113, 1)], 452
print(factorization(5670)) #  [(2, 1), (3, 4), (5, 1), (7, 1)], 5670

# Sieve of Eratosthenes
print("Prime numbers before 100:", ", ".join(map(str, sieve_of_eratosthenes(100, True))))
print("Prime numbers before 200:", ", ".join(map(str, sieve_of_eratosthenes(200, True))))

# Greater common divisor (gcd)
print(gcd, 5, 10) # 6
print(gcd, 5670, 12690) # 270
print(gcd, 567, 16) # 1

# gcd and lcm of many numbers
print(gcd_lcm_of_numbers(567, 126, 21, 3)) # (3, 1134)
print(gcd_lcm_of_numbers(567, 126, 21)) # (21, 1134)

# Extended Euclidean algorithm (gcd_ext)
print(gcd_ext(180, 150)) # (1, -1)
print(gcd_ext(1234, 4574)) # (278, -75)
print(gcd_ext(2, 4)) # (1, 0)

# Modular Multiplicative Inverse (inverse_modulo)
print(inverse_modulo(3, 26)) # 9
print(inverse_modulo(4, 26)) # False
print(inverse_modulo(1234, 12345)) # 9874

# Chinese Remainder Theorem (cheenese_remainder_theorem)
print(CRT.cheenese_remainder_theorem([35, 45], [50, 47])) # 985
print(CRT.cheenese_remainder_theorem([35, 45, 45], [50, 47, 124])) # False
print(CRT.cheenese_remainder_theorem([35, 45, 45], [50, 47, 1247])) # 586135

# CRT operations
CRT = CRT(50, 2)
print(CRT.modulus)

CRT.add(12312123124)
print(CRT.get()) # 12312123174

CRT.sub(12344)
print(CRT.get()) # 12312110830

CRT.mult(456)
print(CRT.get()) # 5614322538480

CRT.mult(-1)
print(CRT.get()) # -5614322538480
