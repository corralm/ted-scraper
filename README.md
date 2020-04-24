# TED-Talks-Scraper
Scrape TED talk data including transcripts in over 100 languages from TED.com

## Requirements
[Python 3](https://www.python.org/downloads/)  
[BeautifulSoup 4](https://pypi.org/project/beautifulsoup4/)

## Usage
```python
# instantiate the scraper
scraper = TEDscraper(lang_code='en', urls='all', exclude_transcript=False)

# scrape the data
ted_dict = scraper.get_data()

# transform dict to pandas DataFrame
df = pd.DataFrame.from_dict(ted_dict, orient='index')

# output as CSV
df.to_csv('../data/ted_talks.csv', index=False)
```
Here is a list of other output formats [Pandas docs](https://pandas.pydata.org/pandas-docs/stable/reference/frame.html#serialization-io-conversion).

### Parameters
* **Languages**
    * English is the default language `lang_code='en'`
    * You can pass in other language codes using the `lang_code` param
    * TED translators don't always translate all features
        * Ex: Title and 'About Speaker' might be in English while the transcript is translated to French
* **URLs** 
    * All urls are scraped by default for the selected language `urls='all'`
    * You may pass in a list of urls using the `urls` param. However, there are a few limitations:
        * TED must have the talks available in the language you specify
        * Only one language can be provided per scrape call
* **Features**
    * All features are scraped by default
    * You can exclude scraping the transcript by setting `exclude_transcript` to 'True'

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
TED talks have been subtitled in over 100 languages. Here are the top languages:

| Code  | Language              |
|-------|-----------------------|
| en    | English               |
| es    | Spanish               |
| pt-br | Portuguese (Brazil)   |
| fr    | French                |
| it    | Italian               |
| zh-cn | Chinese (simplified)  |
| zh-tw | Chinese (traditional) |
| ko    | Korean                |
| ja    | Japanese              |
| tr    | Turkish               |
| ru    | Russian               |
| he    | Hebrew                |

Here is a link to [all language codes available as of April 2020](../data/languages.csv).

You can see all the talks for each language at [TED – Our Languages](https://www.ted.com/participate/translate/our-languages 'TED languages').

## Acknowledgements
The data has been scraped from the official TED Website and is available under the Creative Commons License.
