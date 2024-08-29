配置环境
conda create --name class python=3.8

pip install torch torchvision torchaudio -i https://pypi.tuna.tsinghua.edu.cn/simple

数据集 dataset/audio/
以下翻译成英文
白头鹎 sinensis
斑鸫 naumanni
大嘴乌鸦 raven
戴胜  hoopoe
黄喉鹂 chinensis
灰椋鸟 grackle
灰头绿啄木鸟 woodpecker
灰喜鹊 wingedmagpie
金翅雀 goldfinch
麻雀 sparrow
山斑鸠 dove
喜鹊 magpie
小鸡 chick
棕头鸦雀 bulbul


划分数据集
python create_data.py 
生成label_list.txt  test_list.txt   train_list.txt


模型训练
python train.py

评估
python eval.py

推理
python infer.py





