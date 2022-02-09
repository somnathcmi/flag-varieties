load("classes/tinv_hb.py")
load("classes/straighten.py")
load("classes/tinv_ss_monomials.py")

def lATeX1(T,T2,HB2,Algos,T_latex,HB2_latex,fn):
    T2_latex = list(map((lambda z:T_latex[z[1]]+T_latex[z[2]]),T2)) 
    rel_latex = []
    for S in Algos:
        lateex = T_latex[S[1]]+T_latex[S[2]]+" &= "
        cnt = 0
        include_rel = True
        for term in S[0].poly:
            flag,cnt = False,cnt+1
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
                include_rel = True
                for i in range(len(HB2)):
                    if HB2[i].vec == term.vec:
                        flag,sign,coef = True,"+",""
                        if term.coef < 0:
                            sign = " - "
                        if abs(term.coef)!=1:
                            coef=str(abs(term.coef))
                        lateex = lateex + sign + coef + HB2_latex[i] 
                        break
                if flag == False:
                    lateex = lateex + " + error"
        if include_rel:
            rel_latex.append(lateex+"\\\\\n")
 
    #standard relations   
    '''
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
    '''
    f = open(fn,"w")
    f.writelines(rel_latex)
    f.close()
    return

FV32 = FlagVariety._get_flag_variety([3,2],n=5)
FV32HB = FlagVarietyWithHBOfTInvariants(variety=FV32)
HB32 = TInvariantSemistandardMonomials(variety=FV32,monomials=FV32HB.hb_monomials()) 
HB_tex = ["t_{0}","t_{1}","t_{1}","t_{3}","x_1","x_2","t_{4}"]
Algo1 = [(StraightenAlgo(HB32[2]*HB32[6]),2,6)]
Algo1[0][0].straighten()




#R132 = TInvariantSemistandardMonomials(variety=FV32,degree=1) 
#R232 = TInvariantSemistandardMonomials(variety=FV32,degree=2)
#R1R132 = [R132[i]*R132[j] for i in range(len(R132)) for j in range(i,len(R132))]
#R1R1NS32 = [s for s in R1R132 if s.get_nc_pair()!=None]

