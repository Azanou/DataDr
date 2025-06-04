from math import log, sqrt
from scipy.stats import chi2

def run_bartlett_test(groups, alpha=0.05):
    k = len(groups)
    n_i = [len(group) for group in groups]
    N = sum(n_i)

    # Moyennes et variances individuelles
    var_i = [sum((x - sum(group)/len(group))**2 for x in group) / (len(group) - 1) for group in groups]

    # Variance globale pondérée (sp²)
    numerator = sum((n_i[i] - 1) * var_i[i] for i in range(k))
    sp2 = numerator / (N - k)

    # Terme numérateur de la statistique T
    term1 = (N - k) * log(sp2)
    term2 = sum((n_i[i] - 1) * log(var_i[i]) for i in range(k))
    num = term1 - term2

    # Terme correctif (pour approximation chi²)
    denom = 1 + (1 / (3 * (k - 1))) * (sum(1 / (n_i[i] - 1) for i in range(k)) - (1 / (N - k)))
    T = num / denom

    ddl = k - 1
    chi2_crit = chi2.ppf(1 - alpha, ddl)

    if T > chi2_crit:
        conclusion = (
            f"Au seuil de signification de {alpha:.2f}, la statistique T = {T:.3f} dépasse la valeur critique "
            f"χ²({ddl}) = {chi2_crit:.3f}. Les variances sont significativement différentes."
        )
    else:
        conclusion = (
            f"Au seuil de signification de {alpha:.2f}, la statistique T = {T:.3f} "
            f"n'appartient pas à la zone de rejet définie par χ²({ddl}) = {chi2_crit:.3f}. "
            f"Aucune différence significative entre les variances ne peut être conclue."
        )

    return {
        "T": round(T, 4),
        "ddl": ddl,
        "sp2": round(sp2, 4),
        "var_i": [round(v, 4) for v in var_i],
        "n_i": n_i,
        "chi2_crit": round(chi2_crit, 4),
        "conclusion": conclusion
    }
