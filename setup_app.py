import os
import shutil

def setup_directories():
    os.makedirs("static/images", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # Map extracted assets
    # Image 1 -> Logo
    shutil.copy("extracted_assets/extracted_image_1.png", "static/images/logo.png")
    # Image 2 -> Divider
    shutil.copy("extracted_assets/extracted_image_2.png", "static/images/divider.png")
    # Image 3 -> Sanjay Kumar (CEO) Signature
    shutil.copy("extracted_assets/extracted_image_3.png", "static/images/sig_ceo.png")
    # Image 4 -> Askani David Raj (HR) Signature
    shutil.copy("extracted_assets/extracted_image_4.png", "static/images/sig_hr.png")
    
    print("Folders created and images copied successfully!")

if __name__ == "__main__":
    setup_directories()
