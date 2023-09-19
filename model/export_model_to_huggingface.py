from transformers import AutoTokenizer, T5ForConditionalGeneration

PATH = "model"
TOKEN = "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"

tokenizer = AutoTokenizer.from_pretrained(PATH)

model = T5ForConditionalGeneration.from_pretrained(
    PATH + "/model_w2p.bin", return_dict=True, config=PATH + "/config.json"
)

model.push_to_hub("poemgen_V1", use_auth_token=TOKEN)
