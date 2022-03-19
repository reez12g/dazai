from transformers import (
    pipeline,
    GPT2LMHeadModel,
    T5Tokenizer
)

class NLP:
    def __init__(self):
        self.tokenizer = T5Tokenizer.from_pretrained("rinna/japanese-gpt2-small")
        self.model = GPT2LMHeadModel.from_pretrained("rinna/japanese-gpt2-small")

    def predictive_sentences(self, prompt):
        input = self.tokenizer.encode("私は学生時代に", return_tensors="pt")
        output = self.model.generate(input, do_sample=True, max_length=input.size()[1]+50)
        return self.tokenizer.batch_decode(output)
