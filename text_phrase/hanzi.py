import re

re_han_internal = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&\._]+)")


import jieba.posseg as psg

def get_part_of_speech_taging(sentence, HMM = True):
   """
   词性标注
   Params:
      HMM=False: 非 HMM 词性标注
      HMM=True: HMM 词性标注
   """
   segment_list = psg.cut(sentence, HMM)
   tagged_sentence = " ".join([f"{w}/{t}" for w, t in segment_list])

   return tagged_sentence



if __name__ == "__main__":
   # data
   sentence = "中文分词是文本处理不可或缺的一步!"
   tagged_sentence = get_part_of_speech_taging(sentence)
   print(tagged_sentence)

""" 
Jieba 分词支持自定义词典，其中的词频和词性可以省略。
然而需要注意的是，若在词典中省略词性，采用 Jieba 分词进行词性标注后， 最终切分词的词性将变成 x，
这在如语法分析或词性统计等场景下会对结果有一定的影响。因此，在使用 Jieba 分词设置自定义词典时， 
尽量在词典中补充完整的信息 
"""