

# build-internal-linux-kernel

## 1. get linux kernel source code
Clone internal kernel code from TeamForge
```bash
https://tf-amr-1.devtools.intel.com/ctf/code/projects.otc_gen_graphics/repositories
```
You may need to apply the access at the first time and clone below repos,
```bash
drm-intel	
drm-intel-internal-ci-tags
```
Detailed clone info could be seen by clicking the right side download button. 
Take **atspo** kernel as an example, if you want to build a specific version of kernel by yourself, 
please get the commit ID of that build from 
```bash
https://ubit-gfx.intel.com/overview/24989
```
and checkout the code in the drm-intel repo; if you want to build CI_DII_XXXX kernel by yourself, 
then please checkout the code in drm-intel-internal-ci-tags.

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

## 3. Edit config to enable low level trace
Firstly, please get the config file from the target machine or the released kernel build like 
```bash
linux-image-5.4.17+atspo180_5.4.17+atspo180-1_amd64.deb
```
uncompress it and you can get the
```bash 
config-5.4.17+atspo180
``` 
from folder 
```bash
linux-image-5.4.17+atspo180_5.4.17+atspo180-1_amd64\data\boot
```
rename it to .config and copy to your workspace. Open .config file in editor and search for 
"**CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS**", change it from
```
# CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS is not set
```
to
```
CONFIG_DRM_I915_LOW_LEVEL_TRACEPOINTS=y
```
to enable low level trace

## 4. build 
```bash
make olddefconfig
make deb-pkg
```

## 5. install
The generated kernel(several .deb) will be at the parent folder. You need below debs,
```bash
linux-headers-5.X.XX-XXXXXX.deb
linux-image-5.X.XX-XXXXXX.deb
linux-libc-dev_5.X.XX-XXXXXX.deb
```
just
```bash
sudo dpkg -i *.deb
```
to install the manual build kernel.