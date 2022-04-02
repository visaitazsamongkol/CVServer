# How to run server

- Register Merriam-Webster's free APIs: [Link](https://dictionaryapi.com "Merriam-webster") (choosing Collegiate Dicionary and Collegiate Thesaurus APIs)
- Fill both API keys in a new file:'**server/merriam-webster-key.txt**' using the following format

    ![image](https://user-images.githubusercontent.com/47115113/158423520-c43a0f9d-8de7-447a-bfa4-ce251db1ed15.png)
- Initialize backend APIs by running '**server/app.py**'

<br />

# Testing APIs

### OCR API (route: /ocr)
- request = fill key: image and value: {uploaded .jpg file} in form-data body
- response = list of word and base64 string type of words-bounding-box image

### Dictionary and Thesaurus Search APIs (route: /search/dictionary and /search/thesaurus)
- request = fill list of word in JSON body 
- response = dict whose key is each word and value is descriptions of that word (may have more than one description if that word has many parts of speech)
