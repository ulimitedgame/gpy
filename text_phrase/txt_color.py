import re
from termcolor import colored
import jieba 
import jieba.posseg as pseg
import os

def jieba_flag_to_color(flag):
    if flag == 'n':
        return 'red'
    elif flag == 'v':
        return 'yellow'
    elif flag == 'a':
        return 'blue'
    elif flag == 'd':
        return 'green'
    else:
        return 'magenta'

def get_falgs():
    flags = {}
    # flags['n'] = '名词'
    # flags['v'] = '动词'
    # flags['a'] = '形容词'
    # flags['d'] = '副词'
    flags["a"]="形容词"  #取英语形容词adjective的第1个字母
    flags["ad"]="副形词"  #直接作状语的形容词.形容词代码a和副词代码d并在一起
    flags["ag"]="形语素"  #形容词性语素。形容词代码为a，语素代码ｇ前面置以a
    flags["an"]="名形词"  #具有名词功能的形容词。形容词代码a和名词代码n并在一起
    flags["b"]="区别词"  #取汉字“别”的声母
    flags["c"]="连词"  #取英语连词conjunction的第1个字母
    flags["d"]="副词"  #取adverb的第2个字母，因其第1个字母已用于形容词
    flags["dg"]="副语素"  #副词性语素。副词代码为d，语素代码ｇ前面置以d
    flags["e"]="叹词"  #取英语叹词exclamation的第1个字母
    flags["f"]="方位词"  #取汉字“方” 的声母
    flags["g"]="语素"  #绝大多数语素都能作为合成词的“词根”，取汉字“根”的声母
    flags["h"]="前接成分"	#取英语head的第1个字母
    flags["i"]="成语"       #取英语成语idiom的第1个字母
    flags["j"]="简称略语"	#取汉字“简”的声母
    flags["k"]="后接成分"	 #
    flags["l"]="习用语"	   #习用语尚未成为成语，有点“临时性”，取“临”的声母
    flags["m"]="数词" #取英语numeral的第3个字母，n，u已有他用
    flags["n"]="名词" #取英语名词noun的第1个字母
    flags["ng"]="名语素"	   #名词性语素。名词代码为n，语素代码ｇ前面置以n
    flags["nr"]="人名" #名词代码n和“人(ren)”的声母并在一起
    flags["ns"]="地名" #名词代码n和处所词代码s并在一起
    flags["nt"]="机构团体"	#“团”的声母为t，名词代码n和t并在一起
    flags["nx"]="字母专名"	#
    flags["nz"]="其他专名"	#“专”的声母的第1个字母为z，名词代码n和z并在一起
    flags["o"]="拟声词"	   #取英语拟声词onomatopoeia的第1个字母
    flags["p"]="介词"  #取英语介词prepositional的第1个字母
    flags["q"]="量词"  #取英语quantity的第1个字母
    flags["r"]="代词"  #取英语代词pronoun的第2个字母,因p已用于介词
    flags["s"]="处所词"	   #取英语space的第1个字母
    flags["t"]="时间词"	   #取英语time的第1个字母
    flags["tg"]="时语素"	   #时间词性语素。时间词代码为t,在语素的代码g前面置以t
    flags["u"]="助词"  #取英语助词auxiliary 的第2个字母,因a已用于形容词
    flags["ud"]="结构助词"	#
    flags["ug"]="时态助词"	#
    flags["uj"]="结构助词的" #
    flags["ul"]="时态助词了" #
    flags["uv"]="结构助词地" #
    flags["uz"]="时态助词着" #
    flags["v"]="动词"
    flags["vd"]="副动词"	
    flags["vg"]="动语素"	   #    动词性语素。动词代码为v。在语素的代码g前面置以V
    flags["vn"]="名动词"	   #    指具有名词功能的动词。动词和名词的代码并在一起
    flags["w"]="标点符号" #
    flags["x"]="非语素字" #    非语素字只是一个符号，字母x通常用于代表未知数、符号
    flags["y"]="语气词"    #    取汉字“语”的声母
    flags["z"]="状态词"    #    取汉字“状”的声母的前一个字母
    return flags   
# KEY_COLOR = ["blue", "yellow", "magenta", "red", "cyan"]
KEY_FLAGS_MORE_IMPORT = {"blue":"形容词",
             "yellow":"副词"}
FLAGS = {
    "a" : ["形容词", "a"],
    "ad" : ["副形词", "a"],
    "ag" : ["形语素", "a"],
    "an" : ["名形词", "a"],
    "b" : ["区别词", "o"],
    "c" : ["连词","o"],
    "d" : ["副词","d"],
    "dg" : ["副语素","d"],
    "e" : ["叹词","o"],
    "f" : ["方位词","o"],
    "g" : ["语素","o"],
    "h" : ["前接成分","o"],
    "i" : ["成语","i"],
    "j" : ["简称略语","o"],
    "k" : ["后接成分","o"],
    "l" : ["习用语","l"],
    "m" : ["数词","o"],
    "n" : ["名词","n"],
    "ng" : ["名语素","ng"],
    "nr" : ["人名","nr"],
    "ns" : ["地名","ns"],
    "nt" : ["机构团体","nt"],
    "nx" : ["字母专名","nx"],
    "nz" : ["其他专名","nz"],
    "o" : ["拟声词","o"],
    "p" : ["介词","o"],
    "q" : ["量词","o"],
    "r" : ["代词","o"],
    "s" : ["处所词","o"],
    "t" : ["时间词","o"],
    "tg" : ["时语素","o"],
    "u" : ["助词","o"],
    "ud" : ["结构助词","o"],
    "ug" : ["时态助词","o"],
    "uj" : ["结构助词的","o"],
    "ul" : ["时态助词了","o"],
    "uv" : ["结构助词地","o"],
    "uz" : ["时态助词着","o"],
    "v" : ["动词","v"],
    "vd" : ["副动词","v"],
    "vg" : ["动语素","v"],
    "vn" : ["名动词","v"],
    "w" : ["标点符号","o"],
    "x" : ["非语素字","o"],
    "y" : ["语气词","o"],
    "z" : ["状态词","o"]
}
KEY_FLAGS = {"blue":"形容词",
             "yellow":"副词", 
             "magenta":"名词", 
             "red":"动词",
             "cyan":"习语",
             "light_cyan":"成语"}
def translated_flags():
    flags = {}
    colors = ["blue", "yellow", "magenta", "red", "cyan", "light_cyan" "white"]
    other_color = "white"
    #  a  b blue
    #  d  y yellow
    #  n  m magenta
    #  v  r red
    #  i  c cyan
    #  o  w white
    # 
    flags["a"]="blue"  #取英语形容词adjective的第1个字母
    flags["ad"]="yellow"  #直接作状语的形容词.形容词代码a和副词代码d并在一起
    flags["ag"]="blue"  #形容词性语素。形容词代码为a，语素代码ｇ前面置以a
    flags["an"]="blue"  #具有名词功能的形容词。形容词代码a和名词代码n并在一起
    flags["b"]="b"  #取汉字“别”的声母
    flags["c"]="c"  #取英语连词conjunction的第1个字母
    flags["d"]="yellow"  #取adverb的第2个字母，因其第1个字母已用于形容词
    flags["dg"]="yellow"  #副词性语素。副词代码为d，语素代码ｇ前面置以d
    flags["e"]="e"  #取英语叹词exclamation的第1个字母
    flags["f"]="f"  #取汉字“方” 的声母
    flags["g"]="g"  #绝大多数语素都能作为合成词的“词根”，取汉字“根”的声母
    flags["h"]="h"	#取英语head的第1个字母
    flags["i"]="light_cyan"  #取英语成语idiom的第1个字母
    flags["j"]="j"	#取汉字“简”的声母
    flags["k"]="k"	 #
    flags["l"]="cyan"	   #习用语尚未成为成语，有点“临时性”，取“临”的声母
    flags["m"]="m" #取英语numeral的第3个字母，n，u已有他用
    flags["n"]="magenta" #取英语名词noun的第1个字母
    flags["ng"]="magenta"	   #名词性语素。名词代码为n，语素代码ｇ前面置以n
    flags["nr"]="magenta" #名词代码n和“人(ren)”的声母并在一起
    flags["ns"]="magenta" #名词代码n和处所词代码s并在一起
    flags["nt"]="magenta"	#“团”的声母为t，名词代码n和t并在一起
    flags["nx"]="magenta"	#
    flags["nz"]="magenta"	#“专”的声母的第1个字母为z，名词代码n和z并在一起
    flags["o"]="拟声词"	   #取英语拟声词onomatopoeia的第1个字母
    flags["p"]="介词"  #取英语介词prepositional的第1个字母
    flags["q"]="量词"  #取英语quantity的第1个字母
    flags["r"]="magenta"  #取英语代词pronoun的第2个字母,因p已用于介词
    flags["s"]="处所词"	   #取英语space的第1个字母
    flags["t"]="时间词"	   #取英语time的第1个字母
    flags["tg"]="时语素"	   #时间词性语素。时间词代码为t,在语素的代码g前面置以t
    flags["u"]="助词"  #取英语助词auxiliary 的第2个字母,因a已用于形容词
    flags["ud"]="结构助词"	#
    flags["ug"]="时态助词"	#
    flags["uj"]="结构助词的" #
    flags["ul"]="时态助词了" #
    flags["uv"]="结构助词地" #
    flags["uz"]="时态助词着" #
    flags["v"]="red"
    flags["vd"]="red"	
    flags["vg"]="red"	   #    动词性语素。动词代码为v。在语素的代码g前面置以V
    flags["vn"]="red"	   #    指具有名词功能的动词。动词和名词的代码并在一起
    flags["w"]="标点符号" #
    flags["x"]="非语素字" #    非语素字只是一个符号，字母x通常用于代表未知数、符号
    flags["y"]="语气词"    #    取汉字“语”的声母
    flags["z"]="状态词"    #    取汉字“状”的声母的前一个字母
    # change other colors into other color
    ks = []
    for k,v in flags.items():
        if v not in colors:
            ks.append(k)
    for k in ks:
        flags[k] = other_color
    s = set(f)
    return flags   


def t1():
    text = '青蛙爬上了樱桃树'

    pattern = r'[\u4e00-\u9fa5]+'
    words = re.findall(pattern, text)

    for word in words:
        if len(word) == 1:
            print(colored(word, 'red'), end=' ')
        elif len(word) == 2:
            print(colored(word, 'yellow'), end=' ')
        elif len(word) == 3:
            print(colored(word, 'blue'), end=' ')
        elif len(word) == 4:
            print(colored(word, 'green'), end=' ')
        else:
            print(colored(word, 'magenta'), end=' ')


sentence = '我爱北京天安门'
# words = jieba.lcut(sentence)
# print(words) 

def html_out1(t, w, out):
    out.write('<b class="{}">{}</b>'.format(t,w))
def html_out2(flag, w, out):
    if flag not in FLAGS:
        print("not have {}".format(flag))
        FLAGS[flag] = [flag, "o"]
    t = FLAGS[flag][1]
    if t != "o":
        if t.startswith("n") and len(t) != 1:
            c ="n2"
        else:
            c = t
    else:
        c= ""
    if c != "":
        html_clase = 'class="{}"'.format(c)
    else:
        html_clase= ""
    out.write('<ruby {}>{}<rp>(</rp><rt>{}</rt><rp>)</rp></ruby> '.format(html_clase ,w, flag))
    
    

def convert_to_html(sentence, out, key_freq):
    words_poseg = pseg.lcut(sentence)
    # print(words_poseg)
    out.write('<p>')
    for w in words_poseg:
        # print(w.word, w.flag)
        html_out2(w.flag, w.word, out)
        t = FLAGS[w.flag][1]
        if t not in key_freq:
            key_freq[t] = 1
        else:
            key_freq[t] = key_freq[t] +1
    out.write('<p>')
   

def print_colored_txt(sentence):
    words_poseg = pseg.lcut(sentence)
    # print(words_poseg)
    flags = translated_flags()
    key_freq ={}
    for w in words_poseg:
        # print(w.word, w.flag)
        if w.flag not in flags:
            print("not have {}".format(w.flag))
            flags[w.flag] = "white"
        c = flags[w.flag]

        
        if c in KEY_FLAGS_MORE_IMPORT:
            print(colored(w.word, c,'on_dark_grey', ['bold']), end=' ')
        elif c in KEY_FLAGS:
            print(colored(w.word, c,'on_black', ['bold']), end=' ')
        else:
            print(colored(w.word, c), end=' ')
        
        if c in KEY_FLAGS:
            if c not in key_freq:
                key_freq[c] = 1
            else:
                key_freq[c] = key_freq[c] +1
    print("\n")
    for k, v in key_freq.items():
        print("{}: {}".format( KEY_FLAGS[k], v))

file = "/Users/apple/code/gpy/text_phrase/resource/howToWriteReport.txt"
html = "/Users/apple/code/gpy/text_phrase/out/howToWriteReport.html"
head_html ="/Users/apple/code/gpy/text_phrase/head.html"

def copy_file(src, dst):
    if not os.path.exists(src):
        print("{} is not existed", src)
        return
    s = open(src, "r", encoding="utf-8")
    d = open(dst,"w", encoding="utf-8")
    d.write(s.read())
    s.close()
    d.close

def test():
    with open(file, "r", encoding="utf-8") as f:
        txt = f.read()
        print_colored_txt(txt)
    


with open(file, "r", encoding="utf-8") as f:
    lines = f.readlines()
    key_freq ={}
    # txt = f.read()
    copy_file(head_html, html)
    h = open(html ,"a+", encoding="utf-8")
    for l in lines:
        convert_to_html(l, h, key_freq)
    h.close()

    print("\n")
    for k, v in key_freq.items():
        print("{}: {}".format( k, v))
# stopwords = ['我','爱']
# words_poseg_clean = [] 
# for word in words_poseg: 
#     if word.word not in stopwords: 
#         words_poseg_clean.append(word)        

# print(words_poseg_clean)

