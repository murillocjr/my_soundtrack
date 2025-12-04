import argparse
import pickle
import pandas as pd
import math
import numpy as np
import base64

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder

parser = argparse.ArgumentParser()
parser.add_argument("--input_data", type=str)
parser.add_argument("--field", type=str)
parser.add_argument("--test", type=float)
parser.add_argument("--x_train", type=str)
parser.add_argument("--y_train", type=str)
parser.add_argument("--x_test", type=str)
parser.add_argument("--y_test", type=str)
parser.add_argument("--cat_ordinal_encoder", type=str)
parser.add_argument("--training_categories_array", type=str)
parser.add_argument("--non_feature_fields", type=str)
args = parser.parse_args()

df_dt = pd.read_pickle(args.input_data)
print("input_len:", len(df_dt))

##
if (args.test<1):
    cat_feats = df_dt.select_dtypes(include="category").columns.to_list()

    for name in cat_feats:
        df_dt[name] = df_dt[name].cat.add_categories("NO_CAT_PLACEHOLDER").fillna("NO_CAT_PLACEHOLDER")
        df_dt[name] = df_dt[name].astype(str).str.strip().astype("category")

    enc = OrdinalEncoder(handle_unknown="use_encoded_value", unknown_value=np.nan)
    enc.set_output(transform="pandas")
    enc = enc.fit(df_dt[cat_feats])

    print('=========================================== CATEGORIES ENCODER INFO =====================================================')
    print(enc.feature_names_in_)
    print('-------------')
    print(enc.categories_)
    print('================================================================================================')


    # print('=========================================== BASE64  cat_feats =====================================================')
    # print(base64.b64encode(pickle.dumps(cat_feats)))
    # print('=========================================== BASE64  enc  OrdinalEncoder=====================================================')
    # print(base64.b64encode(pickle.dumps(enc)))
    # print('================================================================================================')

    pickle.dump(enc, open(args.cat_ordinal_encoder, "wb"))
    pickle.dump(cat_feats, open(args.training_categories_array, 'wb'))

    if args.test == 0:
        print('No cat encoder applied, direct Train Export')
        X = df_dt.drop([args.field],axis=1)
        y = df_dt[[args.field]]

        X.to_pickle(args.x_train)
        print("Xlen:", len(X))
        y.to_pickle(args.y_train)
        print("ylen:", len(y))

    else:
        print('================================================================================================')
        print('Smart Split')

        # df_dt = enc_transform(df_dt)
        ##
        non_feature_fields = args.non_feature_fields.split("|")
        print(non_feature_fields)
        print(args.non_feature_fields)
 
        df_id_bkp = df_dt[non_feature_fields]

        X = df_dt.drop([args.field]+non_feature_fields,axis=1)
        y = df_dt[[args.field]]

        print(y[args.field].value_counts())

        spw = y[args.field].value_counts()[0]/y[args.field].value_counts()[1]
        print("======= GLOBAL =======")
        print("positive: ", y[args.field].value_counts()[1])
        print("negative: ", y[args.field].value_counts()[0])
        spw = math.sqrt(spw)
        print("SPW: ",spw)
        print("==============")

        X_train, X_test, y_train, y_test= train_test_split(X, y, test_size=args.test)

        y_train = pd.merge(y_train, df_id_bkp, left_index=True, right_index=True, how='left')
        y_test = pd.merge(y_test, df_id_bkp, left_index=True, right_index=True, how='left')

        X_train = pd.merge(X_train, df_id_bkp, left_index=True, right_index=True, how='left')
        X_test = pd.merge(X_test, df_id_bkp, left_index=True, right_index=True, how='left')

        print("==Test==")
        print(len(X_test), len(y_test))

        X_test.to_pickle(args.x_test)
        y_test.to_pickle(args.y_test)

        print("==Train==")
        print(len(X_train), len(y_train))

        xrow = X_train.iloc[0]
        print(xrow.to_dict())

        print(X_train.info(verbose=True, show_counts=True))

        X_train.to_pickle(args.x_train)
        y_train.to_pickle(args.y_train)

else:
    print('No cat encoder generated, Raw Test Export')
    X = df_dt.drop([args.field],axis=1)
    y = df_dt[[args.field]]

    X.to_pickle(args.x_test)
    print("Xlen:", len(X))
    y.to_pickle(args.y_test)
    print("ylen:", len(y))



