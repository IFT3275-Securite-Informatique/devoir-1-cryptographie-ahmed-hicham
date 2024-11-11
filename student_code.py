import requests
from collections import Counter

# Charge les textes à partir des URLs
def load_texts_from_urls(urls):
  corpus = ""
  for url in urls:
      try:
          response = requests.get(url)
          response.raise_for_status()
          corpus += response.text
      except requests.exceptions.RequestException as e:
          print(f"Erreur lorsqu'on charge: {url}: {e}")
  return corpus

# Fréquence des symboles
def count_symbol_frequency(corpus, symbols):
  frequency_table = Counter()
  for char in corpus:
      if char in symbols:
          frequency_table[char] += 1
  return dict(frequency_table)

# Fréquence des séquences de bytes
def count_byte_sequence_frequency(C):
  byte_sequences = [C[i:i + 8] for i in range(0, len(C), 8)]
  frequency_table = Counter(byte_sequences)
  return dict(frequency_table)

def get_frequency_symbol(item):
  return item[1]


def get_frequency_bit(item):
  return item[1]


# Mapping des séquences de bytes aux symboles
def map_frequencies(symbol_freq, bit_freq):
  # Trier les symboles par fréquence décroissante
  sorted_symbols = sorted(symbol_freq.items(), key=get_frequency_symbol, reverse=True)
  
  # Trier les séquences de bits par fréquence décroissante
  sorted_bits = sorted(bit_freq.items(), key=get_frequency_bit, reverse=True)

  # Créer le dictionnaire de correspondance entre séquences de bits et symboles
  mapping = {}
  for (symbol, _), (bit_sequence, _) in zip(sorted_symbols, sorted_bits):
      mapping[bit_sequence] = symbol

  return mapping


# Décode le cryptogramme en utilisant le mapping
def decode_cryptogram(C, mapping):
  bit_sequences = [C[i:i + 8] for i in range(0, len(C), 8)]
  decoded_text = ""
  for bit_sequence in bit_sequences:
      decoded_text += mapping.get(bit_sequence, '?')
  return decoded_text

# Découpe le texte en paires de caractères (Fonction fournie)
def cut_string_into_pairs(text):
  pairs = []
  for i in range(0, len(text) - 1, 2):
      pairs.append(text[i:i + 2])
  if len(text) % 2 != 0:
      pairs.append(text[-1] + '_')
  return pairs

def decrypt(C):
  urls = [
      "https://www.gutenberg.org/ebooks/13846.txt.utf-8",
      "https://www.gutenberg.org/ebooks/4650.txt.utf-8",
      "https://www.gutenberg.org/cache/epub/69794/pg69794.txt",
      "https://www.gutenberg.org/cache/epub/18092/pg18092.txt",
      "https://www.gutenberg.org/cache/epub/22813/pg22813.txt",
      "https://www.gutenberg.org/cache/epub/13704/pg13704.txt",
      "https://www.gutenberg.org/cache/epub/66927/pg66927.txt",
      "https://www.gutenberg.org/cache/epub/63267/pg63267.txt",
      "https://www.gutenberg.org/cache/epub/17808/pg17808.txt",
      "https://www.gutenberg.org/cache/epub/16901/pg16901.txt",
      "https://www.gutenberg.org/cache/epub/33378/pg33378.txt"
  ]

  #symboles = ['b', 'j', '\r', 'J', '”', ')', 'Â', 'É', 'ê', '5', 't', '9', 'Y', '%', 'N', 'B', 'V', '\ufeff', 'Ê', '?', '’', 'i', ':', 's', 'C', 'â', 'ï', 'W', 'y', 'p', 'D', '—', '«', 'º', 'A', '3', 'n', '0', 'q', '4', 'e', 'T', 'È', '$', 'U', 'v', '»', 'l', 'P', 'X', 'Z', 'À', 'ç', 'u', '…', 'î', 'L', 'k', 'E', 'R', '2', '_', '8', 'é', 'O', 'Î', '‘', 'a', 'F', 'H', 'c', '[', '(', "'", 'è', 'I', '/', '!', ' ', '°', 'S', '•', '#', 'x', 'à', 'g', '*', 'Q', 'w', '1', 'û', '7', 'G', 'm', '™', 'K', 'z', '\n', 'o', 'ù', ',', 'r', ']', '.', 'M', 'Ç', '“', 'h', '-', 'f', 'ë', '6', ';', 'd', 'ô', 'e ', 's ', 't ', 'es', ' d', '\r\n', 'en', 'qu', ' l', 're', ' p', 'de', 'le', 'nt', 'on', ' c', ', ', ' e', 'ou', ' q', ' s', 'n ', 'ue', 'an', 'te', ' a', 'ai', 'se', 'it', 'me', 'is', 'oi', 'r ', 'er', ' m', 'ce', 'ne', 'et', 'in', 'ns', ' n', 'ur', 'i ', 'a ', 'eu', 'co', 'tr', 'la', 'ar', 'ie', 'ui', 'us', 'ut', 'il', ' t', 'pa', 'au', 'el', 'ti', 'st', 'un', 'em', 'ra', 'e,', 'so', 'or', 'l ', ' f', 'll', 'nd', ' j', 'si', 'ir', 'e\r', 'ss', 'u ', 'po', 'ro', 'ri', 'pr', 's,', 'ma', ' v', ' i', 'di', ' r', 'vo', 'pe', 'to', 'ch', '. ', 've', 'nc', 'om', ' o', 'je', 'no', 'rt', 'à ', 'lu', "'e", 'mo', 'ta', 'as', 'at', 'io', 's\r', 'sa', "u'", 'av', 'os', ' à', ' u', "l'", "'a", 'rs', 'pl', 'é ', '; ', 'ho', 'té', 'ét', 'fa', 'da', 'li', 'su', 't\r', 'ée', 'ré', 'dé', 'ec', 'nn', 'mm', "'i", 'ca', 'uv', '\n\r', 'id', ' b', 'ni', 'bl']
  corpus = load_texts_from_urls(urls)
  caracteres = list(set(list(corpus)))
  nb_caracteres = len(caracteres)
  nb_bicaracteres = 256 - nb_caracteres
  bicaracteres = [item for item, _ in Counter(cut_string_into_pairs(corpus)).most_common(nb_bicaracteres)]
  symboles = bicaracteres + caracteres

  # Analyse de fréquence
  symbol_frequency = count_symbol_frequency(corpus, symboles)
  bit_sequence_frequency = count_byte_sequence_frequency(C)

  # Mapping et décodage
  mapping = map_frequencies(symbol_frequency, bit_sequence_frequency)
  M = decode_cryptogram(C, mapping)
  return M
