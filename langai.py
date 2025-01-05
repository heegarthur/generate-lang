import random
import nltk
from nltk.corpus import words

# Zorg ervoor dat de woordenlijst gedownload is
nltk.download('words')

class LanguageAI:
    def __init__(self, english_words):
        self.language_name = ""
        self.dictionary = {}
        self.english_words = english_words  # Lijst met alle Engelse woorden
        self.file_name = "langai.txt"

        # Lettergreeplijsten
        self.syllables_1 = ["a", "e", "i", "o", "u"]
        self.syllables_2 = ["la", "ce", "ti", "so", "tu", "sa", "fe", "qo","bi","da","gi","ho","ji","ka","ma","on","ep","ra","va","wi","xo","yi","zu"]
        self.syllables_3 = ["bar", "lun", "mes", "zon", "sch", "kat", "rev"]

    def generate_language_name(self):
        # Simpele naam voor de taal
        syllables = self.syllables_2
        self.language_name = random.choice(syllables) + random.choice(syllables)
        return self.language_name

    def generate_word(self):
        # Stel de beginlengte in op 4 of 5
        word_length = random.choices([4, 5], weights=[0.6, 0.4])[0]
        duplicate_attempts = 0  # Houd bij hoeveel duplicaten er gevonden zijn
        max_attempts = 10  # Het aantal pogingen voordat we de lengte verhogen

        while True:  # Probeer totdat een uniek woord is gevonden
            word = []
            last_type = None  # Houd bij of de vorige een 1, 2 of 3-lettergreep was

            while len("".join(word)) < word_length:
                if last_type == 1 or last_type == 3:
                    # Na 1 of 3 moet een 2 komen
                    syllable = random.choice(self.syllables_2)
                    last_type = 2
                else:
                    # Kies willekeurig uit 1, 2 of 3, met voorkeur voor 2
                    syllable_type = random.choices([1, 2, 3], weights=[0.2, 0.6, 0.2])[0]
                    if syllable_type == 1:
                        syllable = random.choice(self.syllables_1)
                    elif syllable_type == 2:
                        syllable = random.choice(self.syllables_2)
                    else:
                        syllable = random.choice(self.syllables_3)
                    last_type = syllable_type

                word.append(syllable)

            generated_word = "".join(word)

            # Controleer of het woord al bestaat in de dictionary
            if generated_word not in self.dictionary.values():
                return generated_word  # Als het uniek is, stop en retourneer het
            else:
                duplicate_attempts += 1  # Tel het duplicaat
                if duplicate_attempts >= max_attempts:
                    # Verhoog de lengte van de woorden als er teveel duplicaten zijn
                    word_length = random.choice([5, 6, 7])  # Verhoog naar een langere lengte
                    duplicate_attempts = 0  # Reset duplicaatpogingen


    def translate_to_new_language(self, word):
        # Vertaal een Engels woord naar een uniek woord in de nieuwe taal
        return self.generate_word()

    def load_existing_data(self):
        # Bestaand woordenboek laden
        try:
            with open(self.file_name, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    if ':' in line:
                        english_word, translated_word = line.split(":")
                        self.dictionary[english_word.strip()] = translated_word.strip()
        except FileNotFoundError:
            print("Geen bestaand woordenboek gevonden. Een nieuw bestand wordt gemaakt.")

    def update_dict_and_save(self):
        # Voeg nieuwe vertalingen toe aan het woordenboek en sla op
        with open(self.file_name, 'a') as file:
            for word in self.english_words:
                if word not in self.dictionary:
                    translated_word = self.translate_to_new_language(word)
                    self.dictionary[word] = translated_word
                    file.write(f"{word} : {translated_word}\n")


def main():
    # Haal de lijst met Engelse woorden op
    english_words = words.words()

    if not english_words:
        print("Geen Engelse woorden gevonden, afsluiten.")
        return

    # Initialiseer de taal-AI
    language_ai = LanguageAI(english_words)

    # Stap 1: Genereer taalnaam
    language_name = language_ai.generate_language_name()
    print(f"Gegenereerde taalnaam: {language_name}\n")

    # Laad bestaand woordenboek
    language_ai.load_existing_data()

    # Stap 2: Update woordenboek met nieuwe woorden en sla op
    language_ai.update_dict_and_save()
    print(f"Nieuwe woorden toegevoegd aan {language_ai.file_name}.\n")


if __name__ == "__main__":
    main()
