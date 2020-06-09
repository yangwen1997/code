##CPU 环境配置，支持linux\macOs
conda create -n chineseocr_app python=3.6 pip scipy numpy jupyter ipython ##运用conda 创建python环境
source activate chineseocr_app
cd darknet/ && make && cd ..cd
pip install easydict opencv-contrib-python==4.0.0.21 Cython h5py lmdb pandas requests bs4 matplotlib lxml -i https://pypi.tuna.tsinghua.edu.cn/simple/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda install mahotas
pip install -U pillow -i https://pypi.tuna.tsinghua.edu.cn/simple/
pip install web.py==0.40.dev0 redis
pip install keras==2.1.5 tensorflow==1.8 -i https://pypi.tuna.tsinghua.edu.cn/simple/
# mac
conda install pytorch torchvision -c pytorch
pip install torch
# linux
# conda install pytorch-cpu torchvision-cpu -c pytorch

# windows 安装
1.下载anaconda  安装到 D:\Anaconda3
2.配置anaconda 环境变量 D:\Anaconda3\condabin   D:\Anaconda3\Scripts
3.cd D:\Anaconda3\condabin
4.conda create -n chineseocr_app python=3.6 pip scipy numpy jupyter ipython      #运用conda 创建python环境
5.activate chineseocr_app  #进入虚拟环境 
6.pip install easydict opencv-contrib-python==4.0.0.21 Cython h5py lmdb pandas requests bs4 matplotlib lxml -i https://pypi.tuna.tsinghua.edu.cn/simple/
7.conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
8.conda install mahotas
9.pip install -U pillow -i https://pypi.tuna.tsinghua.edu.cn/simple/
10.pip install web.py==0.40.dev0 redis
11.pip install keras==2.1.5 tensorflow==1.8 -i https://pypi.tuna.tsinghua.edu.cn/simple/
12.conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/  #更改conda清华源
13.conda config --set show_channel_urls yes
14.conda install pytorch torchvision -c pytorch
15.pip install torch

# windows 使用说明
1.activate chineseocr_app
2.cd 到文件夹下，python app.py 8080   # 开启ocr 服务
3.运行post-demo  # 图片检测接口使用例子
4. 退出虚拟环境：conda deactivate chineseocr_app



# 使用说明
1. source activate chineseocr_app
2. cd 到文件夹下，python app.py 端口号
3. 退出虚拟环境：conda deactivate chineseocr_app
# 删除虚拟环境
conda remove -n name --all
