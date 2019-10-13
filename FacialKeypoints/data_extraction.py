import numpy as np
import pandas as pd
import database as db


connection = db.create_connection('facial_keysets.db')

c = db.select(['*'],'training_data',connection)

columns = np.array(c.description)[:,0]

df = pd.DataFrame(np.array(c.fetchall()))
df = df.set_index(0)
del df[32]

df.columns = columns[1:-1]

df.to_csv('facial_keysets.csv')