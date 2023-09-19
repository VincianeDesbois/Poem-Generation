import random

import nltk
from transformers import AutoTokenizer, T5ForConditionalGeneration
from translate import Translator

nltk.download("wordnet")
nltk.download("omw-1.4")
# nltk.download()
from nltk.corpus import wordnet

####
#### IMPORT THE MODEL
####
path = "model"

tokenizer = AutoTokenizer.from_pretrained(path)

model = T5ForConditionalGeneration.from_pretrained(
    "clemmillet/poemgen_V2", return_dict=True, config=path + "/config.json"
)

# Parameters of the model (tested to get optimal text generation)
p = 0.82
k = 90


####
#### A DICTIONARY OF WORDS COMMONLY USED IN FRENCH POESY
####

dico_poesy = [
    "âge",
    "amoureux",
    "amour",
    "amitié",
    "amant",
    "insolence",
    "histoire",
    "fleur",
    "rose",
    "coquelicot",
    "blanc",
    "beau",
    "feu",
    "joie",
    "rire",
    "plonger",
    "saut",
    "océan",
    "étoile",
    "ciel",
    "planète",
    "espace",
    "monde",
    "nuage",
    "torrent",
    "pluie",
    "fée",
    "magie",
    "âme",
    "miroir",
    "reflet",
    "neige",
    "pomme",
    "fauve",
    "merveilleux",
    "baiser",
    "badiner",
    "jouer",
    "épancher",
    "couler",
    "mélancolie",
    "onirique",
    "rêve",
    "ivresse",
    "flâner",
    "vin",
    "épistolaire",
    "plume",
    "chanter",
    "cri",
    "folie",
    "rage",
    "tristesse",
    "courroux",
    "colombe",
    "arène",
    "chasse",
    "bohème",
    "caresse",
    "tendresse",
    "cavale",
    "céleste",
    "or",
    "fronde",
    "firmament",
    "paradis",
    "écrin",
    "deuil",
    "tombe",
    "décès",
    "jadis",
    "aventure",
    "languir",
    "espérer",
    "martyr",
    "message",
    "nymphe",
    "déesse",
    "Olympe",
    "panser",
    "guérir",
    "danser",
    "louve",
    "rosir",
    "musique",
    "note",
    "rime",
    "son",
    "harmonie",
    "mélodie",
    "air",
    "romance",
    "romantique",
    "bruissement",
    "chuchoter",
    "forme",
    "ombre",
    "ténèbre",
    "chaos",
    "enfer",
    "brasier",
    "incendie",
    "sommeil",
    "utopie",
    "conte",
    "silence",
    "lame",
    "poignard",
    "flèche",
    "orner",
    "aurore",
    "aube",
    "zénith",
    "crépuscule",
    "soleil",
    "paisible",
    "dieu",
    "divinité",
    "flotter",
    "profondeur",
    "chevelure",
    "main",
    "oeil",
    "regard",
    "sourire",
    "lèvre",
    "courbe",
    "parfum",
    "odeur",
    "élégance",
    "charme",
    "enchantement",
    "merveille",
    "abysse",
    "abîme",
    "bois",
    "fleuve",
    "désert",
    "sable",
    "pourpre",
    "mauve",
    "azur",
    "rosée",
    "flot",
    "bercer",
    "lit",
    "nid",
    "oiseau",
    "aile",
]

####
#### FUNCTIONS TO GENERATE POEMS
####


def gen_poem(key_w, length):
    """
    Generate a poem of a given length from 3 words.

    Parameters
    ----------
    key_w: list
        List of 3 strings corresponding to the 3 words entered by the user.
    length: int
            Number of verses generated (can only take the values 1, 3 or 5).

    Returns
    -------
    string
        Poem generated.
    """
    if length == 1:
        poem = generate_w2p(str(key_w).replace("'", ""), p, k, model, tokenizer)
    else:
        inputs = list_inputs(key_w)
        # print(inputs)
        print()
        poem = ""
        for i in range(length):
            verse = generate_w2p(inputs[i], p, k, model, tokenizer)
            poem += verse + "\n"
    poem = poem.replace("<pad>", "").replace("</s>", "")
    return poem


def generate_w2p(text, p, k, model, tokenizer):
    """
    Generate one poem verse from an input of three words.

    Parameters
    ----------
    text: string
          String of a list of 3 words (input for the model).
    p: float
       Parameter "top_p" of the NLG model.
    k: float
       Parameter "top_k" of the NLG model.
    model: transformers.models.t5.modeling_t5.T5ForConditionalGeneration
           Generation model (files "pytorch_model.bin" and "config.json").
    tokenizer: transformers.models.t5.tokenization_t5_fast.T5TokenizerFast
               Tokenizer of the model (files "tokenizer.json", "tokenizer_config.json"
               and "special_token_map.json").

    Returns
    -------
    string
        Generated verse.
    """

    # input_ids = tokenizer.encode("{}".format(text), return_tensors="pt")
    input_ids = tokenizer.encode("{}".format(text), return_tensors="pt")

    outputs = model.generate(
        input_ids,
        max_length=25,
        min_length=8,
        do_sample=True,
        top_p=p,
        top_k=k,
        early_stopping=True,
    )

    return tokenizer.decode(outputs[0])


def list_inputs(key_w):
    """
    Create a list of 5 inputs to give to the model (to generate 5 verses), created from a list of 3 words.

    Parameters
    ----------
    key_w: list of 3 strings
           list of the 3 words given by the user to be the theme of the poem.

    Returns
    -------
    list
        List of 5 lists of 3 words, each of the 5 list is an input for one verse of the generated poem.
    """

    gen_list = [
        [],
        [],
        [],
    ]  # each sub-list will contain one of the input words and 2 or 3 words related
    # (synonyms or antonyms)

    for i in range(3):
        gen_list[i].append(key_w[i])

        syn_1 = syn_choice(key_w[i], [])
        if syn_1 == []:
            gen_list[i].append(key_w[i])
            gen_list[i].append(key_w[i])
        else:
            gen_list[i].append(syn_1[0])
            syn_2 = syn_choice(syn_1[0], [key_w[i]])
            if syn_2 == []:
                gen_list[i].append(key_w[i])
            else:
                gen_list[i].append(syn_2[0])

        for wd in gen_list[i]:
            antonym = ant_choice(wd)
            if antonym != []:
                break
        if antonym != []:
            gen_list[i].append(antonym[0])
        else:
            syn_3 = syn_choice(gen_list[i][2], [key_w[i], gen_list[i][1]])
            try:
                gen_list[i].append(syn_3[0])
            except:
                gen_list[i].append(key_w[i])

    # We create a list of the 5 inputs to give to the model to create 5 verses
    inps = [
        [gen_list[0][0], gen_list[1][1], gen_list[2][2]],
        [random.choice(dico_poesy), gen_list[1][2], gen_list[2][0]],
        [gen_list[0][2], gen_list[1][0], gen_list[2][1]],
        [gen_list[0][3], random.choice(dico_poesy), gen_list[2][3]],
        [gen_list[0][1], gen_list[1][3], random.choice(dico_poesy)],
    ]

    inputs = []
    for lst in inps:
        inputs.append(str(lst).replace("'", ""))

    return inputs


def ant_choice(word):
    """
    Find antonyms for a given word if it exists.

    Parameters
    ----------
    word: string
          One of the words given as input of the generation.

    Returns
    -------
    list
        List of strings corresponding to the antonyms found for the input word (can be empty if none found).
    """
    # As this module works only for english words, we translate twice
    translator_f2e = Translator(from_lang="french", to_lang="english")
    translator_e2f = Translator(from_lang="english", to_lang="french")
    ants = []
    ants_fr = []
    try:
        word_eng = translator_f2e.translate(word)

        for ant in wordnet.synsets(word_eng):
            for l in ant.lemmas():
                if l.antonyms():
                    ants.append(l.antonyms()[0].name())
        ants_list = list(set(ants))
        # print(ants_list)
        if ants_list != []:
            for a in ants_list:
                w_fr = translator_e2f.translate(a)
                ants_fr.append(w_fr)
    except:
        pass

    return ants_fr


def syn_choice(word, list_x):
    """
    Choose adequatly one word inside a list of synonyms.

    Parameters
    ----------
    word: string
          One of the words given as input of the generation.
    list_x: list of strings
            list of words not to choose as synonyms (already used in precedent verses of the generated poem).

    Returns
    -------
    list
        List either containing the chosen synonym or empty if no synonyms found.
    """
    synonyms = list_syns(word)
    choice = []
    if synonyms != []:
        for i in range(len(synonyms)):
            if (
                synonyms[i] != word
                and synonyms[i] not in list_x
                and "_" not in synonyms[i]
            ):
                # we take only the one-word synonyms which are different from the words in list_x
                choice.append(synonyms[i])
            if i > 5:
                break
        # print(choice)
        try:
            syn = random.choice(choice)
            choice = [syn]
        except:
            pass
    return choice


def list_syns(word):
    """
    Make a list of synonyms for a given french word.

    Parameters
    ----------
    word: string
          One of the words given as input of the generation.

    Returns
    -------
    list
        List of strings corresponding to the synonyms found for the input word.
    """
    syns = []
    for syn in wordnet.synsets(word, lang="fra"):
        for l in syn.lemmas("fra"):
            syns.append(l.name())
    syns_list = list(set(syns))
    return syns_list


####
#### GENERATE POEMS
####

# start_time = time.time()

# wds = ["douleur", "depression", "mort"]

# length_poem = 5

# print(gen_poem(wds, length_poem))

# print("--- %s seconds ---" % (time.time() - start_time))
