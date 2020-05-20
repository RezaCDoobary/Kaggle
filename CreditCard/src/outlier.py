import pandas as pd 

def delete_outliers(X, Y, lower = 0.01, upper = 0.99):
    X_cols = ['X'+str(i) for i in range(0,len(X[0]))]
    df = pd.concat([pd.DataFrame(X,columns = X_cols),pd.DataFrame(Y, columns = ['target'])],1)

    for x in X_cols:
        q_low = df[x].quantile(lower)
        q_hi  = df[x].quantile(upper)
        df = df[(df[x] < q_hi) & (df[x] > q_low)]

    return df[X_cols].values, df['target'].values