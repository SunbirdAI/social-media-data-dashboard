from pathlib import Path
from string import punctuation
from nltk.corpus import stopwords

ROOT = Path(__file__).resolve().parent
DATA_FOLDER = ROOT.joinpath("data")
STOP_WORDS = set(stopwords.words('english') + list(punctuation) + ['AT_USER', 'URL'])
