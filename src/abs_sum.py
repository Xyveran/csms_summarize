import torch
import torch._dynamo.config
import torch.onnx
import torch.nn.functional as F
import os
from transformers import BartTokenizer, BartForConditionalGeneration
from torch.profiler import profile, record_function, ProfilerActivity
from torch.amp import autocast
from torch.quantization import quantize_dynamic


class Abstractive:

    model = None
    tokenizer = None
    device = None

    @classmethod
    def load_model_and_tokenizer(cls):
        if cls.model is None or cls.tokenizer is None:
            cls.__set_gpu_or_cpu()
            #cls.device = torch.device("cpu")

            cls.model = BartForConditionalGeneration.from_pretrained(
                        "sshleifer/distilbart-cnn-12-6"
                        ).to(cls.device)
            if cls.device == "cpu":
                cls.model = quantize_dynamic(
                    cls.model,
                    {torch.nn.Linear},
                    dtype=torch.qint8
                )
            cls.tokenizer = BartTokenizer.from_pretrained(
                            "sshleifer/distilbart-cnn-12-6"
                            )
            cls.__optimize_model()

    @classmethod
    def __set_gpu_or_cpu(cls, gpu_id=0):
        if torch.cuda.is_available():
            cls.device = torch.device(f"cuda:{gpu_id}")
            torch.backends.cudnn.benchmark = True
            torch.backends.cudnn.deterministic = False
            #torch.cuda.synchronize()
        else:
            cls.device = torch.device("cpu")

    @classmethod
    def __optimize_model(cls):
        cls.model.eval()
        if cls.device.type == "cuda":
            cls.model.half()
        else:
            num_cores = os.cpu_count()
            threads = max(1, num_cores - 1)

            torch.set_num_threads(threads)      
            torch.set_num_interop_threads(threads)

    def __init__(self, new_text=None):
        self.__class__.load_model_and_tokenizer()
        self.text = new_text
        self.original = new_text    

    def set_text(self, set_new_text):
        self.text = set_new_text
        self.original = set_new_text

    def __tokenize(self, text):
        inputs = self.tokenizer(
            [text],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length = 512,
        )  

        inputs["inputs_ids"] = self.pad_to_multiple(inputs["input_ids"])        
        inputs = {key: val.to(self.device) for key, val in inputs.items()}
        
        return inputs
    
    @staticmethod
    def pad_to_multiple(tensor, multiple=8):
        pad_size = (multiple - tensor.size(-1) % multiple) % multiple

        return F.pad(tensor, (0, pad_size), value=0)

    def __create_summary_ids(self, inputs, max_length=300, min_length=50):
        with autocast(device_type=self.device.type):
            input_ids = inputs["input_ids"]
            if not input_ids.is_contiguous():
                input_ids = input_ids.contiguous()

            ids = self.model.generate(
                inputs["input_ids"],
                num_beams=1,
                min_length=min_length,
                max_length=max_length,
                no_repeat_ngram_size=2,
                #num_return_sequences=1,
                length_penalty=1.0,
                early_stopping=False
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
                            max_length=summary_length if summary_length > 50 else 300
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
                        max_length=summary_length if summary_length > 50 else 300
                        )
                summary = self.tokenizer.decode(
                    summary_ids[0], 
                    skip_special_tokens=True, 
                    clean_up_tokenization_spaces=True
                    )   

        return summary
    
    def get_original(self):     
        return self.original