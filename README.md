# 🎬 Youtube Video Summarizer 

A cool open source tool to summarize YouTube videos so you can skip the boring parts.

## 🚀 Quickstart

1. Make sure you have [Python](https://www.python.org/) installed.

2. Grab a Google Bard API access token (read how [here](https://github.com/dsdanielpark/Bard-API#readme), or see below), paste it inside `token.txt`.

3. Download the latest release:
   - 💻 Windows: [YT-Gist-Win.zip](https://github.com/iCaran/YT-Gist/releases/download/1.0.0/YT-Gist-Win.zip)  
   - 🐧 Linux: [YT-Gist-Lin.tar.xz](https://github.com/iCaran/YT-Gist/releases/download/1.0.0/YT-Gist-Lin.tar.xz)

4. Extract and run the setup script:
   - Windows: Double-click `setup.bat`
   - Linux: `chmod +x setup.sh` and `./setup.sh` 
   
5. Summarize a video:  
   - Option 1 (Manual):  
     - Windows: `summ -u https://youtu.be/VIDEO_ID`  
     - Linux: `./summ.sh -u https://youtu.be/VIDEO_ID`  
   - Option 2 (Interactive):  
     - Windows: Double click `sum.bat` and enter a URL when prompted  
     - Linux: `./sum.sh` and enter a URL when prompted

6. Sit back and enjoy your video summaries!

## 🔑 Getting a Bard Token

1. Visit https://bard.google.com/
2. Press F12 to open the dev console  
3. Go to *Session* -> *Application* -> *Cookies*    
4. Copy the value of the `__Secure-1PSID` cookie
5. Paste that value into the file named `token.txt`

> **Warning:** Do not share your Bard token with anyone!
