import warnings
from transformers import BartTokenizer, BartForConditionalGeneration

class Abstractive:

    model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6")
    tokenizer = BartTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    warnings.filterwarnings("ignore")

    def __init__(self, new_text):
        self.text = new_text
        self.original = new_text

    def __tokenize(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", 
                                padding=True, truncation=True)
        
        return inputs
    
    def __create_summary_ids(self, inputs, max_length=150, min_length=40):
        ids = self.model.generate(
            inputs["input_ids"],
            num_beams=4,
            min_length=min_length,
            max_length=max_length,
            early_stopping=True
        )

        return ids

    def run_abstractive_summarization(self, summary_length = 0):
        inputs = self.__tokenize(self.text)
        summary_ids = self.__create_summary_ids(
            inputs, 
            max_length=summary_length if summary_length > 0 else 150
            )

        summary = self.tokenizer.decode(
            summary_ids[0], 
            skip_special_tokens=True, 
            clean_up_tokenization_spaces=True)
        
        return summary
    
    def get_original(self):     

        return self.original