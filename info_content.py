def get_app_description():
    """
    Returns a description of the application for the sidebar.
    """
    return """
    This application uses computer vision and artificial intelligence to analyze images of skin lesions
    and assess the likelihood of skin cancer, specifically melanoma.
    
    ### How It Works
    1. Upload a clear image of the skin lesion
    2. The system will analyze visual patterns and features
    3. A chatbot will guide you through the process and collect relevant information
    4. You'll receive an assessment with recommended next steps
    
    ### Important Note
    This tool is designed for educational purposes and preliminary screening only. It is not a replacement for professional medical advice or diagnosis from a qualified dermatologist.
    """

def get_disclaimer_text():
    """
    Returns the disclaimer text for the application.
    """
    return """
    This application is not a diagnostic tool and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of a qualified health provider with any questions you may have regarding a medical condition.
    
    The predictions provided are based on machine learning algorithms that have inherent limitations. The system has not been FDA-approved for clinical use, and all results should be interpreted by healthcare professionals.
    
    Seek immediate medical attention if you believe you may have a medical emergency.
    """

def get_educational_content():
    """
    Returns educational content about skin cancer.
    """
    return """
    ### Skin Cancer Facts
    
    **Melanoma** is the most dangerous form of skin cancer. It develops in the cells that produce melanin, the pigment that gives skin its color.
    
    **The ABCDE Rule** helps identify warning signs:
    - **A**symmetry: One half doesn't match the other
    - **B**order: Irregular, ragged, notched, or blurred edges
    - **C**olor: Various colors or shades within the same mole
    - **D**iameter: Larger than 6mm (about the size of a pencil eraser)
    - **E**volving: Changing in size, shape, color, or elevation
    
    **Risk Factors**:
    - Excessive sun exposure
    - History of sunburns
    - Family history of skin cancer
    - Fair skin, light hair, freckles
    - Multiple or unusual moles
    
    ### Prevention
    - Apply sunscreen (SPF 30+) regularly
    - Wear protective clothing
    - Seek shade during peak sun hours
    - Perform regular skin self-examinations
    - Visit a dermatologist annually for skin checks
    """

def get_next_steps(prediction):
    """
    Returns recommended next steps based on the prediction.
    
    Args:
        prediction: The prediction label (e.g., 'Melanoma' or 'Benign')
        
    Returns:
        A string with recommended next steps
    """
    if prediction == "Melanoma":
        return """
        ### Recommended Next Steps
        
        1. **Consult a dermatologist promptly** - Schedule an appointment within the next 1-2 weeks.
        
        2. **Prepare for your appointment**:
           - Take additional photos of the lesion for comparison
           - Note any changes you've observed
           - Bring a list of any symptoms you've experienced
           - Download or save the results from this analysis to share
        
        3. **While waiting for your appointment**:
           - Avoid irritating the area
           - Protect the area from sun exposure
           - Do not attempt to remove or treat the lesion yourself
        
        4. **At your appointment**, the dermatologist may:
           - Examine the lesion with a dermoscope
           - Take a biopsy for laboratory analysis
           - Recommend additional tests or imaging
        
        Remember that early detection and treatment significantly improve outcomes for melanoma.
        """
    else:  # Benign
        return """
        ### Recommended Next Steps
        
        1. **Regular monitoring** - Take photos every 3 months to track any changes.
        
        2. **Practice the ABCDE rule** to monitor for:
           - Asymmetry
           - Border irregularity
           - Color changes
           - Diameter increases
           - Evolution of any kind
        
        3. **Routine dermatology check-up** - Consider scheduling a skin examination as part of your regular health maintenance, especially if you have:
           - A family history of skin cancer
           - Previous skin cancers
           - Multiple moles
           - Fair skin or history of sunburns
        
        4. **Sun protection**:
           - Use broad-spectrum sunscreen (SPF 30+)
           - Wear protective clothing
           - Seek shade during peak UV hours (10am-4pm)
        
        Even with a likely benign result, any concerning changes should prompt a dermatologist visit.
        """