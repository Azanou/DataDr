from math import sqrt

def compute_ranks(data):
    """Attribue les rangs en gérant les ex aequos."""
    n = len(data)
    sorted_data = sorted((val, i) for i, val in enumerate(data))
    ranks = [0] * n
    i = 0
    while i < n:
        j = i
        while j < n and sorted_data[j][0] == sorted_data[i][0]:
            j += 1
        rank = (i + 1 + j) / 2  # moyenne des positions
        for k in range(i, j):
            ranks[sorted_data[k][1]] = rank
        i = j
    return ranks

def run_spearman_test(x, y, alpha=0.05):
    if len(x) != len(y):
        raise ValueError("Les deux séries doivent avoir la même taille.")
    
    n = len(x)
    rx = compute_ranks(x)
    ry = compute_ranks(y)

    # Calcul des différences de rangs
    d_squared = [(rx[i] - ry[i]) ** 2 for i in range(n)]
    sum_d2 = sum(d_squared)

    # Formule de Spearman
    rho = 1 - (6 * sum_d2) / (n * (n**2 - 1))

    # Approximation de la statistique Z (valable pour n > 10)
    if n > 10:
        z = rho * sqrt(n - 1)
        z_crit = 1.96  # valeur critique à alpha = 0.05, bilatéral

        if abs(z) > z_crit:
            conclusion = (
                f"Au seuil de signification de {alpha:.2f}, la statistique de test Z = {z:.3f} "
                f"dépasse la valeur critique ±{z_crit}. On conclut à l'existence d'une corrélation "
                f"monotone significative entre les deux variables."
            )
        else:
            conclusion = (
                f"Au seuil de signification de {alpha:.2f}, la statistique de test Z = {z:.3f} "
                f"n'appartient pas à la zone de rejet définie par ±{z_crit}. "
                f"Aucune corrélation monotone significative ne peut être conclue."
            )
    else:
        z = None
        z_crit = None
        conclusion = (
            f"Effectif insuffisant (n = {n}) pour utiliser l'approximation normale. "
            f"Le test n'est pas interprétable pour n ≤ 10."
        )

    return {
        "rho": round(rho, 4),
        "z": round(z, 4) if z is not None else "N/A",
        "z_crit": z_crit,
        "conclusion": conclusion,
        "rangs_x": rx,
        "rangs_y": ry,
        "d²": d_squared,
        "sum_d2": sum_d2
    }
