readme for classes directory

## coordinates.py 
This file defines class "TableauColumn". The class represent a basis of $\wedge^r C^n$. It is naturally presented by list of size $r$ containing integers from 1 to $n$.

The class defines few important methods: for example Bruhat order (\_\_le\_\_), indicator\_vector, standardize (sort_), etc. See function documentation for exact description.

## variety.py
This file contain class "FlagVariety". The implement subvarieties which can be obtained by setting few coordinates of ambient space to 0, important examples include varieties obtained from union and intersection of Schubert varieties and richardsons Varieties in grassmannian. Flag variety is determined by $n$, shape of first graded component in coordinate ring, and nonzero coordinates on variety.

