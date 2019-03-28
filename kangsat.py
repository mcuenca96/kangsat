#!/usr/bin/python

import sys
import random


# get clauses, n_vars, n_clauses from input file
def get_arguments():
    
    #List of lists for all the clauses
    clauses = []

    random.seed(1)

    filename = open(sys.argv[1], "r")


    for i, line in enumerate(filename):

        if i == 0:
            continue

        if i == 1 and line.split()[0] == 'p':

            n_vars = line.split()[2]
            n_clauses = line.split()[3]
            n_vars = int(n_vars)
            #pos_order = [[]] * (n_vars)
            pos_order = [[] for _ in xrange( n_vars + 1)]
            neg_order = [[] for _ in xrange( n_vars + 1)]
           
        
        else:

            tmp = line.split()
            tmp.pop()
            for literal in tmp:
                
                literal = int(literal)
                if literal > 0:
                    pos_order[literal].append(i)
            
                else:
                    literal = -literal
                    neg_order[literal].append(i)
        
            # clause_length = len(tmp)
            clauses += [tmp]
    
    return n_vars, n_clauses, clauses, pos_order, neg_order

class Interpretation():

    def __init__(self, n_vars):

        self.n_vars = int(n_vars)

   #Generate a random interpretation for our formula 
    def random_interpretation(self):
        interpretation = [0]

        for i in range(1,self.n_vars + 1):

            if random.random() < 0.5: 

                interpretation.append(int(i))

            else:
                interpretation.append(-int(i))

        return interpretation


class Solver():


    def __init__(self):

        self.n_vars, self.n_clauses, self.clauses, self.pos_order, self.neg_order = get_arguments()
        self.n_vars = int(self.n_vars)

    
    def get_rand_falsified(self, falsified_clauses):
        
        return random.choice(falsified_clauses)

    def true_lit_count(self, index):

        return len([1 for i in self.clauses[index-2] if i >= 0])
    
    # brk(x) es el nombre de clausules satisfactibles que seran insatisfactibles si girem la variable x
    def compute_break(self, fvariable, brkmin):

        brk = 0
        if fvariable >= 0:
            
            for index in self.pos_order[int(fvariable)]:
                if self.true_lit_count(index) == 1:
                    brk = brk + 1
                if brk > brkmin:
                    pass  
            return brk

        else:
            
            for index in self.pos_order[int(fvariable)]:
                if self.true_lit_count(index) == 1:
                    brk = brk + 1
                if brk > brkmin:
                    pass
           
            return brk 


    def max_sat(self, falsified_clauses, prob = 0.3):

        minVars = []
        brkmin = sys.maxint

        fclause = self.get_rand_falsified(falsified_clauses)
    
        for fvariable in fclause:
            brk = self.compute_break(fvariable, brkmin)

            if brk < brkmin:
                brkmin = brk
                del minVars[:]
                minVars.append(fvariable)
            
            elif brk == brkmin:
                minVars.append(fvariable)
            
            #print 'Break for variable' ,fvariable, '= ' , brk  
       
        if brkmin == 0:    
            fvariable = random.choice(minVars)
                
        elif random.random() < prob:
            fvariable = random.choice(fclause)

        elif 1-random.random() < prob and len(minVars) != 0:
            fvariable = random.choice(minVars)

        # print fclause
        # print 'Flip a random variable from minVars'
        # print fvariable
        return fvariable
    
    
            
    def run(self, max_flips_proportion = 3):
        
        max_flips = self.n_vars * max_flips_proportion
        rand_interpretation = Interpretation(self.n_vars).random_interpretation()
      
        while 1:

            for _ in xrange(max_flips):
    
                falsified_clauses = []
                positive_clauses = []
            
            
                for l in self.clauses:
                    length = len(l)
                    for lit in l:
                        lit = int(lit)
                        if lit == rand_interpretation[abs(lit)]:
                            break
                        else:
                            length -=1

                    if length == 0:
                        falsified_clauses.append(l)
                    
                if not falsified_clauses:

                    return rand_interpretation


                fvariable = int(self.max_sat(falsified_clauses))
                
                rand_interpretation[abs(fvariable)] *= -1
        
     
if __name__ == '__main__':
    my_solver = Solver().run()
    print 's SATISFIABLE'
    print 'v ' + ' '.join(map(str, my_solver[1:])) + ' 0'

