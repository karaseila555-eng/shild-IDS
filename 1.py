import joblib
import pandas as pd 
import matplotlib.pyplot as plt

columns = [
    'duration', 'protocol_type', 'service', 'flag', 'src_bytes', 'dst_bytes',
    'land', 'wrong_fragment', 'urgent', 'hot', 'num_failed_logins', 'logged_in',
    'num_compromised', 'root_shell', 'su_attempted', 'num_root', 'num_file_creations',
    'num_shells', 'num_access_files', 'num_outbound_cmds', 'is_host_login',
    'is_guest_login', 'count', 'srv_count', 'serror_rate', 'srv_serror_rate',
    'rerror_rate', 'srv_serror_rate_2', 'same_srv_rate', 'diff_srv_rate',
    'srv_diff_host_rate', 'dst_host_count', 'dst_host_srv_count',
    'dst_host_same_srv_rate', 'dst_host_diff_srv_rate', 'dst_host_same_src_port_rate',
    'dst_host_srv_diff_host_rate', 'dst_host_serror_rate', 'dst_host_srv_serror_rate',
    'dst_host_rerror_rate', 'dst_host_srv_rerror_rate', 'attack_type', 'difficulty_level'
]

train_df = pd . read_csv('datatrain.txt', names=columns, header=None)
test_df = pd . read_csv('datatest.txt', names=columns, header=None)



print ("Excellent! A comprehensive data file was read within Pandas.")
print ("A quick look at the first 5 lines of data:")
print(train_df.head())



train_df['target'] = train_df['attack_type'].apply(lambda x: 0 if x == 'normal' else 1)
test_df['target'] = test_df['attack_type'].apply(lambda x: 0 if x == 'normal' else 1)

print ("The solution column (0 for normal, 1 for attack) was successfully set up.")



features = ['duration', 'src_bytes', 'dst_bytes', 'count', 'srv_count']

X_train = train_df[features]
y_train = train_df['target']

X_test = test_df[features]
y_test = test_df['target']

print("Data split and features ready!")


# === model training ===

from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier(random_state=42)

print("Model is training and learning security patterns...")
model.fit(X_train, y_train)
print("Model training complete!")


# === model evaluation exam ===

from sklearn.metrics import accuracy_score, classification_report

predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"Accuracy: {accuracy * 100:.2f}%")

print("Classification Report:")
print(classification_report(y_test, predictions))


# === Drawing using matplotlib ===

plt.figure(figsize=(8, 4))
plt.bar(features, model.feature_importances_, color='teal', edgecolor='black')
plt.title('Feature Importance - Baseline Model (78%)')
plt.ylabel('Importance')
plt.tight_layout()
plt.show()


joblib.dump(model, 'my_model.pkl')


