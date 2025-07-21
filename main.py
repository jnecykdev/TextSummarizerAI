import os
import sys
import spacy # Import spacy
from html.parser import HTMLParser

class TextSummarizer:
    def __init__(self):
        # Initialize spaCy model for text processing
        # Make sure you have downloaded the model: python -m spacy download en_core_web_sm
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("SpaCy model 'en_core_web_sm' not found. Please run: python -m spacy download en_core_web_sm")
            sys.exit(1) # Exit if model is not available

    class HTMLTagRemover(HTMLParser):
        """Custom HTML parser to remove HTML tags."""
        def __init__(self):
            super().__init__()
            self.text = []

        def handle_data(self, data):
            self.text.append(data)

        def get_clean_text(self):
            return ''.join(self.text)

    def clean_html_tags(self, text):
        """Remove HTML tags and decode HTML entities."""
        parser = self.HTMLTagRemover()
        parser.feed(text)
        return parser.get_clean_text()

    def summarize(self, text, num_sentences=3): # Increased default to 3 for slightly longer summaries
        """
        Summarizes the given text using spaCy by extracting the most important sentences.
        """
        doc = self.nlp(text)
        sentences = list(doc.sents)
        
        # Simple summarization: rank sentences by length and pick the top N
        # This is a basic approach; for more advanced spaCy summarization,
        # you might use textrank algorithms or other methods based on word frequency.
        ranked_sentences = sorted(sentences, key=lambda s: len(s.text), reverse=True)
        
        # Join the top N sentences to form the summary
        summary = ' '.join([sent.text for sent in ranked_sentences[:num_sentences]])
        
        # Clean any potential HTML tags that might have been in the original text
        # or introduced during processing (though less likely with spaCy).
        summary = self.clean_html_tags(summary)
        return summary

    def summarize_file(self, file_path):
        """
        Reads text from a file and then summarizes it using the main summarize method.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
            summary = self.summarize(text)
            return summary
        except FileNotFoundError:
            return "File not found."
        except Exception as e:
            return f"Error reading file: {e}"

# Example usage (for local testing of main.py)
if __name__ == "__main__":
    summarizer = TextSummarizer()
    
    # Example 1: Summarize a simple string
    text_to_summarize = "Artificial intelligence (AI) is intelligence demonstrated by machines, unlike the natural intelligence displayed by humans and animals. Leading AI textbooks define the field as the study of 'intelligent agents': any device that perceives its environment and takes actions that maximize its chance of successfully achieving its goals. Colloquially, the term 'artificial intelligence' is often used to describe machines that mimic 'cognitive' functions that humans associate with the human mind, such as 'learning' and 'problem-solving'. AI applications include advanced web search engines (e.g., Google Search), recommendation systems (used by YouTube, Amazon, and Netflix), understanding human speech (such as Siri and Alexa), self-driving cars (e.g., Waymo), generative AI, and competing at the highest level in strategic game systems (such as chess and Go)."
    print("\n--- Summarizing a string ---")
    summary = summarizer.summarize(text_to_summarize)
    print("Original Text:\n", text_to_summarize)
    print("\nSummary:\n", summary)

    # Example 2: Summarize from a dummy file (create a dummy.txt for this to work)
    # You would need to create a 'dummy.txt' file in the same directory as main.py
    # with some text content for this example to run.
    # For instance:
    # echo "This is a test sentence for summarization. It contains multiple sentences. We want to see how well the AI summarizes it." > dummy.txt
    dummy_file_path = 'dummy.txt'
    if os.path.exists(dummy_file_path):
        print(f"\n--- Summarizing from file: {dummy_file_path} ---")
        file_summary = summarizer.summarize_file(dummy_file_path)
        print("File Summary:", file_summary)
    else:
        print(f"\nSkipping file summarization example: {dummy_file_path} not found.")

