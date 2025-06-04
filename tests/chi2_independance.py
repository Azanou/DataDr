from math import floor
from scipy.stats import chi2

def run_chi2_indep_test(table, alpha=0.05):
    rows = len(table)
    cols = len(table[0])
    total = sum(sum(row) for row in table)

    # Totaux par lignes et colonnes
    row_totals = [sum(row) for row in table]
    col_totals = [sum(table[i][j] for i in range(rows)) for j in range(cols)]

    # Calcul des effectifs théoriques
    expected = [[(row_totals[i] * col_totals[j]) / total for j in range(cols)] for i in range(rows)]

    # Statistique χ²
    chi2_stat = 0
    for i in range(rows):
        for j in range(cols):
            o = table[i][j]
            e = expected[i][j]
            if e != 0:
                chi2_stat += (o - e)**2 / e

    ddl = (rows - 1) * (cols - 1)
    chi2_crit = chi2.ppf(1 - alpha, ddl)

    if chi2_stat > chi2_crit:
        conclusion = (
            f"Au seuil de {alpha:.2f}, la statistique χ² = {chi2_stat:.3f} "
            f"dépasse la valeur critique χ²({ddl}) = {chi2_crit:.3f}. "
            f"On rejette H₀ : les variables sont dépendantes."
        )
    else:
        conclusion = (
            f"Au seuil de {alpha:.2f}, la statistique χ² = {chi2_stat:.3f} "
            f"n’appartient pas à la zone de rejet définie par χ²({ddl}) = {chi2_crit:.3f}. "
            f"Aucune association significative détectée entre les variables."
        )

    return {
        "observed": table,
        "expected": expected,
        "chi2": round(chi2_stat, 4),
        "ddl": ddl,
        "chi2_crit": round(chi2_crit, 4),
        "row_totals": row_totals,
        "col_totals": col_totals,
        "total": total,
        "conclusion": conclusion
    }
