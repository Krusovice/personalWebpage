
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso, ElasticNet, LassoCV
from sklearn.preprocessing import PolynomialFeatures, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor

#pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns
pd.set_option('display.width', None)  # No line width limit
pd.set_option('display.max_colwidth', None)  # No limit on column width



filePath = r"C:\Users\jmkir\Ramboll\JMKIR - Documents\personalWebpage\foundationResponse\ML\dataFile_test - copy.json"
df = pd.read_json(filePath)

# Substituting no soil values with a hard soil placeholder value
maxSoilLayers = max([len(i) for i in df['soils']])
placeholder_soilValue = 10e7

def fillSoilArray(array,maxLength,placeholderValue):
    fillLength = maxLength - len(array)
    array.extend([placeholderValue] * fillLength) 
    return array

df['soilsNew'] = df.apply(lambda row: fillSoilArray(row['soils'], maxLength=maxSoilLayers, placeholderValue = placeholder_soilValue), axis=1)

soils_df = pd.DataFrame(df['soilsNew'].to_list(), columns=[f'soil_layer_{i}' for i in range(maxSoilLayers)])
df = pd.concat([df, soils_df], axis=1)
df = df.drop(columns=['soils','soilsNew','soilModel'])
#df = df[df['foundationWidth'] > 2]
# Feature Engineering
df = df[df['Uy'] < 0]
df = df.apply(lambda x: 1/x if x.name.startswith('soil_layer') else x)
X = df.drop(columns=['Uy','rot'])
y = df['Uy']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)
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
errors = pd.DataFrame({'error':rf_errors})
df = pd.concat([1/X_test,errors],axis=1)


# Plotting
fig, (ax1) = plt.subplots(1, 1, figsize=(10, 5))

ax1.plot(y_test*1000,lin_errors,marker='o',linestyle='',color='b',label='Linear Regression')
ax1.plot(y_test*1000,rf_errors,marker='o',linestyle='',color='r',label='Random Forest Regression')
ax1.invert_xaxis()
ax1.set_xlabel('Actual settlement [mm]')
ax1.set_ylabel('Predicted settlement / Actual settlement [-]')
ax1.minorticks_on()
ax1.grid(which='major',alpha=0.5)
ax1.grid(which='minor',alpha=0.2)
ax1.legend()
#ax1.set_ylim(ymin=-1, ymax=5)
# Vis plottet
plt.show()

print(df.iloc[:,2:].sort_values('error',ascending=False))