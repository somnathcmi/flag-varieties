from sage.all import *
from classes.coordinates import TableauColumn
from classes.variety import FlagVariety
from classes.monomial import TableauMonomial
from classes.polynomial import TableauPolynomial

class TableauRelation(TableauPolynomial):
    def __init__(self,variety,ncpair):
        monomials = TableauRelation._plucker_relation(variety,ncpair)
        super().__init__(monomials)

    @staticmethod
    def _plucker_relation(v,ncpair):#v is variety
        #if v.d != 3:
        #    raise NotImplementedError("implemented only for d=3")

        def case210(p,q): #len(p)=2,len(q)=2; non-comparable index is 1;
            #following are shuffles required: id; (p0,q0); (p1,q0)
            pc = TableauColumn
            pm = TableauMonomial

            res = \
            [pm(v, 1,coords=[pc(p),pc(q)]), \
            pm(v,-1,coords=[pc([q[0],p[1]]),pc([p[0]])] ), \
            pm(v,-1,coords=[pc([p[0],q[0]]),pc([p[1]])] )]

            return res

        def case221(p,q): #len(p)=2,len(q)=2; non-comparable index is 2;
            #following are shuffles required: id; (p1,q1); (p1,q0);
            pc = TableauColumn
            pm = TableauMonomial

            res = \
            [pm(v, 1,coords=[pc(p),pc(q)]), \
            pm(v,-1,coords=[pc([p[0],q[1]]),pc([q[0],p[1]])]),\
            pm(v,-1,coords=[pc([p[0],q[0]]),pc([p[1],q[1]])])]
            return res

        def case310(p,q): #len(p)=3,len(q)=1; non-comparable index is 1;
            #following are shuffles required: id; (p0,q0); (p1,q0); (p2,q0)
            pc = TableauColumn
            pm = TableauMonomial

            res = \
            [pm(v, 1,coords=[pc(p),pc(q)]), \
            pm(v,-1,coords=[pc([q[0],p[1],p[2]]),pc([p[0]])] ), \
            pm(v,-1,coords=[pc([p[0],q[0],p[2]]),pc([p[1]])] ), \
            pm(v,-1,coords=[pc([p[0],p[1],q[0]]),pc([p[2]])] ) ]

            return res

        def case320(p,q): #len(p)=3,len(q)=2; non-comparable index is 1;
            #following are shuffles required: id; (p0,q0); (p1,q0); (p2,q0)
            pc = TableauColumn
            pm = TableauMonomial

            res = \
            [pm(v, 1,coords=[pc(p),pc(q)]), \
            pm(v,-1,coords=[pc([q[0],p[1],p[2]]),pc([p[0],q[1]])] ), \
            pm(v,-1,coords=[pc([p[0],q[0],p[2]]),pc([p[1],q[1]])] ), \
            pm(v,-1,coords=[pc([p[0],p[1],q[0]]),pc([p[2],q[1]])] ) ]

            return res

        def case321(p,q): #len(p)=3,len(q)=2; non-comparable index is 2;
            #following are shuffles required: id; (p1,q1); (p2,q1); (p1,q0); (p2,q0); (p1,q0)(p2,q1)
            pc = TableauColumn
            pm = TableauMonomial

            res = \
            [pm(v, 1,coords=[pc(p),pc(q)]), \
            pm(v,-1,coords=[pc([p[0],q[1],p[2]]),pc([q[0],p[1]])]),\
            pm(v,-1,coords=[pc([p[0],q[0],p[2]]),pc([p[1],q[1]])]), \
            pm(v,-1,coords=[pc([p[0],p[1],q[1]]),pc([q[0],p[2]])]), \
            pm(v,-1,coords=[pc([p[0],p[1],q[0]]),pc([p[2],q[1]])]), \
            pm(v, 1,coords=[pc([p[0],q[0],q[1]]),pc([p[1],p[2]])])]

            return res

        def case331(p,q): #len(p)=3,len(q)=3; non-comparable index is 2;
            #following are shuffles required: id; (p1,q1); (p2,q1); (p1,q0); (p2,q0); (p1,q0)(p2,q1)
            pc = TableauColumn
            pm = TableauMonomial

            res = \
            [pm(v, 1,coords=[pc(p),pc(q)]), \
            pm(v,-1,coords=[pc([p[0],q[1],p[2]]),pc([q[0],p[1],q[2]])]),\
            pm(v,-1,coords=[pc([p[0],q[0],p[2]]),pc([p[1],q[1],q[2]])]), \
            pm(v,-1,coords=[pc([p[0],p[1],q[1]]),pc([q[0],p[2],q[2]])]), \
            pm(v,-1,coords=[pc([p[0],p[1],q[0]]),pc([p[2],q[1],q[2]])]), \
            pm(v, 1,coords=[pc([p[0],q[0],q[1]]),pc([p[1],p[2],q[2]])])]

            return res

        def case332(p,q): #len(p)=3,len(q)=3; non-comparable index is 3;
            #following are shuffles required: id; (p2,q0); (p2,q1); (p2,q2)
            pc = TableauColumn
            pm = TableauMonomial

            res = \
            [pm(v, 1,coords=[pc(p),pc(q)]), \
            pm(v,-1,coords=[pc([p[0],p[1],q[0]]),pc([p[2],q[1],q[2]])] ), \
            pm(v,-1,coords=[pc([p[0],p[1],q[1]]),pc([q[0],p[2],q[2]])] ), \
            pm(v,-1,coords=[pc([p[0],p[1],q[2]]),pc([q[0],q[1],p[2]])] ) ]

            return res

        def case431(p,q): #len(p)=4,len(q)=3; non-comparable index is 2;
            #following are shuffles required:   id; (p1,q0); (p1,q1);
            #                                   (p2,q0); (p2,q1);
            #                                   (p3,q0); (p3,q1);
            #                                   (p1,q0)(p2,q1); (p2,q0)(p3,q1); (p1,q0)(p3,q2)
            pc = TableauColumn
            pm = TableauMonomial

            res = \
            [pm(v, 1,coords=[pc(p),pc(q)]), \
            pm(v,-1,coords=[pc([p[0],q[0],p[2],p[3]]),pc([p[1],q[1],q[2]])] ), \
            pm(v,-1,coords=[pc([p[0],q[1],p[2],p[3]]),pc([q[0],p[1],q[2]])] ), \
            pm(v,-1,coords=[pc([p[0],p[1],q[0],p[3]]),pc([p[2],q[1],q[2]])] ), \
            pm(v,-1,coords=[pc([p[0],p[1],q[1],p[3]]),pc([q[0],p[2],q[2]])] ), \
            pm(v,-1,coords=[pc([p[0],p[1],p[2],q[0]]),pc([p[3],q[1],q[2]])] ), \
            pm(v,-1,coords=[pc([p[0],p[1],p[2],q[1]]),pc([q[0],p[3],q[2]])] ), \
            pm(v, 1,coords=[pc([p[0],q[0],q[1],p[3]]),pc([p[1],p[2],q[2]])] ), \
            pm(v, 1,coords=[pc([p[0],p[1],q[0],q[1]]),pc([p[2],p[3],q[2]])] ), \
            pm(v, 1,coords=[pc([p[0],q[0],p[2],p[1]]),pc([p[1],p[3],q[2]])] )  ]

            return res

        def case432(p,q): #len(p)=4,len(q)=3; non-comparable index is 3;
            #following are shuffles required:   id; (p2,q0); (p2,q1); (p2,q2);
            #                                   (p3,q0); (p3,q1); (p3,q2);
            #                                   (p2,q0)(p3,q1); (p2,q1)(p3,q2); (p2,q0)(p3,q2)
            pc = TableauColumn
            pm = TableauMonomial

            res = \
            [pm(v, 1,coords=[pc(p),pc(q)]), \
            pm(v,-1,coords=[pc([p[0],p[1],q[0],p[3]]),pc([p[2],q[1],q[2]])] ), \
            pm(v,-1,coords=[pc([p[0],p[1],q[1],p[3]]),pc([q[0],p[2],q[2]])] ), \
            pm(v,-1,coords=[pc([p[0],p[1],q[2],p[3]]),pc([q[0],q[1],p[2]])] ), \
            pm(v,-1,coords=[pc([p[0],p[1],p[2],q[0]]),pc([p[3],q[1],q[2]])] ), \
            pm(v,-1,coords=[pc([p[0],p[1],p[2],q[1]]),pc([q[0],p[3],q[2]])] ), \
            pm(v,-1,coords=[pc([p[0],p[1],p[2],q[2]]),pc([q[0],q[1],p[3]])] ), \
            pm(v, 1,coords=[pc([p[0],p[1],q[0],q[1]]),pc([p[2],p[3],q[2]])] ), \
            pm(v, 1,coords=[pc([p[0],p[1],q[1],q[2]]),pc([q[0],p[2],p[3]])] ), \
            pm(v, 1,coords=[pc([p[0],p[1],q[0],q[2]]),pc([p[2],q[1],p[3]])] )  ]

            return res


        tc1 = TableauColumn(list(ncpair[0]))
        tc2 = TableauColumn(list(ncpair[1]))
        l1,l2 = len(tc1),len(tc2)


        if l1 < l2:
            tc1,tc2 = tc2,tc1
            l1,l2 = l2,l1

        i=0
        if l1==l2:
            while(i<l2 and tc1[i]==tc2[i]):
                i=i+1
            if i==l2:
                raise ValueError("not valid nc pair")
            if tc1[i]>tc2[i]:
                tc1,tc2 = tc2,tc1
                l1,l2 = l2,l1
        while(i<l2 and tc1[i]<=tc2[i]):
            i=i+1
        if i == l2 and tc1[i]<=tc2[i]:
            raise ValueError("not valid nc pair")

        p1,p2 = list(tc1),list(tc2)

        if (l1,l2,i) == (2,1,0):
                return case210(p1,p2)
        elif (l1,l2,i) == (2,2,1):
                return case221(p1,p2)
        elif (l1,l2,i) == (3,1,0):
                return case310(p1,p2)
        elif (l1,l2,i) == (3,2,0):
                return case320(p1,p2)
        elif (l1,l2,i) == (3,2,1):
                return case321(p1,p2)
        elif (l1,l2,i) == (3,3,1):
                return case331(p1,p2)
        elif (l1,l2,i) == (3,3,2):
                return case332(p1,p2)
        elif (l1,l2,i) == (4,3,2):
                return case432(p1,p2)
        elif (l1,l2,i) == (4,3,1):
                return case431(p1,p2)
        else:
            raise NotImplementedError("Relations are not implemented for case %d,%d,%d."%(l1,l2,i))
