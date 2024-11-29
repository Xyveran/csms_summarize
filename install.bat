:: Download application models

@echo off

REM pre-download models and tokenizer
echo Downloading Bart model... 
python -c "from transformers import BartForConditionalGeneration; BartForConditionalGeneration.from_pretrained('sshleifer/distilbart-cnn-12-6'); print('Model downloaded successfully.')"

echo Downloading Bart tokenizer...
python -c "from transformers import BartTokenizer; BartTokenizer.from_pretrained('sshleifer/distilbart-cnn-12-6'); print('Tokenizer downloaded successfully.')"