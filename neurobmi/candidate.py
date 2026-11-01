"""Alpha-path averaged ridge on bilateral-averaged FreeSurfer features.

Idea (improves on the champion): keep the champion's age/sex/ICV
residualisation and its name-based bilateral averaging of left/right homolog
columns, but drop the nested family-grouped CV that selected both the
representation (raw vs averaged) and a single ridge alpha.  Instead, the
averaged training residuals are standardised once and a ridge model is fit for
every alpha on a fixed log-spaced path (np.logspace(0, 4, 9)); the returned
prediction is the plain mean of the nine test predictions.  Averaging over the
alpha path (a) removes a variance-inflated discrete selection step that had
only a handful of family groups to work with, (b) is a smooth shrinkage
approximation to the CV-selected model, and (c) is completely deterministic --
there is no randomness anywhere and nothing is ever fit on the test side.

Because the averaging is applied before standardisation, the representation is
the halved feature set of bilateral means; this also makes the design matrix
better conditioned than the raw doubled columns.
"""

import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.preprocessing import StandardScaler

# Fixed, deterministic shrinkage path (features are standardised first, so
# alpha is on the usual "unit-variance design" scale).
ALPHAS = np.logspace(0.0, 4.0, 9)

# (marker, its contralateral counterpart)
_SWAPS = (
    ("L_", "R_"),
    ("R_", "L_"),
    ("lh_", "rh_"),
    ("rh_", "lh_"),
    ("LH_", "RH_"),
    ("RH_", "LH_"),
    ("Left_", "Right_"),
    ("Right_", "Left_"),
    ("left_", "right_"),
    ("right_", "left_"),
    ("-lh-", "-rh-"),
    ("-rh-", "-lh-"),
    ("_L", "_R"),
    ("_R", "_L"),
    ("_left", "_right"),
    ("_right", "_left"),
    (".L", ".R"),
    (".R", ".L"),
)


def _partner(name):
    """Return the contralateral homolog name, or None if no marker is found."""
    for a, b in _SWAPS:
        if name.startswith(a):
            return b + name[len(a):]
        if name.endswith(a):
            return name[: len(name) - len(a)] + b
        if a in name:
            return name.replace(a, b, 1)
    return None


def _feature_names(split):
    """Best-effort feature names; None if the split does not expose any."""
    try:
        names = split.feature_names
        return [str(s) for s in names]
    except (AttributeError, TypeError):
        pass
    try:
        names = split.X.columns
        return [str(s) for s in names]
    except (AttributeError, TypeError):
        pass
    try:
        names = split.columns
        return [str(s) for s in names]
    except (AttributeError, TypeError):
        pass
    return None


def _name_pairs(names, labels, n):
    """Pair columns by swapping hemisphere markers; unmatched columns stay alone.

    Returns (pairs, n_paired) or None when pairing is not possible.
    """
    if names is None or len(names) != n:
        return None
    index = {}
    for i, nm in enumerate(names):
        if nm not in index:
            index[nm] = i
    used = [False] * n
    pairs = []
    n_paired = 0
    for i in range(n):
        if used[i]:
            continue
        used[i] = True
        j = -1
        p = _partner(names[i])
        if p is not None:
            j = index.get(p, -1)
        if j >= 0 and j != i and not used[j]:
            if labels is None or labels[i] == labels[j]:
                used[j] = True
                pairs.append((i, j))
                n_paired += 1
                continue
        pairs.append((i,))
    return pairs, n_paired


def _avg_map(pairs, n):
    """Dense (n_out, n_in) averaging matrix for a list of column groups."""
    mat = np.zeros((len(pairs), n), dtype=float)
    for r, group in enumerate(pairs):
        w = 1.0 / float(len(group))
        for c in group:
            mat[r, c] = w
    return mat


def fit_predict(train, test):
    x_train = np.asarray(train.X, dtype=float)
    x_test = np.asarray(test.X, dtype=float)
    n = x_train.shape[1]
    y = np.asarray(train.y, dtype=float).ravel()

    # Regress age / sex / ICV out of the raw features (fit on train only).
    # Averaging is linear, so it commutes with this residualisation.
    cov_train = np.asarray(train.covariates, dtype=float)
    cov_test = np.asarray(test.covariates, dtype=float)
    confound = LinearRegression().fit(cov_train, x_train)
    resid_train = x_train - confound.predict(cov_train)
    resid_test = x_test - confound.predict(cov_test)

    labels = None
    try:
        lab = np.asarray(train.feature_groups)
        if lab.shape[0] == n:
            labels = lab
    except (AttributeError, TypeError, IndexError):
        labels = None

    # --- bilateral pairing (names first, contiguous fallback) --------------
    pairs = None
    names = _feature_names(train)
    if names is not None:
        built = _name_pairs(names, labels, n)
        if built is not None and built[1] > 0:
            pairs = built[0]
    if pairs is None and n >= 4:
        # Fallback: assume homologs are stored in adjacent (2k, 2k+1) slots and
        # that any odd leftover (e.g. brain stem) is midline.
        pairs = [(2 * k, 2 * k + 1) for k in range(n // 2)]
        if n % 2:
            pairs.append((n - 1,))

    if pairs is not None:
        mat = _avg_map(pairs, n)
        a_train = resid_train @ mat.T
        a_test = resid_test @ mat.T
    else:
        a_train, a_test = resid_train, resid_test

    # --- standardise once, then average over the fixed alpha path ----------
    scaler = StandardScaler()
    s_train = scaler.fit_transform(a_train)
    s_test = scaler.transform(a_test)

    # Accumulate averaged ridge predictions along the shrinkage path.
    pred = np.zeros(s_test.shape[0], dtype=float)
    n_alphas = 0
    for alpha in ALPHAS:
        model = Ridge(alpha=float(alpha), fit_intercept=True)
        model.fit(s_train, y)
        pred += np.asarray(model.predict(s_test), dtype=float).ravel()
        n_alphas += 1
    pred /= float(n_alphas)

    return np.asarray(pred, dtype=float).ravel()
