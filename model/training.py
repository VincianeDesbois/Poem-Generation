import os
from pathlib import Path
import pandas as pd
import torch
from transformers import (
    T5Tokenizer,
    AutoTokenizer,
    T5ForConditionalGeneration,
    Adafactor,
)
import sentencepiece

num_of_epochs = 1


def progress(loss, value, max=500):
    """
    Indicates the progress of the learning.

    Parameters
    ----------
    loss: float
          The loss of the current batch.
    value: int
           Number of the current batch.
    max: float
         Total number of batches.

    Returns
    -------
    string
        String displaying the 3 input values.
    """
    return """ Batch loss :{loss}  progress value {value}  max={max}""".format(
        loss=loss, value=value, max=max
    )


def trainer(train_df, dev, tokenizer):
    """
    Train the model.

    Parameters
    ----------
    train_df: pd.Dataframe
              Training dataset with: a column "text" for the verses of the webscrapped poems
                                     a column "key_words" for the list of 3 keywords for the corresponding verse
    dev: torch.device
         Type of processing unit (CPU or GPU)
    tokenizer: transformers.models.t5.tokenization_t5_fast.T5TokenizerFast
               Tokenizer of the model T5.

    Returns
    -------
    saved files
        Save 5 files in the given path (3 for the tokenizer, 1 of config and 1 for the weights of the model)
    """
    model_w2t = T5ForConditionalGeneration.from_pretrained("t5-base", return_dict=True)
    model_w2t.to(dev)

    batch_size = 6
    num_of_batches = len(train_df) / batch_size
    print("training for ", num_of_batches, " batches of size", batch_size)

    optimizer = Adafactor(
        model_w2t.parameters(),
        lr=1e-3,
        eps=(1e-30, 1e-3),
        clip_threshold=1.0,
        decay_rate=-0.7,
        beta1=None,
        weight_decay=0.0,
        relative_step=False,
        scale_parameter=False,
        warmup_init=False,
    )

    model_w2t.train()

    loss_per_10_steps = []
    for epoch in range(1, num_of_epochs + 1):
        print("Running epoch: {}".format(epoch))

        running_loss = 0

        for i in range(int(num_of_batches)):
            inputbatch = []
            labelbatch = []
            new_df = train_df[i * batch_size : i * batch_size + batch_size]
            for indx, row in new_df.iterrows():
                if type(row["key_words"]) == str:
                    if type(row["text"]) == str:
                        input = row["key_words"] + "</s>"
                        labels = row["text"] + "</s>"
                        inputbatch.append(input)
                        labelbatch.append(labels)
            inputbatch = tokenizer.batch_encode_plus(
                inputbatch, padding=True, max_length=400, return_tensors="pt"
            )["input_ids"]
            labelbatch = tokenizer.batch_encode_plus(
                labelbatch, padding=True, max_length=400, return_tensors="pt"
            )["input_ids"]
            inputbatch = inputbatch.to(dev)
            labelbatch = labelbatch.to(dev)

            # clear out the gradients of all Variables
            optimizer.zero_grad()

            # Forward propogation
            outputs = model_w2t(input_ids=inputbatch, labels=labelbatch)
            loss = outputs.loss
            loss_num = loss.item()
            logits = outputs.logits
            running_loss += loss_num
            if i % 10 == 0:
                loss_per_10_steps.append(loss_num)
                print(progress(loss_num, i, num_of_batches + 1))
            # calculating the gradients
            loss.backward()

            # updating the params
            optimizer.step()

        running_loss = running_loss / int(num_of_batches)
        print()
        print("Epoch: {} , Running loss: {}".format(epoch, running_loss))
        print()

    root_mod = root + "/model"
    torch.save(model_d2t.state_dict(), (root_mod + "/model_w2p.bin"))

    model_w2t.save_pretrained(root_mod)
    tokenizer.save_pretrained(root_mod)


###     TRAINING OF THE MODEL      ###

# root = "/poem-generation"
# data_train = pd.read_csv(root + "/data_factory/df_key_words.csv", sep = ",", encoding='UTF-8')

# if torch.cuda.is_available():
#    dev = torch.device("cuda:0")
#    print("Running on the GPU")
# else:
#    dev = torch.device("cpu")
# print()
# print('*********  Loading and training  **********')
# print()

# trainer(data_train, dev, tokenizer)
