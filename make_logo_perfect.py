from PIL import Image
import numpy as np

def color_to_alpha(input_path, output_path):
    img = Image.open(input_path).convert("RGBA")
    arr = np.array(img, dtype=float)
    
    r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]
    
    # Calculate distances from white (255, 255, 255)
    dr = 255.0 - r
    dg = 255.0 - g
    db = 255.0 - b
    
    # Alpha is the maximum distance from white, normalized to [0, 255]
    alpha = np.maximum(np.maximum(dr, dg), db)
    
    # Create mask for pixels that are not fully transparent
    mask = alpha > 0
    
    # Recover original foreground color (un-blend from white background)
    # C = alpha * C_f + (1 - alpha) * 255 => C_f = (C - 255 * (1 - alpha)) / alpha
    # normalize alpha to [0.0, 1.0] for math
    alpha_norm = alpha / 255.0
    
    new_r = np.copy(r)
    new_g = np.copy(g)
    new_b = np.copy(b)
    
    new_r[mask] = (r[mask] - 255.0 * (1.0 - alpha_norm[mask])) / alpha_norm[mask]
    new_g[mask] = (g[mask] - 255.0 * (1.0 - alpha_norm[mask])) / alpha_norm[mask]
    new_b[mask] = (b[mask] - 255.0 * (1.0 - alpha_norm[mask])) / alpha_norm[mask]
    
    # Clamp to [0, 255] range
    new_r = np.clip(new_r, 0, 255)
    new_g = np.clip(new_g, 0, 255)
    new_b = np.clip(new_b, 0, 255)
    
    # Combine back into RGBA array
    out_arr = np.zeros_like(arr, dtype=np.uint8)
    out_arr[:,:,0] = new_r.astype(np.uint8)
    out_arr[:,:,1] = new_g.astype(np.uint8)
    out_arr[:,:,2] = new_b.astype(np.uint8)
    out_arr[:,:,3] = alpha.astype(np.uint8)
    
    out_img = Image.fromarray(out_arr, "RGBA")
    out_img.save(output_path, "PNG")
    print(f"Saved perfect transparent image to {output_path}")

if __name__ == "__main__":
    color_to_alpha("logo.png", "static/images/petabytz/img_7.png")
