from sage.all import *
from classes.coordinates import TableauColumn
from classes.variety import FlagVariety
from classes.monomial import TableauMonomial
from classes.polynomial import TableauPolynomial
from classes.tableau_relation import TableauRelation

class StraightenAlgo:
    def __init__(self,monomial):
        self.monomial = monomial.deepcopy()
        self.poly = TableauPolynomial([monomial.deepcopy()])
        self.state = 0   #0:"Not started", 1:"Started", 2:"Finished"
        self.rel_count = 0 # total relations applied till now.
        self.steps = []

    def do_one_step(self):
        if self.state == 2:
            return
        self.state = 1
        (term_idx,ncpair) = self.poly.get_nc_pair()
        if term_idx == None:
            self.state = 2
            return

        R = TableauRelation(self.monomial.variety,ncpair)
        step_details = {"poly":self.poly,"term": term_idx,"ncpair":ncpair,"relation":R}
        self.steps.append(step_details)
        v1 = R[0].vec
        v2 = self.poly[term_idx].vec
        tm_coef = (self.poly[term_idx].coef)#temporary monomial
        tm_temp = TableauMonomial(self.monomial.variety, -tm_coef, vec=v2-v1)
        R = R*TableauPolynomial([tm_temp])
        self.poly = self.poly + R

        self.rel_count = self.rel_count + 1

    def straighten(self,wait=False,max_steps=100):
        while self.state!=2 and max_steps > self.rel_count:
            StraightenAlgo.do_one_step(self)
            #self.print_step(-1)
            if wait:
                x = input("Stop? [y/*] : ")
                if x == "y":
                    return
        return

    def print_steps(self):
        for i in range(self.rel_count):
            self.print_step(i)

    def print_step(self,i):
        if i >= len(self.steps):
            return
        d = self.steps[i]
        print("===========================Step "+str(i)+"===========================")
        print("Polynomial to straighten:")
        print(d["poly"])
        print("Non comparable columns are in term "+str(d["term"]))
        print("Relation being applied is")
        print(d["relation"])
        print("=====================================================================")

        return

    def write_steps(self):

        print("We will straighten following monomial")
        print(self.monomial)
        print("we will apply following plucker relation")
        print(self.steps[0]["relation"])
        for i in range(1,self.rel_count):
            d = self.steps[i]
            print("we get")
            print(d["poly"])
            print(f"Above polynomial is nonstandard and the term {d['term']} contains noncomparable pair. We apply following plucker relation.")
            print(d["relation"])
        print("We have following polynomial which contain all standard monomials.")
        print(self.poly)

    def do_one_step_manual(self,ncpair,term_idx):
        if self.state == 2:
            return
        self.state = 1
        if term_idx == None:
            self.state = 2
            return

        R = TableauRelation(self.monomial.variety,ncpair)
        step_details = {"poly":self.poly,"term": term_idx,"ncpair":ncpair,"relation":R}
        self.steps.append(step_details)
        v1 = R[0].vec
        v2 = self.poly[term_idx].vec
        tm_coef = (self.poly[term_idx].coef)#temporary monomial
        tm_temp = TableauMonomial(self.monomial.variety, -tm_coef, vec=v2-v1)
        R = R*TableauPolynomial([tm_temp])
        self.poly = self.poly + R

        self.rel_count = self.rel_count + 1

