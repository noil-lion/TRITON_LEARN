# 常用的宿主机GPU设备分配docker指令
## docker19.03以前
最初的容器中使用显卡，需要指定硬件名。经历了两种方式  
1. 使用lxc驱动程序运行docker守护进程，以便能够修改配置并让容器访问显卡设备  
2. Docker 0.9中放弃了lxc作为默认执行上下文，但是依然需要指定显卡的名字  

```
docker run -ti --device /dev/nvidia0:/dev/nvidia0 --device /dev/nvidiactl:/dev/nvidiactl --device /dev/nvidia-uvm:/dev/nvidia-uvm tleyden5iwx/ubuntu-cuda /bin/bash
```
## nvidia-docker
英伟达公司开发了nvidia-docker，该软件是对docker的包装，使得容器能够看到并使用宿主机的nvidia显卡.
本质上，他们找到了一种方法来避免在容器中安装CUDA/GPU驱动程序，并让它与主机内核模块匹配。
```
docker run --rm --gpus 2 nvidia/cuda nvidia-smi
```
## docker 19.03
在docker19以前的版本都需要单独下载nvidia-docker1或nvidia-docker2来启动容器，自从升级了docker19后跑需要gpu的docker只需要加个参数–gpus all 即可表示使用所有的gpu。  
如果要使用2个gpu：–gpus 2  
也可直接指定哪几个卡：–gpus '"device=1,2"'

## 运行gpu的容器
所有显卡都对容器可见：
```
docker run --gpus all --name 容器名 -d -t 镜像id
```
只有显卡1对容器可见：
```
docker run --gpus="1" --name 容器名 -d -t 镜像id
```
## 例
```
# 使用所有GPU
$ docker run --gpus all nvidia/cuda:9.0-base nvidia-smi

# 使用两个GPU
$ docker run --gpus 2 nvidia/cuda:9.0-base nvidia-smi

# 指定GPU运行
$ docker run --gpus '"device=1,2"' nvidia/cuda:9.0-base nvidia-smi
$ docker run --gpus '"device=UUID-ABCDEF,1"' nvidia/cuda:9.0-base nvidia-smi
```
[Link](https://www.cnblogs.com/dan-baishucaizi/p/15503578.html)