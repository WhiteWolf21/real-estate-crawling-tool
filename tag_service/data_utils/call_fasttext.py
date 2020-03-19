if __name__ == '__main__':
    import fastText
    from data_utils.constants import ALL_TEXTS, WORD_VEC_PATH
    model = fastText.train_unsupervised(ALL_TEXTS,
                                        model='cbow',
                                        lr=0.05,
                                        dim=300,
                                        ws=5,
                                        epoch=50,
                                        minCount=5,
                                        maxn=0)
    model.save_model(WORD_VEC_PATH)
