###### tags: `淡江大學搶課機器人開源專案`
# 開源專案230830更新
## 前言：
搶課機器人在3月放出來後收到廣大的迴響，但最近Chrome更新，修改了呼叫的方式，舊的機器人已經不能使用了，所以這幾天寫了一個新版的並且新增了一些功能，也感謝新生跟轉學生借我帳號讓我有機會測試，經過測試後可以正常使用，一樣多平台支援

## 打包執行檔適用環境：
* Mac intel 處理器：**macOS 13.5.1以上都可以使用
* Mac Apple Silicon 處理器：**macOS 13.5.1**以上都可以使用
* Windows 系統：**Windows 10**以上都可以使用


## 使用方式：
### 1. 先進資料夾下載執行檔案
[下載位置](https://1drv.ms/u/s!AvwcoqTkdjpWg6gp_bPQIFFvSRJ8nQ?e=K7QFC6)
> Windows平台請下載Public_WYSHBot_230829_Windows
> MacOS Intel處理器的請下載Public_WYSHBot_230829_Mac(intel)
> MacOS M1/M2系列處理器請下載Public_WYSHBot_230829_MacOS(Silicon)


### 2. 開始執行搶課機器人
* Windows直接點擊start.bat
![](https://i.imgur.com/EaUWGCb.jpg)

* Mac系列直接下載後解壓縮直接放到應用程式資料夾中，點兩下執行
![](https://i.imgur.com/eiQkxQj.png)
* 若Mac無法成功執行請參考備註1
* 在230829有修改圖示，請以實際圖示為主

### 3. 設定基本資料(Windows/Mac使用方式相同)
![](https://hackmd.io/_uploads/Ska5BE2an.png)
* 先設定登入資訊(務必按下儲存登入資訊)
* 設定加退選資訊
* 設定完加退選資訊務必按下儲存加退選清單
* **注意，如果沒有使用ChromeDriver的需求，7.就直接使用推薦的不用修改**

### 4. 執行搶課程式(Windows/Mac使用方式相同)
![](https://i.imgur.com/TQmVgpA.png)
* 按下執行搶課主程式

### 5. 設定搶課程式(Windows/Mac使用方式相同)
![](https://hackmd.io/_uploads/B1U5842T2.png)
* 先設定語言
* 再設定是要立即搶課或是預約搶課
* 完成後，執行開始搶課

### 6. 剩下交給上蒼
補充說明：機器人會隨機延遲幾秒鐘，一來是因為學校系統有時候會當機，二來是因為要保障有購買機器人的使用者權利

### Demo影片：
![](https://i.imgur.com/fHAJqUY.jpg)
> https://youtu.be/iINclOsUYpI

P.S.影片中使用Mac做範例，Windows使用介面大同小異

### 備註1(開啟任何來源)：
* 請開啟任終端機：
  ![](https://i.imgur.com/jJsZZBc.png)

* 在終端機中打入以下指令：
![](https://i.imgur.com/Qbtf4bJ.png)
> sudo spctl --master-disable

* 打入密碼(請注意這個密碼不會顯示)：
![](https://i.imgur.com/GOy8pHy.png)

* 打開設定中的隱私權與安全性：
![](https://i.imgur.com/HiaNSls.png)

## 進階功能
本機器人有Premium版本，提供以下功能：
* 完整的搶課速度
* 極速刷課模式
* 單一裝置登入功能
* 帳號密碼加密，強化安全性

![](https://hackmd.io/_uploads/rJ9nP4362.png)

若有需要，可以點擊以下連結：

![](https://hackmd.io/_uploads/H1Xb_N3T3.jpg)

[https://line.me/ti/g2/EQSB4VBKjoVXM0n46GDIrmdTwieWd1LIrtYpJg?utm_source=invitation&utm_medium=link_copy&utm_campaign=default](https://line.me/ti/g2/EQSB4VBKjoVXM0n46GDIrmdTwieWd1LIrtYpJg?utm_source=invitation&utm_medium=link_copy&utm_campaign=default)

## 原始碼開源
以下為原始碼，可以直接下載原始檔案使用
打包：
https://1drv.ms/u/s!AvwcoqTkdjpWg7thc2Y4Pm72H_xErg?e=subqq4

