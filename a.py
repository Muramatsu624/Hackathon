from transformers import BertJapaneseTokenizer
from transformers import BertModel
import torch
import numpy as np

import transformers
transformers.logging.set_verbosity_error()

pretrained = 'cl-tohoku/bert-base-japanese-whole-word-masking'
tokenizer = BertJapaneseTokenizer.from_pretrained(pretrained)