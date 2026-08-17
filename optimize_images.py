import os
from PIL import Image, ImageOps

SRC_DIR = "/home/akhil/StudioProjects/wedding_invitee/wedding_invitee/assets"
DEST_DIR = "/home/akhil/snap/antigravity/5/.gemini/antigravity/scratch/wedding_invity/assets"

# Target widths based on page usage
TARGET_SIZES = {
    # Portraits (260x260 on screen -> 600px max for high DPI)
    "groom": 600,
    "bride": 600,
    # Banner strip columns (1/3 of viewport -> 800px max)
    "banner": 800,
    "banner_try": 800,
    # Full width footer backgrounds
    "footer": 1200,
    "footer1": 1200,
    "footer2": 1200,
}

def get_target_width(filename):
    name_lower = filename.lower()
    for key, size in TARGET_SIZES.items():
        if key in name_lower:
            return size
    return 1000  # Default fallback width

def optimize_image(src_path, dest_path, target_width):
    try:
        with Image.open(src_path) as img:
            # Handle EXIF rotation (so photos aren't rotated sideways)
            img = ImageOps.exif_transpose(img)
            
            # Convert to RGB if needed (WebP/JPEG require RGB)
            if img.mode in ("RGBA", "P") and dest_path.endswith((".jpg", ".jpeg")):
                img = img.convert("RGB")
            
            # Calculate target height keeping aspect ratio
            width, height = img.size
            if width > target_width:
                aspect_ratio = height / width
                target_height = int(target_width * aspect_ratio)
                img = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
                print(f"Resized: {os.path.basename(src_path)} -> {target_width}x{target_height}")
            else:
                print(f"Kept original size for: {os.path.basename(src_path)} ({width}x{height})")
            
            # Save compressed WebP
            img.save(dest_path, "WEBP", quality=85)
            
            orig_size = os.path.getsize(src_path) / (1024 * 1024)
            new_size = os.path.getsize(dest_path) / (1024 * 1024)
            print(f"Optimized {os.path.basename(src_path)}: {orig_size:.2f}MB -> {new_size:.2f}MB ({((orig_size - new_size)/orig_size)*100:.1f}% reduction)")
    except Exception as e:
        print(f"Error optimizing {src_path}: {e}")

def main():
    print("Starting image optimization...")
    
    # Create output directories
    os.makedirs(os.path.join(DEST_DIR, "images"), exist_ok=True)
    os.makedirs(os.path.join(DEST_DIR, "icons"), exist_ok=True)
    
    # Process images
    src_images_dir = os.path.join(SRC_DIR, "images")
    if os.path.exists(src_images_dir):
        for filename in os.listdir(src_images_dir):
            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                src_path = os.path.join(src_images_dir, filename)
                base_name, _ = os.path.splitext(filename)
                dest_path = os.path.join(DEST_DIR, "images", f"{base_name}.webp")
                
                target_width = get_target_width(filename)
                optimize_image(src_path, dest_path, target_width)
    
    # Process icons (simply copy or save as PNG/WebP if small)
    src_icons_dir = os.path.join(SRC_DIR, "icons")
    if os.path.exists(src_icons_dir):
        for filename in os.listdir(src_icons_dir):
            src_path = os.path.join(src_icons_dir, filename)
            if os.path.isfile(src_path):
                dest_path = os.path.join(DEST_DIR, "icons", filename)
                # Copy small icons
                try:
                    with Image.open(src_path) as img:
                        img.save(dest_path)
                    print(f"Copied icon: {filename}")
                except Exception as e:
                    import shutil
                    shutil.copy2(src_path, dest_path)
                    print(f"Copied icon (fallback): {filename}")

if __name__ == "__main__":
    main()
