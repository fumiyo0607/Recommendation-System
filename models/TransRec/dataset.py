import pandas as pd
import scipy.sparse as sp
import numpy as np
from collections import defaultdict
import copy
import os

class Dataset:

    def __init__(self, user_min=2, item_min=2):
        # config
        dataset_name = 'MovieLens100k'
        filename     = '../../data/' + dataset_name + '/ratings.csv'
        df = pd.read_csv(filename, sep=',', header=None,
                names=['user_id', 'item_id', 'rating', 'time'], index_col=False)

        print('\tnum_users = ' + str(len(df['user_id'].unique())))
        print('\tnum_items = ' + str(len(df['item_id'].unique())))
        print('\tdf_shape  = ' + str(df.shape))

        user_counts = df['user_id'].value_counts()
        print('Collected user counts...')
        item_counts = df['item_id'].value_counts()
        print('Collected item counts...')

        # Filter based on user and item counts
        df = df[df.apply(
                lambda x: user_counts[x['user_id']] >= user_min, axis=1)]
        print('User filtering done...')

        df = df[df.apply(
                lambda x: item_counts[x['item_id']] >= item_min, axis=1)]
        print('Item filtering done...')

        print('Second pass')
        print('\tnum_users = ' + str(len(df['user_id'].unique())))
        print('\tnum_items = ' + str(len(df['item_id'].unique())))
        print('\tdf_shape  = ' + str(df.shape))

        # Normalize temporal values
        print('Normalizing temporal values...')
        mean = df['time'].mean()
        std  = df['time'].std()
        ONE_YEAR = (60 * 60 * 24 * 365) / mean
        ONE_DAY  = (60 * 60 * 24) / mean
        df['time'] = (df['time'] - mean) / std

        # 時系列にソート
        df = df.sort_values('time')
        # indexを振り直す
        df = df.reset_index(drop=True)

        # Filter based on user and item counts
        df = df[df.apply(
            lambda x: user_counts[x['user_id']] >= user_min, axis=1)]
        print('User filtering done...')

        df = df[df.apply(
            lambda x: item_counts[x['item_id']] >= item_min, axis=1)]
        print('Item filtering done...')

        print('Second pass')
        print('\tnum_users = ' + str(len(df['user_id'].unique())))
        print('\tnum_items = ' + str(len(df['item_id'].unique())))
        print('\tdf_shape  = ' + str(df.shape))

        self.usernum = len(df['user_id'].unique())
        # self.itemnum = len(df['item_id'].unique())
        self.itemnum = df['item_id'].max()


        # Normalize temporal values
        print('Normalizing temporal values...')
        mean = df['time'].mean()
        std  = df['time'].std()
        ONE_YEAR = (60 * 60 * 24 * 365) / mean
        ONE_DAY  = (60 * 60 * 24) / mean
        df['time'] = (df['time'] - mean) / std

        self.train_df = df.iloc[:70000,:]
        self.varidation_df = df.iloc[70000:90000,:]
        self.test_df = df.iloc[90000:,:]


    def fetch_shaping_dataset(self):
        user_train =  self.shaping_data_set(self.train_df)
        user_validation = self.shaping_data_set(self.varidation_df)
        user_test = self.shaping_data_set(self.test_df)

        return user_train,user_validation,user_test, self.usernum, self.itemnum


    def shaping_data_set(self,df):
        # 時系列にソート
        df = df.sort_values('time')
        # indexを振り直す
        df = df.reset_index(drop=True)
            
        users = df['user_id'].unique()
        users_list = df['user_id']
        item_list = df['item_id']

        target_data_set = {}

        for target_user in users:
            target_users_item_list = []
            for user, item in zip(users_list, item_list):
                if user == target_user:
                    target_users_item_list.append(item)
            target_data_set[target_user] = target_users_item_list
        
        return target_data_set

