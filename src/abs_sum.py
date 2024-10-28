import warnings
from transformers import BartTokenizer, BartForConditionalGeneration
import torch
from torch.profiler import profile, record_function, ProfilerActivity
from torch.amp import autocast

class Abstractive:

    model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6")
    tokenizer = BartTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")
    warnings.filterwarnings("ignore")

    def __init__(self, new_text):
        self.text = new_text
        self.original = new_text
        self.device = None
        self.__set_gpu_or_cpu()

    def __set_gpu_or_cpu(self):
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
        else:
            self.device = torch.device("cpu")

        self.model.to(self.device)

    def __tokenize(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", 
                                padding=True, truncation=True)
        
        inputs = {key: val.to(self.device) for key, val in inputs.items()}
        
        return inputs
    
    def __create_summary_ids(self, inputs, max_length=150, min_length=40):
        with autocast(str(self.device)):
            ids = self.model.generate(
                inputs["input_ids"],
                num_beams=4,
                do_sample=False,
                min_length=min_length,
                max_length=max_length,
                no_repeat_ngram_size=3,
                num_return_sequences=1,
                length_penalty=1.2,
                top_p=0.95,
                early_stopping=True
            )

        return ids           

    def run_abstractive_summarization(self, summary_length = 0, profiling=True):
        with torch.no_grad():
            with profile(
                activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], 
                record_shapes=True
            ) as prof:
                with record_function("abstractive_summarization"):
                    inputs = self.__tokenize(self.text)
                    summary_ids = self.__create_summary_ids(
                        inputs, 
                        max_length=summary_length if summary_length > 0 else 150
                    )

                    summary = self.tokenizer.decode(
                        summary_ids[0], 
                        skip_special_tokens=True, 
                        clean_up_tokenization_spaces=True
                    )

        if profiling:
            print(prof.key_averages().table(sort_by="cuda_time_total"))
      
        return summary
    
    def get_original(self):     
        return self.original