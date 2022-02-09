
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

