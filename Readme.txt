Project name: MosaicAlert — AI-powered offline cassava leaf disease early-warning and advisory mobile app (React Native + on-device ML)

Overview / Mission
You are building MosaicAlert, an offline-first mobile application for smallholder cassava farmers to detect Cassava Mosaic Disease from leaf photos and provide clear, practical advisory steps. The app must run entirely offline for diagnosis (on-device ML), be extremely lightweight and fast on low-end Android devices, and present results in plain Swahili with optional English. The MVP focuses on binary classification (Healthy vs. Mosaic) and is designed as a real startup product for farmers, NGOs, and agricultural extension services.

Primary objectives (MUST)

Accurate offline detection: on-device model that classifies a leaf as Healthy or Cassava Mosaic Disease with a usable confidence score and thresholds.

Farmer-friendly UX: minimal steps to capture a good photo, clear result screen, voice guidance in Swahili, and actionable next steps (remove infected plants, isolate, contact extension).

Extremely lightweight & robust: final app binary + model ideally keeps model <15 MB, inference <300ms on typical low-end Android phones, supports Android (primary) and iOS (secondary).

Data collection & improvement channel: allow opt-in uploads when internet available to collect field images and improve models over time.

Startup readiness: features that demonstrate value to NGOs and investors (analytics dashboard, history export, SMS integration as optional paid feature).

Dataset sources & guidance

Start by using public cassava leaf datasets used in research and competitions (e.g., datasets contributed by institutions such as Makerere University, collaborations with Google AI, and collections available on Kaggle). For MVP extract only the Healthy and Mosaic classes.

Expected minimum initial dataset (after combining public sources + augmentation): ~1,000–3,000 effective samples per class. If raw public samples are fewer, apply augmentation (see below) and bootstrap further from field collection.

Data preparation (detailed)

Curation: Filter out very low quality images (extreme blur / unreadable). Keep diversity: different cameras, lighting, leaf ages, backgrounds, cassava varieties.

Annotation: Binary labels only for MVP: healthy, mosaic. Keep a CSV/JSON manifest with fields: image_path, label, gps(optional), date, device_model, notes.

Preprocessing pipeline:

Leaf detection / segmentation (simple method): run contour detection or lightweight U-Net/Mask approach offline during training to crop the leaf region. Save both full-frame and crop.

Resize to 224×224 (or 192×192 for smaller model footprint).

Normalize using ImageNet stats if transfer learning base used.

Apply augmentation (during training): rotation ±30°, horizontal flip, brightness ±30%, contrast ±20%, random zoom/crop, small Gaussian blur, hue jitter. Avoid unrealistic artifacts.

Split: Train/Validation/Test = 70/15/15, but ensure images from the same farm/device are not split across sets to prevent leakage.

Model architecture & training

Base: Transfer learning from a lightweight backbone (recommended: MobileNetV2 or EfficientNet-Lite0/Lite1).

Head: GlobalAveragePooling + Dense(128, relu) + Dropout(0.3) + Dense(2, softmax).

Loss: Categorical cross-entropy.

Metrics: Accuracy, Precision, Recall, F1 per class, ROC-AUC, and confusion matrix. Also compute per-class false negative rate — minimize FN on mosaic.

Training settings (suggested): batch 32, learning rate 1e-4 with scheduler, early stopping on val loss, 10–50 epochs depending on convergence. Use weight decay 1e-5.

Regularization: MixUp or label smoothing can help generalization.

Model compression: After training, apply post-training quantization (Float16 or INT8) and pruning if necessary to reduce model size while monitoring accuracy drop. Target model size <15 MB for best adoption.

Export: Convert to TensorFlow Lite .tflite with metadata (labels, input shape) and multiple quantization variants (float32, float16, int8) for device compatibility.

On-device inference & pipeline

Camera capture UI: guide overlay (circle or leaf-shaped mask), real-time quality checks (sharpness, exposure, leaf-centered). If quality low, prompt to retake. Optionally implement auto-capture when the leaf is steady and centered.

Preprocessing on-device: crop to leaf area (use lightweight segmentation or classical CV heuristic), resize, normalize, pass to TFLite interpreter.

Inference output: predicted_class, confidence (probability), and a small grad-CAM style heatmap overlay (optional, if model supports explainability).

Decision thresholds:

Confidence ≥ 0.85 → Confirmed

0.60 ≤ Confidence < 0.85 → Likely — suggest retake or second opinion

Confidence < 0.60 → Uncertain — ask user to retake or seek extension officer

UX display: class label (Swahili), confidence %, recommended actions, voice readout option.

React Native engineering details

Framework: React Native (latest stable). Prefer TypeScript.

Key native modules / libraries:

Camera: react-native-vision-camera or react-native-camera for reliable capture and performance.

TFLite: tflite-react-native or custom native bridge to TensorFlow Lite. Provide two build flavors (Android: ARMv7, ARM64; iOS: arm64).

Local DB: react-native-sqlite-storage or WatermelonDB/MMKV for history and settings.

Voice (TTS): react-native-tts with Swahili voice support (fallback to Android/iOS built-in).

File & permissions: react-native-permissions, react-native-fs.

Optional: ONNX Runtime Mobile if you prefer ONNX models.

App modules: CameraScreen, ResultScreen, History, Education, Settings, Admin/Upload (optional), Debug/Test (for collecting labeled images).

Bundle size & performance: Keep dependencies minimal; load the model lazily after first app start. Use code-splitting and proguard/R8 for Android.

Offline-first: All detection and core UX must function with zero network. Any uploads or model updates are opt-in and background when network available.

UX / UI copy & flows (Swahili-first)

Use short, clear Swahili copy. All labels in Swahili with English toggle. Examples:

Home CTA: “Piga Jani” (Scan Leaf)

Result (healthy): “Jani Hivyo Huonekana Kuwa Salama” Confidence: 94% — Endelea kuangalia mara kwa mara.

Result (mosaic): “Dalili za Ugonjwa wa Mosaic Zimepatikana” Confidence: 89% — Ondoa mmea uliougua, sekea mbegu safi, na wasiliana na afisa kilimo.

Confidence low: “Matokeo Hayajidhihirishi” — Rudia picha au wasiliana na mtaalamu.

Accessibility: large fonts, high-contrast colors, voice readout button (“Sikiliza”), and icons.

Data privacy & consent

Default data stays on-device. Any upload of images/data to cloud requires explicit user opt-in and shows purpose, who will access data (research/improvement), and retention policy. Provide a simple consent screen and a way to delete uploaded data.

Field testing & QA

Alpha (internal) tests: engineers + agronomists test on 50–100 lab images.

Beta (field) tests: pilot with 50–200 farmers across multiple regions and devices; collect edge cases.

Metrics to track: real-world accuracy, false negative rate on mosaic, time-to-inference, user task success rate (can user get a usable action in <30s), crash rate, and battery impact.

Acceptance criteria (MVP):

On test set: Accuracy ≥ 88%, Recall (mosaic) ≥ 85%

Model size ≤ 15 MB (quantized variant)

Cold-start inference < 300ms on representative low-end Android (e.g., 2–3 year old mid-tier device)

App works fully offline for detection and advice screens

Basic Swahili TTS works for result readout

Pilot farmers can use the app with minimal training (verified via usability test)

Optional but high-value features (phase 2+)

Multi-class detection (Brown Streak, Nutrient Deficiency, etc.)

Severity estimation (mild/moderate/severe)

GPS heatmaps and aggregated analytics dashboard for NGOs / extension officers (with privacy-preserving aggregation)

SMS alert integration (paid tier) for extension services

Seamless model update mechanism (signed model packages downloaded when internet available)

Explainability (visual heatmap to show which leaf area triggered the prediction)

Deliverables expected from the AI builder

Technical specification document (detailed system architecture, components, data schema, CI/CD, model training recipe).

React Native project scaffold (TypeScript) with CameraScreen, integration stub for TFLite, ResultScreen UI, local DB and Settings. Include README with build & install steps for Android & iOS.

Training pipeline code (Python/TensorFlow Jupyter notebooks or scripts) that: downloads/ingests public datasets, runs preprocessing, trains transfer-learning model, evaluates, and exports quantized .tflite models.

Two working TFLite model variants (float16 and int8) with size and accuracy reports.

Prototype APK installable on Android for testing (with test images included).

Pilot test plan & data collection form (how to recruit farmers, consent, metadata to capture).

One-page investor / partner brief describing product, impact, go-to-market, and monetization options.

Timeline (make sure all are implemented when building at the first time, stating to build)

Data sourcing + initial preprocessing

Train baseline model (transfer learning) + export TFLite prototypes

React Native scaffold + camera + local inference integration (alpha)

Field pilot (50–200 farmers) + collect feedback & more images

Model iteration + polish + production APK and partner outreach

Implementation constraints & non-functional requirements

Offline-first for detection and advisory.

Must run on Android API level 21+ and iOS 13+.

Minimal battery and CPU impact; avoid long on-device training.

Model size ideally <15 MB, app size acceptable <40–50 MB total (excluding media).

Provide logs/analytics only with explicit opt-in.

Final instructions for the AI builder (copyable task text)

You are an engineering AI assigned to deliver MosaicAlert MVP. Deliverables, constraints, acceptance criteria, and concrete steps are described above. Produce:

A single ZIP with: React Native project scaffold (TypeScript), Python training scripts/notebooks, sample .tflite model(s), README with exact build/test steps, and a short pilot recruitment guide.

A short demo script that a non-technical reviewer (agronomist) can follow to validate function in 10 minutes.

Clear documentation of any assumptions and a prioritized backlog for features beyond MVP.

Focus on reliability for low-end devices, Swahili UX, and an ethical data collection approach. When you provide models, include evaluation metrics and the exact commands used to convert and quantize to .tflite. Use MobileNetV2 or EfficientNet-Lite as default backbones, and justify tradeoffs if you choose otherwise.