from math import sqrt
from scipy.stats import f as fisher_f

def run_levene_test(groups, alpha=0.05):
    k = len(groups)
    n_i = [len(g) for g in groups]
    N = sum(n_i)

    # Étape 1 : transformer en Z_ij = |x_ij - moyenne_groupe|
    Z = []
    Z_flat = []
    for group in groups:
        mean_g = sum(group) / len(group)
        z_group = [abs(x - mean_g) for x in group]
        Z.append(z_group)
        Z_flat.extend(z_group)

    overall_mean = sum(Z_flat) / N
    group_means = [sum(zg)/len(zg) for zg in Z]

    # Somme des carrés entre groupes
    ss_between = sum(len(Z[i]) * (group_means[i] - overall_mean)**2 for i in range(k))
    
    # Somme des carrés intra-groupes
    ss_within = sum((z - group_means[i])**2 for i in range(k) for z in Z[i])

    ddl_between = k - 1
    ddl_within = N - k

    ms_between = ss_between / ddl_between
    ms_within = ss_within / ddl_within

    F_obs = ms_between / ms_within
    F_crit = fisher_f.ppf(1 - alpha, ddl_between, ddl_within)

    if F_obs > F_crit:
        conclusion = (
            f"Au seuil de signification de {alpha:.2f}, la statistique F = {F_obs:.3f} "
            f"dépasse la valeur critique F({ddl_between}, {ddl_within}) = {F_crit:.3f}. "
            f"On rejette H₀ : les variances ne sont pas toutes égales."
        )
    else:
        conclusion = (
            f"Au seuil de signification de {alpha:.2f}, la statistique F = {F_obs:.3f} "
            f"n’appartient pas à la zone de rejet définie par F({ddl_between}, {ddl_within}) = {F_crit:.3f}. "
            f"Aucune différence significative entre les variances ne peut être conclue."
        )

    return {
        "F_obs": round(F_obs, 4),
        "F_crit": round(F_crit, 4),
        "ddl_between": ddl_between,
        "ddl_within": ddl_within,
        "ms_between": round(ms_between, 4),
        "ms_within": round(ms_within, 4),
        "group_means": [round(m, 4) for m in group_means],
        "overall_mean": round(overall_mean, 4),
        "conclusion": conclusion
    }
