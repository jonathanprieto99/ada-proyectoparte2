from dataclasses import dataclass
import random
import math
from cmath import inf
import numpy

mem_pg = []

@dataclass 
class Pair:
    i: float
    j: float
    index: int

@dataclass
class Matching:
    tipo: int
    matching: list
    weight: float

@dataclass
class transformation_block:
    start_index: int
    end_index: int 
    scaled_size: float
    direction: bool
    distance: int
    final_position: int
    current_traversed: int

def get_blocks (A):
    blocks = []
    flag = False
    block = Pair (0, 0, 0)
    aux_blocks = []
    j = 0
    for i in range (len (A)):
        aux_blocks.append (Pair (0, 0, 0))
        block.index = len (blocks)
        if A[i] == 1:
            if not flag:
                flag = True
                block.i = i
            if i == len (A) - 1:
                block.j = i
                aux_blocks[j].i = block.i
                aux_blocks[j].j = block.j
                aux_blocks[j].index = block.index
                blocks.append (aux_blocks[j])
                j += 1
        elif A[i] == 0:
            if flag:
                flag = False
                block.j = i - 1
                aux_blocks[j].i = block.i
                aux_blocks[j].j = block.j
                aux_blocks[j].index = block.index
                blocks.append (aux_blocks[j])
                j += 1

    return blocks

def greedy_matching (A, B):
    result = Matching(0, [], 0)

    blocks_A = get_blocks (A)
    blocks_B = get_blocks (B)
    i = 0
    j = 0
    n = len (blocks_A) - 1
    m = len (blocks_B) - 1 

    if n < 0 or m < 0:

        print ("Error: No hay bloques en uno de los vectores")
        return result
    
    max_value = 0
    if n > m:
        max_value = n
        m -= 1
    else:
        max_value = m

    match = Pair (0, 0, 0)
    weight = 0
    aux_matches = []
    k = 0
    while i < max_value and j < max_value:
        aux_matches.append (Pair (0, 0, 0))
        match.i = blocks_A[i].index
        match.j = blocks_B[j].index
        weight += (blocks_A[i].j - blocks_A[i].i + 1) / (blocks_B[j].j - blocks_B[j].i + 1)
        aux_matches[k].i = match.i
        aux_matches[k].j = match.j
        result.matching.append (aux_matches[k])
        k += 1
        if i < n:
            i += 1
        if j < m:
            j += 1

        result.weight = weight
    return result

def greedy_trans (A, B):
    result = []
    temp = Matching (0, [], 0)
    for i in range (len (A)):
        temp = greedy_matching (A[i], B[i])
        result.append (Matching (temp.tipo, temp.matching, temp.weight))
    return result


def merge_matchings (left,right):
    for i in range(len(right)):
        left.append(right[i])
    return left

def getMatchGroup (A, B):
    min_match = Matching (0, [], 0)
    match = Pair (0, 0, 0)
    suma = 0.0
    match.j = B[0].index
    aux_matches = []
    for it in range (len (A)):
        match.i = A[it].index
        aux_matches.append (Pair (match.i, match.j, 0))
        min_match.matching.append (aux_matches[it])
        suma += A[it].j - A[it].i + 1
    min_match.weight = suma / (B[0].j - B[0].i + 1)
    return min_match

def getMatchDivision (A, B):
    min_match = Matching (0, [], 0)
    match = Pair (0, 0, 0)
    suma = 0.0
    match.i = A[0].index
    aux_matches = []
    for it in range (len (B)):
        match.j = B[it].index
        aux_matches.append (Pair (match.i, match.j, 0))
        min_match.matching.append (aux_matches[it])
        suma += B[it].j - B[it].i + 1
    min_match.weight = (A[0].j - A[0].i + 1) / suma
    return min_match

def getMatchGroup_avg (A, B, var):
    min_match = Matching (0, [], 0)
    match = Pair (0, 0, 0)
    suma = 0.0
    match.j = B[0].index
    aux_matches = []
    for it in range (len (A)):
        match.i = A[it].index
        aux_matches.append (Pair (match.i, match.j, 0))
        min_match.matching.append (aux_matches[it])
        suma += A[it].j - A[it].i + 1
    min_match.weight = abs ((suma / (B[0].j - B[0].i + 1)) - var)
    return min_match

def getMatchDivision_avg (A, B, var):
    min_match = Matching (0, [], 0)
    match = Pair (0, 0, 0)
    suma = 0.0
    match.i = A[0].index
    aux_matches = []
    for it in range (len (B)):
        match.j = B[it].index
        aux_matches.append (Pair (match.i, match.j, 0))
        min_match.matching.append (aux_matches[it])
        suma += B[it].j - B[it].i + 1
    min_match.weight = abs (((A[0].j - A[0].i + 1) / suma) - var)
    return min_match

def min_matching_dynamic (A, B):
    blocks_A = get_blocks (A)
    blocks_B = get_blocks (B)

    for i in range (len (A)):
        mem_pg.append ([])
        for j in range (len (blocks_B)):
            mem_pg[i].append (Matching (0, [], 0)) 
    min_matching = fill_matrix (blocks_A, blocks_B)
    return min_matching

def min_matching_dynamic_avg (A, B):
    blocks_A = get_blocks (A)
    blocks_B = get_blocks (B)
    var = get_var (blocks_A, blocks_B)
    for i in range (len (A)):
        mem_pg.append ([])
        for j in range (len (blocks_B)):
            mem_pg[i].append (Matching (0, [], 0))
    min_matching = fill_matrix_avg (blocks_A, blocks_B, var)
    return min_matching

def fill_matrix (blocks_A, blocks_B):
    if len (blocks_A) == 0 or len (blocks_B) == 0:
        return Matching (0, [], 0)
    for i in range (len (blocks_A)):
        part_A = blocks_A[:1 + i]
        part_B = [blocks_B[0]]
        mem_pg[i][0] = getMatchGroup (part_A, part_B)
    for j in range (len (blocks_B)):
        part_A = [blocks_A[0]]
        part_B = blocks_B[:1 + j]
        mem_pg[0][j] = getMatchDivision (part_A, part_B)
    for i in range (1, len (blocks_A)):
        for j in range (1, len (blocks_B)):
            #print ("filling spot " + str(i) + "," + str(j))
            part_A = blocks_A[:1 + i]
            part_B = blocks_B[:1 + j]
            mem_pg[i][j] = opt_solution_dp (part_A, part_B)
    return mem_pg[len (blocks_A) - 1][len (blocks_B) - 1]

def fill_matrix_avg (blocks_A, blocks_B, var):
    for i in range (len (blocks_A)):
        part_A = blocks_A[:1 + i]
        part_B = [blocks_B[0]]
        mem_pg[i][0] = getMatchGroup_avg (part_A, part_B, var)
    for j in range (len (blocks_B)):
        part_A = [blocks_A[0]]
        part_B = blocks_B[:1 + j]
        mem_pg[0][j] = getMatchDivision_avg (part_A, part_B, var)
    for i in range (1, len (blocks_A)):
        for j in range (1, len (blocks_B)):
            part_A = blocks_A[:1 + i]
            part_B = blocks_B[:1 + j]
            mem_pg[i][j] = opt_solution_dp_avg (part_A, part_B, var)
    return mem_pg[len (blocks_A) - 1][len (blocks_B) - 1]


def opt_solution_dp (A, B):
    min_match = Matching (0, [], 0)
    i = len (A) - 1
    j = len (B) - 1
    min_agrupacion = Matching (0, [], inf)
    min_division = Matching (0, [], inf)

    if len (A) == 1 and len (B) == 1:
        pair = Pair (A[0].index, B[0].index, 0)
        matching = Matching (0, [Pair(pair.i, pair.j, 0)],(A[0].j - A[0].i + 1) / (B[0].j - B[0].i + 1))
        return matching
    k = i - 1
    while k >= 0:
        left_A = A[:k + 1]
        right_A = A[k + 1:]
        left_B = B[:len (B) - 1]
        right_B = [B[len (B) - 1]]
        min_left = mem_pg[len (left_A) - 1][len (left_B) - 1]
        min_right = getMatchGroup (right_A, right_B)
        merge = Matching (0, merge_matchings (min_left.matching, min_right.matching), min_left.weight + min_right.weight)
        if merge.weight < min_agrupacion.weight:
            min_agrupacion = Matching (0, merge.matching, merge.weight)
        k-= 1

    k = j - 1
    while k >= 0:
        left_A = A[:len (A) - 1]
        right_A = [A[len (A) - 1]]
        left_B = B[:k + 1]
        right_B = B[k + 1:]
        min_left = mem_pg[len (left_A) - 1][len (left_B) - 1]
        min_right = getMatchDivision (right_A, right_B)
        merge = Matching (0, merge_matchings (min_left.matching, min_right.matching), min_left.weight + min_right.weight)
        if merge.weight < min_division.weight:
            min_division = Matching (0, merge.matching, merge.weight)
        k -= 1
    if min_agrupacion.weight < min_division.weight:
        return min_agrupacion
    else:
        return min_division

def opt_solution_dp_avg (A, B, var):
    min_match = Matching (0, [], 0)
    i = len (A) - 1
    j = len (B) - 1
    min_agrupacion = Matching (0, [], inf)
    min_division = Matching (0, [], inf)
    if len (A) == 1 and len (B) == 1:
        pair = Pair (A[0].index, B[0].index, 0)
        matching = Matching (0, [Pair(pair.i, pair.j, 0)],(A[0].j - A[0].i + 1) / (B[0].j - B[0].i + 1))
        return matching
    k = i - 1
    while k >= 0:
        left_A = A[:k + 1]
        right_A = A[k + 1:]

        left_B = B[:len (B) - 1]
        right_B = [B[len (B) - 1]]

        min_left = mem_pg[len (left_A) - 1][len (left_B) - 1]
        min_right = getMatchGroup_avg (right_A, right_B, var)
        merge = Matching (0, merge_matchings (min_left.matching, min_right.matching), min_left.weight + min_right.weight)
        if merge.weight < min_agrupacion.weight:
            min_agrupacion = Matching (0, merge.matching, merge.weight)
        k-= 1

    k = j - 1
    while k >= 0:
        left_A = A[:len (A) - 1]
        right_A = [A[len (A) - 1]]

        left_B = B[:k + 1]
        right_B = B[k + 1:]
        min_left = mem_pg[len (left_A) - 1][len (left_B) - 1]
        min_right = getMatchDivision_avg (right_A, right_B, var)
        merge = Matching (0, merge_matchings (min_left.matching, min_right.matching), min_left.weight + min_right.weight)
        if merge.weight < min_division.weight:
            min_division = Matching (0, merge.matching, merge.weight)
        k -= 1
    if min_agrupacion.weight < min_division.weight:
        return min_agrupacion
    else:
        return min_division

def get_var (A, B):
    sum_a = 0
    sum_b = 0
    for block in A:
        sum_a += block.j - block.i + 1
    for block in B:
        sum_b += block.j - block.i + 1
    var = sum_a / sum_b
    return var

def dp_trans (A, B):
    result = []
    temp = Matching (0, [], 0)
    for i in range (len (A)):
        temp = min_matching_dynamic (A[i], B[i])
        result.append (Matching (temp.tipo, temp.matching, temp.weight))
    return result

def dp_trans_avg (A, B):
    result = []
    temp = Matching (0, [], 0)
    for i in range (len (A)):
        temp = min_matching_dynamic_avg (A[i], B[i])
        result.append (Matching (temp.tipo, temp.matching, temp.weight))
    return result

def generate_animation (image_1, image_2, matchings):
    transition = generate_transition (image_1, image_2, matchings)
    images = []
    for image in transition:
        for row in image:
            row = numpy.logical_not (row)
    images.append (image_1)
    for image in transition:
        images.append (image)
    images.append (image_2)
    return images 
    
def generate_transition (image_1, image_2, matchings):
    transition = []
    #print (len (image_1))
    for i in range (5):
        transition.append ([])
    for i in range (len (image_1)):
        #print (i)
        matrix = get_matrix (image_1[i], image_2[i], matchings[i])
        for j in range (5):
            transition[j].append (matrix[j + 1])
    return transition

def get_matrix (vector_1, vector_2, matching):
    #print ("row")
    blocks_1 = get_blocks (vector_1)
    blocks_2 = get_blocks (vector_2)
    if len (blocks_1) == 0 or len (blocks_2) == 0 or len(matching.matching) == 0:
        return [vector_1, [False for i in range (len (vector_1))], [False for i in range (len (vector_1))], [False for i in range (len (vector_1))], [False for i in range (len (vector_1))], [False for i in range (len (vector_1))], vector_2]
    matrix = []
    matrix.append (vector_1)
    for i in range (5):
        matrix.append ([])
    matrix.append (vector_2)
    matches = []
    pairs = []
    tipo = 0
    for pair in matching.matching:
        if len (pairs) == 0:
            pairs.append (pair)
            tipo = 0
        else:
            i = len (pairs) - 1
            if pair.i == pairs[i].i or pair.j == pairs[i].j:
                if pair.i == pairs[i].i:
                    tipo = 1
                else:
                    tipo = 2
                pairs.append (pair)
            else:
                matches.append (Matching (tipo, pairs[:], 0))
                pairs.clear ()
                pairs.append (pair)
    matches.append (Matching (tipo, pairs[:], 0))

    transition_blocks = []
    for match in matches:
        if match.tipo == 0:
            #print ("processing one to one")
            start_block = match.matching[0].i
            final_block = match.matching[0].j
            scaled_size = blocks_2[final_block].j - blocks_2[final_block].i + 1
            final_position = blocks_2[final_block].i
            start_index = blocks_1[start_block].i
            end_index = blocks_1[start_block].j
            if blocks_1[start_block].i > blocks_2[final_block].i:
                direction = True
                distance = blocks_1[start_block].i - blocks_2[final_block].i
            elif blocks_1[start_block].i < blocks_2[final_block].i:
                direction = False
                distance = blocks_2[final_block].i - blocks_1[start_block].i
            else:
                direction = False
                distance = 0
            #print ("start_index: " + str(start_index))
            #print ("end_index: " + str(end_index))
            #print ("scaled_size: " + str(scaled_size))
            #print ("direction: " + str(direction))
            #print ("distance: " + str(distance))
            #print ("final_position " + str(final_position))
            transition_blocks.append (transformation_block (start_index, end_index, scaled_size, direction, distance, final_position, 0))
        elif match.tipo == 1:
            #print ("processing division")
            start_block = match.matching[0].i
            start_block_size = blocks_1[start_block].j - blocks_1[start_block].i + 1
            final_blocks = []
            for pair in match.matching:
                final_blocks.append (pair.j)
            total_size = 0.0
            for block in final_blocks:
                total_size += blocks_2[block].j - blocks_2[block].i + 1
            
            next_block_start = blocks_1[start_block].i
            for block in final_blocks:
                start_index = next_block_start
                scaled_size = blocks_2[block].j - blocks_2[block].i + 1
                final_position = blocks_2[block].i
                proportion = scaled_size / total_size
                start_block_portion_size = proportion * start_block_size
                end_index = start_index + math.floor (start_block_portion_size)
                #print ("next block start: " + str(next_block_start))
                next_block_start = end_index + 1
                if start_index > blocks_2[block].i:
                    direction = True
                    distance = start_index - blocks_2[block].i
                elif start_index < blocks_2[block].i:
                    direction = False
                    distance = blocks_2[block].i - start_index
                else:
                    direction = False
                    distance = 0
                #print ("start_index: " + str(start_index))
                #print ("start_block_size: " + str(start_block_size))
                #print ("end_index: " + str(end_index))
                #print ("scaled_size: " + str(scaled_size))
                #print ("direction: " + str(direction))
                #print ("distance: " + str(distance))
                #print ("final_position " + str(final_position))
                transition_blocks.append (transformation_block (start_index, end_index, scaled_size, direction, distance, final_position, 0))
        else:
            #print ("processing agroupation")
            start_blocks = []
            final_block = match.matching[0].j
            final_block_size = blocks_2[final_block].j - blocks_2[final_block].i + 1
            for pair in match.matching:
                start_blocks.append (pair.i)
            total_size = 0.0
            for block in start_blocks:
                total_size += blocks_1[block].j - blocks_1[block].i + 1

            next_block_start = blocks_2[final_block].i
            for block in start_blocks:
                start_index = blocks_1[block].i
                end_index = blocks_1[block].j
                proportion = (end_index - start_index + 1) / total_size
                scaled_size = math.floor (proportion * final_block_size)
                final_position = next_block_start
                next_block_start = final_position + scaled_size + 1
                if start_index > final_position:
                    direction = True
                    distance = start_index - final_position
                elif start_index < final_position:
                    direction = False
                    distance = final_position - start_index
                else:
                    direction = False
                    distance = 0
                if scaled_size == 0:
                    scaled_size = 1
                #print ("start_index: " + str(start_index))
                #print ("final_block_size: " + str (final_block_size))
                #print ("end_index: " + str(end_index))
                #print ("scaled_size: " + str(scaled_size))
                #print ("direction: " + str(direction))
                #print ("distance: " + str(distance))
                #print ("final_position " + str(final_position))
                transition_blocks.append (transformation_block (start_index, end_index, scaled_size, direction, distance, final_position, 0))
    #print (transition_blocks) 
    for i in range (1, 6):
        #print ("=========================")
        #print ("TRANSITION " + str(i))
        for j in range (len (vector_1)):
            matrix[i].append (False)
        for block in transition_blocks:
            #print ("calculating block")
            #print (block)
            if (block.end_index - block.start_index + 1) > block.scaled_size:
                #print ("current bigger than final")
                #print ("end_index: " + str(block.end_index))
                #print ("start_index: " + str(block.start_index))
                #print ("current_traversed: " + str (block.current_traversed))
                #print ("scaled_size: " + str (block.scaled_size))
                #print ("current size growth: " + str (block.current_traversed * (block.end_index - block.start_index + 1 - block.scaled_size) / 5))
                #current_size = (block.end_index - block.start_index + 1) - math.floor (block.current_traversed * (block.end_index - block.start_index + 1 - block.scaled_size) / 5)
                current_size = (block.end_index - block.start_index + 1) - math.floor(block.current_traversed * (block.scaled_size / 5))
            elif (block.end_index - block.start_index + 1) < block.scaled_size:
                #print ("current smaller than final")
                #current_size = (block.end_index - block.start_index + 1) + math.floor (block.current_traversed * (block.scaled_size - block.end_index - block.start_index + 1) / 5)
                current_size = (block.end_index - block.start_index + 1) + math.floor(block.current_traversed * (block.scaled_size / 5))
                #print ("current bigger than final")
                #print ("end_index: " + str(block.end_index))
                #print ("start_index: " + str(block.start_index))
                #print ("current_traversed: " + str (block.current_traversed))
                #print ("scaled_size: " + str (block.scaled_size))
            else:
                #print ("current equal to final")
                current_size = block.scaled_size
            if block.distance != 0:
                if block.direction == True:
                    current_position = block.start_index - math.floor (block.current_traversed * (block.distance / 5))
                else:
                    current_position = block.start_index + math.floor (block.current_traversed * (block.distance / 5))
            else:
                current_position = block.start_index
            #print ("beggining transition")
            #print ("current position: " + str(current_position))
            #print ("current size: " + str(current_size))
            for k in range (current_size):
                if current_position + k < len (vector_1):
                    matrix[i][current_position + k] = True
            block.current_traversed += 1
            #print ("----------------------")
        #print ("=========================")
    print ("matrix obtained")     
    return matrix

#size = 4
#A = [1, 0, 0, 1, 1, 1, 0, 1]
#B = [0, 1, 0, 0, 0, 1, 0, 0]

#for i in range(size):
#    temp = []
#    A.append(temp)
#    B.append(temp)
#for j in range(size):
#        A[i].append(random.randint(0, 1))
#        B[i].append(random.randint(0, 1))
#B.reverse()
#for i in range(size):
#    print(A[i])
#    print(B[i])
#result = dp_trans_avg (A, B)

#for match in result:
#    print (match)

#result = min_matching_dynamic (A, B)
#print (result)
