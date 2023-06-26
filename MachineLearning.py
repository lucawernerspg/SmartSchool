import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import mysql.connector

# connect to the database
cnx = mysql.connector.connect(host='luca.werner.st',
                                                 database='luca_SmartSchool',
                                                 user='luca',
                                                 password='lsgDbpw1!')
cursor = cnx.cursor()

# execute a query and retrieve the data
query = ("SELECT * FROM Weather")
cursor.execute(query)
data = cursor.fetchall()

# create a pandas dataframe from the retrieved data
df = pd.DataFrame(data, columns=['Date', 'Description', 'Temperature', 'Humidity', 'Windspeed'])

# split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df[['Temperature', 'Humidity']], df['Windspeed'], test_size=0.2, random_state=42)

# create a linear regression model and fit it to the training data
model = LinearRegression()
model.fit(X_train, y_train)

# make predictions on the test data
predictions = model.predict(X_test)

# print the accuracy of the model
print(model.score(X_test, y_test))

# close the database connection
cursor.close()
cnx.close()