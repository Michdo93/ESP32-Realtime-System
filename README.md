# ESP32-Realtime-System

**Patent:** Zhao Zijian, Zhu Guangxu, Shen Chao, Shi Qingjiang, Han Kaifeng "Personnel Detection Method, Device, Electronic Equipment and Storage Medium" (Application No.: 2023116499786, 2024)

**Device:** ESP32-S3 (supports other ESP32 models)

![](./fig/main.png)



## 1. Introduction

First, flash [esp-csi/examples/get-started/csi_recv_router at master · espressif/esp-csi (github.com)](https://github.com/espressif/esp-csi/tree/master/examples/get-started/csi_recv_router) onto the ESP32 and connect it to the router.

Then, use the system with the following command:

```shell
python main.py --port <port>
```

![](./fig/ui.png)



For more parameters, you can obtain help with:

```shell
python main.py --help
```

**Note:** After clicking each module button, the program will start running. To stop the program, please click the corresponding button again. **Do not directly close the interface!**



## 2. Functions

- **CSI Display:** Displays CSI amplitude, phase, and spectrum data.
- **LoFi: 2D Image-Based Wi-Fi Positioning Tag Generator:** Generates positioning tags using a 2D image. Users can specify anchor points in the physical world and their corresponding pixel coordinates.
- **Intrusion Detection:** Monitors and detects unauthorized access or breaches in a designated area.
- **Fall Detection:** Identifies and alerts on incidents of falling, utilizing wireless channel state information.
- **Breathing Detection:** Monitors and analyzes breathing patterns.
- **Gesture Recognition / Action Recognition / Person Recognition / Population Estimation:** Advanced functionalities for recognizing gestures, actions, individuals, and estimating the number of people in a given space. (Pending updates)
- **Trajectory Tracking:** In development, this feature will track the movement paths of individuals or objects.

**Note:** The functionalities listed above are currently under development and will be updated as progress is made.



## 3. References

**Overview**

```
@article{zhao2025short,
  title={A Short Overview of Multi-Modal Wi-Fi Sensing},
  author={Zhao, Zijian},
  journal={arXiv preprint arXiv:2505.06682},
  year={2025}
}
```

**Fall Detection**

[shawnnn3di/falldewideo](https://github.com/shawnnn3di/falldewideo)

```
@inproceedings{cai2023falldewideo,
  title={FallDeWideo: Vision-Aided Wireless Sensing Dataset for Fall Detection with Commodity Wi-Fi Devices},
  author={Cai, Zhijie and Chen, Tingwei and Zhou, Fujia and Cui, Yuanhao and Li, Hang and Li, Xiaoyang and Zhu, Guangxu and Shi, Qingjiang},
  booktitle={Proceedings of the 3rd ACM MobiCom Workshop on Integrated Sensing and Communications Systems},
  pages={7--12},
  year={2023}
}
```

```
@article{chen2024deep,
  title={Deep learning-based fall detection using commodity Wi-Fi},
  author={Chen, Tingwei and Li, Xiaoyang and Li, Hang and Zhu, Guangxu},
  journal={Journal of Information and Intelligence},
  year={2024},
  publisher={Elsevier}
}
```

```
@article{陈廷尉2023基于无线信道状态信息的跌倒检测,
  title={基于无线信道状态信息的跌倒检测},
  author={陈廷尉 and 李阳 and 韩凯峰 and 李晓阳 and 李航 and 朱光旭},
  journal={信息通信技术与政策},
  volume={49},
  number={9},
  pages={67},
  year={2023}
}
```



**Gesture Recognition / Action Recognition / Person Recognition / Population Estimation**

[RS2002/CSI-BERT: Official Repository for The Paper, Finding the Missing Data: A BERT-inspired Approach Against Package Loss in Wireless Sensing](https://github.com/RS2002/CSI-BERT)

[RS2002/CSI-BERT2: Official Repository for The Paper, CSI-BERT2: A BERT-Inspired Framework for Efficient CSI Prediction and Recognition in Wireless Communication and Sensing](https://github.com/RS2002/CSI-BERT2)

[RS2002/CrossFi: Official Repository for The Paper, CrossFi: A Cross Domain Wi-Fi Sensing Framework Based on Siamese Network](https://github.com/RS2002/CrossFi)

[RS2002/KNN-MMD: Official Repository for The Paper,KNN-MMD: Cross Domain Wireless Sensing via Local Distribution Alignmen](https://github.com/RS2002/KNN-MMD)

```
@inproceedings{zhang2023ratiofi,
  title={RatioFi: Unlocking the Potential of WiFi CSI},
  author={Zhang, Dengtao and Cai, Zhijie and Zhu, Guangxu and Li, Hang and Li, Xiaoyang and Shi, Qingjiang and Shen, Chao},
  booktitle={2023 International Conference on Ubiquitous Communication (Ucom)},
  pages={421--425},
  year={2023},
  organization={IEEE}
}
```

```
@inproceedings{zhao2024finding,
  title={Finding the missing data: A bert-inspired approach against package loss in wireless sensing},
  author={Zhao, Zijian and Chen, Tingwei and Meng, Fanyi and Li, Hang and Li, Xiaoyang and Zhu, Guangxu},
  booktitle={IEEE INFOCOM 2024-IEEE Conference on Computer Communications Workshops (INFOCOM WKSHPS)},
  pages={1--6},
  year={2024},
  organization={IEEE}
}
```

```
@article{zhao2025csi,
  author={Zhao, Zijian and Meng, Fanyi and Lyu, Zhonghao and Li, Hang and Li, Xiaoyang and Zhu, Guangxu},
  journal={IEEE Transactions on Mobile Computing}, 
  title={CSI-BERT2: A BERT-inspired Framework for Efficient CSI Prediction and Classification in Wireless Communication and Sensing}, 
  year={2025},
  volume={},
  number={},
  pages={1-17}
 }

```

```
@article{zhao2025crossfi,
  title={Crossfi: A cross domain wi-fi sensing framework based on siamese network},
  author={Zhao, Zijian and Chen, Tingwei and Cai, Zhijie and Li, Xiaoyang and Li, Hang and Chen, Qimei and Zhu, Guangxu},
  journal={IEEE Internet of Things Journal},
  year={2025},
  publisher={IEEE}
}
```

```
@article{zhao2025knn,
  author={Zhao, Zijian and Cai, Zhijie and Chen, Tingwei and Li, Xiaoyang and Li, Hang and Chen, Qimei and Zhu, Guangxu},
  journal={IEEE Transactions on Mobile Computing}, 
  title={KNN-MMD: Cross Domain Wireless Sensing Via Local Distribution Alignment}, 
  year={2025},
  volume={},
  number={},
  pages={1-18}
  }
```

```
@INPROCEEDINGS{zhao2025does,
  author={Zhao, Zijian and Cai, Zhijie and Chen, Tingwei and Li, Xiaoyang and Li, Hang and Chen, Qimei and Zhu, Guangxu},
  booktitle={2025 IEEE/CIC International Conference on Communications in China (ICCC)}, 
  title={Does MMD Really Align? A Cross Domain Wireless Sensing Method via Local Distribution}, 
  year={2025},
  volume={},
  number={},
  pages={1-6}
 }

```

**Tracking / Localization**

[RS2002/LoFi: Official Repository for The Paper, LoFi: Vision-Aided Label Generator for Wi-Fi Localization and Tracing](https://github.com/RS2002/LoFi)

```
@INPROCEEDINGS{zhao2025lofi,
  title={LoFi: Vision-Aided Label Generator for Wi-Fi Localization and Tracking},
  author={Zhao, Zijian and Chen, Tingwei and Meng, Fanyi and Cai, Zhijie and Li, Hang and Li, Xiaoyang and Zhu, Guangxu},
  booktitle={2025 IEEE Globecom Workshops (GC Wkshps)}, 
  year={2025},
  volume={},
  number={},
  pages={1-6}
}
```
