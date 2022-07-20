readme for classes directory

## coordinates.py 
This file defines class "TableauColumn". The class represent a basis element of $\wedge^r C^n$. It is naturally presented by list of size $r$ containing integers from 1 to $n$.

The class defines few important methods: for example Bruhat order (\_\_le\_\_), indicator\_vector, standardize (sort_), etc. See function documentation for exact description.

## variety.py
This file contain class "FlagVariety". The class implement subvarieties of flag varieties which can be obtained by setting few coordinates of ambient space to 0, important examples include varieties obtained from union and intersection of Schubert varieties and Richardsons varieties in Grassmannian. Such varieties are determined by $n$, shape of first graded component in coordinate ring, and nonzero coordinates on variety.

The constructor computes important data of such varieties and is stored for later, for example Bruhat poset and trasnpose shape.

Methods implemented are:
\_get\_flag\_variety: static method to get flag variety from different data.
get\_nc\_pairs: scan all coordinates and return list of non comparable pairs under bruhat order, these are useful to genetate plucker relations for variety.
get\_augmented\_indicator\_matrix: columns are indicator vectors of nonzero coordinates on the variety
get\_augmented\_shape\_matrix: as in appendix B.

See documentation for exact description

## monomial.py, polynomial.py
These files contain class TableauMonomial and TableauPolynomial. This implements polynomials in the coordinate ring of FlagVariety, an instance of class flag variety. 

stores varoety reference, coeff, coordinate, the degree vector( $v'\_{\_{S}}$ for monomials, in appendix B).
defines addition(\_\_add\_\_), multiplication (\_\_mul\_\_), negate, indicator matrix, get nc pair, weight vector etc.

## tableau\_relation.py

This file contain class TableauRelation, which stores plucker relation generated from non comparable pairs. This is implemented only for required cases.

## tinv\_hb.py
This file defines class FlagVarietyWithHBOfTInvariants. The compute\_hb function implements section4 and Appendix B. in sequence following are the steps (from line 68)
1. get all maximal chains from Bruhat poset.
2. get augmented indicator matrix $A$ of variety.
3. for each chain, 
3.1 get submatrix $Ac$ of $A$ corresponding to the chain.
3.2 compute Hilbert basis of $ker(Ac) \cap R^{l+1}\_{\ge 0}$.
3.3 append to already computed HBs of previous chains.
 
The function hb\_monomials convert Hilbert basis vectors to standard monomials, an instance of class TableauMonomial.

## tinv\_monomial.py
This file implements following algorithm: given Tinvarient monomial need not be standard check whether there are two Tinvariant factors.
Algorithm is as follows
1. Get indicator matrix of monomial
2. degree vector of given monomial is in Hilbert basis of $ker(A) \cap R^{d+1}\_{\ge} $ iff there are Tinvarient non constant factors 


## straighten.py

This File contain class StraightenAlgo, an implementation of straighteining algorithm.


## tinv\_ss\_monomials.py

wrapper class for list of T invariant semistandard monomials.

##

h 
