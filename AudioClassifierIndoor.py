if __name__ == '__main__':
    from deep_audio_features.bin import basic_test as btest
    d, p = btest.test_model("model/indoor.pt", 'audio.wav', layers_dropped=0, test_segmentation=False)