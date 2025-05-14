import numpy as np
import cv2
from PIL import Image, ImageOps
import io

def preprocess_image(image, target_size=(224, 224)):
    """
    Preprocess the uploaded image for the skin lesion classification model.
    
    Args:
        image: PIL Image object or file path
        target_size: Tuple of (height, width) for resizing
        
    Returns:
        Preprocessed numpy array ready for model input
    """
    # Convert PIL Image to numpy array if needed
    if isinstance(image, Image.Image):
        img_array = np.array(image)
    else:
        # Handle file paths or bytes
        try:
            if isinstance(image, str):
                image = Image.open(image)
            elif isinstance(image, bytes) or isinstance(image, io.BytesIO):
                image = Image.open(io.BytesIO(image))
            img_array = np.array(image)
        except Exception as e:
            raise ValueError(f"Could not load image: {e}")
    
    # Convert grayscale to RGB if needed
    if len(img_array.shape) == 2:
        img_array = cv2.cvtColor(img_array, cv2.COLOR_GRAY2RGB)
    elif img_array.shape[2] == 4:  # RGBA
        img_array = cv2.cvtColor(img_array, cv2.COLOR_RGBA2RGB)
    
    # Resize image
    img_array = cv2.resize(img_array, target_size)
    
    # Apply preprocessing steps specific to skin lesions
    # 1. Color normalization - helps standardize colors across images
    img_array = color_normalize(img_array)
    
    # 2. Hair removal (simplified version)
    img_array = remove_hair(img_array)
    
    # 3. Contrast enhancement
    img_array = enhance_contrast(img_array)
    
    # 4. Standardize pixel values to [0, 1]
    img_array = img_array.astype('float32') / 255.0
    
    return img_array

def color_normalize(image):
    """
    Normalizes the color distribution of the image.
    """
    # Convert to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    
    # Normalize L channel
    l, a, b = cv2.split(lab)
    l_norm = cv2.normalize(l, None, 0, 255, cv2.NORM_MINMAX)
    
    # Merge channels
    lab_norm = cv2.merge([l_norm, a, b])
    
    # Convert back to RGB
    rgb_norm = cv2.cvtColor(lab_norm, cv2.COLOR_LAB2RGB)
    
    return rgb_norm

def remove_hair(image):
    """
    Simple hair removal technique using morphological operations.
    In a production system, a more sophisticated algorithm would be used.
    """
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Apply blackhat morphological operation
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, kernel)
    
    # Threshold the blackhat image
    _, mask = cv2.threshold(blackhat, 10, 255, cv2.THRESH_BINARY)
    
    # Invert the mask
    mask = cv2.bitwise_not(mask)
    
    # Create an output image
    result = image.copy()
    
    # Apply inpainting to remove hair
    for i in range(3):  # For each color channel
        result[:,:,i] = cv2.inpaint(image[:,:,i], mask, 3, cv2.INPAINT_TELEA)
    
    return result

def enhance_contrast(image):
    """
    Enhance the contrast of the image using CLAHE.
    """
    # Convert to LAB color space
    lab = cv2.cvtColor(image, cv2.COLOR_RGB2LAB)
    
    # Split the LAB image into different channels
    l, a, b = cv2.split(lab)
    
    # Apply CLAHE to L channel
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    l = clahe.apply(l)
    
    # Merge the channels back
    lab = cv2.merge([l, a, b])
    
    # Convert back to RGB
    rgb = cv2.cvtColor(lab, cv2.COLOR_LAB2RGB)
    
    return rgb
