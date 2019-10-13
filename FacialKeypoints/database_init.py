import database as db
import numpy as np
import pandas as pd

training_dataset = '/Volumes/Seagate/kaggle/facial-keypoints-detection/training.csv'
testing_dataset = '/Volumes/Seagate/kaggle/facial-keypoints-detection/test.csv'
db_name = 'facial_keysets.db'
#################
conn = db.create_connection(db_name)


#################
db.drop_table('FACIAL_KEYPOINTS',conn)
db.drop_table('NEW_IMAGES',conn)
db.drop_table('IMAGES',conn)


#################
new_table = db.table('IMAGES')
new_table.add_column('IMAGE_ID', 'INTEGER', is_primary = True, is_foreign = None , is_done = False)
new_table.add_column('IMAGE_STRING', 'BLOB', is_primary = False, is_foreign = None , is_done = True)
new_table.commit(conn)


#################
df = pd.read_csv(training_dataset)

new_table = db.table('FACIAL_KEYPOINTS')
for columns in np.array(df.columns[:-1]):
    new_table.add_column(columns.upper(), 'FLOAT', is_primary = False, is_foreign = None , is_done = False)
new_table.add_column('IMAGE_ID', 'INTEGER', is_primary = False, is_foreign = 'IMAGES', is_done = True)
new_table.commit(conn)


#################

IMAGE = [df.columns[-1].upper() + '_STRING']
FACIAL_KEYSET = list(map(lambda x : x.upper(), df.columns[:-1]))
FACIAL_KEYSET.append('IMAGE_ID')

for i in range(0,len(df)):
    image_string = df.iloc[i][-1]
    facial_keypoint = list(df.iloc[i][:-1].values)

    ins = db.insert('IMAGES')
    ins.insert_into_table((image_string,),IMAGE)
    cursor = ins.commit_one(conn)
    cursor.close()

    facial_keypoint.append(cursor.lastrowid)
    ins = db.insert('FACIAL_KEYPOINTS')
    ins.insert_into_table(tuple(facial_keypoint),FACIAL_KEYSET)

    cursor = ins.commit_one(conn)
conn.commit()

#################

df = pd.read_csv(testing_dataset)


#################
new_table = db.table('NEW_IMAGES')
new_table.add_column('IMAGE_ID', 'INTEGER', is_primary = True, is_foreign = None , is_done = False)
new_table.add_column('IMAGE_STRING', 'BLOB', is_primary = False, is_foreign = None , is_done = True)
new_table.commit(conn)

#################
IMAGE = ['IMAGE_ID', 'IMAGE_STRING']

for i in range(0,len(df)):
    image_id = int(df.iloc[i][0])
    image_string = df.iloc[i][-1]

    ins = db.insert('NEW_IMAGES')
    ins.insert_into_table((image_id,image_string),IMAGE)
    cursor = ins.commit_one(conn)
    cursor.close()
    
################
#create a view

view = """CREATE VIEW IF NOT EXISTS training_data
AS 
   SELECT * FROM 
   IMAGES i, FACIAL_KEYPOINTS fk
   WHERE i.IMAGE_ID = fk.IMAGE_ID;"""

c = conn.cursor()
c.execute(view)
c.close()



    
conn.commit()