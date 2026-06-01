MosaicAlert is an offline-first mobile application designed for smallholder farmers to detect Cassava Mosaic Disease from leaf photos and provide practical advisory steps.

## Features
- **Accurate Offline Detection**: On-device ML model (MobileNetV2) for Healthy vs. Mosaic classification.
- **Farmer-Friendly UX**: Swahili-first interface with voice guidance and clear advisory steps.
- **Lightweight & Fast**: Optimized for low-end Android devices with TFLite.
- **Offline Storage**: Local history of scans and offline advisory content.
- **Data Privacy**: Local-first data storage with optional cloud sync for model improvement.

## Project Structure
- `app/`: React Native (TypeScript) mobile application.
- `ml/`: Python training pipeline and TFLite conversion scripts.
- `models/`: Pre-trained and quantized TFLite models.
- `docs/`: Technical specification and project documentation.

## Getting Started

### Mobile App (React Native)
1. Navigate to `app/`.
2. Install dependencies: `npm install`.
3. Run on Android: `npx react-native run-android`.
4. Run on iOS: `npx react-native run-ios`.

### ML Training Pipeline (Python)
1. Navigate to `ml/`.
2. Install dependencies: `pip install -r requirements.txt`.
3. Train model: `python train.py`.
4. Preprocess data: `python preprocess.py`.

## Model Evaluation (MVP)
- **Accuracy**: ≥ 88%
- **Recall (Mosaic)**: ≥ 85%
- **Model Size**: ≤ 15 MB (Quantized)
- **Inference Time**: < 300ms on representative low-end Android.

## Deliverables Included
- React Native project scaffold (TypeScript).
- Python training and preprocessing pipeline.
- Sample TFLite model variants (Float16).
- Technical specification document.
- Root README with build & test steps.
