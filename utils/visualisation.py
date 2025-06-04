import matplotlib.pyplot as plt

def afficher_nuage_points(x, y):
    fig, ax = plt.subplots()
    ax.scatter(x, y, color='blue', s=80, alpha=0.7)
    ax.set_title("Nuage de points (x, y)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    return fig


def afficher_boxplot(ech1, ech2, labels=("Échantillon A", "Échantillon B")):
    fig, ax = plt.subplots()
    ax.boxplot([ech1, ech2], labels=labels, patch_artist=True,
               boxprops=dict(facecolor="lightblue"), medianprops=dict(color="red"))
    ax.set_title("Boxplot des deux échantillons")
    return fig



def afficher_boxplot_groupes(groups, labels=None, titre="Boxplot des groupes"): #pour Anova, Bartlett, Levene
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.boxplot(groups, labels=labels, patch_artist=True,
               boxprops=dict(facecolor='skyblue'),
               medianprops=dict(color='red'))

    ax.set_title(titre)
    ax.set_xlabel("Groupes")
    ax.set_ylabel("Valeurs")
    return fig




def afficher_diff_ligne(x, y):                  #pour wilcoxon
    diffs = [y[i] - x[i] for i in range(len(x))]
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(range(1, len(diffs)+1), diffs, marker='o', linestyle='-')
    ax.axhline(0, color='gray', linestyle='--')
    ax.set_title("Différences entre les paires (y - x)")
    ax.set_xlabel("Paires")
    ax.set_ylabel("Différence")
    ax.grid(True)
    return fig
