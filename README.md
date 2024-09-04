# AudioClassification
GUI.py用于最后显示预测置信结果  
## 9.4 晚21:16日志：
下一步修改on_start_clicked函数，与AudioClassifier.py连接，分类程序未完成时prob块显示Calculating...，返回后显示概率  
分两个文件编写检测程序(Indoor_AudioClassifier.py和Outdoor_AudioClassifier.py)，在on_start_clicked中加入if判断执行哪个文件
