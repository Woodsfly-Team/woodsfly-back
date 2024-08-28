from BirdClass.macls.predict import MAClsPredictor

#  获取识别器
predictor = MAClsPredictor(
    configs="BirdClass/configs/resnet_se.yml",
    model_path="BirdClass/models/ResNetSE_Fbank/best_model/",
    use_gpu=False,
)


def infer(audio_path: str):
    label, score = predictor.predict(audio_data=audio_path)

    print(f'音频：{audio_path} 的预测结果标签为：{label}，得分：{score}')
    return label, score