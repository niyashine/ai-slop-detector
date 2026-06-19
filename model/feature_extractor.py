import re
import textstat

def extract_features(text):

    words = text.split()

    word_count = len(words)

    sentences = re.split(r'[.!?]+', text)
    sentences = [s for s in sentences if s.strip()]

    avg_sentence_length = (
        word_count / len(sentences)
        if sentences else 0
    )

    vocab_diversity = (
        len(set(words)) / word_count
        if word_count else 0
    )

    readability = textstat.flesch_reading_ease(text)

    return [
        word_count,
        avg_sentence_length,
        vocab_diversity,
        readability
    ]