import pandas as pd
import re
import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from string import punctuation

from typing import List, Union, Optional

class Preprocessor:
    def __init__(self):
        self.stemmer = StemmerFactory().create_stemmer()
        self.tokenizer = word_tokenize
        self.stopwords = list(stopwords.words('indonesian') + list(punctuation))

    def lowercasing(self, text: str) -> Optional[str]:
        """
        Converts the input text to lowercase and cleans special characters.

        This function:
        1. Handles non-string inputs and NaN values
        2. Removes emojis and emoticons
        3. Removes HTML tags
        4. Removes special characters while preserving valid punctuation
        5. Converts text to lowercase

        Args:
            text: Input text to be processed

        Returns:
            Optional[str]: Processed lowercase text, or None if input is NaN/None

        Examples:
            >>> preprocessor.lowercasing("Hello World! 😊 <p>Test</p>")
            'hello world test'
            >>> preprocessor.lowercasing(None)
            None
        """
        try:
            # Handle None and NaN values
            if pd.isna(text):
                return None

            # Convert to string if not already
            if not isinstance(text, str):
                text = str(text)

            # Remove emojis and emoticons
            # This pattern covers both Unicode emojis and ASCII-style emoticons
            emoji_pattern = re.compile("["
                u"\U0001F600-\U0001F64F"  # emoticons
                u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                u"\U0001F680-\U0001F6FF"  # transport & map symbols
                u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                u"\U00002702-\U000027B0"  # dingbats
                u"\U000024C2-\U0001F251"  # enclosed characters
                "]+|"
                "[:;=][-']?[)(/\\|dpP]"   # ASCII emoticons
            )
            text = emoji_pattern.sub('', text)

            # Remove HTML tags
            text = re.sub(r'<[^>]+>', '', text)

            # Remove special characters but preserve valid punctuation
            # This keeps spaces between words and removes other special characters
            text = re.sub(r'[^\w\s\.]', ' ', text)
            
            # Remove extra whitespace
            text = ' '.join(text.split())

            return text.lower()
        except Exception as e:
            print(f"Error in lowercasing: {str(e)}")
            return None
        
    def stemming(self, text: str) -> str:
        """
        Performs stemming on the input text with error handling.

        Args:
            text: The input text to be stemmed.

        Returns:
            The stemmed version of the input text. If the input is not a string and is NaN, returns None.
        """
        if not text:
            return ""
        
        try:
            return self.stemmer.stem(text)
        except Exception as e:
            print(f"Warning: Error pada stemming '{text[:50]}...': {str(e)}")
            return text
        
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenizes the input text into a list of words with error handling.

        Args:
            text: The input text to be tokenized.

        Returns:
            A list of words from the input text. If the input is not a string and is NaN, returns an empty list. If an error occurs during tokenization, splits the input by whitespace instead.
        """
        if not text:
            return []
        
        try:
            return self.tokenizer(text)
        except Exception as e:
            print(f"Warning: Error pada tokenizing '{text[:50]}...': {str(e)}")
            return text.split()
        
    def stopwords_removal(self, tokens: List[str]) -> List[str]:
        """
        Removes stopwords from the input tokens with error handling.

        Args:
            tokens: The input list of tokens to be filtered.

        Returns:
            A list of tokens with stopwords removed. If the input is empty, returns an empty list. If an error occurs during removal, returns the original input list.
        """
        if not tokens:
            return []
        
        try:
            return [token for token in tokens if token not in self.stopwords]
        except Exception as e:
            print(f"Warning: Error pada stopwords removal '{tokens[:50]}...': {str(e)}")
            return tokens
        
    def fit(self, text: str, concate: bool = False) -> Union[List[str], str]:
        """
        Performs the entire preprocessing pipeline on the input text with error handling.

        Args:
            text: The input text to be preprocessed.
            concate: If True, returns the preprocessed text as a string. If False, returns the preprocessed text as a list of strings.

        Returns:
            The preprocessed version of the input text. If the input is not a string and is NaN, returns an empty string or an empty list, depending on the value of concate. If an error occurs during preprocessing, returns an empty string or an empty list, depending on the value of concate.
        """
        try:
            if pd.isna(text):
                return "" if concate else []
            
            X = self.lowercasing(str(text))
            X = self.tokenize(X)
            X = self.stopwords_removal(X)
            
            if concate:
                X = " ".join(X) if X else ""
            
            return X
        except Exception as e:
            print(f"Warning: Error pada preprocessing '{str(text)[:50]}...': {str(e)}")
            return "" if concate else []