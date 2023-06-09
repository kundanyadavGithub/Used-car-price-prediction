# -*- coding: utf-8 -*-
"""Predict_Car_Price.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17lB9C4Vca4_6-oYiBlsKk6FAUk_v_Hqg
"""

import pandas as pd              # Deals with data
import numpy as np               # For fast numerical calculations
import matplotlib.pyplot as plt  # For making plots
import seaborn as sns            # Makes beautiful plots
import warnings
warnings.filterwarnings('ignore') # To ignore warning messages

from google.colab import drive
drive.mount('/content/drive')

df = pd.read_csv("/content/drive/MyDrive/CAR_DETAILS.csv")
df

"""#### Feature Engineering
As we see that the Column "Name" contains for eg.Hyundai Creta 1.6 CRDi SX Option	this kind of large information and for the shake of ease we limit this information till its Brand Name. So, here we do apply feature enginnering for this column "Name" and we create another column "Brand Name".That I have done using Excel before uploading this Dataset.

#### Check the shape
"""

df.shape               # Columns=4340 and Rows=9

df.info()

"""#### Data Preprocessing

Now Let's check for null values:

1) Handle the null values
"""

df.isnull().sum() # dataset has no null values

"""Great! There are no null values

2) Handle the duplicates</br>
Sometimes with this kind of datasets we might face duplicates which will affect our analysis, so let's remove them, if there are.
"""

df.duplicated().sum()

df.drop_duplicates(inplace=True)  # here inplace = True so that actual changes may reflect in the dataframe

df.duplicated().sum()   # duplicated rows have been dropped

"""4) Drop Redundant columns"""

df.columns

df['name'].nunique()

df.drop('name',axis=1,inplace=True)
df.columns

"""'name' column is dropped

5) Check the data types
"""

print(df.dtypes)

"""See name,Brand name,fuel,seller_type,transmission,owner columns are of object datatype as ML can't accept object datatype so we need to perform encode -> so we encode these columns using pipeline technique. Before this we do </br>
1)EDA </br>
2)Correlation</br>
3)Handling Outliers

#### EDA -> Exploratory Data Analysis
"""

df.columns

"""Depict count of top 10 different Brand name on a count plot"""

sns.countplot(y=df['Brand_name'],order=df['Brand_name'].value_counts().sort_values(ascending=False).index)
plt.show()

"""Inference: Maruti,Hyundai,Mahindra are the most sort after brands.

Depict count of fuel type on a count plot
"""

sns.countplot(y=df['fuel'],order=df['fuel'].value_counts().sort_values(ascending=False).index)
plt.show()

"""Inference: Diesel and petrol are the most used fuel

Depict countplot based on a seller_type
"""

sns.countplot(y=df['seller_type'],order=df['seller_type'].value_counts().sort_values(ascending=False).index)
plt.show()

"""Inference: Individual is the most sort after seller type

Depict countplot based on transmission
"""

sns.countplot(y=df['transmission'],order=df['transmission'].value_counts().sort_values(ascending=False).index)
plt.show()

"""Inference: Manual is the most sort after transmission

Depict top owner type based on a count
"""

sns.countplot(y=df['owner'],order=df['owner'].value_counts().sort_values(ascending=False).index)
plt.show()

"""Inference: First owner is the most sort after owner.Most of the cars are of first owner, which is a good thing for car seekers.

Checking Boxplot for different Brand Name based on selling price
"""

sns.boxplot(y=df['Brand_name'],x=df['selling_price'])
plt.show()

"""Checking boxplot for different fuel types based on selling price"""

sns.boxplot(y=df['fuel'],x=df['selling_price'])
plt.show()

"""Checking boxplot for transmission type based on selling price"""

sns.boxplot(y=df['transmission'],x=df['selling_price'])
plt.show()

"""Distribution plot for year"""

sns.displot(df['year'])
plt.show()

"""Distribution plot for selling price"""

sns.displot(df['selling_price'])
plt.show()

"""#### Correlation"""

corr = df.corr()
plt.title('Correlation Matrix', fontsize=18)
sns.heatmap(corr,cbar=True,annot=True,cmap='RdBu')
plt.show()

"""Checking correlation where abs(corr)>0.4"""

sns.heatmap(corr[abs(corr)>0.4],annot=True,cmap='RdBu')
plt.show()

"""Checking for Outliers"""

pd.set_option('display.float_format', lambda x: '%.0f' % x)    #To get rid of the "e" exponential notation

df.describe()#(percentiles=[0.01,0.02,0.03,0.05,0.97,0.98,0.99])

df.describe(include = "object")

sns.boxplot(x=df['km_driven'])
plt.show()

"""How many cars have driven more than 400000 km"""

print(df[df['km_driven']>108000].shape)

df['km_driven']=np.where(df['km_driven']>108000,108000,df['km_driven'])
sns.boxplot(x=df['km_driven'])
plt.show()

"""How many cars have driven more than 300000 km"""

print(df[df['km_driven']>300000].shape)

"""Now let's check outliers for year"""

sns.boxplot(x=df['year'])
plt.show()

print(df[df['year']<=2000].shape)

df['year']=np.where(df['year']<=2001,2001,df['year'])
sns.boxplot(x=df['year'])
plt.show()

"""Car used before the year 2000"""

print(df[df['year']<2000].shape)

print(df[df['year']<1998].shape)

print(df[df['year']<1997].shape)

print(df[df['year']<1996].shape)

print(df[df['year']<1995].shape)

"""Now let's check outlier for selling price"""

sns.boxplot(x=df['selling_price'])
plt.grid()
plt.show()

"""Now where selling price is more than 10,*50000*"""

print(df[df['selling_price']>1050000].shape)

df['selling_price']=np.where(df['selling_price']>1050000,1050000,df['selling_price'])
sns.boxplot(x=df['selling_price'])
plt.show()

"""Outliers are removed but still the column are not labelled so, we will handle Encoding categorical columns using column transformer

columns index that needs to undergo LabelEncoding -[0,4,5,6,7]
"""

from sklearn.preprocessing import LabelEncoder

lb = LabelEncoder()

df.columns

#Con_list = ['Brand_name','fuel','seller_type','transmission','owner']
#for i in Con_list:
#  df[i] = lb.fit_transform(df[i])

df.dtypes

"""select x (independent feature) and y (dependent feature)"""

x = df.drop('selling_price',axis=1)
y = df['selling_price']
print(type(x))
print(type(y))
print(x.shape)
print(y.shape)

"""Split the data into trian and test"""

from sklearn.model_selection import train_test_split

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.20,random_state=80)
print(x_train.shape)
print(x_test.shape)
print(y_train.shape)
print(y_test.shape)

"""Create function to compute MSE,RMSE,MAE,Train and test score"""

from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score

def eval_model(ytest,ypred):
  mae = mean_absolute_error(ytest,ypred)
  mse = mean_squared_error(ytest,ypred)
  rmse = np.sqrt(mse)
  r2s = r2_score(ytest,ypred)
  print("MAE",mae)
  print("MSE",mse)
  print("RMAE",rmse)
  print("R2 Score",r2s)

"""Import ML Model Building Libraries"""

from sklearn.linear_model import LinearRegression,Ridge,Lasso
from sklearn.ensemble import RandomForestRegressor,AdaBoostRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

"""Building LinearRegression Model"""

print(x_train)

step1 = ColumnTransformer(transformers=[('ohe',OneHotEncoder(handle_unknown = 'ignore',categories='auto',sparse_output=False),[0,3,4,5,6])],remainder='passthrough')

step2 = LinearRegression()
pipe_lr = Pipeline([('step1',step1),('step2',step2)])
pipe_lr.fit(x_train,y_train)
ypred_lr = pipe_lr.predict(x_test)
eval_model(y_test,ypred_lr)

"""Building Ridge Regression model"""

step1 = ColumnTransformer(transformers=[('ohe',OneHotEncoder(handle_unknown = 'ignore',categories='auto',sparse_output=False),[0,3,4,5,6])],remainder='passthrough')

step2 = Ridge(alpha=2.41)
pipe_rid = Pipeline([('step1',step1),('step2',step2)])
pipe_rid.fit(x_train,y_train)
ypred_rid = pipe_rid.predict(x_test)
eval_model(y_test,ypred_rid)

"""Building Lasso Regression model"""

step1 = ColumnTransformer(transformers=[('ohe',OneHotEncoder(handle_unknown = 'ignore',categories='auto',sparse_output=False),[0,3,4,5,6])],remainder='passthrough')

step2 = Lasso(alpha=54.41)
pipe_las = Pipeline([('step1',step1),('step2',step2)])
pipe_las.fit(x_train,y_train)
ypred_las = pipe_las.predict(x_test)
eval_model(y_test,ypred_las)

print(type(x_test))

print(x_test)

"""Building Random Forest model"""

step1 = ColumnTransformer(transformers=[('ohe',OneHotEncoder(handle_unknown = 'ignore',categories='auto',sparse_output=False),[0,3,4,5,6])],remainder='passthrough')

step2 = RandomForestRegressor(n_estimators=80,max_depth=8,min_samples_split=12,random_state=8)
pipe_rf = Pipeline([('step1',step1),('step2',step2)])
pipe_rf.fit(x_train,y_train)
ypred_rf = pipe_rf.predict(x_test)
eval_model(y_test,ypred_rf)

"""Building Decision tree regressor model"""

step1 = ColumnTransformer(transformers=[('ohe',OneHotEncoder(handle_unknown = 'ignore',categories='auto',sparse_output=False),[0,3,4,5,6])],remainder='passthrough')

step2 = DecisionTreeRegressor(max_depth=8,min_samples_split=12,random_state=5)
pipe_dt = Pipeline([('step1',step1),('step2',step2)])
pipe_dt.fit(x_train,y_train)
ypred_dt = pipe_dt.predict(x_test)
eval_model(y_test,ypred_dt)

"""Save the Best model
From the above model performance we can see that RandomForestRegressor is giving the best r2score i.e R2 Score 0.7390235291557294. So, I will save this Model
"""

import pickle

#pickle.dump('pipe_rf',open('pipeline_rf.pkl','wb'))

# Save object to a pickle file
with open("pipeline_rf_1.pkl", "wb") as file:
    pickle.dump(pipe_rf, file)

# Load object from pickle file
with open("pipeline_rf_1.pkl", "rb") as file:
    loaded_object = pickle.load(file)

# Print the loaded object
#print(loaded_object)

print(type(loaded_object))

"""Saving the dataset"""

pickle.dump(df,open('car_details_data3.pkl','wb'))

# Save the pipeline object to a file
with open('pipeline_rf.pkl', 'wb') as f:
    pickle.dump(pipe_rf, f)

"""Load the Model"""

loaded_model = pickle.load(open('pipeline_rf.pkl','rb'))

# Load the saved pipeline object from the file
with open('pipeline_rf.pkl', 'rb') as f:
    loaded_pipeline = pickle.load(f)

print(type(loaded_model))

# Use the loaded pipeline to make predictions on new data
#ypred_dt = loaded_pipeline.predict(x_test)

"""Take the original data set and make another dataset by randomly picking 20 data points from the oil spill dataset and apply the saved model on the same."""

new_df = x.sample(3000)
new_df

print(type(loaded_pipeline))

predict_price = loaded_pipeline.predict(new_df)

new_df['predict_price']= predict_price
new_df.head(20)

# Save object to a pickle file
#with open("", "wb") as file:
 #   pickle.dump(my_object, file)

# Load object from pickle file
#with open("my_object.pkl", "rb") as file:
 #   loaded_object = pickle.load(file)

# Print the loaded object
#print(loaded_object)



#from sklearn.compose import ColumnTransformer
#from sklearn.pipeline import Pipeline
#from sklearn.preprocessing import LabelEncoder

# Assuming you have a DataFrame called 'data' with categorical columns 'cat1', 'cat2', 'cat3', ...
# and numerical columns 'num1', 'num2', 'num3', ...

# Define the categorical columns
#categorical_columns = ['Brand_name','fuel','seller_type','transmission','owner']

# Create a ColumnTransformer to apply label encoding to categorical columns
#preprocessor = ColumnTransformer(transformers=[('label_encoder', LabelEncoder(), categorical_columns)])