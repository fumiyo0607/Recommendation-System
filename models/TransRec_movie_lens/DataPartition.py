
# coding: utf-8

# @author: wang-cheng kang, yfzhou

# In[24]:

import gzip
import math
import json
import random
import numpy as np

dataset_name = 'Video_Games'
dataset=np.load('meta_'+dataset_name+'.npy')

[User,Item,usermap,itemmap,usernum,itemnum]=dataset


# In[25]:

for user in User:
    User[user] = [b for a,b in User[user]]
print(usernum,itemnum)
t=0
for user in User: t+=len(User[user])
print(t) 


# In[26]:

#t=0
#for item in Item:
#    for k in Item[item]['related']:
#        t+=len(Item[item]['related'][k])
#t    


# In[3]:

#devided to train/validation/test 
user_train=dict()
user_validation=dict()
user_test=dict()

for user in User:
    nfeedback=len(User[user])
    if nfeedback<3:
        user_train[user]=User[user]
        user_validation[user]=[]
        user_test[user]=[]
    else:
        user_train[user]=User[user][:-2]
        user_validation[user]=[]
        user_validation[user].append(User[user][-3])
        user_validation[user].append(User[user][-2])
        user_test[user]=[]
        user_test[user].append(User[user][-2])
        user_test[user].append(User[user][-1])

        
    


# In[4]:

user_train[2]


# In[5]:
import numpy as np
dataset=[user_train,user_validation,user_test, usernum,itemnum]  # exclude item
np.save('../data/'+dataset_name+'Partitioned.npy',dataset)
