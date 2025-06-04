from math import sqrt
from scipy.stats import norm

def run_proportion_test(x, n, p0, alpha=0.05):
    p_hat = x / n 
    std_error = sqrt(p0 * (1 - p0) / n)
    z = (p_hat - p0) / std_error
    z_crit = norm.ppf(1 - alpha / 2)

    if abs(z) > z_crit:
        conclusion = (
            f"Au seuil de {alpha:.2f}, Z = {z:.3f} dépasse ±{z_crit:.3f}. "
            f"On rejette H₀ : la proportion observée ({p_hat:.3f}) diffère de {p0:.2f}."
        )
    else:
        conclusion = (
            f"Au seuil de {alpha:.2f}, Z = {z:.3f} n’appartient pas à la zone de rejet ±{z_crit:.3f}. "
            f"Aucune différence significative entre la proportion observée ({p_hat:.3f}) et {p0:.2f}."
        )

    return {
        "p_hat": round(p_hat, 4),
        "z": round(z, 4),
        "z_crit": round(z_crit, 4),
        "std_error": round(std_error, 4),
        "conclusion": conclusion
    }
