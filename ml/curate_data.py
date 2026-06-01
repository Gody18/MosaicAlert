import os
import pandas as pd
import shutil
import cv2
import json
from tqdm import tqdm

def curate_kaggle_dataset(raw_data_dir, output_dir, csv_label_file='train.csv'):
    """
    Curates the Kaggle Cassava Leaf Disease Classification dataset.
    Labels in that dataset:
    0: Cassava Bacterial Blight (CBB)
    1: Cassava Brown Streak Disease (CBSD)
    2: Cassava Green Mottle (CGM)
    3: Cassava Mosaic Disease (CMD) -> Mosaic
    4: Healthy -> Healthy
    """
    if not os.path.exists(raw_data_dir):
        print(f"Raw data directory {raw_data_dir} not found.")
        return

    # Load labels
    labels_df = pd.read_csv(os.path.join(raw_data_dir, csv_label_file))
    
    # Filter for CMD (3) and Healthy (4)
    mosaic_df = labels_df[labels_df['label'] == 3]
    healthy_df = labels_df[labels_df['label'] == 4]
    
    # Create output directories
    os.makedirs(os.path.join(output_dir, 'mosaic'), exist_ok=True)
    os.makedirs(os.path.join(output_dir, 'healthy'), exist_ok=True)
    
    manifest = []

    def process_subset(df, label_name, target_dir):
        print(f"Processing {label_name} images...")
        for _, row in tqdm(df.iterrows(), total=len(df)):
            img_id = row['image_id']
            src_path = os.path.join(raw_data_dir, 'train_images', img_id)
            dest_path = os.path.join(target_dir, img_id)
            
            if not os.path.exists(src_path):
                continue
                
            # Quality Filter: Blur detection (Laplacian variance)
            image = cv2.imread(src_path)
            if image is None:
                continue
                
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            fm = cv2.Laplacian(gray, cv2.CV_64F).var()
            
            if fm < 100: # Threshold for blur (low value = more blur)
                continue
            
            # Copy file
            shutil.copy(src_path, dest_path)
            
            # Add to manifest
            manifest.append({
                'image_path': os.path.relpath(dest_path, output_dir),
                'label': label_name,
                'blur_score': fm,
                'original_id': img_id
            })

    process_subset(mosaic_df, 'mosaic', os.path.join(output_dir, 'mosaic'))
    process_subset(healthy_df, 'healthy', os.path.join(output_dir, 'healthy'))
    
    # Save manifest
    with open(os.path.join(output_dir, 'manifest.json'), 'w') as f:
        json.dump(manifest, f, indent=4)
    
    print(f"Curation complete. Manifest saved to {os.path.join(output_dir, 'manifest.json')}")

if __name__ == "__main__":
    # Example paths
    RAW_DIR = './kaggle_data' # User should point to their downloaded Kaggle data
    OUTPUT_DIR = './data/curated'
    
    print("MosaicAlert Data Curation Tool")
    print("------------------------------")
    print(f"Source: {RAW_DIR}")
    print(f"Destination: {OUTPUT_DIR}")
    
    curate_kaggle_dataset(RAW_DIR, OUTPUT_DIR)
