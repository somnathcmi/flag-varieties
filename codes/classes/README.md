readme for classes directory

## coordinates.py 
This file defines class "TableauColumn". The class represent a basis of $\wedge^r C^n$. It is naturally presented by list of size $r$ containing integers from 1 to $n$.

The class defines few important methods: for example Bruhat order (\_\_le\_\_), indicator\_vector, standardize (sort_), etc. See function documentation for exact description.

## variety.py
This file contain class "FlagVariety". The class implement subvarieties of flag varieties which can be obtained by setting few coordinates of ambient space to 0, important examples include varieties obtained from union and intersection of Schubert varieties and richardsons Varieties in grassmannian. Such varieties are determined by $n$, shape of first graded component in coordinate ring, and nonzero coordinates on variety.

important data of such varieties is computed and stored for later use during construction of an instance. for example Bruhat poset and trasnpose shape.

important methods implemented are:
\_get\_flag\_variety: static method to get flag variety from different data.
get\_nc\_pairs: scan all coordinates and return list of non comparable pairs under bruhat order, these are useful to genetate plucker relations for variety.
get\_augmented\_indicator\_matrix: columns are indicator vectors of nonzero coordinates on the variety
get\_augmented\_shape\_matrix: as in appendix B.


