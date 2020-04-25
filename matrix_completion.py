import numpy as np
from numpy.linalg import svd


def matrix_completion(M):
    A = M
    m, n = A.shape
    O = np.ones(m,n)

    for i in range(m):
        for j in range(n):
            if M[i][j] is None:
                O[i][j] = 0
                A[i][j] = 0
    for step_size in range(15):
        A = helper(A, O, step_size)


def helper(M, O, step_size):
    A = M
    previous = A
    m, n = A.shape
    nuc_norm = 1e100
    U, S, V = svd(A)

    while np.sum(np.diag(S)) < nuc_norm:
        nuc_norm = np.sum(np.diag(S))
        previous = A
        min_sigma = 0
        i = np.min(S.shape)

        while i > 0:
            S[i][i] = np.round(S[i][i], step_size)
            if S[i][i] > 0:
                min_sigma = S[i][i]
                break
            else:
                S[i][i] = 0
            i -= 1
        while i > 0:
            S[i][i] -= min_sigma
            if S[i][i] < 0:
                S[i][i] = 0.0
            i -= 1

        temp_M = U@S@V
        if temp_M == 0:
            break
        else:
            for i in range(m):
                for j in range(n):
                    if O[i][j] == 0:
                        A[i][j] = temp_M[i][j]
        U, S, V = svd(A)
    return previous