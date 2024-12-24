import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression, Lasso, ElasticNet, LassoCV
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

filePath = "dataFile.json"
df = pd.read_json(filePath)

# Substituting no soil values with a hard soil placeholder value
maxSoilLayers = max([len(i) for i in df['soils']])
placeholder_soilValue = 10e7

maxSoilLength = 80
def fillSoilArray(array,maxLength,placeholderValue):
    fillLength = maxLength - len(array)
    array.extend([placeholderValue] * fillLength) 
    return array

df['soilsNew'] = df.apply(lambda row: fillSoilArray(row['soils'], maxLength=maxSoilLayers, placeholderValue = placeholder_soilValue), axis=1)

soils_df = pd.DataFrame(df['soilsNew'].to_list(), columns=[f'soil_layer_{i}' for i in range(80)])
df = pd.concat([df, soils_df], axis=1)
df = df.drop(columns=['soils','soilsNew'])

# Feature Engineering
df = df[df['Uy'] < 0]
for i in range(10):
    df = df[df[f'soil_layer_{i}'] > 20000]


X = df.drop(columns=['Uy','rot'])
y = df['Uy']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=6)
#model = LinearRegression()
#model = Lasso(alpha=0.2)
model = LassoCV(alphas=[0.001, 0.01, 0.1, 1, 10, 100], cv=5, random_state=1)

# poly = PolynomialFeatures(degree=2)
# X_train = poly.fit_transform(X_train)
# X_test = poly.transform(X_test)
# model = LinearRegression()


model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Evaluer modellen
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)

print(f"Mean Absolute Error: {mae}")
print(f'Mean Squared Error (MSE): {mse}')
print(f'R^2 Score: {r2}')

import matplotlib.pyplot as plt
import numpy as np

# Brug X_test som input til modellen for at få forudsigelserne
y_pred = model.predict(X_test)
y_pred_trained = model.predict(X_train)

# Opret en række indekser for plottene (fra 0 til længden af y_test)
indices = np.arange(len(y_test))

# Lav et bar plot
fig, (ax1) = plt.subplots(1, 1, figsize=(10, 5))  

ax1.plot(y_test*1000,y_pred/y_test,marker='o',linestyle='',color='b')
#ax1.plot(y_train*1000,y_pred_trained/y_train,marker='o',linestyle='',color='r')
ax1.invert_xaxis()
ax1.set_xlabel('Actual settlement [mm]')
ax1.set_ylabel('Predicted settlement / Actual settlement [-]')
ax1.minorticks_on()
ax1.grid(which='major',alpha=0.5)
ax1.grid(which='minor',alpha=0.2)
ax1.set_ylim(ymin=0, ymax=5)
# Vis plottet
plt.show()
