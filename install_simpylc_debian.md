### Install Debian requirements
```bash
sudo apt update && apt upgrade && apt autoremove
sudo apt install build-essential freeglut3-dev
```

### Install conda requirements
```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-py39_4.12.0-Linux-aarch64.sh
bash ./Miniconda3-py39_4.12.0-Linux-aarch64.sh
conda install 
conda install -c conda-forge lidar numpy pyopengl tensorflow keras
```

### Install pip requirements
```bash
python -m pip install pip update
python -m pip install setuptools sonar simpylc
```

### Test
```bash
python -m simpylc -s
python simulations/car/world.py
```
