from math import sqrt
from scipy.stats import t as student_t

def run_pearson_test(x, y, alpha=0.05):
    if len(x) != len(y):
        raise ValueError("Les deux séries doivent avoir la même taille.")

    n = len(x)
    if n < 3:
        raise ValueError("Le test de Pearson nécessite au moins 3 observations.")

    # Moyennes
    x_bar = sum(x) / n
    y_bar = sum(y) / n

    # Calcul de r
    num = sum((x[i] - x_bar) * (y[i] - y_bar) for i in range(n))
    den_x = sqrt(sum((x[i] - x_bar)**2 for i in range(n)))
    den_y = sqrt(sum((y[i] - y_bar)**2 for i in range(n)))
    r = num / (den_x * den_y)

    # Statistique de test t
    t_obs = (r * sqrt(n - 2)) / sqrt(1 - r**2)

    # Valeur critique de Student à n-2 ddl
    ddl = n - 2
    t_crit = student_t.ppf(1 - alpha/2, df=ddl)

    # Conclusion
    if abs(t_obs) > t_crit:
        conclusion = (
            f"Au seuil de signification de {alpha:.2f}, la statistique de test t = {t_obs:.3f} "
            f"dépasse la valeur critique ±{t_crit:.3f} (ddl = {ddl}). "
            f"On conclut à l'existence d'une corrélation linéaire significative entre les deux variables."
        )
    else:
        conclusion = (
            f"Au seuil de signification de {alpha:.2f}, la statistique de test t = {t_obs:.3f} "
            f"n'appartient pas à la zone de rejet définie par ±{t_crit:.3f} (ddl = {ddl}). "
            f"Aucune corrélation linéaire significative ne peut être conclue."
        )

    return {
        "r": round(r, 4),
        "t_obs": round(t_obs, 4),
        "t_crit": round(t_crit, 4),
        "ddl": ddl,
        "x_bar": round(x_bar, 4),
        "y_bar": round(y_bar, 4),
        "conclusion": conclusion
    }
