import pandas as pd
import scipy.sparse as sp
import numpy as np
from collections import defaultdict
import copy
import os


# TODO:
# ・movie_id のインデックスを振り直す
# ・movie_idのユニークな配列を作成する
# ・dictを作成して，dfのmovie_idを振り直す
# ・考察したいので，moviesとの紐付けが可能なように中間テーブルを出力する

class Dataset:

    def __init__(self, user_min=2, item_min=2):
        # config
        dataset_name = 'MovieLens100k'
        filename     = '../../data/' + dataset_name + '/ratings.csv'
        df = pd.read_csv(filename, sep=',', header=None,
                names=['user_id', 'item_id', 'rating', 'time'], index_col=False)

        # item_idを振り直す

        # ユニークなitem_idのリストを作成
        item_list = df['item_id']
        item_list = item_list.sort_values()
        item_list = item_list.reset_index(drop=True)
        item_list = item_list.unique()

        # マスタとなるdictを作成
        item_idex_master = {}

        for i in range(len(item_list)):
            item_idex_master[ item_list[i]] = i

        # 元のitem_id
        item_id= list(item_idex_master.keys())
        # idxを振り直した後のitem_is
        fixed_item_idx =  list(item_idex_master.values())

        df_item_ids_master = pd.DataFrame(
            data = {
                'item_id' : item_id,
                'fixed_item_idx' : fixed_item_idx
            },
            columns=['item_id','fixed_item_idx']
        )

        df_item_ids_master.to_csv('df_item_ids_master.csv')

        # dfのitem_idを振り直す
        target_item_list = df['item_id']
        fixed_item_ids = []

        for item_id in target_item_list:
            fixed_item_ids.append(item_idex_master[item_id])

        df['item_id'] = fixed_item_ids
        print('Fixed item_id...')

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

        # # Filter based on user and item counts
        # df = df[df.apply(
        #     lambda x: user_counts[x['user_id']] >= user_min, axis=1)]
        # print('User filtering done...')

        # df = df[df.apply(
        #     lambda x: item_counts[x['item_id']] >= item_min, axis=1)]
        # print('Item filtering done...')

        # print('Second pass')
        # print('\tnum_users = ' + str(len(df['user_id'].unique())))
        # print('\tnum_items = ' + str(len(df['item_id'].unique())))
        # print('\tdf_shape  = ' + str(df.shape))

        self.usernum = len(df['user_id'].unique())
        self.itemnum = len(df['item_id'].unique())
        # self.itemnum = df['item_id'].max()


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

