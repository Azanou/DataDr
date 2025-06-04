from math import sqrt
from scipy.stats import f as fisher_f

def run_one_way_anova(groups, alpha=0.05):
    k = len(groups)
    all_data = [x for group in groups for x in group]
    N = len(all_data)
    overall_mean = sum(all_data) / N

    # Somme des carrés entre groupes (inter-group)
    ss_between = sum(
        len(group) * (sum(group)/len(group) - overall_mean) ** 2
        for group in groups
    )

    # Somme des carrés intra-groupes
    ss_within = sum(
        sum((x - sum(group)/len(group)) ** 2 for x in group)
        for group in groups
    )

    df_between = k - 1
    df_within = N - k

    ms_between = ss_between / df_between
    ms_within = ss_within / df_within

    F_obs = ms_between / ms_within
    F_crit = fisher_f.ppf(1 - alpha, df_between, df_within)

    if F_obs > F_crit:
        conclusion = (
            f"Au seuil de signification de {alpha:.2f}, la statistique F = {F_obs:.3f} "
            f"dépasse la valeur critique F(α; {df_between}, {df_within}) = {F_crit:.3f}. "
            f"On rejette H₀ et on conclut qu’au moins une moyenne diffère."
        )
    else:
        conclusion = (
            f"Au seuil de signification de {alpha:.2f}, la statistique F = {F_obs:.3f} "
            f"n’appartient pas à la zone de rejet définie par F(α; {df_between}, {df_within}) = {F_crit:.3f}. "
            f"Aucune différence significative entre les moyennes ne peut être conclue."
        )

    return {
        "F_obs": round(F_obs, 4),
        "F_crit": round(F_crit, 4),
        "ss_between": round(ss_between, 4),
        "ss_within": round(ss_within, 4),
        "ms_between": round(ms_between, 4),
        "ms_within": round(ms_within, 4),
        "df_between": df_between,
        "df_within": df_within,
        "overall_mean": round(overall_mean, 4),
        "conclusion": conclusion
    }
