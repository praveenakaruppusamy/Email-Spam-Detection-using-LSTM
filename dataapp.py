from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np

# Step 1: Load the pre-trained model
model = load_model('spam_analysis_lstm.h5')  # Use your model's path

# Step 2: Prepare the tokenizer (use the same tokenizer used during training)
tokenizer = Tokenizer(num_words=10000)  # Same parameters used during training

# Example data
texts = ["I love this product!"]

# Step 3: Preprocess the text data
tokenizer.fit_on_texts(texts)  # Fit the tokenizer (if not saved)
sequences = tokenizer.texts_to_sequences(texts)
max_sequence_length = 100  # Same length used during training
padded_sequences = pad_sequences(sequences, maxlen=max_sequence_length)

# Step 4: Predict sentiment using the model
predictions = model.predict(padded_sequences)
print(predictions)
rounded_numbers = [round(num) for num in predictions[0]]
print(rounded_numbers)
labels=["Normal", "Fraudulent","Harrasment","Suspicious"]

predicted_labels = [labels[np.argmax(pred)] for pred in predictions]

print(predicted_labels[0])