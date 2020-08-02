def speaker_level_df(df):
    """Returns DataFrame with a row per each speaker."""
    dlist = []
    # get number of speakers
    for row in df.itertuples():
        num_spk = []
        speakers = [None, None, None, None, None, None,]
        occupations = [None, None, None, None, None, None,]
        about_speakers = [None, None, None, None, None, None,]
        try:
            if isinstance(row.all_speakers, dict):
                num_spk.append(len(row.all_speakers))
                speakers = row.all_speakers
            if isinstance(row.occupations, dict):
                num_spk.append(len(row.occupations))
                occupations = row.occupations
            if isinstance(row.about_speakers, dict):
                num_spk.append(len(row.about_speakers))
                about_speakers = row.about_speakers
            else:
                num_spk = [1]
                speakers = [row.speaker_1]
        except:
            speakers = [row.speaker_1]
        max_spk = max(num_spk)
        for i in range(max_spk):
            try:
                if row.photo_urls[i] == '':
                    photo_urls = [None, None, None, None, None, None,]
                else:
                    photo_urls = row.photo_urls
                row_dict = {'talk_id': row.talk_id,
                            'speaker': speakers[i],
                            'occupation': occupations[i], 
                            'about_speaker': about_speakers[i],
                            'photo_url': photo_urls[i]}
                dlist.append(row_dict)
            except:
                row_dict = {'talk_id': row.talk_id,
                            'speaker': speakers[i],
                            'occupation': occupations[i], 
                            'about_speaker': about_speakers[i],
                            'photo_url': None}
                dlist.append(row_dict)
    return pd.DataFrame(dlist)


# merged_df = pd.merge(spk_df, df, how='left', on='talk_id')