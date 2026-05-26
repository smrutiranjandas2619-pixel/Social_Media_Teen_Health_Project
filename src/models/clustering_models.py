from sklearn.cluster import KMeans


def build_kmeans_model():

    model = KMeans(

        n_clusters=3,

        random_state=42

    )

    return model