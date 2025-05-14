def get_example_images():
    """
    Returns a list of tuples with (label, image URL) for example skin lesion images.
    These are educational examples from publicly available medical datasets.
    
    Returns:
        List of tuples with (label, image URL)
    """
    # Using publicly available medical image URLs for educational purposes
    return [
        ("Typical Benign Nevus", "https://www.isic-archive.com/api/v1/image/5436e3abbae478396759f0cf/thumbnail"),
        ("Atypical Nevus", "https://www.isic-archive.com/api/v1/image/5436e3acbae478396759f0d1/thumbnail"),
        ("Melanoma Example", "https://www.isic-archive.com/api/v1/image/5436e3adbae478396759f0dd/thumbnail"),
        ("Early Melanoma", "https://www.isic-archive.com/api/v1/image/5436e3adbae478396759f0df/thumbnail")
    ]

def get_educational_image_examples():
    """
    Returns a dictionary of educational image examples with descriptions.
    
    Returns:
        Dictionary with image types as keys and descriptions as values
    """
    return {
        "benign_nevus": {
            "title": "Benign Nevus (Mole)",
            "description": "Common moles are usually round or oval, with a smooth edge and consistent color. They're typically smaller than 6mm (pencil eraser size).",
            "image_url": "https://www.isic-archive.com/api/v1/image/5436e3abbae478396759f0cf/thumbnail"
        },
        "dysplastic_nevus": {
            "title": "Dysplastic Nevus (Atypical Mole)",
            "description": "Atypical moles may be larger than common moles and have irregular or indistinct borders, varying colors, and asymmetrical shapes.",
            "image_url": "https://www.isic-archive.com/api/v1/image/5436e3acbae478396759f0d1/thumbnail"
        },
        "melanoma": {
            "title": "Melanoma",
            "description": "Melanomas often show the ABCDE warning signs: Asymmetry, Border irregularity, Color variation, Diameter >6mm, and Evolution (changing over time).",
            "image_url": "https://www.isic-archive.com/api/v1/image/5436e3adbae478396759f0dd/thumbnail"
        },
        "early_melanoma": {
            "title": "Early Melanoma",
            "description": "Early melanomas may be smaller but still show irregular borders, uneven coloration, or asymmetry. Early detection greatly improves treatment outcomes.",
            "image_url": "https://www.isic-archive.com/api/v1/image/5436e3adbae478396759f0df/thumbnail"
        }
    }

def get_abcde_examples():
    """
    Returns examples illustrating the ABCDE rule for melanoma detection.
    
    Returns:
        Dictionary with ABCDE criteria as keys and examples as values
    """
    return {
        "asymmetry": {
            "title": "A - Asymmetry",
            "description": "Melanomas are typically asymmetrical: if you draw a line through the middle, the two halves won't match.",
            "benign_example": "https://www.skincancer.org/wp-content/uploads/20190701-ABCDE-MOLE-GUIDE-BENIGN-ASYMMETRY.jpg",
            "malignant_example": "https://www.skincancer.org/wp-content/uploads/20190701-ABCDE-MOLE-GUIDE-MALIGNANT-ASYMMETRY.jpg"
        },
        "border": {
            "title": "B - Border",
            "description": "Borders of melanomas tend to be uneven, ragged, notched, or blurred.",
            "benign_example": "https://www.skincancer.org/wp-content/uploads/20190701-ABCDE-MOLE-GUIDE-BENIGN-BORDER.jpg",
            "malignant_example": "https://www.skincancer.org/wp-content/uploads/20190701-ABCDE-MOLE-GUIDE-MALIGNANT-BORDER.jpg"
        },
        "color": {
            "title": "C - Color",
            "description": "Melanomas often contain multiple colors or shades (black, brown, tan, red, white, or blue).",
            "benign_example": "https://www.skincancer.org/wp-content/uploads/20190701-ABCDE-MOLE-GUIDE-BENIGN-COLOR.jpg",
            "malignant_example": "https://www.skincancer.org/wp-content/uploads/20190701-ABCDE-MOLE-GUIDE-MALIGNANT-COLOR.jpg"
        },
        "diameter": {
            "title": "D - Diameter",
            "description": "Melanomas are often larger than 6mm (about the size of a pencil eraser), although they can be smaller.",
            "benign_example": "https://www.skincancer.org/wp-content/uploads/20190701-ABCDE-MOLE-GUIDE-BENIGN-DIAMETER.jpg",
            "malignant_example": "https://www.skincancer.org/wp-content/uploads/20190701-ABCDE-MOLE-GUIDE-MALIGNANT-DIAMETER.jpg"
        },
        "evolving": {
            "title": "E - Evolving",
            "description": "Melanomas often change over time (size, shape, color, elevation) or develop new symptoms (itching, bleeding).",
            "benign_example": "https://www.skincancer.org/wp-content/uploads/20190701-ABCDE-MOLE-GUIDE-BENIGN-EVOLVING.jpg",
            "malignant_example": "https://www.skincancer.org/wp-content/uploads/20190701-ABCDE-MOLE-GUIDE-MALIGNANT-EVOLVING.jpg"
        }
    }