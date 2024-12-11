import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

filePath = r"C:\Users\jmkir\Ramboll\JMKIR - Documents\10. projects\94. ML, Rocking foundation\dataFile.json"
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

X = df.drop(columns=['Uy','rot'])
y = df['Uy']


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.02, random_state=42)
model = LinearRegression()
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

# Opret en række indekser for plottene (fra 0 til længden af y_test)
indices = np.arange(len(y_test))

# Lav et bar plot
plt.figure(figsize=(10, 6))

# Plot de faktiske Uy-værdier fra testdatasættet (blå)
plt.bar(indices - 0.2, y_test, width=0.4, label="Actual Uy (Test Data)", color='blue')

# Plot de forudsigte Uy-værdier fra modellen (rød)
plt.bar(indices + 0.2, y_pred, width=0.4, label="Predicted Uy (Model)", color='red')

# Tilføj labels, titel og legend
plt.title("Actual Uy vs Predicted Uy for Test Data")
plt.xlabel("Index")
plt.ylabel("Uy Values")
plt.legend()

# Vis plottet
plt.show()
