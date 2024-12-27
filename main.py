import requests
import json
import pandas as pd

# Base URL for the API
base_url = "https://api2.quranwbw.com/v1/chapter?chapter={}&word_type=1&word_translation=6&word_transliteration=1&verse_translation=1%2C3&version=125"

# Function to get data from the API for each chapter
def get_chapter_data(chapter_number):
    url = base_url.format(chapter_number)
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Function to extract and format data from the API response
def extract_verse_data(chapter_data):
    verses = []
    for verse_key, verse_info in chapter_data['data']['verses'].items():
        meta = verse_info['meta']
        words = verse_info['words']
        translations = verse_info['translations']

        arabic_words = words['arabic'].split('||')
        translation_words = words['translation'].split('||')
        transliteration_words = words['transliteration'].split('||')
        line_numbers = words['line'].split('||')
        # https://audios.quranwbw.com/words/2/002_001_001.mp3?version=2
        
        # Ensure we have the same number of words and line numbers
        if len(arabic_words) == len(translation_words) == len(transliteration_words) == len(line_numbers):
            for i in range(len(arabic_words)):
                verse_data = {
                    'chapter': meta['chapter'],
                    'verse': meta['verse'],
                    #'page': meta['page'],
                    #'juz': meta['juz'],
                    #'hizb': meta['hizb'],
                    #'manzil': meta['manzil'],
                    #'ruku': meta['ruku'],
                    'arabic': arabic_words[i],
                    'translation': translation_words[i],
                    'transliteration': transliteration_words[i],
                    #'line': line_numbers[i],
                    #'translations': '; '.join([t['text'] for t in translations]),
                    'word_order': i + 1,  # Word order is index + 1,
                    'sound_url': f"https://audios.quranwbw.com/words/{meta['chapter']}/{meta['chapter']:03d}_{meta['verse']:03d}_{i+1:03d}.mp3?version=2"
                }

                verse_data['sound_url'] = verse_data['sound_url'].replace(r'\/', '/')
                print(verse_data['sound_url'])
                verses.append(verse_data)
        else:
            # Handle the case where words and other fields do not match in length
            print(f"Warning: Mismatch in word counts for verse {verse_key}")
    
    return verses

# Loop through chapters 1 to 114 and collect data
all_verses = []
for chapter in range(1, 115):  # Change range as needed for multiple chapters
    chapter_data = get_chapter_data(chapter)
    if chapter_data:
        verses = extract_verse_data(chapter_data)
        all_verses.extend(verses)

# Create a pandas DataFrame
df = pd.DataFrame(all_verses)

# unique df by arabic
df_unique = df.drop_duplicates(subset=['arabic'])

# Display the DataFrame
print(df.head())

# to json dump json.dumps(df.to_dict('records')))
dict = df.to_dict('records')
dict_unique = df_unique.to_dict('records')

# to file
with open('data.json', 'w') as f:
    json.dump(dict, f)

with open('data_unique.json', 'w') as f:
    json.dump(dict_unique, f)

