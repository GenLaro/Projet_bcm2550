from pyplink import PyPlink
import statsmodels.api as sm
import numpy as np
import csv


with PyPlink("data") as bed:
    with open('results.csv', 'w') as csv_file:

        writer = csv.writer(csv_file, lineterminator = '\n')
        writer.writerow(["snp", "reference_allele", "effect_allele", "beta", "odds_ratio", "p"])

        bim = bed.get_bim()
        fam = bed.get_fam()

        samples = bed.get_fam()
        markers = bed.get_bim()

        ##changement des statuts
        samples.loc[:, "status"] = samples.status - 1

        # Régression logistique et ecriture csv
        for marker_id, genotypes in bed:
            endog = np.array(samples['status'])     # Problème : plus de 2 collones
            exog = sm.add_constant(np.array(genotypes))

            model = sm.GLM(endog, exog, family=sm.families.Binomial())
            regression = model.fit()   # Problème : l'objet n'est pas un fit

            beta = regression.params[1]
            p = regression.pvalues[1]
            allele_1 =  bim.loc[marker_id]['a1']
            allele_2 =  bim.loc[marker_id]['a2']

            writer.writerow([marker_id, allele_2, allele_1, beta, np.exp(beta), p])
