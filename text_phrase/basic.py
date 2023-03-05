import jieba
seg_list = jieba.cut("我来到北京清华大学,感到非常开心", cut_all=True)
print("Full Mode:"+"/".join(seg_list))  # 全模式
 
seg_list = jieba.cut("我来到北京清华大学，感到非常开心", cut_all=False)
print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
 
seg_list = jieba.cut("我来到北京清华大学，感到非常开心")
print("/ ".join(seg_list))  # 默认精确模式
 
seg_list = jieba.cut_for_search("烟花从正面看，还是从侧面看呢？")   # 搜索引擎模式
print("/ ".join(seg_list))