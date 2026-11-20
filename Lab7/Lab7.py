import numpy as np 
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

data = np.loadtxt("Bank_Customer.csv",skiprows=1,dtype=str,delimiter=',')
print("Original data shape:", data.shape)
print("Country:", np.unique(data[:, 2]))
print("Gender:", np.unique(data[:, 3]))

country_france = (data[:, 2] == "France").astype(int)
country_germany = (data[:, 2] == "Germany").astype(int)
country_spain = (data[:, 2] == "Spain").astype(int)
gender = (data[:, 3] == "Male").astype(int)

pre_data = np.column_stack((
    data[:, 1],
    country_france,
    country_germany,
    country_spain,
    gender,
    data[:, 4:]
)).astype(float)

X = pre_data[:, :-1]
y = pre_data[:, -1].astype(int)

x_train, x_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

scaler = StandardScaler()

x_train = scaler.fit_transform(x_train)
x_test = scaler.transform(x_test)

pre_data = np.column_stack((
    scaler.transform(X),
    y
))

np.savetxt(
    "Bank_Customer_Preprocessed.csv",
    pre_data,
    delimiter=",",
    fmt="%.8f"
)

clf = LogisticRegression()
clf.fit(x_train, y_train)
pred = clf.predict(x_test)

print("Preprocessed data shape:", pre_data.shape)
print("Training data:", x_train.shape)
print("Testing data:", x_test.shape)

print("Prediction Accuracy:")
print(str(round(accuracy_score(pred, y_test)*100, 2)) + "% ")
