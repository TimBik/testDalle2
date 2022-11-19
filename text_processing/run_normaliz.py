# Работа с нормализацией текста
import normaliz
import json
with open('songs_info.json', 'r', encoding="utf-8") as j:
    json_data = json.load(j)

text_normalizer = normaliz.TextNormalizer()
for song in json_data['songs_info']:
    text = song['text']
    normalized = text_normalizer.normalize(text)
    song['significant_words'] = normalized.get_significant_words()

with open('songs_info_words.json', 'w', encoding="utf8") as file:
    json.dump(json_data, file, ensure_ascii=False)
