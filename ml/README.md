# MosaicAlert ML Training Guide

This directory contains the pipeline for training the MosaicAlert cassava leaf disease detection model.

## Prerequisites
- Python 3.10+
- `pip install -r requirements.txt`

## 1. Data Sourcing
We use the **Cassava Leaf Disease Classification** dataset from Kaggle.
1. Download the dataset from [Kaggle](https://www.kaggle.com/c/cassava-leaf-disease-classification/data).
2. Extract it into a directory named `kaggle_data/` in the root of the project.
   - It should contain `train_images/` and `train.csv`.

## 2. Data Curation & Preprocessing
Run the curation script to filter for Healthy and Mosaic classes and remove low-quality images.
```bash
python curate_data.py
```
This will:
- Extract images with labels `3` (Mosaic) and `4` (Healthy).
- Filter out blurred images (Laplacian variance < 100).
- Organize them into `data/curated/healthy` and `data/curated/mosaic`.
- Generate a `manifest.json`.

## 3. Training the Model
Run the training script to train the MobileNetV2-based model and export TFLite variants.
```bash
python train.py
```
The script includes:
- **Advanced Augmentation**: Rotation, flip, brightness, zoom.
- **Leaf Detection**: Contour-based cropping in `preprocess.py`.
- **Optimization**: Adam optimizer with weight decay and learning rate scheduler.
- **Evaluation**: Precision, Recall, F1-score, ROC-AUC, and Confusion Matrix.
- **Export**: Generates `mosaicalert_f16.tflite` and `mosaicalert_int8.tflite` in `../models/`.

##  acceptance Criteria
- **Accuracy**: ≥ 88%
- **Recall (Mosaic)**: ≥ 85%
- **Model Size**: ≤ 15 MB (Quantized)
- **Inference Time**: < 300ms on representative low-end Android.
