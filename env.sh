pip3 install torch torchvision torchaudio
pip install numpy deprecation torchinfo torch_optimizer torchviz captum LessHash-BloomFilter nltk phe torchsummaryX sortedcontainers

# install faiss

conda install -c conda-forge faiss-cpu


# run

python src/train_beijing_fedsim.py -g 1 -p 1e0 -k 5 -ds