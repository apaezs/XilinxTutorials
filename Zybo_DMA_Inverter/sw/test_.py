import serial
import numpy as np
import time
import matplotlib.pyplot as plt
from PIL import Image
import sys

# Configuration
SERIAL_PORT = 'COM4'  # Change to your port (e.g., '/dev/ttyUSB0' on Linux)
BAUD_RATE = 115200
IMG_SIZE = 28 * 28  # 784 bytes

def load_and_prepare_image(image_path):
    """Load image from path and prepare it for transmission"""
    try:
        # Load image
        img = Image.open(image_path)
        
        # Convert to grayscale
        img_gray = img.convert('L')
        original_array = np.array(img_gray, dtype=np.uint8)
        
        # Resize to 28x28
        img_resized = img_gray.resize((28, 28), Image.Resampling.LANCZOS)
        
        # Convert to numpy array
        img_array = np.array(img_resized, dtype=np.uint8)
        
        print(f"Loaded image: {image_path}")
        print(f"Original size: {original_array.shape}")
        print(f"Resized to: {img_array.shape}")
        print(f"Value range: [{img_array.min()}, {img_array.max()}]")
        
        return original_array, img_array.flatten()
        
    except Exception as e:
        print(f"Error loading image: {e}")
        return None, None

def create_test_image():
    """Create a simple test pattern - letter 'C' shape"""
    img = np.zeros((28, 28), dtype=np.uint8)
    
    # Draw a 'C' shape
    img[5:23, 6:12] = 255    # Left vertical
    img[5:11, 6:18] = 255     # Top horizontal
    img[17:23, 6:18] = 255    # Bottom horizontal
    
    return img.flatten()

def display_images(original_img, tx_img, rx_img, expected_img, mismatches):
    """Display the original, transmitted, received, and expected images"""
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))
    
    # Original image (before resizing)
    axes[0, 0].imshow(original_img, cmap='gray')
    axes[0, 0].set_title(f'Original Image\n({original_img.shape[1]}x{original_img.shape[0]})')
    axes[0, 0].axis('off')
    
    # Transmitted image (28x28)
    axes[0, 1].imshow(tx_img, cmap='gray', vmin=0, vmax=255)
    axes[0, 1].set_title('Transmitted (28x28)')
    axes[0, 1].axis('off')
    
    # Received image
    axes[1, 0].imshow(rx_img, cmap='gray', vmin=0, vmax=255)
    axes[1, 0].set_title('Received from FPGA')
    axes[1, 0].axis('off')
    
    # Expected image
    axes[1, 1].imshow(expected_img, cmap='gray', vmin=0, vmax=255)
    axes[1, 1].set_title('Expected Inverted')
    axes[1, 1].axis('off')
    
    # Add overall title with result
    if mismatches == 0:
        fig.suptitle('✓ SUCCESS! All pixels inverted correctly!', 
                     fontsize=16, color='green', fontweight='bold', y=0.98)
    else:
        fig.suptitle(f'✗ FAILED! {mismatches}/{IMG_SIZE} mismatches', 
                     fontsize=16, color='red', fontweight='bold', y=0.98)
    
    plt.tight_layout()
    plt.savefig('inversion_result.png', dpi=150, bbox_inches='tight')
    print("Saved visualization as 'inversion_result.png'")
    plt.show()

def main():
    # Check if image path provided as argument
    original_img = None
    if len(sys.argv) > 1:
        image_path = sys.argv[1]
        print(f"Loading image from: {image_path}")
        original_img, tx_data = load_and_prepare_image(image_path)
        if tx_data is None:
            print("Failed to load image. Exiting.")
            return
    else:
        print("No image path provided. Using default test pattern.")
        print("Usage: python script.py <path_to_image>")
        print("Example: python script.py my_image.png")
        print("\nUsing default 'C' pattern instead...\n")
        tx_data = create_test_image()
        original_img = tx_data.reshape(28, 28)
    
    print("Opening serial port...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=5)
    time.sleep(2)  # Wait for board to be ready
    
    # Clear any existing data in buffer
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    
    print(f"Sending {len(tx_data)} bytes...")
    ser.write(tx_data.tobytes())
    ser.flush()
    
    print("Waiting for response...")
    rx_data = ser.read(IMG_SIZE)
    
    if len(rx_data) != IMG_SIZE:
        print(f"ERROR: Expected {IMG_SIZE} bytes, got {len(rx_data)}")
        ser.close()
        return
    
    # Convert to numpy array
    rx_array = np.frombuffer(rx_data, dtype=np.uint8)
    expected = 255 - tx_data
    
    # Compare results
    mismatches = np.sum(rx_array != expected)
    
    print(f"\nResults:")
    print(f"Mismatches: {mismatches}/{IMG_SIZE}")
    
    if mismatches == 0:
        print("✓ SUCCESS! All pixels inverted correctly!")
    else:
        print(f"✗ FAILED! {mismatches} pixels don't match")
        
        # Show first few mismatches
        print("\nFirst mismatches:")
        mismatch_indices = np.where(rx_array != expected)[0]
        for i in mismatch_indices[:10]:
            print(f"  Index {i}: expected {expected[i]}, got {rx_array[i]}")
    
    # Reshape for visualization
    tx_img = tx_data.reshape(28, 28)
    rx_img = rx_array.reshape(28, 28)
    expected_img = expected.reshape(28, 28)
    
    # Save as text files
    print("\nSaving text files...")
    np.savetxt('tx_image.txt', tx_img, fmt='%d')
    np.savetxt('rx_image.txt', rx_img, fmt='%d')
    np.savetxt('expected_image.txt', expected_img, fmt='%d')
    print("Saved: tx_image.txt, rx_image.txt, expected_image.txt")
    
    # Display images
    print("\nDisplaying images...")
    display_images(original_img, tx_img, rx_img, expected_img, mismatches)
    
    ser.close()
    print("\nDone!")

if __name__ == "__main__":
    main()