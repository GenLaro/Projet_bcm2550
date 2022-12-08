from pyplink import PyPlink
import statsmodels.api as sm
import numpy as np


with PyPlink("data") as bed:
    bim = bed.get_bim()
    fam = bed.get_fam()

    ## Getting the genotypes of a single marker (numpy.ndarray):   # genotypes = bed.get_geno_marker("rs12345")
    
    # print(bed.get_nb_samples())
    # print(bed.get_nb_markers())
    # print(samples.head())

    samples = bed.get_fam()
    markers = bed.get_bim()
    #print(markers.head())
    

    ##changement des statuts
    for index, row in samples.iterrows():
        if row["status"] == 1 :
            samples.loc[index, "status"] = 0
        if row["status"] == 2 :
            samples.loc[index, "status"] = 1
    # print(samples.head())

    # print(samples.loc[1013,'status'])

    ## lecture des genotypes de chaque echantillon pour chaque marqueur
    for marker_id, genotypes in bed:
        print(marker_id)
        print(genotypes)
        print(samples.row["status"])

	# Régression logistique
    for marker_id, genotypes in bed:
        endog = np.array(samples['status'])     # Problème : plus de 2 collones
        exog = sm.add_constant(np.array(genotypes))
    
        regression = sm.GLM(endog, exog, family=sm.families.Binomial())
        regression = regression.fit()   # Problème : l'objet n'est pas un fit