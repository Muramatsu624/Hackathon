from transformers import BertJapaneseTokenizer
from transformers import BertModel
import torch
import numpy as np

import transformers
transformers.logging.set_verbosity_error()

# 単語のトークン化
def tokenize(word, tokenizer, max_len):
    encoded_word = tokenizer(
        word,
        padding = "max_length",
        max_length = max_len,
        truncation = True
    )
    return encoded_word

# トークンのベクトル化
def embedding(word, pretrained):
    input_ids = torch.tensor(word["input_ids"], dtype = torch.int32)
    attention_mask = torch.tensor(word["attention_mask"], dtype = torch.int32)
    token_type_ids = torch.tensor(word["token_type_ids"], dtype = torch.int32)

    input_ids = input_ids.unsqueeze(dim=0)
    attention_mask = attention_mask.unsqueeze(dim=0)
    token_type_ids = token_type_ids.unsqueeze(dim=0)

    bert = BertModel.from_pretrained(pretrained)
    embed = bert(input_ids=input_ids, attention_mask=attention_mask, token_type_ids=token_type_ids, output_attentions=True)

    return embed["last_hidden_state"][:, 0, :].to('cpu').detach().numpy().copy()

# コサイン類似度を計算
def cos_sim(v1, v2):
  return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

# 歌詞とお題から類似度を評価
def evaluate(lyrics1, lyrics2 ,theme):
    #パラメータの設定
    MAX_LENGTH = 512
    lyrics1_list = lyrics1.split(" ")
    lyrics2_list = lyrics1.split(" ")
    
    #Tokenizerの設定
    pretrained = 'cl-tohoku/bert-base-japanese-whole-word-masking'
    tokenizer = BertJapaneseTokenizer.from_pretrained(pretrained)

    # 単語のトークン化
    encoded_lyrics1 = tokenize(lyrics1, tokenizer, MAX_LENGTH)
    encoded_lyrics2 = tokenize(lyrics2, tokenizer, MAX_LENGTH)
    encoded_theme = tokenize(theme, tokenizer, MAX_LENGTH)

    # トークンのベクトル化
    embed_lyrics1 = embedding(encoded_lyrics1, pretrained)
    embed_lyrics2 = embedding(encoded_lyrics2, pretrained)
    embed_theme = embedding(encoded_theme, pretrained)

    # print(type(embed_theme))    # <class 'numpy.ndarray'>
    # print(embed_theme.shape)    # (1, 768)

    #類似度の計算
    # 0～2の範囲で計算
    lyrics1_point = cos_sim(embed_lyrics1[0], embed_theme[0]) + 1       
    lyrics2_point = cos_sim(embed_lyrics2[0], embed_theme[0]) + 1
    # 0～100の範囲に変換
    lyrics1_point *= 50       
    lyrics2_point *= 50
    # print(type(lyrics1_point))  # <class 'numpy.float32'>
    # print(lyrics1_point)        # 0.8112952

    # 結果の出力
    print("１曲目の歌詞")
    print(lyrics1)
    print("２曲目の歌詞")
    print(lyrics2)
    print("お題")
    print(theme)
    print("１曲目の点数：", lyrics1_point)
    print("２曲目の点数：", lyrics2_point)


    #追記--------------------------------------
    return lyrics1_point, lyrics2_point

    #-----------------------------------------

