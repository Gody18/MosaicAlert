# MosaicAlert Technical Specification

## System Architecture

### 1. Mobile Application (React Native)
- **Framework**: React Native with TypeScript.
- **Camera**: `react-native-vision-camera` for low-latency image capture and real-time guidance.
- **ML Engine**: `react-native-fast-tflite` for on-device inference using quantized TFLite models.
- **Storage**: 
  - `react-native-mmkv` for high-performance settings and simple state.
  - `react-native-sqlite-storage` for history and local data collection.
- **Voice**: `react-native-tts` for Swahili voice guidance.
- **Offline-First**: All core features work without internet. Syncing to cloud is opt-in and occurs only when connected.

### 2. ML Training Pipeline (Python)
- **Framework**: TensorFlow / Keras.
- **Backbone**: MobileNetV2 (recommended for low-end Android devices).
- **Quantization**: Post-training quantization to Float16 (target < 15MB) and INT8 for maximum efficiency.
- **Data Augmentation**: Rotation, flip, brightness, contrast, and zoom to improve generalization in field conditions.

## Data Schema (Local SQLite)

### Table: `Scans`
| Field | Type | Description |
|---|---|---|
| `id` | UUID | Unique identifier |
| `timestamp` | DATETIME | Time of scan |
| `class` | STRING | Healthy / Mosaic |
| `confidence` | FLOAT | Model confidence score |
| `image_path` | STRING | Local path to the captured image |
| `is_synced` | BOOLEAN | Whether uploaded to cloud |

## UI/UX Design Principles
- **Swahili-First**: All labels and voice prompts default to Swahili.
- **Accessibility**: Large touch targets, high-contrast colors, and voice readout.
- **Efficiency**: Minimal steps from home screen to diagnosis (< 3 clicks).

## Performance Targets
- **Model Size**: < 15MB.
- **Inference Time**: < 300ms on 2GB RAM Android devices.
- **Accuracy**: > 88% on validation set.
- **Recall (Mosaic)**: > 85% to minimize false negatives.
