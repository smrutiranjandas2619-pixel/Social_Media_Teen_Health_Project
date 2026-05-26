from sklearn.model_selection import GridSearchCV


def tune_random_forest(

        model,
        X_train,
        y_train
):

    param_grid = {

        'n_estimators': [50,100],

        'max_depth': [5,10,None]

    }

    grid = GridSearchCV(

        estimator=model,

        param_grid=param_grid,

        cv=5,

        scoring='accuracy'

    )

    grid.fit(

        X_train,
        y_train
    )

    print(
        "\nBest Parameters:"
    )

    print(
        grid.best_params_
    )

    return grid.best_estimator_