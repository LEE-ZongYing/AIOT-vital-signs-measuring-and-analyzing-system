# AIOT生理量測與分析系統

## About this project (關於計畫)
This project have the source file of vital signs monitoring system running on a Zenbo Junior robot made by ASUS Inc.
本計畫中結合機器人Zenbo Junior、Raspberry Pi 3 MB+、眾多的藍芽檢測設備(如額溫槍、體重計、血壓機…等等)，利用這些裝置能夠做到資料蒐集、分析、預測…等動作，而機器人也會對應目前的生理指標(血壓、體重、額溫、心跳)給予適當的建議，此外，本計畫展示成果中，為了增加實用及便利性，經由開發網頁的方式，將建議的內容、生理指標的周/月趨勢折線圖、直線圖呈現在網頁上，綜合上述的設備及功能，便能開發出一套應用於長者照護的即時健康監控AI機器人。

## Environment (系統環境)
* Anaconda 
* Python 3.7.7
* [pyzenbo 1.0.17](https://zenbo.asus.com/developer/tools/)
* ZeroMQ 版本....8 
* [MySQL...8.0.22](https://www.mysql.com/)
## Requirement(需要裝置)
1. Window電腦/Mac for controling network connection and Raspberry Pi  
2. Zenbo Junior robot  
3. Raspberry Pi 3 model B+
4. USB讀卡機
5. 藍芽感測設備(額溫槍IR40B、體重計W310、血壓計D40)
## Installation 安裝
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
* pexpect
   ```sh
   sudo apt-get install -y python-pexpect
   ```
* pyscard
   ```sh
   sudo apt-get install -y python-pyscard
   ```
* Zenbo Junior
  - navigate to *pyzenbo* folder and install the SDK using
  ```python3.7
    python setup.py install
  ```
* Django
  * 安裝python和django(虛擬環境下)
  ```sh
  python -m pip install --upgrade pip
  ```
  ```sh
  pip install django
  ```
  ```sh
  pip install python
  ```
* MySQL
  * 下載API Key [ＭysQl installer](http://dev.mysql.com/downloads/windows/installer/)
## 使用說明
可在VS Code中終端機執行，執行時需輸入如下例子，或是在儲存程式資料夾處，使用command line執行
```sh
python test.py
```
* Zenbo Junior
  1. 執行project/Code/版本一/Zenbo/FsmZenbo.py，連接Zenbo Junior。
* Server
  1. 架設Server執行project/Code/版本一/Server/FSM.py。
* Raspberry Pi 3
  1. 在Raspberry Pi 3中執行project/Code/版本一/Raspberry/test.py，即可接收藍芽的數據。
* Django
  1. 執行`python manage.py runserver`即可跑出網頁
* MySQL
  1. 建立專屬於Iccard資料庫
  2. 設定使用者密碼及權限
  3. 建立Iccard資料表儲存使用者各項資料
## System Demo(系統展示)
1. Demo 網址:https://youtu.be/vt5fpE0bzSY
2. 系統實際執行從5:48開始
## 參考資料
* [ZeroMQ](https://zeromq.org/download/)
* [Bluez相關的各種tools的使用](https://b8807053.pixnet.net/blog/post/347831957-bluez%E7%9B%B8%E9%97%9C%E7%9A%84%E5%90%84%E7%A8%AEtools%E7%9A%84%E4%BD%BF%E7%94%A8)
* [GitHub Pages](https://pages.github.com)
* [ASUS Zenbo Junior](https://zenbo.asus.com/product/zenbojunior/overview/)
* [Raspberry Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b/)
* [架設 Django 開發環境](https://developer.mozilla.org/zh-TW/docs/Learn/Server-side/Django/development_environment)

