
import os
import shutil

load("./classes/tinv_hb.py")
load("./classes/straighten.py")
load("./classes/tinv_ss_monomials.py")
load("./classes/apply_relation.py")


cwd = os.getcwd()
prefix = cwd+"/paper_data/generated_data/gr37/"
chains_data = prefix+"chains_data/"
hb_data = prefix+"hb_data/"
factor_data_deg_3 = prefix+"factor_data/deg_21/"
factor_data_deg_2 = prefix+"factor_data/deg_14/"


def create_directory_structure():
    try:
        shutil.rmtree(prefix)
    except Exception as e:
        print(f"message from shutil.rmtree: {e}")
    else:
        print(f"message from shutil.rmtree: success")

    try:
        os.makedirs(chains_data)
        os.mkdir(hb_data)
        os.makedirs(factor_data_deg_3)
        os.mkdir(factor_data_deg_2)
    except Exception as e:
        print (f"Creation of the directory failed. {e}")
        return False
    else:
        print ("Successfully created the directory structure")
        return True


def save_coordinates(variety,fname=""):
    if fname=="":
        return False

    f = open(fname,"w")
    m = variety.coordinates
    monomial = TableauMonomial(variety,1,coords=m)
    #print(monomial)
    f.writelines(str(monomial))
    f.close()
    return True
'''
variety: required to get plucker relations
hbmonomials: monomials in hb to be factored using relations
prefered_ncpairs: indices of the list ncpairs, these ncpairs are prefered ncpairs
verbose: print data in between or not
factor_all: If true then we try to factor each monomial using each relation else monomial once factored will not be considered again for factoring.
save_data: whether to save data in file or not. if true fname_prefix is required.
fname_prefix: if save_data is true then fname_prefix is directory in which factoring data will be saved, else ignored.
'''
def factor_hb_monomials(variety,hbmonomials,prefered_ncpairs=[],ncpairs=[],verbose=False,factor_all=True,save_data=False,fname_prefix=""):
    #rename variable for compatibility
    use_ncpairs = prefered_ncpairs

    # make sure all inputs are consistant
    if save_data and fname_prefix =="":
        save_data=False
    if save_data:
        factor_all = False
    
    #keep track of what is already factored
    already_factored = [False]*len(hbmonomials)

    #indexing set for relations
    if ncpairs==[]:
        print("generating ncpairs. may get unexpected result")
        ncpairs=variety.get_nc_pairs()

    #indexes of used relations till now along with list indices of monomials factored using the relation.
    used_rels = []
    used_rels_bool = [False]*len(ncpairs)
    factored_count = 0
    scanned_ncpairs_count = 0

    relation_preference = use_ncpairs + [i for i in range(len(ncpairs))]

    print(f"{scanned_ncpairs_count:04}/{len(ncpairs):04} {factored_count:04}/{len(hbmonomials):04}"+"\b"*19, end="",flush=True)
    
    for j1 in range(len(relation_preference)):
        

        j = relation_preference[j1]
        if not(used_rels_bool[j]):
            used_rels_bool[j]=True
        else:
            continue
        ncpair=ncpairs[j]
        jlist = []
        
        #create filename to save
        fnm = "relation"+str(j)+"_"+ "".join([str(x) for x in ncpair[0]])+"_"+"".join([str(x) for x in ncpair[1]])

        for i in range(len(hbmonomials)):

            if not(already_factored[i]) or factor_all:
                monomial = hbmonomials[i]
                Algo = ApplyRelation(monomial)

                if Algo.do_one_step(ncpair,fname=fname_prefix+fnm,step_name=f"h_{3,{i}}",save_data=save_data):
                    already_factored[i]=True
                    factored_count = factored_count + 1
                    Algo.print_step(verbose=verbose)
                    jlist.append(i)

        if jlist!= []:
            used_rels.append((j,jlist))
        
        scanned_ncpairs_count = scanned_ncpairs_count + 1
        print(f"{j1+1:04}/{len(relation_preference):04} {factored_count:04}/{len(hbmonomials):04}"+"\b"*19, end="",flush=True)
    

    print("")
    #print(used_rels)
    return used_rels



#===============================================================================================================
#===============================================================================================================

print("------------------- G(3,7) data generation started ------------------")

# set to tru if you want to save data  in files.
SAVE = True

if SAVE:
    if not(create_directory_structure()):
        SAVE = False


print("generating gr37 variety object ")
G37 = FlagVariety._get_flag_variety([3]*7,n=7)

#===============================================================================================================
#===============================================================================================================

print("saving gr37 bruhat poset image")
p = G37.print_poset(size=15)
p.save_image(filename=prefix+"bruhat_poset.png")

#===============================================================================================================
#===============================================================================================================

print("saveing plucker coordinates")
save_coordinates(G37,fname=prefix+"plucker_coordinates")

#===============================================================================================================
#===============================================================================================================

print("generating gr37 hb for each chain")
print("1. modifying gr37 variety object for hb calculations")
G37HB = FlagVarietyWithHBOfTInvariants(variety=G37)

print("2. calculating hb")
#G37HB.hb = load(hb_data+"gr37hb.hb_vecs_list")
HB37 = TInvariantSemistandardMonomials(variety=G37,monomials=G37HB.hb_monomials(verbose = False,save_data=SAVE,fname_prefix=chains_data)) 
print("3. separating hb elements degree wise")
print("3.1. collecting degree 1 elements in hb")
HB371 = TInvariantSemistandardMonomials(variety=G37,monomials=G37HB.hb_monomials(deg = 1,verbose=False,save_data=SAVE,fname_prefix=hb_data)) 
print("3.2. collecting degree 2 elements in hb")
HB372 = TInvariantSemistandardMonomials(variety=G37,monomials=G37HB.hb_monomials(deg = 2,verbose=False,save_data=SAVE,fname_prefix=hb_data)) 
print("3.3. collecting degree 3 elements in hb")
HB373 = TInvariantSemistandardMonomials(variety=G37,monomials=G37HB.hb_monomials(deg = 3,verbose=False,save_data=SAVE,fname_prefix=hb_data)) 


#===============================================================================================================
#===============================================================================================================


print("factoring hb monomials of degree 3")

#deg_3_rel_pref = [139, 0] # indices of list G37.get_nc_pairs()

deg_3_ncpairs = [\
[[1, 2, 5], [1, 3, 4]],\
[[3, 6, 7], [4, 5, 7]]\
]

used_rels_deg_3 = factor_hb_monomials(G37,HB373,[],ncpairs=deg_3_ncpairs,save_data=SAVE,factor_all=False,fname_prefix=factor_data_deg_3)

#===============================================================================================================
#===============================================================================================================

print("factoring hb monomials of degree 2")

#deg_2_rel_pref = [60, 83, 36, 139, 0, 125, 26, 134, 2, 132, 6] # indices of list G37.get_nc_pairs()

deg_2_ncpairs =[\
[[1, 4, 7], [2, 4, 6]],\
[[1, 5, 7], [2, 5, 6]],\
[[1, 3, 7], [2, 3, 6]],\
[[3, 6, 7], [4, 5, 7]],\
[[1, 2, 5], [1, 3, 4]],\
[[2, 5, 7], [3, 4, 7]],\
[[1, 3, 6], [1, 4, 5]],\
[[2, 6, 7], [4, 5, 7]],\
[[1, 2, 6], [1, 3, 4]],\
[[2, 6, 7], [3, 5, 7]],\
[[1, 2, 6], [2, 3, 5]]\
]

used_rels_deg_2 = factor_hb_monomials(G37,HB372,[],ncpairs=deg_2_ncpairs,save_data=SAVE,factor_all=False,fname_prefix=factor_data_deg_2)


print("------------------- G(3,7) data generation finished ------------------")
#===============================================================================================================
#===============================================================================================================

