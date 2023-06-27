# 🎬 Youtube Video Summarizer 

A tool to summarize YouTube videos so you can skip the boring parts.

https://github.com/iCaran/YT-Gist/assets/91419527/0032aa87-7069-4849-acea-599ad4f2da3d

# 🔔  IMPORTANT UPDATE
### UPDATE - Bard API issues

Google has been messing with their internal apis, and [breaking the bardapi](https://github.com/dsdanielpark/Bard-API/issues/80).
Thanks to the constant effort of [dsdanielpark](https://github.com/dsdanielpark) the api is fixed and maintained consistently.

If you're a new installer and have never run `setup.bat` or `./setup.sh` before this, do so and after wards in a cmd/terminal run the following command, and do this everytime the script breaks
`pip install bardapi` or `pip install --upgrade bardapi`

Old users are recommended to the same to keep this script functioning.

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
---
### There is a [v2](https://github.com/iCaran/YT-Gist/tree/v2-gensim_based) available, which is for specific use cases, this version is for general purposes.
