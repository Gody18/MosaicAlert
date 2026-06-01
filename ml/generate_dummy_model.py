import tensorflow as tf
import os

# Create a very simple model that takes 224x224x3 image and outputs 2 classes
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(224, 224, 3)),
    tf.keras.layers.GlobalAveragePooling2D(),
    tf.keras.layers.Dense(2, activation='softmax')
])

model.compile(optimizer='adam', loss='categorical_crossentropy')

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Define paths
output_dir = '../app/src/assets/models'
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, 'mosaicalert_f16.tflite')

# Save the model
with open(output_path, 'wb') as f:
    f.write(tflite_model)

print(f"Dummy model generated at: {output_path}")
print(f"Size: {len(tflite_model) / 1024:.2f} KB")
