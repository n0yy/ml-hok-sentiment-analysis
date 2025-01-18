import pandas as pd
import nltk
nltk.download('stopwords')
nltk.download('punkt_tab')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from string import punctuation
from tqdm.auto import tqdm

from typing import List, Union

class Preprocessor:
    def __init__(self):
        self.stemmer = StemmerFactory().create_stemmer()
        self.tokenizer = word_tokenize
        self.stopwords = list(stopwords.words('indonesian') + list(punctuation))

    def lowercasing(self, text: str) -> str:
        """
        Converts the input text to lowercase with error handling.

        Args:
            text: The input text to be converted to lowercase.

        Returns:
            The lowercase version of the input text. If the input is not a string and is NaN, returns None.
        """

        if not isinstance(text, str):
            if pd.isna(text):
                return None
            text = str(text)
        return text.lower()
    
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