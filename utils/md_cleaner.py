import re

class MarkdownCleaner:
    def __init__(self):
        self.patterns = [
            # Заголовки (#)
            (re.compile(r'^#+\s+', re.MULTILINE), ''),
            
            # Жирный текст (**-**)
            (re.compile(r'\*\*(.*?)\*\*', re.DOTALL), r'\1'),
            
            # Курсив (*-*)
            (re.compile(r'\*(.*?)\*', re.DOTALL), r'\1'),
            
            # Подчеркнутый (__-__)
            (re.compile(r'__(.*?)__', re.DOTALL), r'\1'),
            
            # Зачеркнутый (~~-~~)
            (re.compile(r'~~(.*?)~~', re.DOTALL), r'\1'),
            
            # Inline код (`-`)
            (re.compile(r'`(.*?)`', re.DOTALL), r'\1'),
            
            # Блочный код (``` -- ```)
            (re.compile(r'```.*?```', re.DOTALL), ''),
        ]
    
    def clean(self, text): # очистка текста от markdown разметки, оставили самое важное
        if not text:
            return text
        
        result = text
        for pattern, replacement in self.patterns:
            result = pattern.sub(replacement, result)
        
        return result

cleaner = MarkdownCleaner()