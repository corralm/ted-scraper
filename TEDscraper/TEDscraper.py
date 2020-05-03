#!/usr/bin/env python
# coding: utf-8

# # TEDscraper Notebook

# In[ ]:


import pandas as pd
import re

import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random

import pickle


# ## Soup Maker

# In[ ]:


class SoupMaker:
    """Make soup objects and put your machine to sleep."""
    

    def sleep_short(self):
        """Suspends execution time between 0 - .2 seconds."""
        return time.sleep(random.uniform(0, .2))

    def sleep_two(self):
        """Suspends execution time between .5 - 2 seconds."""
        return time.sleep(random.uniform(.5, 2))
    
    def sleep_five(self):
        """Suspends execution time between 3 - 5 seconds."""
        return time.sleep(random.uniform(3, 5))

    def make_soup(self, url):
        """Returns soup object from a URL."""
        # generate random user-agent
        user_agent = {'User-agent': UserAgent().random}
        # request page and make soup
        page = requests.get(url, headers=user_agent)
        soup = BeautifulSoup(page.content, 'lxml')
        return soup


# ## CreateCSV

# In[ ]:


class CreateCSV(SoupMaker):
    """Create CSVs of TED topics and languages."""


    def create_topics_csv(self):
        """Creates CSV of all topics available from TED."""
        soup = self.make_soup('https://www.ted.com/topics')
        topic_list = []
        topic_tag = soup.find_all(class_='d:b', style='line-height:3;')
        for tag in topic_tag:
            topic = re.sub(r'\s+', '', tag.text)
            topic_list.append(topic)
        topics_series = pd.Series(topic_list, name='Topic')
        topics_series.to_csv('../data/topics.csv', index=False)

    def create_languages_csv(self):
        """Creates CSV of all language codes supported by TED."""
        lang_url = 'https://www.ted.com/participate/translate/our-languages'
        soup = self.make_soup(lang_url)
        lang_list = []
        lang_tags = soup.find_all('div', class_='h9')
        for tag in lang_tags:
            if tag.a == None:
                continue
            else:
                lang_code = re.search(r'(?<=\=)[\w-]+', tag.a['href']).group(0)
                lang_name = tag.text
                lang_list.append([lang_code] + [lang_name])
        lang_df = pd.DataFrame(data=lang_list, columns=['lang_code', 'language'])
        lang_df.to_csv('../data/languages.csv', index=False)
        
    def create_dataset(self, DataFrame):
        """Creates CSV from a DataFrame."""
        pass


# ## Talk Features

# In[ ]:


class TalkFeatures(SoupMaker):
    """Class to get TED talk features."""


    def get_talk_id(self, soup):
        """Returns the talk_id provided by TED."""
        talk_id = re.search(r"(?<=\"current_talk\":)\"(\d+)\"", soup.text).group(1)
        return talk_id

    def get_title(self, soup):
        """Returns the title of the talk."""
        title_tag = soup.find(attrs={'name': 'title'}).attrs['content']
        tag_list = title_tag.split(':')
        title = ":".join(tag_list[1:]).lstrip()
        return title

    def get_speaker_1(self, soup):
        """Returns the first speaker in TED's speaker list."""
        speaker_tag = re.findall(r"(?<=\"speakers\":).*?\"}]", soup.text)[0]
        # convert to DataFrame
        speakers_df = pd.read_json(speaker_tag)
        full_name_raw = (speakers_df.loc[:, 'firstname'] + ' '
                     + speakers_df.loc[:, 'middleinitial'] + ' '
                     + speakers_df.loc[:, 'lastname'])
        full_name_clean = full_name_raw.str.replace('\s+', ' ')
        # transform series to a dict
        speaker_1 = full_name_clean.iloc[0]
        return speaker_1

    def get_all_speakers(self, soup):
        """Returns dict of all speakers per talk."""
        speaker_tag = re.findall(r"(?<=\"speakers\":).*?\"}]", soup.text)[0]
        # convert to DataFrame
        speakers_df = pd.read_json(speaker_tag)
        full_name_raw = (speakers_df.loc[:, 'firstname'] + ' '
                     + speakers_df.loc[:, 'middleinitial'] + ' '
                     + speakers_df.loc[:, 'lastname'])
        full_name_clean = full_name_raw.str.replace('\s+', ' ')
        # transform series to a dict
        speakers = full_name_clean.to_dict()
        return speakers

    def get_occupations(self, soup):
        """Returns list of the occupation(s) of the speaker(s) per talk."""
        occupations_tag = re.findall(r"(?<=\"speakers\":).*?\"}]", soup.text)[0]
        # convert json to DataFrame
        occupations_series = pd.read_json(occupations_tag)['description']
        if occupations_series.all():
            # clean and create dict
            occupations = occupations_series.str.lower().str.split(', ')
            occupations = occupations.to_dict()
        else:
            occupations = None
        return occupations

    def get_about_speakers(self, soup):
        """Returns dict with each 'About the Speaker' blurb per talk."""
        speaker_tag = re.findall(r"(?<=\"speakers\":).*?\"}]", soup.text)[0]
        # convert to DataFrame
        about_series = pd.read_json(speaker_tag)['whotheyare']
        if about_series.all():
            # transform series to a dict
            about_speakers = about_series.to_dict()
        else:
            about_speakers = None
        return about_speakers

    def get_views(self, soup):
        """Returns viewed count per talk."""
        view_count = re.search(r"(?<=\"viewed_count\":)\d+", soup.text).group(0)
        return view_count

    def get_recorded_date(self, soup):
        """Returns date a talk was recorded."""
        recorded_at = re.search(r"(?<=\"recorded_at\":\")[\d-]+", soup.text).group(0)
        return recorded_at

    def get_published_date(self, soup):
        """Returns date a talk was published in TED.com."""
        published_raw = soup.find(attrs={'itemprop': 'uploadDate'}).attrs['content']
        published_date = re.search(r"[\d-]+", published_raw).group(0)
        return published_date

    def get_event(self, soup):
        """Returns name of the event in which the talk was given."""
        event = re.search(r"(?<=\"event\":)\"(.*?)\"", soup.text).group(1)
        return event
    
    def get_native_lang(self, soup):
        """Returns native language code for each talk as a string."""
        native_lang = re.search(r'(?<=nativeLanguage\":)\"(.*?)\"', soup.text).group(1)
        return native_lang
    
    def get_available_lang(self, soup):
        """Returns list of all available languages (lang codes) for a talk."""
        languages = re.findall(r'(?<=languageCode\":)\"(.*?)\"', soup.text)
        clean_lang = sorted(list(set(languages)))
        return clean_lang

    def get_comments_count(self, soup):
        """Return the count of comments per talk."""
        try:
            comments_count = re.search(r"(?<=\"count\":)(\d+)", soup.text).group(1)
        except AttributeError:
            comments_count = None
        return comments_count

    def get_duration(self, soup):
        """Returns duration of a talk in seconds."""
        duration =  re.search(r"(?<=\"duration\":)(\d+)", soup.text).group(1)
        return duration

    def get_topics(self, soup):
        """Returns list of tags (topics) per talk."""
        match_obj = re.search(r"\"tag\":\"(.*?)\"", soup.text)
        topics = match_obj.group(1).split(',')
        return topics

    def get_related_talks(self, soup):
        """Returns dict (keys: id & title) of related talks."""
        related_tag = re.search(r"(?<=\"related_talks\":).*?]", soup.text).group(0)
        related_sr = pd.read_json(related_tag)
        related_talks = dict(zip(related_sr['id'], related_sr['title']))
        return related_talks

    def get_talk_url(self, soup):
        """Returns url for each talk as a string."""
        talk_tag = soup.find(attrs={'property': 'og:url'}).attrs['content']
        talk_url = talk_tag.split('transcript')[0]
        return talk_url

    def get_description(self, soup):
        """Returns description of the talk."""
        desc_tag = soup.find(attrs={'property': 'og:description'}).attrs['content']
        talk_desc = desc_tag.split(': ', 1)[1]
        return talk_desc

    def get_transcript(self, soup):
        """Returns talk's transcript as a single string.""" 
        transcript = ''
        transcript_strings = []
        for div in soup.find_all('div', class_="Grid__cell flx-s:1 p-r:4"):
            for p in div.find_all('p'):
                # add every string in the transcript to a list
                transcript_strings.append(" ".join(p.text.split()))
            else:
                # after all strings have been added, create a single transcript string
                transcript = " ".join(transcript_strings)
        return transcript


# ## URLs

# In[ ]:


class URLs(SoupMaker):
    """Get and process urls to scrape."""

    
    def topics_url_param(self):
        """Returns string of the url query from topics parameter."""
        topics_param = ''
        if self.topics != 'all':
            if isinstance(self.topics, list):
                for topic in self.topics:
                    topics_param += ('&topics[]=' + topic)
            else:
                raise ValueError("'topics' param needs to be a list")
        return topics_param

    def get_max_page(self):
        """Returns max pagination number from www.ted.com/talks."""
        page_num = [1]
        # make soup from ted.com/talks with specified language
        soup = self.make_soup(self.base_url + '&page=1&sort=newest')
        # iterate through each pagination element and get the max
        page_elem = soup.find_all('a', class_='pagination__item pagination__link')
        for element in page_elem:
            page_num.append(int(element.text))
        return max(page_num)
    
    def get_all_url_paths(self):
        """Returns list of all the talk url paths available in www.ted.com/talks"""
        url_path_list = []
        # construct url with lang code specified by the user
        talks_url = (self.base_url + '&page=')
        # set range from 1 to the max page in the pagination element
        page_range = range(1, self.get_max_page()+1)
        # iterate through each page and get the url for each talk
        for i in page_range:
            # try a second attempt if first attempt fails
            for attempt in range(2):
                try:
                    talks_page_url = talks_url + str(i) + '&sort=newest'
                    soup = self.make_soup(talks_page_url)
                    # delay between searches
                    self.sleep_short()
                    for div in soup.find_all('div', attrs={'class': 'media__image'}):
                        for a in div.find_all('a'):
                            url_path_list.append(a.get('href'))
                except:
                    # delay before continuing to second attempt
                    self.sleep_two()
                # break from attempts loop if no exceptions are raised
                else:
                    break
        return url_path_list

    def get_all_urls(self):
        """Returns list of complete urls for each talk's transcript page."""
        # '/talks/jen_gunter_why_can_t_we_talk_about_periods?language=fa'
        url_list = []
        for url in self.get_all_url_paths():
            url_list.append(('https://www.ted.com'
                             + url.replace(
                                 # to replace
                                 '?language=' + self.lang_code,
                                 # replace with
                                 '/transcript' + '?language=' + self.lang_code)
                            ))
        return url_list
    
    def clean_urls(self, urls):
        """Returns list of clean urls from urls the user inputs."""
        clean_urls = []
        for idx, url in enumerate(urls):
            if url.startswith('https://www.ted.com/talks'):
                parts = url.split('/')
                joined = '/'.join(parts[:5])
                clean = joined.split('?')
                lang = clean[0] + '/transcript?language=' + self.lang_code
                topic = lang + self.topics_url_param()
                clean_urls.append(lang)
            else:
                print(f'bad url @ {idx} >> {url}')
                continue
        return clean_urls
    
    def url_issues(self):
        """Returns DataFrame of urls with known issues."""
        issues_df = pd.read_csv('../data/urls_issues.csv')
        return issues_df
    
    def remove_urls_with_issues(self):
        """Remove urls with known issues to prevent unnecessary scraping."""
        urls = self.url_attribute()
        final_urls = []
        removed_urls = []
        removed_counter = 0
        issues_df = pd.read_csv('../data/urls_issues.csv')
        for url in urls:
            try:
                base_url = url.replace('transcript?language=' + self.lang_code, '')
                # is base url in the issues df?
                url_in_issues = (issues_df['url'] == base_url).any()
                # get the lang_codes of the base_url
                langs = issues_df.loc[issues_df['url'] == base_url, 'lang_code']
                # check if the url in issues_df
                if not url_in_issues:
                    final_urls.append(url)
                # if the url is in issues_df, check if it's for the same lang_code
                elif self.lang_code in langs.any():
                    removed_urls.append(url)
                    removed_counter += 1
                    continue
                else:
                    final_urls.append(url)
            except:
                removed_urls.append(url)
                removed_counter += 1
                continue
        if removed_urls:
            print(f"Removed the following {removed_counter} urls as they have "
                  "known issues:\n", removed_urls, end='\n\n')
        return final_urls


# ## TEDscraper

# In[ ]:


class TEDscraper(TalkFeatures, URLs):
    """Gets urls and scrapes TED talk data in the specified language.

    Attributes:
        lang_code (str): Language code. Defaults to 'en'.
        language (str): Language name derived from lang_code.
        urls (list): URLs of talks. Defaults to 'all'.
        topics (list): Talk topics. Defaults to 'all'.
        exclude (bool): Exclude transcript. Defaults to False.
        ted_dict (dict): Dict to store ted talk features after scraping.
        dict_id (int): Index of nested dict in 'ted_dict'.
        failed_counter: Counts urls that failed to get scraped.
    """
    

    def __init__(self, lang_code='en', urls='all', topics='all',
                 force_fetch = False, exclude_transcript=False):
        self.lang_code = lang_code
        self.language = self.convert_lang_code()
        self.urls = urls
        self.topics = topics
        self.exclude = exclude_transcript
        self.ted_dict = {}
        self.dict_id = 0
        self.failed_counter = 0
        self.failed_urls = []
        self.force_fetch = force_fetch
        self.base_url = ('https://www.ted.com/talks'
                         + '?language=' + self.lang_code
                         + self.topics_url_param())
        
    def url_attribute(self):
        """Define urls attribute based on parameter 'urls'."""
        # define url attribute
        if self.urls == 'all':
            urls = self.get_all_urls()
        else:
            if isinstance(self.urls, list):
                urls = self.clean_urls(self.urls)
            else:
                raise ValueError("'urls' param needs to be a list")
        return urls

    def convert_lang_code(self):
        """Reads languages.csv and returns language.
        Parameters:
            lang_code (str): Language code
        """
        df = pd.read_csv('../data/languages.csv')
        lang_series = df.loc[(df['lang_code'] == self.lang_code), 'language']
        language = lang_series.values[0]
        return language
    
    def scrape_all_features(self, soup):
        """Scrapes all features to a nested dict."""
        # create nested dict
        self.ted_dict[self.dict_id] = {}
        nested_dict = self.ted_dict[self.dict_id]
        # add the features to the nested dict
        nested_dict['talk_id'] = self.get_talk_id(soup)
        nested_dict['title'] = self.get_title(soup)
        nested_dict['speaker_1'] = self.get_speaker_1(soup)
        nested_dict['all_speakers'] = self.get_all_speakers(soup)
        nested_dict['occupations'] = self.get_occupations(soup)
        nested_dict['about_speakers'] = self.get_about_speakers(soup)
        nested_dict['views'] = self.get_views(soup)
        nested_dict['recorded_date'] = self.get_recorded_date(soup)
        nested_dict['published_date'] = self.get_published_date(soup)
        nested_dict['event'] = self.get_event(soup)
        nested_dict['native_lang'] = self.get_native_lang(soup)
        nested_dict['available_lang'] = self.get_available_lang(soup)
        nested_dict['comments'] = self.get_comments_count(soup)
        nested_dict['duration'] = self.get_duration(soup)
        nested_dict['topics'] = self.get_topics(soup)
        nested_dict['related_talks'] = self.get_related_talks(soup)
        nested_dict['url'] = self.get_talk_url(soup)
        nested_dict['description'] = self.get_description(soup)
        # add transcript if param is set to False (default)
        if not self.exclude:
            nested_dict['transcript'] = self.get_transcript(soup)
        return nested_dict

    def get_data(self):
        """Returns nested dictionary of features from each talk's transcript page."""
        print("Fetching urls...\n")
        # define url attribute
        if self.force_fetch:
            urls = self.url_attribute()
        else:
            urls = self.remove_urls_with_issues()
        print(f"Scraping {len(urls)} TED talks in '{self.language}'...")
        print(f"Estimated time to complete is {round((.9*len(urls)/60), 1)} minutes\n")
        # iterate through each ted talk transcript url
        for url in urls:
            # make soup
            soup = self.make_soup(url)
            # taste soup
            taster = soup.title.text
            bad_soup = re.search(r'404: Not Found', taster)
            if bad_soup:
                print(f"[BAD_SOUP] {self.lang_code} {url}")
                self.failed_urls.append(url)
                self.failed_counter += 1
                continue
            # delay between searches
            self.sleep_short()
            # try up to three attempts to scrape data
            for attempt in range(1, 3+1):
                try:
                    # create nested dict
                    self.ted_dict[self.dict_id] = {}
                    # scrape features and add to a nested dict
                    self.scrape_all_features(soup)
                    # indicate successful scrape
                    print(f"[OK] {self.dict_id} {url}")
                    # add 1 to create a new nested dict
                    self.dict_id += 1
                except Exception as e:
                    # if the last attempt fails, update the failed counter
                    # and print the exception & talk url
                    if attempt == 3:
                        self.failed_counter += 1
                        self.failed_urls.append(url)
                        print(f"[EXCEPTION] {e} {url}")
                        continue
                    # delay before another attempt
                    self.sleep_five()
                # break if no exceptions are raised
                else:
                    break
        print(f"""\nTed.com scraping results:
            \n\t• Successful: {self.dict_id}
            \n\t• Failed: {self.failed_counter}\n""")
        if self.failed_counter:
            print(f"Failed to scrape:\n{self.failed_urls}\n")
        return self.ted_dict
    
    def to_dataframe(self, ted_dict):
        """Creates DataFrame object from dict."""
        df = pd.DataFrame.from_dict(ted_dict, orient='index')
        return df


# # Get Data

# In[ ]:


# # english
# scraper_en = TEDscraper()
# ted_dict = scraper_en.get_data()