import sounddevice as sd
import torch
import torchaudio
import numpy as np

# 设置录音参数
samplerate = 44100  # 采样率
channels = 1        # 通道数
dtype = 'float32'   # 数据类型
duration = 5        # 录音时长（秒）
n_samples = int(samplerate * duration)  # 计算样本数

# 录制音频
recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=channels, dtype=dtype)
sd.wait()  # 等待录音结束

# 转换为2D torch tensor
recording_tensor = torch.from_numpy(recording).squeeze()
recording_tensor = torch.unsqueeze(recording_tensor, 0)  # 增加一个维度

# 保存音频文件
output_path = 'audio.wav'
torchaudio.save(output_path, recording_tensor, samplerate)


