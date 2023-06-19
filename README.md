# 🎬 Youtube Video Summarizer (v2)

A (more precise but less practical) tool to summarize YouTube videos so you can skip the boring parts.

### v1 vs v2 comparison (v1 on the left and v2 on the right)
1. https://youtu.be/FtTGGcXizsw
![image](https://github.com/iCaran/YT-Gist/assets/91419527/afa30961-27d6-46ed-9ee4-265f94cc4c1d)
2. https://youtu.be/1GSq7Je32iw
![image](https://github.com/iCaran/YT-Gist/assets/91419527/ef8e10a3-e65c-4f48-a808-0b559e564bc0)
3. https://youtu.be/wwsgCkbogMM
![image](https://github.com/iCaran/YT-Gist/assets/91419527/d1e60a74-5137-4ef2-a079-7cf5b99c1c3a)
4. https://youtu.be/EhnNA4g_lTw (it even identified the background music captions)
![image](https://github.com/iCaran/YT-Gist/assets/91419527/3a88901a-15c8-4776-9bbc-9f0241e45327)


# v2
- [v1](https://github.com/iCaran/YT-Gist/tree/master) uses TF-IDF based NLP summary, which is less accurate in extracting the meaning of the text, but provides shorter summaries
- v2 uses Gensim based NLP summary, which is much more accurate in extracting the meaning of the text, but provides much larger summaries
- Overall, due to the max token size limit of any AI Chatbot (especially in free plans), larger NLP summaries as prompts will exceed the limit and will fail
### Use this version when the video size is short and more accuracy is required

## 🚀 Quickstart

1. Make sure you have [Python 3.8.10](https://www.python.org/downloads/release/python-3810/) only (required for proper execution of Gensim 3.8.3).

2. Grab a Google Bard API access token (read how [here](https://github.com/dsdanielpark/Bard-API#readme), or see below), paste it inside `token.txt`.

3. Download the latest release:
   - 💻 Windows: [YT-Gist-2-Win.zip](https://github.com/iCaran/YT-Gist/releases/download/2.0.0/YT-Gist-2-Win.zip)  
   - 🐧 Linux: [YT-Gist-2-Lin.tar.xz](https://github.com/iCaran/YT-Gist/releases/download/2.0.0/YT-Gist-2-Lin.tar.xz)

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
