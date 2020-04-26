import numpy as np
from numpy.linalg import svd


def complete(M):
    A = np.matrix.astype(M, dtype='float')
    m, n = A.shape
    O = np.ones((m, n))

    for i in range(m):
        for j in range(n):
            if M[i,j] is None:
                O[i,j] = 0
                A[i,j] = 0
    for step_size in range(15):
        A = helper(A, O, step_size)
    return A


def helper(M, O, step_size):
    A = M
    previous = A
    m, n = A.shape
    nuc_norm = 1e100
    U, S, Vh = svd(A)
    V = Vh.T

    C = np.array([[S[j] if i == j else 0 for j in range(n)] for i in range(m)])
    S = C

    while np.sum(np.diag(S)) < nuc_norm:
        nuc_norm = np.sum(np.diag(S))
        previous = A
        min_sigma = 0
        i = np.min(S.shape) - 1

        while i > 0:
            S[i,i] = np.round(S[i,i], step_size)
            if S[i,i] > 0:
                min_sigma = S[i,i]
                break
            else:
                S[i,i] = 0
            i -= 1
        while i > 0:
            S[i,i] -= min_sigma
            if S[i,i] < 0:
                S[i,i] = 0.0
            i -= 1

        temp_M = U @ S @ V.conj().T
        if temp_M.any() == 0:
            break
        else:
            for i in range(m):
                for j in range(n):
                    if O[i,j] == 0:
                        A[i,j] = temp_M[i,j]
        U, S, Vh = svd(A)
        V = Vh.T
        C = np.array([[S[j] if i == j else 0 for j in range(n)] for i in range(m)])
        S = C
    A = previous
    return A
