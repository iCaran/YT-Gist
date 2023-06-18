# Youtube Summarizer

A tool to summarize youtube videos, so you don't have to watch every single one of them. Especially the clickbaits.

# Requirements:
- Windows or Linux machine with [python](https://www.python.org/) installed
- Google Bard authentication token, [click here](https://github.com/dsdanielpark/Bard-API#readme) and read under "Authentication"
- Active working internet connection

# Installation:
### For Windows, 
   download the ```YT-Gist-Win.zip``` from the latest releases, or click here
### For Linux, 
   download the ```YT-Gist-Lin.tar.gz``` from the latest releases, or click here

# Setup:
- Make sure you have Python installed on your machine, check using:
  ```
  
  python --version
  ```
- On Windows,
  - run the ```setup.bat``` file by double clicking on it
  
- On Linux, 
  - make the ```setup.sh``` file executable by the following command:
  ```
  chmod +x setup.sh
  ```
  - run the ```setup.sh``` file by the following command:
  ```
  
  ./setup.sh
  ```
  
## Bard Token
> **Warning** Do not expose the `__Secure-1PSID` 
1. Visit https://bard.google.com/
2. F12 for console
3. Session: Application → Cookies → Copy the value of  `__Secure-1PSID` cookie
4. Paste the token as is in the ```token.txt``` file.
  
# Usage
## Single use
   - On Windows, open a Command Prompt in the extracted directory and run:
   ```
   
   summ -u {url}
   ```
   replace {url} with the url of the video, for example
   ```summ -u https://youtu.be/DMQWirkx5EY```
   - On Linux, open a Terminal in the extracted directory and run:
   ```
   
   ./summ -u {url}
   ```
   replace {url} with the url of the video, for example
   ```summ -u ttps://youtu.be/fuWPuJZ9NcU```
    
## Application mode
   - On Windows, double click on the ```sum.bat``` file and keep entering the url when prompted.
