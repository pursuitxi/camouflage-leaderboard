from PIL import Image
import numpy as np

def combine_images(original_path, mask_path, output_path):
    # Load the original image
    original = Image.open(original_path).convert("RGB")
    
    # Load the mask image
    mask = Image.open(mask_path).convert("RGBA")  # Ensure mask is in RGBA format
    mask_data = np.array(mask)
    
    # Extract RGB channels where alpha is greater than 128, and set the rest to black
    mask_rgb_data = np.zeros_like(mask_data[:, :, :3], dtype=np.uint8)
    mask_rgb_data[mask_data[:, :, 3] > 128] = mask_data[mask_data[:, :, 3] > 128, :3]
    mask_rgb = Image.fromarray(mask_rgb_data, "RGB")
    
    # Ensure both images have the same height
    if original.size[1] != mask_rgb.size[1]:
        raise ValueError("The height of the original image and mask image must be the same.")
    
    # Create a new image with the same size as the original
    combined_image = Image.new("RGB", original.size)
    
    # Copy the left half of the original image to the new image
    combined_image.paste(original.crop((0, 0, original.size[0] // 2, original.size[1])), (0, 0))
    
    # Create the right half: mask result + black background
    right_half = Image.new("RGB", (original.size[0] // 2, original.size[1]), (0, 0, 0))
    right_half.paste(mask_rgb.crop((mask_rgb.size[0] // 2, 0, mask_rgb.size[0], mask_rgb.size[1])), (0, 0))
    
    # Paste the right half into the new image
    combined_image.paste(right_half, (original.size[0] // 2, 0))
    
    # Save the combined image
    combined_image.save(output_path)
    print(f"Combined image saved to {output_path}")

# Example usage
for i in range(1, 7):
    combine_images(
        original_path=fr"C:\Users\16781\benchmark-leaderboard\public\data\demo-{i}-l.jpg",
        mask_path=fr"C:\Users\16781\benchmark-leaderboard\public\data\demo-{i}-r.png",
        output_path=fr"C:\Users\16781\benchmark-leaderboard\public\data\output_combined_{i}.png"
    )
# combine_images(
#     original_path=fr"C:\Users\16781\benchmark-leaderboard\public\data\demo-1-l.jpg",
#     mask_path=fr"C:\Users\16781\benchmark-leaderboard\public\data\demo-1-r.png",
#     output_path=fr"C:\Users\16781\benchmark-leaderboard\public\data\output_combined_1.png"
# )