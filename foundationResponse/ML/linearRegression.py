
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso, ElasticNet, LassoCV
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import seaborn as sns

#pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # No line width limit
pd.set_option('display.max_colwidth', None)  # No limit on column width



filePath = r"C:\Users\jmkir\Ramboll\JMKIR - Documents\personalWebpage\foundationResponse\ML\dataFile_test - copy.json"
df = pd.read_json(filePath)
df = df[df['Uy'] != 'Calculation failed']

# Substituting no soil values with a hard soil placeholder value
maxSoilLayers = max([len(i) for i in df['soils']])

# Taking the inverse of the soil layers, as it is expected that a linear relationship between settlements and the inverse Emodulus, rather than the Emodulus.
df['soils'].apply(lambda x: [1/i for i in x])

# Filling all soil layers under BC's with zero.
def fillSoilArray(array,maxLength):
    fillLength = maxLength - len(array)
    array.extend([0] * fillLength) 
    return array

df['soilsNew'] = df.apply(lambda row: fillSoilArray(row['soils'], maxLength=maxSoilLayers), axis=1)
soils_df = pd.DataFrame(df['soilsNew'].to_list(), columns=[f'soil_layer_{i}' for i in range(maxSoilLayers)])
df = pd.concat([df, soils_df], axis=1)
df = df.drop(columns=['soils','soilsNew'])
#%%
#df = df[df['foundationWidth'] > 2]
# Feature Engineering
#df = df[df['Uy'] < -0.001]
#df = df[df['foundationWidth'] == 4]
# df = df[df['eccentricity'] > 0.01]
df = df[df['soilModel'] == 'MC'].drop(columns=['soilModel'])
X = df.drop(columns=['Uy','rot'])
y = df['Uy']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

lin_model = LinearRegression()
lin_model.fit(X_train_scaled, y_train)
lin_pred = lin_model.predict(X_test_scaled)
lin_errors = (lin_pred-y_test)/y_test



rf_model = RandomForestRegressor(n_estimators=100)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)
rf_errors = (rf_pred-y_test)/y_test

# Exploring max errors
errors = pd.DataFrame({'error':lin_errors})
X_test = X_test.apply(lambda x: 1/x if x.name.startswith('soil_layer') else x)
df2 = pd.concat([X_test,errors],axis=1)

# Plotting
fig, (ax1) = plt.subplots(1, 1, figsize=(10, 5))

ax1.plot(y_test*1000,rf_errors,marker='o',linestyle='',color='r',label='Random Forest Regression',alpha=0.3)
ax1.plot(y_test*1000,lin_errors,marker='o',linestyle='',color='b',label='Linear Regression',alpha=0.3)
ax1.invert_xaxis()
ax1.set_xlabel('Actual settlement [mm]')
ax1.set_ylabel('Predicted settlement / Actual settlement [-]')
ax1.minorticks_on()
ax1.grid(which='major',alpha=0.5)
ax1.grid(which='minor',alpha=0.2)
ax1.legend()
plt.show()

#%% 
from sklearn.inspection import PartialDependenceDisplay

# PDP for Random Forest-modelen
features_to_plot = ['soil_layer_9', 'soil_layer_0']  # Indeks eller feature-navne fra X_train (f.eks. 'foundationWidth', 'soil_layer_0')

fig, ax = plt.subplots(figsize=(12, 6))
PartialDependenceDisplay.from_estimator(
    rf_model,               # Din Random Forest-model
    X_train,                # Utrænede data (før skalering)
    features=features_to_plot,  # Features at analysere (vælg relevante kolonner)
    ax=ax,
    kind='average'          # Gennemsnitlig PDP
)
plt.show()

importances = rf_model.feature_importances_
feature_names = X.columns

# Plot feature importance
plt.figure(figsize=(12, 6))
plt.barh(feature_names, importances)
plt.xlabel('Feature Importance')
plt.title('Feature Importance from Random Forest')
plt.show()

#%% Correlation matrix on linear regression model

# Get the coefficients (feature importances)
coefficients = pd.DataFrame(lin_model.coef_, X_train.columns, columns=['Coefficient']).reset_index()
# Plot feature importance
plt.figure(figsize=(12, 6))
plt.barh(coefficients['index'], coefficients['Coefficient'])
plt.xlabel('Feature Importance')
plt.title('Feature coefficients on linear regression model')
plt.show()