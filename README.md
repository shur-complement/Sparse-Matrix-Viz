# Sparse-Matrix-Viz

_Documenting a technique for visualizing large sparse matrices_

_Date: July 29, 2023_

![powerlaw_tree](https://github.com/shur-complement/Sparse-Matrix-Viz/assets/139090555/918f5837-691a-41fa-906d-93e86f833e1a)
<figcaption>A Powerlaw Tree Graph rendered at progressively higher resolutions </figcaption>

## Background

When working with sparse matrices, you occasionally want to visualize your data, to determine the underlying structure
of the matrix. Is it symmetric, banded, diagonal, block-sparse? etc.

Matplotlib offers some useful functionality for visualizing the non-zeros of a matrix via [`spy`](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.spy.html).
It renders nice bitmap images like so:

![sparsegraph_shrunk](https://github.com/shur-complement/Sparse-Matrix-Viz/assets/139090555/292d774c-33f1-4f01-807c-4f81e7b991b0)

_a small adjacency matrix_


Where `spy` starts to choke, is for very large matrices, with millions of rows and columns. I was working with large graphs and wanted to
peek at the structure of the adjacency matrix, but was unable to do so with `spy` out of the box. So I searched online and didn't quite find
anything about it. So I thought about it and came up with an idea! If I was sitting down with pencil and paper, I would "sketch" a rough
version of what my matrix looks like. The point isn't 100% accuracy, it's to get a lossy approximation of my extremely large matrix, in a size
that I can actually visualize. I came up with this:

## Code

```py
from math import floor, ceil                                           
                                                                       
def compress(mat, n):                                                  
    """                                                                
    Draws a sketch of a square CSR matrix by scanning an nxn grid      
    and computing the nnz values per each block.                       
    n should be a factor of the matrix dimension                       
    """                                                                
    (rows, cols) = mat.shape                                           
    d = int(ceil(rows/n))                                              
    sketch = [[0]*n for _ in range(n)]                                 
    for row in range(rows):                                            
        s = mat.indptr[row]                                            
        e = mat.indptr[row+1]                                          
        for j in range(s, e):                                          
            k = mat.indices[j]                                         
            si = row//d                                                
            sj = k//d                                                  
            sketch[si][sj] += 1                                        
    return sketch
```

## Explanation

Basically, it breaks up a matrix into tiles and just counts the non-zero elements:

```
┌──────┬─────┬──────┬─────┐
│  5   │  0  │  0   │ 0   │
│      │     │      │     │
├──────┼─────┼──────┼─────┤
│  1   │  3  │  0   │ 0   │
│      │     │      │     │
├──────┼─────┼──────┼─────┤
│  0   │  0  │  5   │  0  │
│      │     │      │     │
├──────┼─────┼──────┼─────┤
│  0   │  0  │  0   │  0  │
│      │     │      │     │
└──────┴─────┴──────┴─────┘
```

What's nice about this approach is that it is trivially parallelizable over the rows (for CSR matrices) and columns (for CSC matrices).

## Some Images

For fun, here are some sample large graphs from the [Stanford SNAP](https://snap.stanford.edu/data/facebook-large-page-page-network.html) repository:

![triangle](https://github.com/shur-complement/Sparse-Matrix-Viz/assets/139090555/7ece5f28-6930-476b-a306-2ce7e8ab7c0a)

[FB musae](https://snap.stanford.edu/data/facebook-large-page-page-network.html)

![sparse_thing](https://github.com/shur-complement/Sparse-Matrix-Viz/assets/139090555/b956f579-6769-4bd3-9d91-e94e034e2c9a)

[Astro Physics Collaboration Network](https://snap.stanford.edu/data/ca-AstroPh.html)

It's not a perfect technique, but it lets you eyeball the data.
