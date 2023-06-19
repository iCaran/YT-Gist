# 🎬 Youtube Video Summarizer (v2)

A (more precise but less practical) tool to summarize YouTube videos so you can skip the boring parts.

https://github.com/iCaran/YT-Gist/assets/91419527/0032aa87-7069-4849-acea-599ad4f2da3d

# v2
- [v1](https://github.com/iCaran/YT-Gist/tree/master) uses TF-IDF based NLP summary, which is less accurate in extracting the meaning of the text, but provides shorter summaries
- v2 uses Gensim based NLP summary, which is much more accurate in extracting the meaning of the text, but provides much larger summaries
- Overall, due to the max token size limit of any AI Chatbot (especially in free plans), larger NLP summaries as prompts will exceed the limit and will fail
### Use this version when the video size is short and more accuracy is required

## 🚀 Quickstart

1. Make sure you have [Python 3.8.10](https://www.python.org/downloads/release/python-3810/) only (required for proper execution of Gensim 3.8.3).

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
