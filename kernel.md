# build-linux-kernel

## 1. get linux kernel source code
download latest stable kernel from https://www.kernel.org/ and extract to local folder or 

get ubuntu kernel source use below command
```bash
apt-get source linux-image-unsigned-$(uname -r)
```
https://wiki.ubuntu.com/Kernel/SourceCode

## 2. install prerequisites
```bash
sudo apt install \
libncurses5-dev \
libssl-dev \
build-essential \
openssl \
zlibc \
minizip \
libidn11-dev \
libidn11 \
bison \
flex
```

## 3. generate config
```bash
cd kernel_source
sudo make mrproper 
sudo make clean 
# just exit to use default config. it will generate .config file at current folder
sudo make menuconfig
```
Open .config file in editor and search for "**CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS**", change it from
```
# CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS is not set
```
to
```
CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS=y
```

## 4. build 
```bash
make -j8
```

## 5. install
```bash
sudo make modules_install 
sudo make install 
```