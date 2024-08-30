from ResNetSE.macls.predict import MAClsPredictor

#  获取识别器
predictor = MAClsPredictor(
    configs="ResNetSE/configs/resnet_se.yml",
    model_path="ResNetSE/models/ResNetSE_Fbank/best_model/",
    use_gpu=False,
)

# 封装识别函数
def infer(audio_path: str):
    label, score = predictor.predict(audio_data=audio_path)

    print(f'音频：{audio_path} 的预测结果标签为：{label}，得分：{score}')
    return label, score