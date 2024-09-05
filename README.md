# AudioClassification
本项目用于音频分类  
基于数据集：https://github.com/karolpiczak/ESC-50  
基于神经网络框架：https://github.com/tyiannak/deep_audio_features  
## GUI.py
运行此文件可以显示交互界面，实现从采集音频到分析音频到输出结果的全流程
## train.py
用于训练神经网络
## analysis.py
用于分析.wav音频数据 输出form和mel-spectrogram
## dataset_processing.py
用于预处理数据集 从raw data中提取所需要的文件
## AudioAcquisitioin.py
用于录取5s的音频数据并保存在项目文件夹下
## AudioClassifierIndoor.py & AudioClassifierOutdoor.py
用于对采集到的音频数据进行检测 输出检测结果与置信概率
