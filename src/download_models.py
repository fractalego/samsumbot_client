import nltk
import transformers

from src.dense_retriever import DenseRetriever
from src.toxicity_detector import ToxicityDetector


if __name__ == "__main__":
    _tokenizer = transformers.AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
    _retriever = DenseRetriever("msmarco-distilbert-base-v3")
    _toxic_detector = ToxicityDetector("original")
    nltk.download("punkt")
    nltk.download("averaged_perceptron_tagger")
