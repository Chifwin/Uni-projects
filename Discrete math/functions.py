def _raise_if_not_positive_integer(x) -> None:
    '''
    Internal_finction for checking function arguments is they positive number
    If not, it raise exception
    '''
    if not isinstance(x, int) or x <= 0:
        raise ValueError("arguments must be positive integer")

def _raise_if_not_integer(x) -> None:
    '''
    Internal_finction for checking function arguments is they number
    If not, it raise exception
    '''
    if not isinstance(x, int):
        raise ValueError("arguments must be integer")

def factorization(num: int) -> list:
    '''
    Optimized algorithm for factorization - check divisors only for sqrt(num)
    return list of tuples (prime_number, multiplier_degree)
    '''
    _raise_if_not_positive_integer(num)
    ret = list()
    for p in range(2, num):
        if p*p > num:
            # optimization
            break

        count = 0
        while num%p == 0:
            count += 1
            num //= p

        if count:
            ret.append((p, count))

    if num > 1:
        # case when num is prime number or have one big prime divisor
        ret.append((num, 1))

    return ret

def sieve_of_eratosthenes(num: int, need_only_primes=False) -> list:
    '''
    Optimized realization of sieve of Eratosphenes
    Return list of bool values, where sieve[i] indicate is i prime number
    '''
    _raise_if_not_positive_integer(num)
    
    sieve = [True]*(num+1)
    sieve[0] = False
    sieve[1] = False

    for i in range(num+1):
        if sieve[i]:
            for j in range(i*i, num+1, i):
                # optimized with start from i*i, because numbers from 2*i to (i-1)*i
                # calculated before
                sieve[j] = False
    if not need_only_primes:
        return sieve

    primes = list()
    for i in range(num+1):
        if sieve[i]:
            primes.append(i)
    return tuple(primes)

def gcd(a: int, b: int) -> int:
    '''
    Euclidean algorithm for computing greatest common divisor (GCD)
    '''
    for i in (a, b):
        # check function arguments for validity
        if i != 0:
            _raise_if_not_positive_integer(i)
    if b == 0:
        return a
    return gcd(b, a%b)
    
def gcd_lcm_of_numbers(first: int, *nums) -> tuple:
    '''
    Return tuple (greatest_common_divisor, least_common_multiple) 
    of at least one positive integer, passed to function

    first is dedicated argument to prevent zero arguments
    '''
    _raise_if_not_positive_integer(first)
    _gcd = first
    _lcm = first
    for num in nums:
        _raise_if_not_positive_integer(num)
    
        _gcd = gcd(_gcd, num)

        # lcm of numbers a and b is (a*b)/gcd(a, b)
        _lcm = int(_lcm*num/_gcd)

    return (_gcd, _lcm)

def gcd_ext(a: int, b: int) -> tuple:
    '''
    Extended Euclidean algorithm for solving equation
    a*x + b*y = gcd(a, b)
    '''
    for i in (a, b):
        # check function arguments for validity
        # this algorithm can work also with negative numbers
        _raise_if_not_integer(i)
    if a == 0:
        x = 0
        y = 1
        return (x, y)

    new_x, new_y = gcd_ext(b%a, a)
    x = new_y - (b//a) * new_x
    y = new_x
    return (x, y)
    
def inverse_modulo(a: int, m:int):
    '''
    Compute modular multiplicative inverse x of a in modilus m
    x is such positive number such that a*x = 1 (mod m)
    '''
    _raise_if_not_positive_integer(a)
    _raise_if_not_positive_integer(m)

    if gcd(a, m) != 1:
        # In this case inverse does not exist
        return False
    ret = gcd_ext(a, m)[0]
    # if ret is negative or more than m we need to fetch it to interval [0, m)
    ret = (ret%m + m) % m
    return ret

def solve_2_sat(dis: list) -> list:
    '''
    Solve problem "2-satisfability", which consist of assigning true/false values to all variables 
        in boolean formula in conjunctive normal form to make formula equal true
    Example of the form: (a || c) && (a || !d) && (b || !d) && (b || !e) && (c || d)
    Only argument is list of disjunctions (pairs (a, b) which mean that there is (a || b))
    For convinience, in input !a shoud be designated by -a, and no "zero" vertex
    As output return false if soluntion doesn't exist, or list of vertices with true value
    '''
    n = 0
    for a, b in dis:
        _raise_if_not_integer(a)
        _raise_if_not_integer(b)
        n = max(n, max(abs(a), abs(b)))
    n = n*2 # as we create 2 vertex per variable

    # Adjacency list of future graph
    edges = [[] for i in range(n)]
    # Adjacency list of reversed future graph
    rev_edges = [[] for i in range(n)]
    
    # edges in graph is this (!a => b) and (!b => a) for disjunction (a, b)
    for a, b in dis:
        # more convinient to vertex numbers positive and a^(!a) = 1, ^ is bitwise xor
        a *= 2
        if a < 0: 
            a = -a + 1
        b *= 2
        if b < 0: 
            b = -b + 1
        a -= 2
        b -= 2
        edges[a^1].append(b)
        edges[b^1].append(a)

        rev_edges[b].append(a^1)
        rev_edges[a].append(b^1)
        
    # list of used vertices
    was = [False]*n
    order = list()

    # depth-first search for topological sort
    def dfs1(v: int):
        was[v] = True
        for u in edges[v]:
            if not was[u]:
                dfs1(u)
        order.append(v)

    for v in range(n):
        if not was[v]:
            dfs1(v)
            
    
    # number of component where vertex lies
    comp = [-1]*n

    # depth-first search for finding strongly connected components
    def dfs2(v: int, cp: int):
        comp[v] = cp
        for u in rev_edges[v]:
            if comp[u] == -1:
                # vertex wasn't visited
                dfs2(u, cp)

    comp_number = 0
    for v in order[::-1]:
        if comp[v] == -1:
            comp_number += 1
            dfs2(v, comp_number)

    ret = list()
    for v in range(n):
        if comp[v] == comp[v^1]:
            # a and !a lie in same component, so answer doesn't exist
            return False
        if comp[v] > comp[v^1] and v < v^1:
            ret.append(v//2+1)

    return ret
