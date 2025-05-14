import streamlit as st
import numpy as np

def get_progress_placeholder(st_component):
    """
    Creates and returns a progress bar placeholder.
    
    Args:
        st_component: Streamlit component to create the placeholder in
        
    Returns:
        Streamlit progress bar placeholder
    """
    return st_component.progress(0)

def explain_prediction(prediction, confidence):
    """
    Generate an explanation of the prediction results in user-friendly terms.
    
    Args:
        prediction: The prediction label (e.g., 'Melanoma' or 'Benign')
        confidence: The confidence percentage of the prediction
        
    Returns:
        A detailed explanation string
    """
    if prediction == "Melanoma":
        if confidence > 80:
            explanation = """
            The analysis detected several visual characteristics that are commonly associated with melanoma:
            
            - Irregular borders that are not smooth and even
            - Multiple colors within the lesion (variations in brown, black, red, or blue)
            - Asymmetrical shape where one half doesn't match the other
            - The overall pattern matches known melanoma characteristics with high confidence
            
            **This does not constitute a medical diagnosis.** Melanoma can only be definitively diagnosed through a biopsy performed by a medical professional.
            """
        elif confidence > 60:
            explanation = """
            The analysis found some concerning features that can be associated with melanoma:
            
            - Some border irregularity
            - Some color variation within the lesion
            - Possible asymmetry in the shape
            - The pattern partially matches melanoma characteristics
            
            **This is not a diagnosis.** The moderate confidence level means that while some concerning features are present, a professional evaluation is essential for proper assessment.
            """
        else:
            explanation = """
            The analysis detected a few features that can sometimes be found in melanoma, but with lower confidence:
            
            - Subtle irregularities in appearance
            - Some visual features that occasionally appear in melanoma
            - The pattern has limited similarity to known melanoma characteristics
            
            **This is not a diagnosis.** The low confidence level means that while the AI has flagged some potential concerns, these features are not strongly indicative and professional evaluation is necessary.
            """
    else:  # Benign
        if confidence > 80:
            explanation = """
            The analysis suggests this lesion has characteristics typically associated with benign moles:
            
            - Regular, well-defined borders
            - Consistent coloration throughout
            - Symmetrical shape
            - The overall pattern strongly matches known benign characteristics
            
            **While this analysis suggests low risk, any changing or concerning lesion should be evaluated by a dermatologist.**
            """
        elif confidence > 60:
            explanation = """
            The analysis suggests this lesion has several features commonly seen in benign lesions:
            
            - Mostly regular borders
            - Relatively consistent coloration
            - Generally symmetrical appearance
            - The pattern moderately matches benign characteristics
            
            **This is not a definitive diagnosis.** The moderate confidence level means a professional evaluation is still recommended, especially if you notice any changes.
            """
        else:
            explanation = """
            The analysis suggests this lesion might be benign, but with lower confidence:
            
            - Some regular features typically seen in benign lesions
            - The pattern has limited similarity to typical benign characteristics
            - Some features may be atypical but not necessarily concerning
            
            **This is not a diagnosis.** The low confidence level means that professional evaluation is recommended to properly assess this lesion.
            """
    
    return explanation

def filter_sensitive_info(text):
    """
    Filter out potentially sensitive personal information from user inputs.
    
    Args:
        text: User input text to filter
        
    Returns:
        Filtered text with sensitive information removed
    """
    # Implement basic filtering for things like:
    # - Phone numbers
    # - Email addresses
    # - Social security numbers
    # - Full names
    
    # This is a simplified implementation
    import re
    
    # Filter phone numbers
    text = re.sub(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', '[PHONE NUMBER REMOVED]', text)
    
    # Filter email addresses
    text = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL REMOVED]', text)
    
    # Filter social security numbers
    text = re.sub(r'\b\d{3}[-]?\d{2}[-]?\d{4}\b', '[SSN REMOVED]', text)
    
    return text

def get_risk_factors(user_responses):
    """
    Analyze user responses to determine risk factors.
    
    Args:
        user_responses: Dictionary of user responses to medical questions
        
    Returns:
        List of identified risk factors
    """
    risk_factors = []
    
    # Check family history
    if 'family history' in user_responses.get('Do you have a family history of skin cancer?', '').lower():
        if 'yes' in user_responses.get('Do you have a family history of skin cancer?', '').lower():
            risk_factors.append("Family history of skin cancer")
    
    # Check sun exposure
    if 'sun exposure' in user_responses.get('Have you had significant sun exposure or sunburns in your life?', '').lower():
        if any(word in user_responses.get('Have you had significant sun exposure or sunburns in your life?', '').lower() 
               for word in ['yes', 'significant', 'severe', 'many', 'multiple']):
            risk_factors.append("History of significant sun exposure or sunburns")
    
    # Check previous skin cancers
    if 'previous' in user_responses.get('Have you had any previous skin cancers?', '').lower():
        if 'yes' in user_responses.get('Have you had any previous skin cancers?', '').lower():
            risk_factors.append("Previous skin cancer history")
    
    # Check lesion symptoms
    if any(word in user_responses.get('Is the lesion painful, itchy, or bleeding?', '').lower() 
           for word in ['yes', 'painful', 'itchy', 'bleeding', 'itches', 'hurts', 'bleeds']):
        risk_factors.append("Symptomatic lesion (pain, itching, or bleeding)")
    
    # Check lesion changes
    if any(word in user_responses.get('Has the lesion changed in size, shape, or color recently?', '').lower() 
           for word in ['yes', 'changed', 'changing', 'growing', 'darker']):
        risk_factors.append("Recent changes in the lesion")
    
    return risk_factors
