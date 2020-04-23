# TED-Talks-Scraper
💬 scrape transcripts &amp; other features from your favorite TED talks

## Features

| Feature          | Description                                   | Data Type  |
|------------------|-----------------------------------------------|------------|
| talk_id          | Talk identification number provided by TED    | int        |
| title            | Title of the talk                             | string     |
| speakers         | Speakers in the talk (may be multiple)        | dictionary |
| occupations      | *Occupations of the speakers (may be multiple) | dictionary |
| about_speakers   | *Blurb about each speaker (may be multiple)    | dictionary |
| views            | Count of views                                | int        |
| recorded_date    | Date the talk was recorded                    | string     |
| published_date   | Date the talk was published to TED.com        | string     |
| event            | Event or medium in which the talk was given   | string     |
| native_lang      | Language the talk was given in                | string     |
| available_lang   | All available languages for a talk            | list       |
| comments         | Count of comments                             | int        |
| duration         | Duration in %M%S format                       | string     |
| duration_sec     | Duration in seconds                           | int        |
| topic_tags       | Related tags or topics for the talk           | list       |
| talk_description | Description of the talk                       | string     |
| related_talks    | Related talks                                 | dictionary |
| talk_url         | Url of the talk                               | string     |
| transcript       | Full transcript of the talk                   | string     |

*The dictionary key maps to the speaker in ‘speakers’.

## Languages
TED talks have been subtitled in over 100 languages. You can see the most updated list of talks [here](https://www.ted.com/participate/translate/our-languages 'TED languages').

Below is a list of languages available:  

| code       | language              |
|------------|-----------------------|
| af         | Afrikaans             |
| sq         | Albanian              |
| arq        | Algerian Arabic       |
| am         | Amharic               |
| ar         | Arabic                |
| hy         | Armenian              |
| as         | Assamese              |
| ast        | Asturian              |
| az         | Azerbaijani           |
| eu         | Basque                |
| be         | Belarusian            |
| bn         | Bengali               |
| bi         | Bislama               |
| bs         | Bosnian               |
| bg         | Bulgarian             |
| my         | Burmese               |
| ca         | Catalan               |
| ceb        | Cebuano               |
| zh-cn      | Chinese, Simplified   |
| zh-tw      | Chinese, Traditional  |
| zh         | Chinese, Yue          |
| ht         | Creole, Haitian       |
| hr         | Croatian              |
| cs         | Czech                 |
| da         | Danish                |
| nl         | Dutch                 |
| dz         | Dzongkha              |
| en         | English               |
| eo         | Esperanto             |
| et         | Estonian              |
| fil        | Filipino              |
| fi         | Finnish               |
| fr         | French                |
| fr-ca      | French (Canada)       |
| gl         | Galician              |
| ka         | Georgian              |
| de         | German                |
| el         | Greek                 |
| gu         | Gujarati              |
| cnh        | Hakha Chin            |
| ha         | Hausa                 |
| he         | Hebrew                |
| hi         | Hindi                 |
| hu         | Hungarian             |
| hup        | Hupa                  |
| is         | Icelandic             |
| ig         | Igbo                  |
| id         | Indonesian            |
| inh        | Ingush                |
| ga         | Irish                 |
| it         | Italian               |
| ja         | Japanese              |
| kn         | Kannada               |
| kk         | Kazakh                |
| km         | Khmer                 |
| tlh        | Klingon               |
| ko         | Korean                |
| ku         | Kurdish               |
| ky         | Kyrgyz                |
| lo         | Lao                   |
| ltg        | Latgalian             |
| la         | Latin                 |
| lv         | Latvian               |
| lt         | Lithuanian            |
| lb         | Luxembourgish         |
| rup        | Macedo                |
| mk         | Macedonian            |
| mg         | Malagasy              |
| ms         | Malay                 |
| ml         | Malayalam             |
| mt         | Maltese               |
| mr         | Marathi               |
| mfe        | Mauritian Creole      |
| mn         | Mongolian             |
| srp        | Montenegrin           |
| ne         | Nepali                |
| nb         | Norwegian Bokmal      |
| nn         | Norwegian Nynorsk     |
| oc         | Occitan               |
| ps         | Pashto                |
| fa         | Persian               |
| pl         | Polish                |
| pt         | Portuguese            |
| pt-br      | Portuguese, Brazilian |
| pa         | Punjabi               |
| ro         | Romanian              |
| ru         | Russian               |
| ry         | Rusyn                 |
| sc         | Sardinian             |
| sr         | Serbian               |
| sh         | Serbo-Croatian        |
| szl        | Silesian              |
| si         | Sinhala               |
| sk         | Slovak                |
| sl         | Slovenian             |
| so         | Somali                |
| es         | Spanish               |
| sw         | Swahili               |
| sv         | Swedish               |
| art-x-bork | Swedish Chef          |
| tl         | Tagalog               |
| tg         | Tajik                 |
| ta         | Tamil                 |
| tt         | Tatar                 |
| te         | Telugu                |
| th         | Thai                  |
| bo         | Tibetan               |
| aeb        | Tunisian Arabic       |
| tr         | Turkish               |
| tk         | Turkmen               |
| uk         | Ukrainian             |
| ur         | Urdu                  |
| ug         | Uyghur                |
| uz         | Uzbek                 |
| vi         | Vietnamese            |