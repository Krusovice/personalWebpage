import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
import seaborn as sns
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV
import warnings
from sklearn.exceptions import ConvergenceWarning

# Suppress only ConvergenceWarnings (specific to logistic regression)
warnings.filterwarnings("ignore", category=ConvergenceWarning)
#% Loading data
df_train = pd.read_csv(r'C:\Users\Bruger\personalWebpage\kaggleCompetitions\titanicCompetition\train.csv')
df_test = pd.read_csv(r'C:\Users\Bruger\personalWebpage\kaggleCompetitions\titanicCompetition\train.csv')

#% Exploring data
df = df_train

df.info()
df.head()

# Plotting with Seaborn
sns.countplot(data=df[(df['Age']<9) & (df['Sex'] == 'male')], x='Pclass', hue='Survived')
plt.show()
#sns.countplot(data=df[(df['SibSp']<1)], x='Pclass', hue='Survived')
#plt.show()

#%%
# plt.figure(figsize=(45,8))
# sns.countplot(data=df, x='Age', hue='Survived')

# #%%
# plt.figure(figsize=(45,8))
# sns.countplot(data=df, x='Age', hue='Pclass')



#%% Training data

df = df[['Age', 'Sex', 'Pclass', 'Survived','Parch','SibSp']]
df = df.dropna()
X = df[['Age', 'Sex', 'Pclass','Parch','SibSp']]
X['Sex'] = X['Sex'].map({'female': 0, 'male': 1})
X['aboveAge'] = np.where(X['Age'] < 9, 1,0)
y = df['Survived']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.01, random_state=3)

model = LogisticRegression()

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Evaluate the model
print("✅ Accuracy Score:", accuracy_score(y_test, y_pred))
print("\n✅ Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\n✅ Classification Report:\n", classification_report(y_test, y_pred))

#%% Creating submission
df = pd.read_csv(r'C:\Users\Bruger\personalWebpage\kaggleCompetitions\titanicCompetition\test.csv')
X = df[['Age', 'Sex', 'Pclass','Parch','SibSp']]
X['Age'] = X['Age'].fillna(30)
X['Sex'] = X['Sex'].map({'female': 0, 'male': 1})
X['aboveAge'] = np.where(X['Age'] < 9, 1,0)
y_pred = model.predict(X)
#%%
submission = pd.DataFrame({
    'PassengerId': df['PassengerId'],
    'Survived': y_pred
})
#%%
# Save to CSV
submission.to_csv(r'C:\Users\Bruger\personalWebpage\kaggleCompetitions\titanicCompetition\submission.csv', index=False)
