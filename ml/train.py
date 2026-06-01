import os
import tensorflow as tf
from keras import layers, models, optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import EarlyStopping, ReduceLROnPlateau
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score


# Constants
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 200 # Increased for deeper training as requested
LEARNING_RATE = 1e-4
WEIGHT_DECAY = 1e-5

def create_data_generators(data_dir):
    """
    Creates data generators for training and validation with advanced augmentation.
    Assumes a directory structure: data_dir/train/class_name and data_dir/val/class_name
    """
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        brightness_range=[0.7, 1.3], # ±30% brightness
        fill_mode='nearest'
    )

    val_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        os.path.join(data_dir, 'train'),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical'
    )

    val_generator = val_datagen.flow_from_directory(
        os.path.join(data_dir, 'val'),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        shuffle=False # Important for evaluation
    )

    return train_generator, val_generator

def build_model(num_classes=2):
    """
    Builds a MobileNetV2-based model for binary classification.
    """
    base_model = tf.keras.applications.MobileNetV2(
        input_shape=(*IMG_SIZE, 3),
        include_top=False,
        weights=None # Changed from 'imagenet' to avoid download failure in restricted env
    )
    base_model.trainable = True # Set to True since we are training from scratch

    model = models.Sequential([
        base_model,
        layers.GlobalAveragePooling2D(),
        layers.Dense(128, activation='relu', kernel_regularizer=tf.keras.regularizers.l2(WEIGHT_DECAY)),
        layers.Dropout(0.3),
        layers.Dense(num_classes, activation='softmax', kernel_regularizer=tf.keras.regularizers.l2(WEIGHT_DECAY))
    ])

    model.compile(
        optimizer=optimizers.Adam(learning_rate=LEARNING_RATE),
        loss='categorical_crossentropy',
        metrics=[
            'accuracy', 
            tf.keras.metrics.AUC(name='auc'),
            tf.keras.metrics.Precision(name='precision'),
            tf.keras.metrics.Recall(name='recall')
        ]
    )
    return model

def convert_to_tflite(model, output_path, quantization='float16', representative_data=None):
    """
    Converts a Keras model to TFLite format with quantization.
    """
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    if quantization == 'float16':
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.target_spec.supported_types = [tf.float16]
    elif quantization == 'int8' and representative_data is not None:
        def representative_dataset_gen():
            for i in range(100):
                data = next(representative_data)[0]
                yield [data.astype(np.float32)]
        
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
        converter.representative_dataset = representative_dataset_gen
        converter.target_spec.supported_ops = [tf.lite.OpsSet.TFLITE_BUILTINS_INT8]
        converter.inference_input_type = tf.uint8
        converter.inference_output_type = tf.uint8
    
    tflite_model = converter.convert()
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(tflite_model)
    print(f"Model saved to {output_path} (size: {os.path.getsize(output_path) / (1024*1024):.2f} MB)")

if __name__ == "__main__":
    DATA_DIR = os.path.join(os.getcwd(), 'data', 'final')
    MODELS_DIR = os.path.join(os.getcwd(), 'models')
    os.makedirs(MODELS_DIR, exist_ok=True)
    
    print("MosaicAlert Model Training Pipeline")
    print("-----------------------------------")
    print(f"Loading data from: {DATA_DIR}")
    
    if os.path.exists(DATA_DIR):
        train_gen, val_gen = create_data_generators(DATA_DIR)
        model = build_model(num_classes=train_gen.num_classes)
        
        # Callbacks
        early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
        lr_scheduler = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)

        print("Starting training...")
        history = model.fit(
            train_gen,
            validation_data=val_gen,
            epochs=EPOCHS,
            callbacks=[early_stopping, lr_scheduler]
        )
        
        # Evaluate
        print("\nEvaluating on validation set...")
        val_gen.reset()
        predictions = model.predict(val_gen)
        y_pred = np.argmax(predictions, axis=1)
        y_true = val_gen.classes
        
        print("\nClassification Report:")
        print(classification_report(y_true, y_pred, target_names=list(val_gen.class_indices.keys())))
        
        # Save results
        model.save(os.path.join(MODELS_DIR, 'mosaicalert_final.h5'))
        convert_to_tflite(model, os.path.join(MODELS_DIR, 'mosaicalert_f16.tflite'), quantization='float16')
        # convert_to_tflite(model, os.path.join(MODELS_DIR, 'mosaicalert_int8.tflite'), quantization='int8', representative_data=train_gen)
    else:
        print(f"Data directory {DATA_DIR} not found. Running build and convert only.")
        model = build_model()
        convert_to_tflite(model, os.path.join(MODELS_DIR, 'mosaicalert_f16.tflite'), quantization='float16')
