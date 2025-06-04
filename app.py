import streamlit as st
from tests.kendall import kendall_tau_simplifie
from tests.mann_whitney import run_mann_whitney_test
from utils.visualisation import afficher_nuage_points
from tests.pearson import run_pearson_test
from tests.spearman import run_spearman_test
from tests.one_way_anova import run_one_way_anova
from tests.wilcoxon import run_wilcoxon_test
from tests.bartlett import run_bartlett_test
from tests.levene import run_levene_test
from tests.proportion import run_proportion_test
from tests.chi2_independance import run_chi2_indep_test






st.set_page_config(page_title="Application de tests statistiques", layout="centered")

st.title("📊 Application de test statistique")
st.sidebar.header("🧪 Choix du test")


# Liste des tests disponibles (à étendre)
test_choisi = st.sidebar.selectbox("Sélectionner un test :", ["Test de Kendall Tau simplifié", "Test de Mann-Whitney", "Test de Pearson", "Test de Spearman", "Test One-Way ANOVA", "Test de Wilcoxon","Test de Bartlett (égalité des variances)","Test de Levene","Test de proportion","Test du χ² d’indépendance",
])

alpha = st.sidebar.number_input(
    "Seuil de signification α",
    min_value=0.001, max_value=0.1, value=0.05,
    step=0.005, format="%.3f"
)

uploaded_file = st.sidebar.file_uploader("📤 Importer un fichier de données (.csv, .xls)", type=["csv","xls"])
imported_data = None

if uploaded_file:
    import pandas as pd
    try:
        imported_data = pd.read_csv(uploaded_file)
        st.sidebar.success("✅ Données importées avec succès")
    except Exception as e:
        st.sidebar.error(f"Erreur de lecture du fichier : {e}")


##si on selectionne un test de kendall
if test_choisi == "Test de Kendall Tau simplifié":
    st.markdown("## 🔹 Test de Kendall Tau simplifié (corrélation de rangs)")

    x = []
    y = []

    if imported_data is not None:
        if list(imported_data.columns)[:2] == ['X', 'Y']:
            try:
                x = list(imported_data['X'].dropna())
                y = list(imported_data['Y'].dropna())
                st.success("✅ Données importées automatiquement depuis le fichier CSV")
            except Exception as e:
                st.error(f"Erreur dans le format des données importées : {e}")
        else:
            st.warning("⚠️ Les colonnes attendues sont : X et Y")

    n = min(len(x), len(y)) if x and y else st.number_input("Taille des séries", min_value=3, max_value=100, value=5, step=1, key="n_kendall")
    

    with st.form("form_kendall"):
        st.markdown("### 📥 Données des variables")
        col1, col2 = st.columns(2)

        for i in range(n):
            with col1:
                xi = st.number_input(f"x[{i+1}]", value=x[i] if i < len(x) else 0.0, key=f"px_{i}")
            with col2:
                yi = st.number_input(f"y[{i+1}]", value=y[i] if i < len(y) else 0.0, key=f"py_{i}")
            if i >= len(x):
                x.append(xi)
                y.append(yi)
            else:
                x[i] = xi
                y[i] = yi

        submit = st.form_submit_button("✅ Exécuter le test")

    if submit:
        try:
            tau, c, d, z, z_crit, conclusion = kendall_tau_simplifie(x, y, alpha)

            st.markdown("### ✅ Résultats du test")
            st.write(f"**Tau simplifié** : {tau:.4f}")
            st.write(f"**Nombre de paires concordantes** : {c}")
            st.write(f"**Nombre de paires discordantes** : {d}")
            st.write(f"**Statistique de test Z** : {z:.4f}")
            st.write(f"**Valeur critique à α = {alpha:.2f}** : ±{z_crit}")
            st.info(conclusion)

            with st.expander("🔍 Détails des calculs"):
                st.markdown(f"""
                - Nombre total de paires comparées : {c + d}
                - Tau = (C - D) / (C + D) = ({c} - {d}) / ({c + d}) = {tau:.4f}
                - Variance de τ sous H₀ : Var(τ) = 2(2n + 5) / (9n(n - 1))  
                → Var(τ) = {((2 * (2 * n + 5)) / (9 * n * (n - 1))):.6f}
                - Statistique Z = τ / √Var(τ) = {z:.4f}
                - Valeur critique pour α = {alpha:.2f} : ±{z_crit}
                """)


            # Optionnel : nuage de points
            from utils.visualisation import afficher_nuage_points
            fig = afficher_nuage_points(x, y)
            st.markdown("### 📊 Nuage de points (x vs y)")
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Erreur : {e}")


##si on selectionne un test de Mann-whitney
elif test_choisi == "Test de Mann-Whitney":
    st.markdown("## 🔹 Test de Mann-Whitney")

    ech1 = []
    ech2 = []

    # 🔹 Données importées automatiquement si dispo
    if imported_data is not None:
        if list(imported_data.columns)[:2] == ['A', 'B']:
            try:
                ech1 = list(imported_data['A'].dropna())
                ech2 = list(imported_data['B'].dropna())
                st.success("✅ Données importées automatiquement depuis le fichier CSV")
            except Exception as e:
                st.error(f"Erreur dans le format des données importées : {e}")
        else:
            st.warning("⚠️ Les colonnes attendues sont : A et B")

    n1 = len(ech1) if ech1 else st.number_input("Taille de l’échantillon 1", min_value=2, max_value=100, value=5, step=1, key="n1_mw")
    n2 = len(ech2) if ech2 else st.number_input("Taille de l’échantillon 2", min_value=2, max_value=100, value=5, step=1, key="n2_mw")

    with st.form("form_mann_whitney"):
        st.markdown("### 📥 Données des échantillons")
        col1, col2 = st.columns(2)

        for i in range(n1):
            with col1:
                xi = st.number_input(f"A[{i+1}]", value=ech1[i] if i < len(ech1) else 0.0, key=f"mw_a_{i}")
            if i >= len(ech1):
                ech1.append(xi)
            else:
                ech1[i] = xi

        for i in range(n2):
            with col2:
                yi = st.number_input(f"B[{i+1}]", value=ech2[i] if i < len(ech2) else 0.0, key=f"mw_b_{i}")
            if i >= len(ech2):
                ech2.append(yi)
            else:
                ech2[i] = yi

        submit = st.form_submit_button("✅ Exécuter le test")

    if submit:
        try:
            result = run_mann_whitney_test(ech1, ech2, alpha)

            st.markdown("### ✅ Résultats du test")
            st.write(f"**U1** : {result['U1']}")
            st.write(f"**U2** : {result['U2']}")
            st.write(f"**U observé** : {result['U_obs']}")
            st.write(f"**Z** : {result['z']}")
            st.write(f"**Valeur critique à α = {alpha:.2f}** : ±{result['z_crit']}")
            st.info(result['conclusion'])

            with st.expander("🔍 Détails des calculs"):
                st.markdown(f"""
                - W1 (somme des rangs de l’échantillon 1) : {result['W1']}  
                - W2 (somme des rangs de l’échantillon 2) : {result['W2']}  

                $$
                U_1 = W_1 - \\frac{{n_1(n_1 + 1)}}{{2}} = {result['U1']} \\\\
                U_2 = W_2 - \\frac{{n_2(n_2 + 1)}}{{2}} = {result['U2']} \\\\
                U = \\min(U_1, U_2) = {result['U_obs']}
                $$

                - Moyenne de U sous H₀ : μ = {result['mu_U']}  
                - Écart-type de U sous H₀ : σ = {result['sigma_U']}  

                $$
                Z = \\frac{{U - \\mu}}{{\\sigma}} = \\frac{{{result['U_obs']} - {result['mu_U']}}}{{{result['sigma_U']}}} = {result['z']}
                $$

                - Zone de non-rejet : ±{result['z_crit']}
                """, unsafe_allow_html=True)

            from utils.visualisation import afficher_boxplot
            fig = afficher_boxplot(ech1, ech2)
            st.markdown("### 📊 Boxplot des deux échantillons")
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Erreur : {e}")


#si test de  Pearson
elif test_choisi == "Test de Pearson":
    st.markdown("## 🔹 Test de corrélation linéaire de Pearson")

    x = []
    y = []

    if imported_data is not None:
        if list(imported_data.columns)[:2] == ['X', 'Y']:
            try:
                x = list(imported_data['X'].dropna())
                y = list(imported_data['Y'].dropna())
                st.success("✅ Données importées automatiquement depuis le fichier CSV")
            except Exception as e:
                st.error(f"Erreur dans le format des données importées : {e}")
        else:
            st.warning("⚠️ Les colonnes attendues sont : X et Y")

    n = min(len(x), len(y)) if x and y else st.number_input("Taille des séries", min_value=3, max_value=100, value=5, step=1, key="n_pearson")
    

    with st.form("form_pearson"):
        st.markdown("### 📥 Données des variables")
        col1, col2 = st.columns(2)

        for i in range(n):
                with col1:
                    xi = st.number_input(f"x[{i+1}]", value=x[i] if i < len(x) else 0.0, key=f"px_{i}")
                with col2:
                    yi = st.number_input(f"y[{i+1}]", value=y[i] if i < len(y) else 0.0, key=f"py_{i}")
                if i >= len(x):
                    x.append(xi)
                    y.append(yi)
                else:
                    x[i] = xi
                    y[i] = yi

        submit = st.form_submit_button("✅ Exécuter le test")

    if submit:
        try:
            result = run_pearson_test(x, y, alpha)

            st.markdown("### ✅ Résultats du test")
            st.write(f"**Coefficient r** : {result['r']}")
            st.write(f"**Statistique de test t** : {result['t_obs']}")
            st.write(f"**Valeur critique à α = {alpha:.2f}** : ±{result['t_crit']} (ddl = {result['ddl']})")
            st.info(result['conclusion'])

            with st.expander("🔍 Détails des calculs"):
                st.markdown(f"""
                - Moyenne de X : {result['x_bar']}  
                - Moyenne de Y : {result['y_bar']}  
                - Formule du r :  
                    $$
                    r = \\frac{{\\sum (x_i - \\bar{{x}})(y_i - \\bar{{y}})}}{{\\sqrt{{\\sum (x_i - \\bar{{x}})^2}} \\cdot \\sqrt{{\\sum (y_i - \\bar{{y}})^2}}}} = {result['r']}
                    $$
                - Statistique t :
                    $$
                    t = \\frac{{r \\cdot \\sqrt{{n - 2}}}}{{\\sqrt{{1 - r^2}}}} = {result['t_obs']}
                    $$
                - Valeur critique (bilatéral) : ±{result['t_crit']} pour ddl = {result['ddl']}
                """)

            from utils.visualisation import afficher_nuage_points
            fig = afficher_nuage_points(x, y)
            st.markdown("### 📊 Nuage de points (x vs y)")
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Erreur : {e}")


#si test de  Spearmann
elif test_choisi == "Test de Spearman":
    st.markdown("## 🔹 Test de corrélation de Spearman (implémenté manuellement)")

    x = []
    y = []

    if imported_data is not None:
        if list(imported_data.columns)[:2] == ['X', 'Y']:
            try:
                x = list(imported_data['X'].dropna())
                y = list(imported_data['Y'].dropna())
                st.success("✅ Données importées automatiquement depuis le fichier CSV")
            except Exception as e:
                st.error(f"Erreur dans le format des données importées : {e}")
        else:
            st.warning("⚠️ Les colonnes attendues sont : X et Y")

    n = min(len(x), len(y)) if x and y else st.number_input("Taille des séries", min_value=3, max_value=100, value=5, step=1, key="n_pearson")
    

    with st.form("form_spearman"):
        st.markdown("### 📥 Données des variables")
        col1, col2 = st.columns(2)

        for i in range(n):
            with col1:
                xi = st.number_input(f"x[{i+1}]", value=x[i] if i < len(x) else 0.0, key=f"px_{i}")
            with col2:
                yi = st.number_input(f"y[{i+1}]", value=y[i] if i < len(y) else 0.0, key=f"py_{i}")
            if i >= len(x):
                x.append(xi)
                y.append(yi)
            else:
                x[i] = xi
                y[i] = yi
        submit = st.form_submit_button("✅ Exécuter le test")

    if submit:
        try:
            result = run_spearman_test(x, y, alpha)

            st.markdown("### ✅ Résultats du test")
            st.write(f"**Coefficient ρ (rho)** : {result['rho']}")
            st.write(f"**Statistique de test Z** : {result['z']}")
            if result['z_crit']:
                st.write(f"**Valeur critique à α = {alpha:.2f}** : ±{result['z_crit']}")
            st.info(result['conclusion'])

            with st.expander("🔍 Détails des calculs"):
                st.markdown(f"""
                - Rang(x) : {result['rangs_x']}
                - Rang(y) : {result['rangs_y']}
                - d² = (rangX - rangY)² : {result['d²']}
                - ∑ d² = {result['sum_d2']}
                - ρ = 1 - (6 × ∑d²) / n(n² - 1)
                  = 1 - (6 × {result['sum_d2']}) / {n}({n}² - 1) = {result['rho']}
                """)
                if result['z'] != "N/A":
                    st.markdown(f"""
                    - Approximation normale : z = ρ × √(n - 1)
                      = {result['rho']} × √({n} - 1) = {result['z']}
                    - Zone de rejet : ±{result['z_crit']}
                    """)

            from utils.visualisation import afficher_nuage_points
            fig = afficher_nuage_points(x, y)
            st.markdown("### 📊 Nuage de points (x vs y)")
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Erreur : {e}")

# si test one Way Anova
elif test_choisi == "Test One-Way ANOVA":
    st.markdown("## 🔹 Test One-Way ANOVA (analyse de variance à un facteur)")

    groups = []
    column_labels = []

    if imported_data is not None:
        try:
            # On lit chaque colonne comme un groupe (valeurs numériques seulement)
            for col in imported_data.columns:
                groupe_valide = imported_data[col].dropna().tolist()
                if len(groupe_valide) >= 2:
                    groups.append(groupe_valide)
                    column_labels.append(str(col))
            nb_groupes = len(groups)
            st.success(f"✅ {nb_groupes} groupes importés automatiquement depuis le fichier CSV")
        except Exception as e:
            st.error(f"Erreur lors de l’importation des groupes : {e}")
            nb_groupes = st.number_input("Nombre de groupes à comparer", min_value=2, max_value=10, value=3, step=1)
    else:
        nb_groupes = st.number_input("Nombre de groupes à comparer", min_value=2, max_value=10, value=3, step=1)

    if not groups:  # si pas importé
        groups = []
        column_labels = []
        for g in range(nb_groupes):
            group_size = st.number_input(f"Nombre d’observations dans le groupe {g+1}", min_value=2, max_value=100, value=3, step=1, key=f"taille_g{g}")
            group_data = []
            with st.expander(f"📥 Saisir les données pour le groupe {g+1}"):
                for i in range(group_size):
                    val = st.number_input(f"Groupe {g+1} - Valeur {i+1}", key=f"g{g}_v{i}")
                    group_data.append(val)
            groups.append(group_data)
            column_labels.append(f"Groupe {g+1}")

    if st.button("✅ Exécuter le test"):
        try:
            result = run_one_way_anova(groups, alpha)

            st.markdown("### ✅ Résultats du test")
            st.write(f"**Statistique F observée** : {result['F_obs']}")
            st.write(f"**Valeur critique F à α = {alpha:.2f}** : {result['F_crit']} "
                     f"(ddl = {result['df_between']} ; {result['df_within']})")
            st.info(result['conclusion'])

            with st.expander("🔍 Détails des calculs"):
                st.markdown(f"""
                - Moyenne globale : **{result['overall_mean']}**
                - Somme des carrés entre groupes : SS_inter = {result['ss_between']}
                - Somme des carrés intra-groupes : SS_intra = {result['ss_within']}
                - ddl inter : {result['df_between']}, ddl intra : {result['df_within']}
                - MS_inter = SS_inter / ddl = {result['ms_between']}
                - MS_intra = SS_intra / ddl = {result['ms_within']}

                $$
                F = \\frac{{MS_{{inter}}}}{{MS_{{intra}}}} = \\frac{{{result['ms_between']}}}{{{result['ms_within']}}} = {result['F_obs']}
                $$

                Zone de non-rejet : F < {result['F_crit']}
                """, unsafe_allow_html=True)

            # 📊 Graphe : Boxplot par groupe
            from utils.visualisation import afficher_boxplot_groupes
            fig = afficher_boxplot_groupes(groups, column_labels, titre="ANOVA")

            st.markdown("### 📊 Visualisation des groupes")
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Erreur : {e}")


#Si test de wilcoxon
elif test_choisi == "Test de Wilcoxon":
    st.markdown("## 🔹 Test de Wilcoxon signé-rang (données appariées)")

    # Données chargées depuis un fichier (optionnel)
    x = []
    y = []

    if imported_data is not None:
        if list(imported_data.columns)[:2] == ['A', 'B']:
            try:
                x = list(imported_data['A'].dropna())
                y = list(imported_data['B'].dropna())
                st.success("✅ Données importées automatiquement depuis le fichier CSV")
            except Exception as e:
                st.error(f"Erreur dans le format des données importées : {e}")
        else:
            st.warning("⚠️ Les colonnes attendues sont : A et B")

    # Taille estimée automatiquement
    n = min(len(x), len(y)) if x and y else st.number_input(
        "Taille de l’échantillon (apparié)", min_value=2, max_value=100, value=5, step=1, key="n_wilcoxon")

    with st.form("form_wilcoxon"):
        st.markdown("### 📥 Données appariées")
        col1, col2 = st.columns(2)

        for i in range(n):
            with col1:
                xi = st.number_input(f"x[{i+1}]", value=x[i] if i < len(x) else 0.0, key=f"wx_{i}")
            with col2:
                yi = st.number_input(f"y[{i+1}]", value=y[i] if i < len(y) else 0.0, key=f"wy_{i}")
            if i >= len(x):
                x.append(xi)
                y.append(yi)
            else:
                x[i] = xi
                y[i] = yi

        submit = st.form_submit_button("✅ Exécuter le test")

    if submit:
        try:
            result = run_wilcoxon_test(x, y, alpha)

            st.markdown("### ✅ Résultats du test")
            st.write(f"**Somme des rangs positifs (R⁺)** : {result['R_pos']}")
            st.write(f"**Somme des rangs négatifs (R⁻)** : {result['R_neg']}")
            st.write(f"**Statistique W (observée)** : {result['W']}")
            st.write(f"**Z calculé** : {result['z']}")
            st.write(f"**Valeur critique à α = {alpha:.2f}** : ±{result['z_crit']}")
            st.info(result['conclusion'])

            with st.expander("🔍 Détails des calculs"):
                st.markdown(f"""
                - Nombre de paires effectives (≠ 0) : {len(result['ranks'])}
                - Moyenne de W sous H₀ : μ = {result['mu_W']}
                - Écart-type de W : σ = {result['sigma_W']}

                $$
                Z = \\frac{{W - \\mu}}{{\\sigma}} = \\frac{{{result['W']} - {result['mu_W']}}}{{{result['sigma_W']}}} = {result['z']}
                $$

                - Zone de non-rejet : ±{result['z_crit']}
                """, unsafe_allow_html=True)

            from utils.visualisation import afficher_diff_ligne
            fig = afficher_diff_ligne(x, y)
            st.markdown("### 📊 Visualisation des différences (y - x)")
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Erreur : {e}")

#Si test de Bartlett
elif test_choisi == "Test de Bartlett (égalité des variances)":
    st.markdown("## 🔹 Test de Bartlett (homogénéité des variances)")

    groups = []
    column_labels = []

    if imported_data is not None:
        try:
            for col in imported_data.columns:
                valeurs = imported_data[col].dropna().tolist()
                if len(valeurs) >= 2:
                    groups.append(valeurs)
                    column_labels.append(str(col))
            nb_groupes = len(groups)
            st.success(f"✅ {nb_groupes} groupes importés automatiquement depuis le fichier CSV")
        except Exception as e:
            st.error(f"Erreur lors de l’importation des données : {e}")
            nb_groupes = st.number_input("Nombre de groupes", min_value=2, max_value=10, value=3)
    else:
        nb_groupes = st.number_input("Nombre de groupes", min_value=2, max_value=10, value=3)

    if not groups:
        groups = []
        column_labels = []
        for g in range(nb_groupes):
            group_size = st.number_input(f"Nombre d’observations dans le groupe {g+1}", min_value=2, max_value=100, value=3, step=1, key=f"taille_bartlett_g{g}")
            group_data = []
            with st.expander(f"📥 Saisir les données pour le groupe {g+1}"):
                for i in range(group_size):
                    val = st.number_input(f"Groupe {g+1} - Valeur {i+1}", key=f"bartlett_g{g}_v{i}")
                    group_data.append(val)
            groups.append(group_data)
            column_labels.append(f"Groupe {g+1}")

    if st.button("✅ Exécuter le test de Bartlett"):
        try:
            result = run_bartlett_test(groups, alpha)

            st.markdown("### ✅ Résultats du test")
            st.write(f"**Statistique T observée** : {result['T']}")
            st.write(f"**Valeur critique χ²({result['ddl']}) à α = {alpha:.2f}** : {result['chi2_crit']}")
            st.info(result['conclusion'])

            with st.expander("🔍 Détails des calculs"):
                st.markdown(f"""
                - Variances des groupes : {result['var_i']}  
                - Taille des groupes : {result['n_i']}  
                - Variance globale pondérée (sp²) : {result['sp2']}

                $$
                T = \\frac{{(N - k) \\cdot \\ln(s_p^2) - \\sum (n_i - 1) \\cdot \\ln(s_i^2)}}{{1 + \\frac{{1}}{{3(k - 1)}} \\left( \\sum \\frac{{1}}{{n_i - 1}} - \\frac{{1}}{{N - k}} \\right)}} = {result['T']}
                $$

                Zone de non-rejet : T < {result['chi2_crit']}
                """, unsafe_allow_html=True)

            # 📊 Graphe : Boxplot des groupes
            from utils.visualisation import afficher_boxplot_groupes
            fig = afficher_boxplot_groupes(groups, column_labels, titre="BartLett")
            st.markdown("### 📊 Visualisation des variances par groupe")
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Erreur : {e}")

#Test de Levene
elif test_choisi == "Test de Levene":
    st.markdown("## 🔹 Test de Levene")

    groups = []
    column_labels = []

    if imported_data is not None:
        try:
            for col in imported_data.columns:
                valeurs = imported_data[col].dropna().tolist()
                if len(valeurs) >= 2:
                    groups.append(valeurs)
                    column_labels.append(str(col))
            nb_groupes = len(groups)
            st.success(f"✅ {nb_groupes} groupes importés automatiquement depuis le fichier CSV")
        except Exception as e:
            st.error(f"Erreur lors de l’importation des données : {e}")
            nb_groupes = st.number_input("Nombre de groupes", min_value=2, max_value=10, value=3)
    else:
        nb_groupes = st.number_input("Nombre de groupes", min_value=2, max_value=10, value=3)

    if not groups:
        groups = []
        column_labels = []
        for g in range(nb_groupes):
            group_size = st.number_input(f"Nombre d’observations dans le groupe {g+1}", min_value=2, max_value=100, value=3, step=1, key=f"taille_levene_g{g}")
            group_data = []
            with st.expander(f"📥 Saisir les données pour le groupe {g+1}"):
                for i in range(group_size):
                    val = st.number_input(f"Groupe {g+1} - Valeur {i+1}", key=f"levene_g{g}_v{i}")
                    group_data.append(val)
            groups.append(group_data)
            column_labels.append(f"Groupe {g+1}")

    if st.button("✅ Exécuter le test de Levene"):
        try:
            result = run_levene_test(groups, alpha)

            st.markdown("### ✅ Résultats du test")
            st.write(f"**Statistique F observée** : {result['F_obs']}")
            st.write(f"**Valeur critique F à α = {alpha:.2f}** : {result['F_crit']} "
                     f"(ddl = {result['ddl_between']} ; {result['ddl_within']})")
            st.info(result['conclusion'])

            with st.expander("🔍 Détails des calculs"):
                st.markdown(f"""
                - Moyenne globale des |différences| : **{result['overall_mean']}**  
                - Moyenne par groupe des |x - moyenne_groupe| : {result['group_means']}  
                - MS_inter : {result['ms_between']}  
                - MS_intra : {result['ms_within']}

                $$
                F = \\frac{{MS_{{inter}}}}{{MS_{{intra}}}} = \\frac{{{result['ms_between']}}}{{{result['ms_within']}}} = {result['F_obs']}
                $$

                Zone de non-rejet : F < {result['F_crit']}
                """, unsafe_allow_html=True)

            from utils.visualisation import afficher_boxplot_groupes
            fig = afficher_boxplot_groupes(groups, column_labels, titre="Levene")
            st.markdown("### 📊 Boxplot des groupes")
            st.pyplot(fig)

        except Exception as e:
            st.error(f"Erreur : {e}")

#Si test de proportion
elif test_choisi == "Test de proportion":
    st.markdown("## 🔹 Test de proportion (bilatéral)")

    x = None
    n = None
    p0 = None

    # Si un CSV est importé avec colonnes "x" et "n"
    if imported_data is not None:
        try:
            if "x" in imported_data.columns and "n" in imported_data.columns:
                x = int(imported_data["x"].iloc[0])
                n = int(imported_data["n"].iloc[0])
                p0 = float(imported_data["p0"].iloc[0]) if "p0" in imported_data.columns else 0.5
                st.success("✅ Données importées depuis le fichier CSV")
        except Exception as e:
            st.error(f"Erreur de lecture du fichier : {e}")

    with st.form("form_proportion"):
        col1, col2, col3 = st.columns(3)
        with col1:
            x = st.number_input("Nombre de succès (x)", min_value=0, max_value=100000, value=x if x else 10, step=1)
        with col2:
            n = st.number_input("Taille de l’échantillon (n)", min_value=1, max_value=100000, value=n if n else 20, step=1)
        with col3:
            p0 = st.number_input("Proportion attendue (p₀)", min_value=0.0, max_value=1.0, value=p0 if p0 else 0.5, step=0.01)

        submit = st.form_submit_button("✅ Exécuter le test")

    if submit:
        if x > n:
            st.error("❌ Le nombre de succès (x) ne peut pas dépasser la taille de l’échantillon (n).")
        else:
            try:
                result = run_proportion_test(x, n, p0, alpha)

                st.markdown("### ✅ Résultats du test")
                st.write(f"**Proportion observée** : p̂ = {result['p_hat']}")
                st.write(f"**Erreur standard** : {result['std_error']}")
                st.write(f"**Statistique Z observée** : {result['z']}")
                st.write(f"**Valeur critique (bilatérale)** : ±{result['z_crit']}")
                st.info(result['conclusion'])

                with st.expander("🔍 Détails des calculs"):
                    st.markdown(f"""
                    $$
                    Z = \\frac{{\\hat{{p}} - p_0}}{{\\sqrt{{\\frac{{p_0(1 - p_0)}}{{n}}}}}} = \\frac{{{result['p_hat']} - {p0}}}{{{result['std_error']}}} = {result['z']}
                    $$

                    Zone de non-rejet : ±{result['z_crit']}
                    """, unsafe_allow_html=True)

                # Bonus graphe
                import matplotlib.pyplot as plt
                fig, ax = plt.subplots()
                ax.bar(["Succès", "Échecs"], [x, n - x], color=["green", "gray"])
                ax.set_title("Répartition des succès et échecs")
                st.markdown("### 📊 Visualisation")
                st.pyplot(fig)

            except Exception as e:
                st.error(f"Erreur : {e}")


#Si test d'independance de KHi-2 
elif test_choisi == "Test du χ² d’indépendance":
    st.markdown("## 🔹 Test du χ² d’indépendance (variables qualitatives)")

    table = []
    row_labels = []
    col_labels = []

    if imported_data is not None:
        try:
            df = imported_data.dropna(how="all").dropna(axis=1, how="all")
            table = df.values.tolist()
            col_labels = list(df.columns)
            row_labels = list(df.index) if df.index.dtype == "object" else [f"Ligne {i+1}" for i in range(len(df))]
            st.success("✅ Tableau de contingence importé avec succès")
        except Exception as e:
            st.error(f"Erreur lors de l’importation : {e}")
            nb_rows = st.number_input("Nombre de lignes", min_value=2, max_value=10, value=2)
            nb_cols = st.number_input("Nombre de colonnes", min_value=2, max_value=10, value=2)
    else:
        nb_rows = st.number_input("Nombre de lignes", min_value=2, max_value=10, value=2)
        nb_cols = st.number_input("Nombre de colonnes", min_value=2, max_value=10, value=2)

        st.markdown("### 📥 Remplir le tableau de contingence")
        table = []
        for i in range(nb_rows):
            row = []
            cols = st.columns(nb_cols)
            for j in range(nb_cols):
                val = cols[j].number_input(f"Cellule [{i+1},{j+1}]", min_value=0, value=10, key=f"chi2_r{i}_c{j}")
                row.append(val)
            table.append(row)

        col_labels = [f"C{j+1}" for j in range(nb_cols)]
        row_labels = [f"L{i+1}" for i in range(nb_rows)]

    if st.button("✅ Exécuter le test"):
        try:
            result = run_chi2_indep_test(table, alpha)

            st.markdown("### ✅ Résultats du test")
            st.write(f"**Statistique χ² observée** : {result['chi2']}")
            st.write(f"**Valeur critique à α = {alpha:.2f}** : {result['chi2_crit']} (ddl = {result['ddl']})")
            st.info(result['conclusion'])

            with st.expander("🔍 Détails du tableau (théorique vs observé)"):
                import pandas as pd
                obs_df = pd.DataFrame(result['observed'], columns=col_labels, index=row_labels)
                exp_df = pd.DataFrame(result['expected'], columns=col_labels, index=row_labels)
                st.write("**Tableau Observé :**")
                st.dataframe(obs_df)
                st.write("**Tableau Théorique (H₀) :**")
                st.dataframe(exp_df)

        except Exception as e:
            st.error(f"Erreur : {e}")

