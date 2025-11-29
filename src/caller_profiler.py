
from src.database import Database
import logging

logger = logging.getLogger(__name__)


def get_caller_profile(phone_number):
    """
    Get profile info for a caller to customize your response.
    If caller not in database, return default profile.
    """
    try:
        db = Database()
        profile = db.get_caller_profile(phone_number)
        db.close()
        
        if not profile:
            logger.info(f"New caller: {phone_number}")
            return {
                'phone_number': phone_number,
                'name': 'Unknown Caller',
                'relationship': 'unknown',
                'tone': 'neutral',
                'usual_topics': None
            }
        
        return profile
    except Exception as e:
        logger.error(f"Error getting caller profile: {str(e)}")
        return {
            'phone_number': phone_number,
            'name': 'Caller',
            'relationship': 'unknown',
            'tone': 'neutral',
            'usual_topics': None
        }


def identify_caller_type(relationship):
    """Map relationship to communication style"""
    styles = {
        'friend': {'tone': 'casual', 'detail_level': 'low'},
        'family': {'tone': 'warm', 'detail_level': 'medium'},
        'professor': {'tone': 'formal', 'detail_level': 'high'},
        'recruiter': {'tone': 'professional', 'detail_level': 'high'},
        'teammate': {'tone': 'professional', 'detail_level': 'medium'},
        'unknown': {'tone': 'polite', 'detail_level': 'low'}
    }
    return styles.get(relationship, styles['unknown'])