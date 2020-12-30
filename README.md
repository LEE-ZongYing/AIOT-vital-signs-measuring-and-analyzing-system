# project ： 高齡智慧生理監控系統


## 關於計畫
本計畫中結合了機器人、Raspberry Pi 3 、眾多的藍芽檢測設備(如額溫槍、體重器、血壓機…等等)，利用這些裝置能夠做到資料蒐集、分析、預測…等動作，而機器人也會對應目前的生理指標(血壓、體重、額溫、心跳)給予適當的建議，此外，本計畫展示成果中，為了增加實用及便利性，經由開發網頁的方式，將建議的內容、生理指標的周/月趨勢折線圖、直線圖呈現在網頁上，綜合上述的設備及功能，便能開發出一套應用於長者照護的即時健康監控AI機器人。

### 系統環境

Window10/Linux

### 需要裝置
1. window電腦/mac
2. ZenboJunior
3. Raspberry Pi3

### Prerequisites



### Installation
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
   * Linux
       Fedora
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

1. Get a free API Key at [https://example.com](https://example.com)
2. Clone the repo
   ```sh
   git clone https://github.com/your_username_/Project-Name.git
   ```
3. Install NPM packages
   ```sh
   npm install
   ```
4. Enter your API in `config.js`
   ```JS
   const API_KEY = 'ENTER YOUR API';
   ```



<!-- USAGE EXAMPLES -->
## Usage


## Roadmap


## Contributing

**greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



## License


## Contact


## Acknowledgements
* [GitHub Emoji Cheat Sheet](https://www.webpagefx.com/tools/emoji-cheat-sheet)
* [Img Shields](https://shields.io)
* [Choose an Open Source License](https://choosealicense.com)
* [GitHub Pages](https://pages.github.com)
* [Animate.css](https://daneden.github.io/animate.css)
* [Loaders.css](https://connoratherton.com/loaders)
* [Slick Carousel](https://kenwheeler.github.io/slick)
* [Smooth Scroll](https://github.com/cferdinandi/smooth-scroll)
* [Sticky Kit](http://leafo.net/sticky-kit)
* [JVectorMap](http://jvectormap.com)
* [Font Awesome](https://fontawesome.com)





<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/othneildrew/Best-README-Template.svg?style=for-the-badge
[contributors-url]: https://github.com/othneildrew/Best-README-Template/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/othneildrew/Best-README-Template.svg?style=for-the-badge
[forks-url]: https://github.com/othneildrew/Best-README-Template/network/members
[stars-shield]: https://img.shields.io/github/stars/othneildrew/Best-README-Template.svg?style=for-the-badge
[stars-url]: https://github.com/othneildrew/Best-README-Template/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/othneildrew/Best-README-Template/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/othneildrew
[product-screenshot]: images/screenshot.png



