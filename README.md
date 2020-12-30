# project ： 高齡智慧生理監控系統


## 關於計畫
本計畫中結合了機器人、Raspberry Pi 3 、眾多的藍芽檢測設備(如額溫槍、體重器、血壓機…等等)，利用這些裝置能夠做到資料蒐集、分析、預測…等動作，而機器人也會對應目前的生理指標(血壓、體重、額溫、心跳)給予適當的建議，此外，本計畫展示成果中，為了增加實用及便利性，經由開發網頁的方式，將建議的內容、生理指標的周/月趨勢折線圖、直線圖呈現在網頁上，綜合上述的設備及功能，便能開發出一套應用於長者照護的即時健康監控AI機器人。

## 系統環境

Window10/Linux

## 需要裝置
1. window電腦/mac
2. ZenboJunior
3. Raspberry Pi3

## 安裝
* VS Code
* Anaconda
* ZeroMQ
   * Window(Anaconda)
      ```sh
      conda install -c conda-forge pyzmq
      ```
   * OSX
      ```sh
      brew install zmq
      ``` 
   * Linux<br>
       Fedora</br>
       ```sh
        dnf install zeromq-devel
        ```
       Ubuntu/Debian/Mint
        ```sh
        apt-get install libzmq3-dev
        ```
        Arch
        ```sh
        pacman -S zeromq
        ```
        SUSE
        ```sh
        zypper install zeromq-devel
        ```
* BlueZ
   ```sh
   sudo apt-get update
   ```
   ```sh
   sudo apt-get install bluetooth bluez bluez-hcidump
   ```
* Zenbo Junior

* Django

* MySQL

## 使用說明
可在VS Code中終端機執行，執行時需輸入如下例子，或是在儲存程式資料夾處，使用cmd執行
```sh
python test.py
```
1. 執行project/Code/版本一/Zenbo/版本一流程Code.py，連接Zenbo Junior。
2. 架設Server執行project/Code/版本一/Server/Server.py。
3. 在Raspberry Pi3中執行project/Code/版本一/Raspberry/test.py，即可接收藍芽的數據。
4. 最後project/Code/版本一/Django_project/安裝至電腦中即可顯示出網頁。



## 參考資料
* [ZeroMQ](https://zeromq.org/download/)
* [Bluez相關的各種tools的使用](https://b8807053.pixnet.net/blog/post/347831957-bluez%E7%9B%B8%E9%97%9C%E7%9A%84%E5%90%84%E7%A8%AEtools%E7%9A%84%E4%BD%BF%E7%94%A8)
* [GitHub Pages](https://pages.github.com)
* [ASUS Zenbo Junior](https://zenbo.asus.com/product/zenbojunior/overview/)
* [Raspberry Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)

