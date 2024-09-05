if __name__ == '__main__':
    from deep_audio_features.bin import basic_training as bt
    bt.train_model(['G:\\Data\\AudioClassification\\dataset\\CarHorn',
                    'G:\\Data\\AudioClassification\\dataset\\Dog',
                    'G:\\Data\\AudioClassification\\dataset\\Rain',], "outdoor")

    bt.train_model(['G:\\Data\\AudioClassification\\dataset\\MouseClick',
                    'G:\\Data\\AudioClassification\\dataset\\Footsteps',
                    'G:\\Data\\AudioClassification\\dataset\\Rain', ], "Laughing")