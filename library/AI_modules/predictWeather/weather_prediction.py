import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report

# Read the CSV file
data = pd.read_csv("library\AI_modules\predictWeather\HCM_Dataset.csv")

# Function to create list
def Create_list(x):
    list_of_lists = [w.split() for w in x.split(',')]
    flat_list = [item for sublist in list_of_lists for item in sublist]
    return flat_list

# Function to get weather
def Get_Weather(list1):
    if 'Cloudy' in list1:
        return 'CLOUDY'
    elif 'Rainy' in list1:
        return 'RAINY'
    elif 'Sunny' in list1:
        return 'SUNNY'
    elif 'Clear' in list1:
        return 'CLEAR'

# Apply functions to create standardized weather column
data['Std_Weather'] = data['Weather'].apply(lambda x: Get_Weather(Create_list(x)))

# Sample data for balanced classes
cloudy_df = data[data['Std_Weather'] == 'CLOUDY'].sample(1500)
rainy_df = data[data['Std_Weather'] == 'RAINY'].sample(1500)
clear_df = data[data['Std_Weather'] == 'CLEAR'].sample(1500)
sunny_df = data[data['Std_Weather'] == 'SUNNY']

# Concatenate sampled dataframes
weather_df = pd.concat([cloudy_df, clear_df, rainy_df, sunny_df], axis=0)

# Drop unnecessary columns
weather_df.drop(columns=['Date/Time', 'Weather', 'Temperature'], axis=1, inplace=True)

# Encode categorical variable
label_encoder = LabelEncoder()
weather_df['Std_Weather'] = label_encoder.fit_transform(weather_df['Std_Weather'])

# Standardize features
scaler = StandardScaler()
X = weather_df.drop(['Std_Weather'], axis=1)
X_std = scaler.fit_transform(X)
y = weather_df['Std_Weather']

# Split data into training and testing sets
x_train, x_test, y_train, y_test = train_test_split(X_std, y, test_size=0.2, random_state=42)

# Train a Random Forest Classifier
rf_model = RandomForestClassifier(max_features='sqrt', n_estimators=100)
rf_model.fit(x_train, y_train)

# Make predictions on the test set
y_pred_rf = rf_model.predict(x_test)

# Evaluate the model
print("Accuracy:", accuracy_score(y_test, y_pred_rf))
print(classification_report(y_test, y_pred_rf))

# Example usage
Humidity = float(input('Enter the Humidity %= '))
Temperature = float(input('Enter the Temperature_C = '))
input_data = [Humidity, Temperature]
scaled_data = scaler.transform([input_data])
prediction = rf_model.predict(scaled_data)
if prediction[0] == 0:
    print('CLEAR')
elif prediction[0] == 1:
    print('CLOUDY')
elif prediction[0] == 2:
    print('RAINY')
else:
    print('SUNNY')
