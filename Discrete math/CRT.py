from functions import _raise_if_not_positive_integer, sieve_of_eratosthenes, _raise_if_not_integer, inverse_modulo

class CRT:
    def __init__(self, x: int, num=None) -> None:
        '''
        Create list of modulus for using arithmetic under Cheenese Remainder Theorem
        modulus choosed more than 10^9, their number up to 1000 let us use arithmetic with numbers up to 10^9000
        As input pass number for initializing in CRT system and number of modulus, no more than 1000
        If latter number isn't specified, than it is choosen such that let use numbers squared bigger
        '''
        _raise_if_not_integer(x)
        if num == None:
            num = 1
            cur = abs(x)
            while cur > 1:
                num += 1
                x /= 10**9
            num = min(1000, num**2)

        _raise_if_not_positive_integer(num)
        if num > 1000:
            raise ValueError("Argument is too big")

        # For factorizing numbers up to 10**10
        primes = sieve_of_eratosthenes(10**5, True)
        self.modulus = list()

        # bucket sieve of Eratosthenes
        start = 10**9+7
        end = start + 10**5
        sieve = [True]*(end-start+1)

        for p in primes:
            for j in range((start+p-1)//p*p, end+1, p):
                sieve[j-start] = False

        big_primes = []
        for i in range(start, end+1):
            if sieve[i-start]:
                big_primes.append(i)

        # set as modulus in CRT first num primes
        self.modulus = big_primes[:num]
        print(self.modulus)

        # list of remainders by CRT modulus
        self.vals = list()
        for m in self.modulus:
            self.vals.append(x%m)

        
    def mult(self, x: int) -> None:
        '''
        Multiply instance by x in CRT system
        '''
        _raise_if_not_integer(x)

        for i, m in enumerate(self.modulus):
            self.vals[i] = (x*self.vals[i])%m

    def add(self, x: int) -> None:
        '''
        Add x to instance in CRT system
        '''
        _raise_if_not_integer(x)

        for i, m in enumerate(self.modulus):
            self.vals[i] = (x+self.vals[i])%m
    
    def sub(self, x: int) -> None:
        '''
        Substract x from instance in CRT system
        '''
        _raise_if_not_integer(x)

        for i, m in enumerate(self.modulus):
            self.vals[i] = (self.vals[i] - x)%m

    def get(self) -> int:
        '''
        Return CRT instance as int
        '''
        return CRT.cheenese_remainder_theorem(self.vals, self.modulus)

    def cheenese_remainder_theorem(a: list, m: list) -> int:
        '''
        Solve system of modular equations of type
        x = a_1 (mod m_1)
        ...
        x = a_k (mod m_k)
        using Garner's algorithm
        If the function returns False, then modulus aren't pairwise relatively prime
        '''
        try:
            a[0], m[0], len(a), len(m)
        except:
            raise ValueError("Agruments must be objects with random access")
        if len(a) != len(m) or len(a) == 0:
            raise ValueError("Arguments must be equal size and non-empty") 

        for i in a: _raise_if_not_positive_integer(i)
        for i in m: _raise_if_not_positive_integer(i)

        k = len(a)

        # r[i][j] will be equal to inverse m[i] by modulus m[j]
        r = [[False]*k for _ in range(k)]

        # answer will be in form x[0] + x[1]*m[0] + x[2]*(m[0]*m[1]) + ... x[k-1]*(m[0]*...*m[k-2])
        x = [0]*k

        # in mult will be product of previous m, so on i-th stage
        # mult = m[0]*m[1]*...*m[i-1]
        mult = 1

        ret = 0
        for i in range(k):
            for j in range(k):
                r[i][j] = inverse_modulo(m[i], m[j])

        for i in range(k):
            x[i] = a[i]
            for j in range(i):
                if r[j][i] == False:
                    return False

                x[i] = r[j][i] * (x[i] - x[j])

                # if x is negative or more than p[i]
                # we need to fetch it to interval [0, p[i])
                x[i] = (x[i]%m[i] + m[i]) % m[i]

            ret += mult * x[i]

            # add new modulus to mult
            mult *= m[i]
        if ret >= mult/2:
            # this let us use negative numbers
            ret -= mult
        return ret