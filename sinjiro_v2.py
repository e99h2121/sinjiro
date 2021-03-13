#!python3.8

import random
import sqlite3
conn = sqlite3.connect("wnjpn.db")

word = input("どうぞ、好きな言葉を入力してください: ")

# 特定の単語を入力とした時に、類義語を検索する関数
# Wordnet http://compling.hss.ntu.edu.sg/wnja/ のwnjpn.dbを利用

# 日本語ワードネット 2009-2011 NICT, 2012-2015 Francis Bond and 2016-2017 Francis Bond, Takayuki Kuribayashi
# linked to http://compling.hss.ntu.edu.sg/wnja/index.ja.html

def SearchSimilarWords(word):

    # 問い合わせしたい単語がWordnetに存在するか確認する
    cur = conn.execute(f"select wordid from word where lemma='{word}'")
    word_id = 99999999  #temp 
    for row in cur:
        word_id = row[0]

    # Wordnetに存在する語であるかの判定
    if word_id==99999999:
        print(f"「{word}」は、Wordnetに存在しない単語です。")
        return
    else:
        print(f"【「{word}」の類似語はね、以下ですよ】\n")

    # 入力された単語を含む概念を検索する
    cur = conn.execute(f"select synset from sense where wordid='{word_id}'")
    synsets = []
    for row in cur:
        synsets.append(row[0])

    # 概念に含まれる単語を検索して画面出力する
    no = 1
    l_empty = []
    for synset in synsets:
        cur1 = conn.execute(f"select name from synset where synset='{synset}'")
        for row1 in cur1:
            print("%sつめの概念 : %s" %(no, row1[0]))
        cur2 = conn.execute("select def from synset_def where (synset='%s' and lang='jpn')" % synset)
        sub_no = 1
        for row2 in cur2:
            print("意味%s : %s" %(sub_no, row2[0]))
            # 対象に追加
            l_empty.append(row2[0])
            sub_no += 1
        cur3 = conn.execute(f"select wordid from sense where (synset='{synset}' and wordid!={word_id})")
        sub_no = 1
        for row3 in cur3:
            target_word_id = row3[0]
            cur3_1 = conn.execute(f"select lemma from word where wordid={target_word_id}")
            for row3_1 in cur3_1:
                print("類義語%s : %s" % (sub_no, row3_1[0]))
                # 対象に追加
                l_empty.append(row3_1[0])
                sub_no += 1
        print("\n")
        no += 1
    
    answer = random.choice(l_empty)
    l_phrase = []
    l_phrase.append(f"私はね、{word} とはですね、言ってみればもはや {answer} だと思うんですよ。")
    l_phrase.append(f"{word} ってことはですよ、{answer} とも考えられるということですよ。")
    l_phrase.append(f"{word} って、もう {answer} ですよね。")
    phrase = random.choice(l_phrase)
    print(phrase)

SearchSimilarWords(word)
