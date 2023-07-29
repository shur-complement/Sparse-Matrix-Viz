from math import ceil

def compress(mat, n):
    """
    mat is a scipy.sparse.csr_matrix
    Draws a sketch of a square CSR matrix by scanning an nxn grid
    and computing the nnz values per each block.
    n should be a factor of the matrix dimension
    """
    (rows, cols) = mat.shape
    d = int(ceil(rows/n))
    sketch = [[0]*n for _ in range(n)]
    for row in range(rows):
        if row % 10_000_000 == 0:
            print("on row:", row)
        s = mat.indptr[row]
        e = mat.indptr[row+1]
        for j in range(s, e):
            k = mat.indices[j]
            si = row//d
            sj = k//d
            sketch[si][sj] += 1
    return sketch

if __name__ == "__main__":
    import networkx as nx
    import scipy.sparse as sparse
    import matplotlib.pyplot as plt
    import sys
    G = nx.generators.random_powerlaw_tree(n=100,tries=10000)
    A = sparse.csr_matrix(nx.adjacency_matrix(G))
    f, ax = plt.subplots(1,4)
    D = [10,25,50]
    ax[0].matshow(compress(A,D[0]), cmap=plt.cm.Greys)
    ax[1].matshow(compress(A,D[1]), cmap=plt.cm.Greys)
    ax[2].matshow(compress(A,D[2]), cmap=plt.cm.Greys)
    ax[3].spy(A,markersize=3)
    plt.show()
