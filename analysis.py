import torchaudio
import matplotlib.pyplot as plt

# 读取音频文件
file_path = 'CarHorn(7).wav'  # 替换为你的音频文件路径
waveform, sample_rate = torchaudio.load(file_path)

# 绘制波形
plt.figure(figsize=(10, 4))
plt.plot(waveform.t().numpy())
plt.title('Waveform')
plt.xlabel('Time (samples)')
plt.ylabel('Amplitude')
plt.show()

# 计算和绘制频谱图
specgram = torchaudio.transforms.Spectrogram()(waveform)

plt.figure(figsize=(10, 4))
plt.imshow(specgram.log2()[0,:,:].numpy(), cmap='viridis', aspect='auto', origin='lower')
plt.title('Spectrogram')
plt.xlabel('Time')
plt.ylabel('Frequency')
plt.colorbar(format='%+2.0f dB')
plt.show()


