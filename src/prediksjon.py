from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

def regresjonsmodell(X, y):
    modell = LinearRegression()
    modell.fit(X, y)
    y_pred = modell.predict(X)
    r2 = r2_score(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    return modell, r2, mse