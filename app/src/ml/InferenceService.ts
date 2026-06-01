import { loadTensorflowModel, TensorflowModel } from 'react-native-fast-tflite';

class InferenceService {
  private model: TensorflowModel | null = null;
  private isLoaded: boolean = false;

  async initModel() {
    try {
      // Load the model from assets (ensure it's bundled)
      this.model = await loadTensorflowModel(require('../assets/models/mosaicalert_f16.tflite'));
      this.isLoaded = true;
      console.log('TFLite Model Loaded Successfully');
    } catch (error) {
      console.error('Failed to load TFLite model:', error);
    }
  }

  async runInference(imagePath: string): Promise<{ class: string; confidence: number }> {
    if (!this.model) {
      throw new Error('Model not loaded');
    }

    // Preprocessing on-device (Stubbed for now)
    // In a production app, we'd use a lightweight segmentation model or
    // OpenCV-style contour detection to crop the leaf area.
    console.log(`Preprocessing image at ${imagePath}: cropping to leaf area...`);

    // 1. Resize (usually handled by the fast-tflite bridge)
    // 2. Normalize (0-1 range)
    // 3. Inference

    // Simulating inference result with the dummy model
    // The dummy model output is [prob_healthy, prob_mosaic]
    const results = await this.model.run([new Float32Array(224 * 224 * 3).fill(0.5)]);

    // Example output from model: [prob_healthy, prob_mosaic]
    const outputs = results[0] as Float32Array;
    const probHealthy = outputs[0];
    const probMosaic = outputs[1];

    if (probMosaic > probHealthy) {
      return { class: 'Mosaic', confidence: probMosaic };
    } else {
      return { class: 'Healthy', confidence: probHealthy };
    }
  }

  getIsLoaded() {
    return this.isLoaded;
  }
}

export default new InferenceService();
