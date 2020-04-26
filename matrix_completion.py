import numpy as np
from numpy.linalg import svd


def complete(M):
    A = np.matrix.astype(M, dtype='float')
    m, n = A.shape
    O = np.ones((m, n))
    # If the entry is known, set value to 1
    # If the entry is missing, set value to 0
    for i in range(m):
        for j in range(n):
            if M[i, j] is None:
                O[i, j] = 0
                A[i, j] = 0

    # Predicting the values of the matrix to the 15th decimal place
    for step_size in range(15):
        # helper is a rough estimate of the prediction
        # helperAccurate gives a more accurate prediction
        A = helper(A, O, step_size)
        A = helperAccurate(A, O, step_size)
    return A


def helper(M, O, step_size):
    # Make a copy of M, keep the orgin Matrix, change A
    A = M
    # Preserve the copy in case result worsens
    previous = A
    m, n = A.shape
    # Initialize the nuclear norm as an arbitrarily large value
    nuc_norm = 1e100
    U, S, Vh = svd(A)
    V = Vh.T

    C = np.array([[S[j] if i == j else 0 for j in range(n)] for i in range(m)])
    S = C

    # Objective: minimize nuclear norm
    while np.sum(np.diag(S)) < nuc_norm:
        # Shrink nuc_norm
        nuc_norm = np.sum(np.diag(S))
        # Preserve best Matrix so far
        previous = A
        min_sigma = 0
        i = np.min(S.shape) - 1

        # Find lowest positive singular value
        while i > 0:
            S[i, i] = np.round(S[i, i], step_size)
            if S[i, i] > 0:
                min_sigma = S[i, i]
                break
            else:
                S[i, i] = 0
            i -= 1

        # For the other singular values subtract by min_sigma
        # Set to 0 if singular value is < 0
        while i > 0:
            S[i, i] -= min_sigma
            if S[i, i] < 0:
                S[i, i] = 0.0
            i -= 1

        temp_M = U @ S @ V.conj().T
        if temp_M.any() == 0:
            break
        else:
            for i in range(m):
                for j in range(n):
                    if O[i, j] == 0:
                        A[i, j] = temp_M[i, j]
        U, S, Vh = svd(A)
        V = Vh.T
        C = np.array([[S[j] if i == j else 0 for j in range(n)] for i in range(m)])
        S = C
    A = previous
    return A


def helperAccurate(M, O, step_size):
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
            if np.round(S[i, i], step_size) > 0:
                # helperAccurate will not round min_sigma
                min_sigma = S[i, i]
                break
            else:
                S[i, i] = 0
            i -= 1
        while i > 0:
            S[i, i] -= min_sigma
            if S[i, i] < 0:
                S[i, i] = 0.0
            i -= 1

        temp_M = U @ S @ V.conj().T
        if temp_M.any() == 0:
            break
        else:
            for i in range(m):
                for j in range(n):
                    if O[i, j] == 0:
                        A[i, j] = temp_M[i, j]
        U, S, Vh = svd(A)
        V = Vh.T
        C = np.array([[S[j] if i == j else 0 for j in range(n)] for i in range(m)])
        S = C
    A = previous
    return A
