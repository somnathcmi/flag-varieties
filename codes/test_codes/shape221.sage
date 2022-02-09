load("classes/tinv_hb.py")
load("classes/straighten.py")
load("classes/tinv_ss_monomials.py")

def lATeX(T,T2,Algos,T_latex,fn):
#latex
    #T_latex = list(map((lambda z:"t_{"+str(z)+"}"),range(len(T))))
    T2_latex = list(map((lambda z:T_latex[z[1]]+T_latex[z[2]]),T2)) 
    rel_latex = []
    for S in Algos:
        lateex = T_latex[S[1]]+T_latex[S[2]]+" &= "
        cnt = 0
        for term in S[0].poly:
            flag,cnt = False,cnt+1
            if cnt%11 == 0:
                lateex = lateex + "\\\\\n&"
            for i in range(len(T2)):
                if T2[i][0].vec == term.vec:
                    flag,sign,coef = True,"+",""
                    if term.coef < 0:
                        sign = " - "
                    if abs(term.coef)!=1:
                        coef=str(abs(term.coef))
                    lateex = lateex + sign + coef + T2_latex[i] 
                    break
            if flag == False:
                lateex = lateex + "error"
                break
    
        rel_latex.append(lateex+"\\\\\n")
 
    #standard relations    
    done = [False]*len(T2)
    for i in range(len(T2)):
        if done[i]:
            continue
        done[i],flag,S=True,False,T2[i]
        lateex = T_latex[S[1]]+T_latex[S[2]]+" & "
        term = S[0] 
        for j in range(i+1,len(T2)):
            if T2[j][0].vec == term.vec:
                lateex = lateex + " = " + T2_latex[j]
                done[j],flag = True,True
        if flag:
            rel_latex.append(lateex+"\\\\\n")

    f = open(fn,"w")
    f.writelines(rel_latex)
    f.close()
    return

FV221 = FlagVariety._get_flag_variety([2,2,1],n=5)
FV221HB = FlagVarietyWithHBOfTInvariants(variety=FV221)

HB221 = TInvariantSemistandardMonomials(variety=FV221,monomials=FV221HB.hb_monomials()) 
HBHB221 = [HB221[i]*HB221[j] for i in range(len(HB221)) for j in range(i+1,len(HB221))]
AlgoHB221 = [StraightenAlgo(h) for h in HBHB221]
for h in AlgoHB221: h.straighten()

#R1221 = TInvariantSemistandardMonomials(variety=FV221,degree=1) 
#R2221 = TInvariantSemistandardMonomials(variety=FV221,degree=2)

#R1R1221 = [(R1221[i]*R1221[j],i,j) for i in range(len(R1221)) for j in range(i,len(R1221))]
#R1R1NS221 = [s for s in R1R1221 if s[0].get_nc_pair()!=None]
#AlgoR1221 = [(StraightenAlgo(s[0]),s[1],s[2]) for s in R1R1NS221]
#for S in AlgoR1221: S[0].straighten()
#tex_str = list(map((lambda z:"x_{"+str(z)+"}"),range(len(R1221))))
#lATeX(R1221,R1R1221,AlgoR1221,tex_str,"shape_221_R1_rels.tex")

#R2R2221 = [(R2221[i]*R2221[j],i,j) for i in range(len(R2221)) for j in range(i,len(R2221))]
#R2R2NS221 = [s for s in R2R2221 if s[0].get_nc_pair()!=None]
#AlgoR2221 = [(StraightenAlgo(s[0]),s[1],s[2]) for s in R2R2NS221]
#for S in AlgoR2221: S[0].straighten()
#tex_str = list(map((lambda z:"t_{"+str(z)+"}"),range(len(R2221))))
#lATeX(R2221,R2R2221,AlgoR2221,tex_str,"shape_221_R2_rels.tex")

