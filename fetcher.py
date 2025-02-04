import csv
import time
from googletrans import Translator
import asyncio
def generate_audio(word, output_dir):
    """Generate an audio file for the Polish pronunciation."""
    try:
        tts = gTTS(word, lang="en")
        audio_path = os.path.join(output_dir, f"{word}.mp3")
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        print(f"Error generating audio for '{word}': {e}")
        return None

def load_words_from_txt(file_path):
    """Load words from a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        words = [line.strip() for line in file.readlines() if line.strip()]
    return words


async def translate_word(translator, word, src_lang='en', dest_lang='pl'):
    """Translate a single word asynchronously."""
    try:
        translated = await translator.translate(word, src=src_lang, dest=dest_lang)
        return word, translated.text
    except Exception as e:
        print(f"Error translating {word}: {e}")
        return word, "ERROR"


async def translate_words(words, src_lang='en', dest_lang='pl'):
    """Translate a list of words from English to Polish asynchronously."""
    translator = Translator()
    tasks = [translate_word(translator, word, src_lang, dest_lang) for word in words]
    translations = await asyncio.gather(*tasks)
    return dict(translations)


def save_to_csv(translations, output_file):
    """Save translations to a CSV file."""
    with open(output_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["English", "Polish"])
        for eng, pl in translations.items():
            writer.writerow([eng, pl])


def main():
    input_file = "oxford5000.txt"  # Change this to your actual file name
    output_file = "oxford5000_translated.csv"
    words = load_words_from_txt(input_file)
    print(f"Loaded {len(words)} words.")

    translations = asyncio.run(translate_words(words))
    save_to_csv(translations, output_file)
    print(f"Translations saved to {output_file}")


if __name__ == "__main__":
    main()
