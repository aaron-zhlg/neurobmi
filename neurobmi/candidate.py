"""Scored BMI model for autoresearch. The seed champion is the linear baseline.

The harness calls fit_predict(train, test) once per fold. `train` and `test`
are autoresearch.harness.Split objects: X (n, 225 FreeSurfer features),
covariates (age, sex, ICV), feature_groups, and on the train side y (BMI) and
families (for grouped inner CV). Only numpy / scipy / sklearn may be imported.

Seed model: regress age, sex and ICV out of every feature (fit on train only),
standardize, ridge regression with alpha chosen by family-grouped inner CV.
"""

import numpy as np
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import GridSearchCV, GroupKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ALPHAS = np.logspace(-1, 5, 13)


def fit_predict(train, test):
    confound = LinearRegression().fit(train.covariates, train.X)
    x_train = train.X - confound.predict(train.covariates)
    x_test = test.X - confound.predict(test.covariates)
    search = GridSearchCV(
        make_pipeline(StandardScaler(), Ridge()),
        {"ridge__alpha": ALPHAS},
        scoring="neg_mean_squared_error",
        cv=GroupKFold(n_splits=5),
    )
    search.fit(x_train, train.y, groups=train.families)
    return search.predict(x_test)
