"""
Explanation Translation Module

Handles translation of quiz explanations with hybrid approach:
1. Use pre-translated explanations from YAML if available
2. Fall back to automatic translation if needed
"""

import functools
from typing import Optional
try:
    from googletrans import Translator
    GOOGLETRANS_AVAILABLE = True
except ImportError:
    GOOGLETRANS_AVAILABLE = False
    print("Warning: googletrans not available. Explanation translation will be limited.")


class ExplanationTranslator:
    """Handles explanation translation with caching"""
    
    def __init__(self):
        self.translator = Translator() if GOOGLETRANS_AVAILABLE else None
        self._translation_cache = {}
    
    @functools.lru_cache(maxsize=128)
    def translate_text(self, text: str, target_language: str) -> str:
        """
        Translate text to target language with caching
        
        Args:
            text: Text to translate
            target_language: Target language code ('zh_TW', 'zh_CN', 'en')
            
        Returns:
            Translated text or original if translation fails
        """
        if not self.translator or not text:
            return text
        
        # Create cache key
        cache_key = f"{text}_{target_language}"
        if cache_key in self._translation_cache:
            return self._translation_cache[cache_key]
        
        try:
            # Map language codes to Google Translate accepted codes
            lang_map = {
                'zh_TW': 'zh-tw',  # Traditional Chinese
                'zh_CN': 'zh-cn',  # Simplified Chinese  
                'zh': 'zh-tw',     # Default Chinese to Traditional
                'en': 'en'         # English
            }
            
            target_lang = lang_map.get(target_language, None)
            
            # If target language is English or not supported, return original
            if target_lang == 'en' or target_lang is None:
                return text
            
            # Validate that we have a supported target language
            if target_lang not in ['zh-tw', 'zh-cn']:
                print(f"Unsupported target language: {target_language}, returning original text")
                return text
            
            result = self.translator.translate(text, dest=target_lang)
            translated_text = result.text
            
            # Cache the result
            self._translation_cache[cache_key] = translated_text
            return translated_text
            
        except Exception as e:
            print(f"Translation error for '{target_language}': {e}")
            print(f"Returning original text: {text[:50]}...")
            return text  # Return original text if translation fails
    
    def get_explanation(self, question_obj, language: str) -> str:
        """
        Get explanation in the specified language
        
        Args:
            question_obj: Question object with explanation fields
            language: Target language code
            
        Returns:
            Explanation in target language
        """
        # Priority 1: Check for pre-translated explanation
        explanation_key = f"explanation_{language}"
        if hasattr(question_obj, explanation_key):
            pre_translated = getattr(question_obj, explanation_key)
            if pre_translated:
                return pre_translated
        
        # Priority 2: Check for alternative language formats
        if language == 'zh_TW':
            # Try different Chinese variants
            for alt_key in ['explanation_zh_CN', 'explanation_zh']:
                if hasattr(question_obj, alt_key):
                    alt_explanation = getattr(question_obj, alt_key)
                    if alt_explanation:
                        return alt_explanation
        
        # Priority 3: Use original explanation (usually English)
        original_explanation = getattr(question_obj, 'explanation', '')
        if not original_explanation:
            return ''
        
        # Priority 4: Auto-translate if target is not English
        if language != 'en' and GOOGLETRANS_AVAILABLE:
            return self.translate_text(original_explanation, language)
        
        # Fallback: Return original explanation
        return original_explanation


# Global translator instance
_translator_instance = None

def get_translator() -> ExplanationTranslator:
    """Get global translator instance (singleton pattern)"""
    global _translator_instance
    if _translator_instance is None:
        _translator_instance = ExplanationTranslator()
    return _translator_instance


def get_translated_explanation(question_obj, language: str) -> str:
    """
    Convenience function to get translated explanation
    
    Args:
        question_obj: Question object
        language: Target language code
        
    Returns:
        Explanation in target language
    """
    translator = get_translator()
    return translator.get_explanation(question_obj, language)


# Manual translation dictionary for common educational terms
EDUCATIONAL_TERMS = {
    'en': {
        'grammar': 'grammar',
        'spelling': 'spelling',
        'subject-verb agreement': 'subject-verb agreement',
        'pronoun': 'pronoun',
        'adjective': 'adjective',
        'correct': 'correct',
        'incorrect': 'incorrect',
    },
    'zh_TW': {
        'grammar': '語法',
        'spelling': '拼字',
        'subject-verb agreement': '主詞動詞一致性',
        'pronoun': '代名詞',
        'adjective': '形容詞',
        'correct': '正確',
        'incorrect': '錯誤',
    }
}

def enhance_explanation_with_terms(explanation: str, language: str) -> str:
    """
    Enhance explanation by replacing key educational terms
    
    Args:
        explanation: Original explanation
        language: Target language
        
    Returns:
        Enhanced explanation with better terminology
    """
    if language not in EDUCATIONAL_TERMS:
        return explanation
    
    enhanced = explanation
    terms = EDUCATIONAL_TERMS[language]
    
    # Replace common terms (case-insensitive)
    for en_term, translated_term in terms.items():
        if language != 'en':
            # Replace English terms with translated ones
            import re
            pattern = re.compile(re.escape(en_term), re.IGNORECASE)
            enhanced = pattern.sub(translated_term, enhanced)
    
    return enhanced
