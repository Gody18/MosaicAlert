import os
from PIL import Image

def generate_icons(source_image_path):
    # Android icon sizes (mipmap)
    android_sizes = {
        'mipmap-mdpi': 48,
        'mipmap-hdpi': 72,
        'mipmap-xhdpi': 96,
        'mipmap-xxhdpi': 144,
        'mipmap-xxxhdpi': 192
    }
    
    android_res_path = 'G:/MosaicAlert/app/android/app/src/main/res'
    
    # Open source image
    img = Image.open(source_image_path)
    
    # Generate Android icons
    for folder, size in android_sizes.items():
        folder_path = os.path.join(android_res_path, folder)
        os.makedirs(folder_path, exist_ok=True)
        
        # ic_launcher.png (Square)
        icon = img.resize((size, size), Image.Resampling.LANCZOS)
        icon.save(os.path.join(folder_path, 'ic_launcher.png'))
        
        # ic_launcher_round.png (Round - simple crop)
        # Create a circular mask
        mask = Image.new('L', (size, size), 0)
        from PIL import ImageDraw
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        
        round_icon = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        round_icon.paste(icon, (0, 0), mask)
        round_icon.save(os.path.join(folder_path, 'ic_launcher_round.png'))
        
    print("Android icons generated successfully.")

    # iOS icon sizes
    ios_sizes = [
        (20, 1), (20, 2), (20, 3),
        (29, 1), (29, 2), (29, 3),
        (40, 1), (40, 2), (40, 3),
        (60, 2), (60, 3),
        (76, 1), (76, 2),
        (83.5, 2),
        (1024, 1)
    ]
    
    ios_res_path = 'G:/MosaicAlert/app/ios/MosaicAlert/Images.xcassets/AppIcon.appiconset'
    os.makedirs(ios_res_path, exist_ok=True)
    
    for size, scale in ios_sizes:
        actual_size = int(size * scale)
        name = f"icon-{size}x{size}@{scale}x.png" if scale > 1 else f"icon-{size}x{size}.png"
        icon = img.resize((actual_size, actual_size), Image.Resampling.LANCZOS)
        icon.save(os.path.join(ios_res_path, name))
        
    print("iOS icons generated successfully.")

if __name__ == "__main__":
    # Corrected image path based on user feedback
    generate_icons('G:/MosaicAlert/app/android/app/src/main/res/mosaicicon.png')
