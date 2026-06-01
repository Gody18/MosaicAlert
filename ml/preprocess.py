import cv2
import numpy as np
import os
import glob
from sklearn.model_selection import train_test_split

# Constants
IMG_SIZE = (224, 224)

def detect_and_crop_leaf(image):
    """
    Simple leaf detection using contour detection to crop the leaf region.
    1. Convert to grayscale.
    2. Threshold to find the largest object (the leaf).
    3. Find the bounding box of the largest contour.
    4. Crop the image to this bounding box.
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Simple thresholding or edge detection could work here.
    # We'll use Otsu's thresholding for better results in different lighting.
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return image # Return original if no contours found
    
    # Find the largest contour (assume it's the leaf)
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Get bounding box
    x, y, w, h = cv2.boundingRect(largest_contour)
    
    # Add a small padding if possible
    padding = 10
    h_orig, w_orig = image.shape[:2]
    x = max(0, x - padding)
    y = max(0, y - padding)
    w = min(w_orig - x, w + 2 * padding)
    h = min(h_orig - y, h + 2 * padding)
    
    cropped = image[y:y+h, x:x+w]
    return cropped

def preprocess_image(image_path, target_size=IMG_SIZE, crop=True):
    """
    Full preprocessing pipeline for a single image.
    """
    image = cv2.imread(image_path)
    if image is None:
        return None
    
    if crop:
        image = detect_and_crop_leaf(image)
    
    # Resize to target size
    image = cv2.resize(image, target_size)
    
    # Normalization is usually handled by the training generator,
    # but for manual inference/evaluation, we'd divide by 255.
    return image

def create_dataset_manifest(data_dir):
    """
    Scans the data directory and creates a list of (image_path, label).
    Assumes binary classification for MVP: 'healthy' and 'mosaic'.
    """
    manifest = []
    classes = ['healthy', 'mosaic']
    
    for label in classes:
        class_dir = os.path.join(data_dir, label)
        if not os.path.exists(class_dir):
            continue
            
        for img_path in glob.glob(os.path.join(class_dir, '*.*')):
            manifest.append((img_path, label))
            
    return manifest

if __name__ == "__main__":
    print("MosaicAlert Image Preprocessing Module Initialized.")
    # Example usage (not executed automatically)
    # manifest = create_dataset_manifest('./data/raw')
    # train, val = train_test_split(manifest, test_size=0.15)
