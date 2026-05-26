from sklearn.decomposition import PCA


def apply_pca(
        df,
        components=5
):

    pca = PCA(
        n_components=components
    )

    transformed = pca.fit_transform(df)

    return transformed