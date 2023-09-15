import numpy as np
import matplotlib.pyplot as plt
from sklearn import cluster
from sklearn.cluster import KMeans


def plot_results(inertials):
    """
    Show the inertia curve for clusters
    """
    x, y = zip(*[inertia for inertia in inertials])
    plt.plot(x, y, 'ro-', markersize=8, lw=2)
    plt.grid(True)
    plt.xlabel('Num Clusters')
    plt.ylabel('Inertia')
    plt.show()


def elbow_method(weights, clusters, max_iterations):
    """
    Help to find the ideal number of cluster with the elbow method
    loops: maximun number of cluster to prove
    max_iterations : maximum number of iterations for the kmean algorithm

    """
    inertia_clusters = []

    for i in range(1, clusters + 1):
        kmeans = KMeans(n_clusters=i, max_iter=max_iterations)
        kmeans.fit(weights)

        # Obtain inertia
        inertia_clusters.append([i, kmeans.inertia_])

    plot_results(inertia_clusters)

if __name__ == '__main__':
    data = np.array( [ [1, 2], [1, 4], [1, 0],
               [10, 2], [10, 4], [10, 0]])

    elbow_method(data , 6, 50)
