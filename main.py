import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score, KFold
from sklearn.feature_selection import f_regression, SelectKBest
from sklearn.metrics import mean_absolute_error, explained_variance_score, mean_squared_error, r2_score, roc_auc_score, plot_roc_curve, RocCurveDisplay
from keras.models import Sequential
from keras.layers import Dense
from keras.wrappers.scikit_learn import KerasRegressor
from tqdm import tqdm
import pickle
import pdb
import seaborn as sns
from yellowbrick.regressor import PredictionError


RANDOM_FOREST_REGRESSOR_FILENAME = 'random_forest_regressor.sav'
DECISION_TREE_REGRESSOR_FILENAME = 'decision_tree_regressor.sav'
SUPPORT_VECTOR_MACHINE_FILENAME = 'svm_regressor.sav'


def load_dataset(file_path):
  df = pd.read_csv(file_path)

  return df


def visualize_dataset(df):
  sns.set_theme(color_codes=True)


def dataset_splitting(df):
  x_train = df.loc[df['Dataset']==1].iloc[:, df.columns!='N Values'].values
  x_test = df.loc[df['Dataset']==0].iloc[:, df.columns!='N Values'].values

  y_train = df.loc[df['Dataset']==1]['N Values'].values
  y_test = df.loc[df['Dataset']==0]['N Values'].values

  return x_train, y_train, x_test, y_test


def feature_selection(x_train, y_train, x_test):
  # selecting the best k number of features by change k parameter.
  fs = SelectKBest(score_func=f_regression, k=350)
  fs.fit(x_train, y_train)

  x_train_fs = fs.transform(x_train)
  x_test_fs = fs.transform(x_test)

  # for i in range(len(fs.scores_)):
  #   print('Feature %d: %f' % (i, fs.scores_[i]))

  # uncomment the lines to plot the scores of each feature
  # plt.bar([i for i in range(len(fs.scores_))], fs.scores_)
  # plt.show()

  return x_train_fs, x_test_fs


def decision_tree_regressor(x_train, y_train):
  regressor = DecisionTreeRegressor(max_depth=10, random_state=0)

  print('Decision tree regressor Information:')
  print(regressor.get_params())

  regressor.fit(x_train, y_train)

  # pickle.dump(regressor, open(DECISION_TREE_REGRESSOR_FILENAME, 'wb'))

  return regressor


def random_forest_regressor(x_train, y_train):
  regressor = RandomForestRegressor(max_depth=20, verbose=1, n_jobs=-1)

  print('Random forest regressor Information:')
  print(regressor.get_params())

  regressor.fit(x_train, y_train)

  # pickle.dump(regressor, open(RANDOM_FOREST_REGRESSOR_FILENAME, 'wb'))

  return regressor


def support_vector_machine_regressor(x_train, y_train):
  regressor = make_pipeline(StandardScaler(), SVR(C=1.0, epsilon=0.2, max_iter=50000, verbose=True))

  print('SVM Information:')
  print(regressor.get_params())

  regressor.fit(x_train, y_train)

  # pickle.dump(regressor, open(SUPPORT_VECTOR_MACHINE_FILENAME, 'wb'))

  return regressor


def model_evaluation(x_test, y_test, regressor):
  # regressor = pickle.load(open(filename, 'rb'))

  y_predict = regressor.predict(x_test)

  accuracy = regressor.score(x_test, y_test)
  print('Accuracy: ', accuracy*100)

  variance_score = explained_variance_score(y_test, y_predict)
  print('Explained variance score: ', variance_score)

  r2_accuracy = r2_score(y_test, y_predict)
  print('r2 score: ', r2_accuracy)

  mae = mean_absolute_error(y_test, y_predict)
  print('Mean absolute error: %.3f' % mae)

  mse = mean_squared_error(y_test, y_predict)
  print('Mean squared error: %.3f' % mse)


def visualize_model_performance(x_test, y_test, regressor):
  visualizer = PredictionError(regressor)
  visualizer.score(x_test, y_test)
  visualizer.show()




df = load_dataset('Meanspectra.csv')
visualize_dataset(df)
x_train, y_train, x_test, y_test = dataset_splitting(df)
x_train, x_test = feature_selection(x_train, y_train, x_test)
# model = decision_tree_regressor(x_train, y_train)
model = random_forest_regressor(x_train, y_train)
# model = support_vector_machine_regressor(x_train, y_train)
model_evaluation(x_test, y_test, model)
visualize_model_performance(x_test, y_test, model)

