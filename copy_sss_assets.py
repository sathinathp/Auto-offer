import os
import shutil

dest_dir = os.path.join('static', 'images', 'softstandard')
os.makedirs(dest_dir, exist_ok=True)

# Copy and rename appropriately
shutil.copy('sss_assets/extracted_image_3.jpeg', os.path.join(dest_dir, 'logo.jpg'))
shutil.copy('sss_assets/extracted_image_4.png', os.path.join(dest_dir, 'divider.png'))
shutil.copy('sss_assets/extracted_image_1.png', os.path.join(dest_dir, 'sig_ceo.png'))
shutil.copy('sss_assets/extracted_image_2.png', os.path.join(dest_dir, 'sig_hr.png'))

print("SoftStandard assets copied successfully to:", dest_dir)
