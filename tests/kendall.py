from math import sqrt

def kendall_tau_simplifie(x, y, alpha=0.05):
    if len(x) != len(y):
        raise ValueError("Les deux séries doivent avoir la même taille.")
    
    n = len(x)
    concordant = 0
    discordant = 0

    for i in range(n):
        for j in range(i + 1, n):
            dx = x[i] - x[j]
            dy = y[i] - y[j]
            if dx * dy > 0:
                concordant += 1
            elif dx * dy < 0:
                discordant += 1

    total = concordant + discordant
    if total == 0:
        tau = 0.0
    else:
        tau = (concordant - discordant) / total

    # Calcul de la variance et de la statistique Z
    var_tau = (2 * (2 * n + 5)) / (9 * n * (n - 1))
    z = tau / sqrt(var_tau)

    # Valeur critique pour test bilatéral à alpha = 0.05
    z_crit = 1.96  # valeur z de la loi normale centrée réduite

    # Interprétation correcte, sans p-value
    if abs(z) > z_crit:
        conclusion = (
            f"Au seuil de signification de {alpha:.2f}, la statistique de test Z = {z:.3f} "
            f"dépasse la valeur critique z = ±{z_crit}. Il existe donc une corrélation significative "
            f"entre les deux variables."
        )
    else:
        conclusion = (
            f"Au seuil de signification de {alpha:.2f}, la statistique de test Z = {z:.3f} "
            f"n'appartient pas à la zone de rejet définie par z = ±{z_crit}. "
            f"Aucune corrélation significative entre les deux variables ne peut être conclue."
        )

    return tau, concordant, discordant, z, z_crit, conclusion
