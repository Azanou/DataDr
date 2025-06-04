from math import sqrt
from scipy.stats import norm

def run_wilcoxon_test(x, y, alpha=0.05):
    if len(x) != len(y):
        raise ValueError("Les deux séries doivent avoir la même taille.")
    
    n = len(x)
    diffs = [y[i] - x[i] for i in range(n)]
    
    # Exclusion des différences nulles
    data = [(abs(d), 1 if d > 0 else -1) for d in diffs if d != 0]
    if not data:
        raise ValueError("Toutes les différences sont nulles.")

    data.sort(key=lambda x: x[0])
    
    # Attribution des rangs
    ranks = []
    i = 0
    while i < len(data):
        j = i
        while j < len(data) and data[j][0] == data[i][0]:
            j += 1
        rank_avg = (i + 1 + j) / 2
        for k in range(i, j):
            ranks.append((rank_avg, data[k][1]))
        i = j

    # Rangs positifs et négatifs
    R_pos = sum(r for r, s in ranks if s > 0)
    R_neg = sum(r for r, s in ranks if s < 0)
    W = min(R_pos, R_neg)

    n_eff = len(ranks)
    mu_W = n_eff * (n_eff + 1) / 4
    sigma_W = sqrt(n_eff * (n_eff + 1) * (2 * n_eff + 1) / 24)

    z = (W - mu_W) / sigma_W
    z_crit = norm.ppf(1 - alpha / 2)

    if abs(z) > z_crit:
        conclusion = (
            f"Au seuil de {alpha:.2f}, la statistique Z = {z:.3f} dépasse ±{z_crit:.3f}. "
            f"On rejette H₀ : les deux échantillons diffèrent significativement."
        )
    else:
        conclusion = (
            f"Au seuil de {alpha:.2f}, la statistique Z = {z:.3f} n'appartient pas à la zone de rejet ±{z_crit:.3f}. "
            f"Aucune différence significative n’est détectée entre les deux échantillons."
        )

    return {
        "W": round(W, 4),
        "R_pos": round(R_pos, 4),
        "R_neg": round(R_neg, 4),
        "mu_W": round(mu_W, 4),
        "sigma_W": round(sigma_W, 4),
        "z": round(z, 4),
        "z_crit": round(z_crit, 4),
        "conclusion": conclusion,
        "ranks": ranks
    }
