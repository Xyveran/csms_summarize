import torch
from transformers import BartTokenizer, BartForConditionalGeneration
from torch.profiler import profile, record_function, ProfilerActivity
from torch.amp import autocast

class Abstractive:

    model = None
    tokenizer = None
    device = None

    @classmethod
    def load_model_and_tokenizer(cls):
        if cls.model is None or cls.tokenizer is None:
            cls.__set_gpu_or_cpu()

            cls.model = BartForConditionalGeneration.from_pretrained("sshleifer/distilbart-cnn-12-6").to(cls.device)
            cls.tokenizer = BartTokenizer.from_pretrained("sshleifer/distilbart-cnn-12-6")

    @classmethod
    def __set_gpu_or_cpu(cls, gpu_id=0):
        if torch.cuda.is_available():
            cls.device = torch.device(f"cuda:{gpu_id}")
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False
        else:
            cls.device = torch.device("cpu")

    def __init__(self, new_text=None):
        self.__class__.load_model_and_tokenizer()
        self.text = new_text
        self.original = new_text    

    def __tokenize(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", 
                                padding="longest", truncation=True)  
        inputs = {key: val.to(self.device) for key, val in inputs.items()}
        
        return inputs
    
    def set_text(self, set_new_text):
        self.text = set_new_text
        self.original = set_new_text
    
    def __create_summary_ids(self, inputs, max_length=150, min_length=40):
        with autocast(device_type=self.device.type):
            ids = self.model.generate(
                inputs["input_ids"],
                attention_mask=inputs.get("attention_mask", None),
                num_beams=4,
                min_length=min_length,
                max_length=max_length,
                no_repeat_ngram_size=2,
                num_return_sequences=1,
                length_penalty=1.0,
                early_stopping=True
            )

        return ids           

    def run_abstractive_summarization(self, summary_length = 0, profiling=False):
        with torch.no_grad():
            inputs = self.__tokenize(self.text)

            if profiling:
                with profile(
                    activities=[ProfilerActivity.CPU, ProfilerActivity.CUDA], 
                    record_shapes=True
                    ) as prof:
                    with record_function("abstractive_summarization"):
                        summary_ids = self.__create_summary_ids(
                            inputs, 
                            max_length=summary_length if summary_length > 0 else 150
                            )
                        summary = self.tokenizer.decode(
                            summary_ids[0], 
                            skip_special_tokens=True, 
                            clean_up_tokenization_spaces=True
                            )            
                print(prof.key_averages().table(sort_by="cuda_time_total"))

            else:
                summary_ids = self.__create_summary_ids(
                        inputs, 
                        max_length=summary_length if summary_length > 0 else 150
                        )
                summary = self.tokenizer.decode(
                    summary_ids[0], 
                    skip_special_tokens=True, 
                    clean_up_tokenization_spaces=True
                    )   

        return summary
    
    def get_original(self):     
        return self.original