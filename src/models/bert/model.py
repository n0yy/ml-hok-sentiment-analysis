import pandas as pd
from tqdm.auto import tqdm
from dataclasses import dataclass
from functools import lru_cache
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
from datasets import Dataset
from typing import Dict, Optional

@dataclass
class SentimentModelConfig:
    model_id: str = "mdhugol/indonesia-bert-sentiment-classification"
    labels: Dict[str, str] = None

    def __post_init__(self):
        if self.labels is None:
            self.labels = {
                "LABEL_0": "positif",
                "LABEL_1": "netral",
                "LABEL_2": "negatif"
            }

class IndoBERTForSentimentAnalysis:
    def __init__(self, config: Optional[SentimentModelConfig] = None):
        self.config = config or SentimentModelConfig()
        self._initialize_model()

    def _initialize_model(self) -> None:
        try:
            self.model = AutoModelForSequenceClassification.from_pretrained(self.config.model_id)
            self.tokenizer = AutoTokenizer.from_pretrained(self.config.model_id)
            self.sentiment_pipe = pipeline(
                "sentiment-analysis",
                model=self.model,
                tokenizer=self.tokenizer
            )
        except Exception as e:
            raise RuntimeError(f"Gagal memuat model IndoBERT: {str(e)}")
        
    @lru_cache
    def analyze(self, text: str) -> str:
        if not isinstance(text, str):
            if pd.isna(text):
                return "netral"
            text = str(text)
        
        text = text.strip()
        if not text:
            return "netral"
        
        try:
            result = self.sentiment_pipe(text)
            return self.config.labels[result[0]["label"]]
        except Exception as e:
            return "netral"
        
    def analyze_dataframe(self, df: pd.DataFrame, X: str, y: str = "sentiment", batch_size: int = 32) -> pd.DataFrame:
        """Menganalisis sentimen teks dalam kolom X dari DataFrame df dan mengembalikan DataFrame yang sama dengan kolom y yang berisi sentimen.

        Args:
            df (pd.DataFrame): DataFrame yang berisi teks yang ingin dianalisis.
            X (str): Nama kolom yang berisi teks.
            y (str, optional): Nama kolom yang akan dibuat untuk menyimpan sentimen. Defaults to "sentiment".
            batch_size (int, optional): Ukuran batch untuk pengolahan sentimen. Defaults to 32.

        Returns:
            pd.DataFrame: DataFrame yang sama dengan kolom y yang berisi sentimen.
        """
        if X not in df.columns:
            raise ValueError(f"Kolom '{X}' tidak ditemukan dalam DataFrame")

        # Pastikan kolom dinamai 'text' agar sesuai dengan pipeline
        dataset = Dataset.from_pandas(df[[X]].rename(columns={X: "text"}).astype(str))

        # Debugging tambahan untuk memeriksa input
        print("Sample input data:", dataset[0])

        # Inisialisasi tqdm
        pbar = tqdm(total=len(dataset), desc="Processing Sentiments", unit="text")

        def batch_process(examples):
            texts = examples["text"]
            # Pastikan input berupa list string
            if not all(isinstance(text, str) for text in texts):
                raise ValueError("Semua input dalam batch harus berupa string.")
            results = self.sentiment_pipe(texts, batch_size=batch_size)
            sentiments = [self.config.labels[result["label"]] for result in results]
            pbar.update(len(texts))  # Update progres
            return {"sentiments": sentiments}

        # Proses data dalam batch
        result = dataset.map(batch_process, batched=True, batch_size=batch_size)

        # Tutup tqdm
        pbar.close()

        # Tambahkan hasil ke DataFrame
        df[y] = result["sentiments"]
        return df

