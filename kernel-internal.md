
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
(To apply the access, please click **Request a role in this Project** at the project home page.)
Detailed clone info could be seen by clicking the right side download button. 
```bash
Note: 
The default branch is master branch but it's empty by default. You need to checkout the branch
you want as,
git checkout atspo
```
Take **atspo** kernel as an example, if you want to build a specific version of kernel by yourself, 
please get the commit ID of that build from 
```bash
https://ubit-gfx.intel.com/overview/24989
Commit ID could be found at the “SCM-Changes” section 
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
flex  \
libelf-dev 
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
to enable low level trace. You could change CONFIG_LOCALVERSION to include a suitable nametag to 
identify the change being made. (no capital letters should be used) Example:
```bash
CONFIG_LOCALVERSION="+atspo204-debug-disable"
```

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