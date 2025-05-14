import re
import random
from datetime import datetime

class ChatbotInterface:
    """
    A class to handle the chatbot interaction for the skin cancer prediction application.
    Manages conversations with users, collects information, and provides guidance.
    """
    
    def __init__(self):
        # Questions about the skin lesion and medical history
        self.medical_questions = [
            "How long have you noticed this skin lesion?",
            "Has the lesion changed in size, shape, or color recently?",
            "Do you have a family history of skin cancer?",
            "Have you had significant sun exposure or sunburns in your life?",
            "Is the lesion painful, itchy, or bleeding?",
            "Have you had any previous skin cancers?"
        ]
        self.current_question_idx = 0
        
        # Guidance messages for image capture
        self.image_guidance = [
            "Please ensure the skin lesion is centered in the image.",
            "Use natural lighting without flash if possible.",
            "Take the photo from about 10-15 cm (4-6 inches) away.",
            "Include a ruler or coin next to the lesion if possible to show its size.",
            "If possible, take multiple photos from different angles."
        ]
    
    def get_welcome_message(self):
        """Returns the initial welcome message for the user."""
        current_time = datetime.now().hour
        greeting = "Good morning" if 5 <= current_time < 12 else "Good afternoon" if 12 <= current_time < 18 else "Good evening"
        
        return f"{greeting}! I'm your Skin Assessment Assistant. I can help analyze images of skin lesions and provide guidance on next steps.\n\nI'm not a replacement for professional medical advice, but I can help you understand if a skin lesion might need attention from a dermatologist.\n\nWould you like me to guide you through uploading and analyzing an image?"
    
    def get_guidance_message(self):
        """Returns guidance on how to take and upload an image."""
        message = "Great! Here are some tips for taking a good photo of your skin lesion:\n\n"
        message += "\n".join([f"• {tip}" for tip in self.image_guidance])
        message += "\n\nWhen you're ready, please upload your image using the panel on the right. Would you like to proceed, or do you have any questions?"
        
        return message
    
    def get_medical_question(self):
        """Returns the next medical question to ask the user."""
        if self.current_question_idx < len(self.medical_questions):
            question = self.medical_questions[self.current_question_idx]
            self.current_question_idx += 1
            return question
        else:
            return "Thank you for providing that information. This will help with interpreting the results. Is there anything else you'd like to add about the lesion or your medical history?"
    
    def get_prediction_message(self, prediction, confidence):
        """Generates a message to deliver the prediction results to the user."""
        if prediction == "Melanoma":
            if confidence > 80:
                message = f"Based on the image analysis, there is a high likelihood ({confidence:.1f}%) that this lesion shows characteristics of melanoma, which is a serious form of skin cancer."
            elif confidence > 60:
                message = f"The analysis indicates a moderate to high likelihood ({confidence:.1f}%) that this lesion has features concerning for melanoma."
            else:
                message = f"The analysis shows some features that could be concerning ({confidence:.1f}% likelihood of melanoma), though the confidence is not extremely high."
                
            message += "\n\n**Important:** This result suggests you should consult with a dermatologist as soon as possible for a professional evaluation."
        else:  # Benign
            if confidence > 80:
                message = f"The analysis suggests with high confidence ({confidence:.1f}%) that this lesion appears to be benign (non-cancerous)."
            elif confidence > 60:
                message = f"The analysis indicates with moderate confidence ({confidence:.1f}%) that this lesion is likely benign."
            else:
                message = f"The analysis suggests this might be benign, but the confidence level is lower ({confidence:.1f}%). It's still advisable to have it checked."
                
            message += "\n\nEven with a low-risk result, it's always good practice to monitor the lesion for any changes and consider a dermatologist visit if you have concerns."
        
        message += "\n\nWould you like me to explain what features the system looks for in analyzing skin lesions?"
        
        return message
    
    def process_message(self, message, current_stage, user_responses, prediction=None, confidence=None):
        """
        Process user message based on the current conversation stage
        Returns a tuple of (response, next_stage)
        """
        message = message.strip().lower()
        
        # Process based on current stage
        if current_stage == "introduction":
            # User responded to welcome message
            if any(word in message for word in ["yes", "sure", "okay", "start", "guide", "help"]):
                return self.get_guidance_message(), "guidance"
            else:
                return "I understand you may have questions. This application can analyze images of skin lesions to help determine if they might be concerning. Would you like me to guide you through the process?", "introduction"
                
        elif current_stage == "guidance":
            # User responded to guidance on image upload
            if any(word in message for word in ["yes", "sure", "okay", "proceed", "continue", "ready"]):
                return self.get_medical_question(), "medical_history"
            elif "question" in message or "?" in message:
                return "I'm happy to answer questions. This tool helps identify potential skin cancer concerns, but it's not a replacement for professional medical advice. Please upload a clear image of your skin lesion using the panel on the right. Would you like to proceed with some medical history questions while you prepare your image?", "guidance"
            else:
                return "When you're ready, please upload an image using the panel on the right. In the meantime, I'd like to ask you a few questions that might help with the assessment. " + self.get_medical_question(), "medical_history"
                
        elif current_stage == "medical_history":
            # Store user's response to medical question
            question_idx = self.current_question_idx - 1
            if question_idx < len(self.medical_questions):
                user_responses[self.medical_questions[question_idx]] = message
            
            # Get next question or move to next stage
            if self.current_question_idx < len(self.medical_questions):
                return self.get_medical_question(), "medical_history"
            else:
                return "Thank you for providing that information. Please upload an image of the skin lesion if you haven't already, and I'll analyze it for you.", "waiting_for_image"
                
        elif current_stage == "waiting_for_image":
            # User is supposed to upload an image at this point
            return "I'm waiting for you to upload an image of the skin lesion. Please use the upload panel on the right side of the screen.", "waiting_for_image"
                
        elif current_stage == "post_prediction":
            # User interaction after prediction is made
            if prediction == "Melanoma":
                if any(word in message for word in ["explain", "features", "why", "how", "what"]):
                    return "The system analyzes visual characteristics including: asymmetry (irregular shape), border irregularity, color variations, diameter (larger lesions are more concerning), and evolving features. In melanomas, we often see irregular borders, multiple colors, and asymmetric patterns. Based on these features, I recommend consulting with a dermatologist who can perform a proper examination. Would you like me to explain what steps you should take next?", "post_prediction"
                elif any(word in message for word in ["next", "steps", "do", "should"]):
                    return "Given the results, I recommend: 1) Make an appointment with a dermatologist as soon as possible, 2) Mention that you used an AI tool that suggested possible melanoma concerns, 3) Don't panic - further testing is needed for a definitive diagnosis, 4) Until your appointment, protect the area from sun exposure. Is there anything specific about the process you'd like to know?", "post_prediction"
                else:
                    return "I understand this result may be concerning. Remember that this is a preliminary screening tool, not a diagnosis. A dermatologist can perform additional tests like dermoscopy or a biopsy if needed. Do you have any specific questions about the results or next steps?", "post_prediction"
            else:  # Benign
                if any(word in message for word in ["explain", "features", "why", "how", "what"]):
                    return "The system analyzes visual characteristics including: symmetry, regular borders, uniform color, smaller size, and stable appearance over time. Benign moles typically have more regular, symmetrical patterns with consistent coloration. However, it's still good practice to monitor any skin lesions for changes. Would you like advice on monitoring your skin health?", "post_prediction"
                elif any(word in message for word in ["next", "steps", "do", "should", "monitor"]):
                    return "Even with a benign result, I recommend: 1) Take photos every 3-6 months to track any changes, 2) Use the 'ABCDE rule' to monitor: Asymmetry, Border irregularity, Color changes, Diameter increases, or Evolution of any kind, 3) Practice sun protection with sunscreen, protective clothing, and avoiding peak UV hours, 4) Consider a routine skin check with a dermatologist, especially if you have risk factors. Would you like more information on any of these points?", "post_prediction"
                else:
                    return "I'm glad the results suggest a benign lesion. While this is reassuring, it's always good practice to monitor your skin for changes and practice sun protection. Is there anything specific about skin health monitoring you'd like to know more about?", "post_prediction"
                    
        else:
            # Default response if stage is not recognized
            return "I'm here to help analyze skin lesions and provide guidance. Would you like to upload an image or ask questions about the process?", 
current_stage