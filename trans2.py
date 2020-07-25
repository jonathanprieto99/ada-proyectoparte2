from cmath import inf
from dataclasses import dataclass
import random


@dataclass
class Pair:
    i: float
    j: float
    index: int

mem_pg=[]
@dataclass
class Matching:
    matching: list
    weight: float


def get_blocks(A):
    blocks = []
    flag = False
    block = Pair(0, 0, 0)
    aux_blocks = []
    j = 0
    for i in range(len(A)):
        aux_blocks.append(Pair(0, 0, 0))
        block.index = len(blocks)
        if A[i] == 1:
            if not flag:
                flag = True
                block.i = i
            if i == len(A) - 1:
                block.j = i
                aux_blocks[j].i = block.i
                aux_blocks[j].j = block.j
                aux_blocks[j].index = block.index
                blocks.append(aux_blocks[j])
                j += 1
        elif A[i] == 0:
            if flag:
                flag = False
                block.j = i - 1
                aux_blocks[j].i = block.i
                aux_blocks[j].j = block.j
                aux_blocks[j].index = block.index
                blocks.append(aux_blocks[j])
                j += 1

    return blocks


def greedy_matching(A, B):
    result = Matching([], 0)

    blocks_A = get_blocks(A)
    blocks_B = get_blocks(B)
    i = 0
    j = 0
    n = len(blocks_A)
    m = len(blocks_B)

    if n == 0 or m == 0:
        print("Error: No hay bloques en uno de los vectores")

    max_value = 0
    if n > m:
        max_value = n
        m -= 1
    else:
        max_value = m

    match = Pair(0, 0, 0)
    weight = 0
    aux_matches = []
    k = 0
    while i < max_value and j < max_value:
        aux_matches.append(Pair(0, 0, 0))
        match.i = blocks_A[i].index
        match.j = blocks_B[j].index
        weight += (blocks_A[i].j - blocks_A[i].i + 1) / (blocks_B[j].j - blocks_B[j].i + 1)
        aux_matches[k].i = match.i
        aux_matches[k].j = match.j
        result.matching.append(aux_matches[k])
        k += 1
        if i < n:
            i += 1
        if j < m:
            j += 1

        result.weight = weight
    return result

def merge_matchings (left,right):
    for i in range(len(right)):
        left.append(right[i])
    return left
def getMatchGroup(A,B):
    min_match = Matching([], 0)
    match = Pair(0, 0, 0)
    sum=0
    match.j = B[0].index
    for it in range(len(A)):
        match.i = A[it].index
        min_match.matching.append(match)
        sum += A[it].j-A[it].i+1
    min_match.weight=sum/(B[0].j-B[0].i+1)
    return min_match
def getMatchDivision(A,B):
    min_match = Matching([], 0)
    match = Pair(0, 0, 0)
    sum=0
    match.i = A[0].index
    for it in range(len(B)):
        match.i = B[it].index
        min_match.matching.append(match)
        sum += B[it].j-B[it].i+1
    min_match.weight=(A[0].j-A[0].i+1)/sum
    return min_match
def min_matching_dynamic(A,B):
    result = Matching([], 0)

    blocks_A = get_blocks(A)
    blocks_B = get_blocks(B)
    for i in blocks_A:
        mem_pg.append ([])
        for j in blocks_B:
            mem_pg[i].append (Matching([], 0))

def fill_matrix(blocks_A, blocks_B):
    for i in range(len(blocks_A)-1):
        part_A = blocks_A[0:1+i]
        part_B = blocks_B[0]
        mem_pg[i][0] = getMatchGroup(part_A, part_B)
    for j in range(len(blocks_B) - 1):
        part_B(blocks_B, blocks_B + 1 + j)
        part_A
        part_A.append(blocks_A[0])
        mem_pg[0][j] = getMatchDivision(part_A, part_B)
    for i in range(len(blocks_A) - 1):
        for j in range(len(blocks_B) - 1):
            part_A(blocks_A, blocks_A + 1 + i)
            part_B(blocks_B, blocks_B + 1 + j)
            mem_pg[i][j]=opt_solucion_dp(part_A, part_B)

    return mem_pg[len(blocks_A)-1][len(blocks_B)-1]

def opt_solution_dp(A,B):
    result = Matching([], 0)
    i = len(A)-1
    j = len(B)-1
    min_agrupacion = Matching([], 0)
    min_division = Matching([], 0)

    min_agrupacion.weight = inf
    min_division.weight = inf

    if len(A) == 1 and len(B)==1:
        match = Pair(0, 0, 0)
        match.i = A[0].index
        match.j = B[0].index
        result.matching.append(match)
        result.weight = (A[0].j - A[0].i + 1) / (B[0].j - B[0].i + 1)
        return result

    for k in range(i-1,0):
        left_A = A[:k+1]
        right_A = A[k+1:]

        left_B = B[:k-1]
        right_B = B[B-1:]

def greedy_trans(A, B):
    result = []
    temp = Matching([], 0)
    for i in range(len(A)):
        temp = greedy_matching(A[i], B[i])
        result.append(temp)
    print(result)
    return result




#def process_greedy ():
#   with open ('array.txt', 'r') as array:
#       matrix = list(array.read ())
#       print (matrix)
#   return 0
size = 4
A = []
B = []

for i in range (size):
    temp = []
    A.append (temp)
    B.append (temp)
    for j in range (size):
        A[i].append (random.randint (0, 1))
        B[i].append (random.randint (0, 1))

for i in range (size):
    print (A[i])
    print (B[i])

trans_greedy = greedy_trans (A, B)

for i in range (len (trans_greedy)):
    print (trans_greedy[i])
