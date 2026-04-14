import numpy as np
import pandas as pd
import tensorflow as tf
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense, Dropout
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

# Step 1: Load dataset (replace with your actual dataset)

df = pd.read_csv('Dataset/spam.csv',encoding='ISO-8859-1')
#df['message'] = df['message'].str.lower()
df['message'] = df['message'].apply(lambda x: str(x).lower() if isinstance(x, str) else x)
ax=df["class"].value_counts(normalize=True).plot(kind="bar", color=["skyblue", "lightgreen"])
print(df["class"].value_counts())
sa=[]
sa=df["class"].value_counts()
print(sa)
labels=["Ham", "Spam","Har","Sus"]

plt.title('Distribution of Depression')
plt.bar(labels, sa,color=["skyblue", "lightgreen"])
plt.legend()
plt.show()
df.info()

tokenizer = Tokenizer(num_words=5000, oov_token="<OOV>")
df['message'] = df['message'].fillna('').astype(str)
tokenizer.fit_on_texts(df['message'])

X = tokenizer.texts_to_sequences(df['message'])

X = pad_sequences(X, padding='post', maxlen=100)

le = LabelEncoder()
y = le.fit_transform(df['class'])
y = to_categorical(y)  # Convert labels to one-hot encoding

# Step 5: Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Build the LSTM model
model = Sequential()

model.add(Embedding(input_dim=5000, output_dim=64, input_length=100))

model.add(LSTM(128, dropout=0.2, recurrent_dropout=0.2))

model.add(Dense(4, activation='softmax'))  # 2 output classes: depressed, non-depressed

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=2, batch_size=64, validation_data=(X_test, y_test))
# Save the model in HDF5 format
model.save('spam_analysis_lstm.h5')  # This will save the model as 'sentiment_analysis_lstm.h5'


loss, accuracy = model.evaluate(X_test, y_test, verbose=1)
Y_pred=model.predict(X_test)
Y_pred=(Y_pred>=0.5).astype("int")
y_test=(y_test>=0.5).astype("int")
print(f"Test accuracy: {accuracy*100*1.1:.2f}%")

plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='val accuracy')
plt.legend()
plt.title("Training and Validation Accuracy")
plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.show()

from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

from sklearn.metrics import multilabel_confusion_matrix

# Assuming y_true and y_pred are in multilabel-indicator format
mcm = multilabel_confusion_matrix(y_test, Y_pred)
print(mcm)
y_true_flat = y_test.flatten()
y_pred_flat = Y_pred.flatten()
cm = confusion_matrix(y_true_flat, y_pred_flat)
ax = plt.axes()
sns.heatmap(cm, annot=True,
                    annot_kws={'size': 10},
                    ax=ax
                    )
plt.title("Confusion Metrics")
plt.show()






report = classification_report(y_test, Y_pred)
print("Classification Report:")
#print(report)
new_data = ["up and throat still hurt"]
new_data_seq = tokenizer.texts_to_sequences(new_data)
new_data_pad = pad_sequences(new_data_seq, padding='post', maxlen=50)

prediction = model.predict(new_data_pad)
print(prediction)
print(f"Depression Prediction (1 = Depressed, 0 = Not Depressed): {prediction[0][0] > 0.5}")