import os
import asyncio
from googletrans import Translator
from gtts import gTTS


def load_words(file_path):
    """Load words from a text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        words = [line.strip() for line in f if line.strip()]
    return words


async def translate_word(word, translator):
    """Translate a word from English to Polish."""
    try:
        translation = await translator.translate(word, src="en", dest="pl")
        return translation.text
    except Exception as e:
        print(f"Error translating '{word}': {e}")
        return None


def generate_audio(word, translation, output_dir):
    """Generate an audio file for the Polish pronunciation."""
    try:
        tts = gTTS(word, lang="en")
        audio_path = os.path.join(output_dir, f"{word}.mp3")
        tts.save(audio_path)
        return audio_path
    except Exception as e:
        print(f"Error generating audio for '{word}': {e}")
        return None


async def main(input_file, output_dir):
    # Initialize the async translator
    translator = Translator()

    # Load words from file
    words = load_words(input_file)

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Process each word asynchronously
    translations = {}
    tasks = []
    for word in words:
        tasks.append(translate_word(word, translator))

    results = await asyncio.gather(*tasks)

    for word, translation in zip(words, results):
        if translation:
            translations[word] = translation
            audio_path = generate_audio(word, translation, output_dir)
            if audio_path:
                print(f"Audio saved: {audio_path}")

    # Save translations to a file
    translations_file = os.path.join(output_dir, "translations.txt")
    with open(translations_file, "w", encoding="utf-8") as f:
        for word, translation in translations.items():
            f.write(f"{word}: {translation}\n")

    print(f"Translations and audio files saved to '{output_dir}'.")


if __name__ == "__main__":
    input_file = "oxford5000.txt"  # Replace with your input file
    output_dir = "output"  # Replace with your desired output directory

    # Run the event loop
    asyncio.run(main(input_file, output_dir))
