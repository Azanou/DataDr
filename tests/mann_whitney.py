from math import sqrt
from scipy.stats import norm

def run_mann_whitney_test(ech1, ech2, alpha=0.05):
    n1 = len(ech1)
    n2 = len(ech2)
    n = n1 + n2

    # Attribuer les rangs combinés
    data = [(val, 'ech1') for val in ech1] + [(val, 'ech2') for val in ech2]
    data.sort(key=lambda x: x[0])

    ranks = {}
    i = 0
    while i < len(data):
        val = data[i][0]
        j = i
        while j < len(data) and data[j][0] == val:
            j += 1
        avg_rank = sum(range(i + 1, j + 1)) / (j - i)
        for k in range(i, j):
            ranks[k] = avg_rank
        i = j

    W1 = sum(ranks[i] for i in range(n) if data[i][1] == 'ech1')
    W2 = sum(ranks[i] for i in range(n) if data[i][1] == 'ech2')

    U1 = W1 - n1 * (n1 + 1) / 2
    U2 = W2 - n2 * (n2 + 1) / 2
    U_obs = min(U1, U2)

    # Approximation normale
    mu_U = n1 * n2 / 2
    sigma_U = sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    z = (U_obs - mu_U) / sigma_U
    z_crit = norm.ppf(1 - alpha / 2)

    if abs(z) > z_crit:
        conclusion = (
            f"Au seuil de signification de {alpha:.2f}, la statistique de test Z = {z:.3f} "
            f"dépasse la valeur critique ±{z_crit:.3f}. On conclut à une différence significative entre les deux groupes."
        )
    else:
        conclusion = (
            f"Au seuil de signification de {alpha:.2f}, la statistique de test Z = {z:.3f} "
            f"n'appartient pas à la zone de rejet définie par ±{z_crit:.3f}. "
            f"Aucune différence significative entre les deux groupes ne peut être conclue."
        )

    return {
        "U1": round(U1, 4),
        "U2": round(U2, 4),
        "U_obs": round(U_obs, 4),
        "W1": round(W1, 4),
        "W2": round(W2, 4),
        "z": round(z, 4),
        "z_crit": round(z_crit, 4),
        "mu_U": round(mu_U, 4),
        "sigma_U": round(sigma_U, 4),
        "conclusion": conclusion
    }
