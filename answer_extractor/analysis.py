import pandas as pd
from collections import Counter
from preprocessing import (
    Features,
    get_all_words,
    lower_case,
    on_start_up,
    remove_special_character_words,
    stop_word_removal,
)


on_start_up()

data = pd.read_csv("questions_and_answers_labeled.csv")

yes_no_features = Features(data[data["Type"] == "Yes/No"])
# entity_features = Features(data[data['Type'] == 'Entity'])


n = 100
# yes_no_counter = Counter(yes_no_features.all_words).most_common(n)
# entity_counter = Counter(entity_features.all_words).most_common(n)

# print("Yes/No answers that don't appear in Entity answers:")
# for word, count in yes_no_counter:
#     if word not in entity_counter:
#         print(word, count)

# yes: yes, surely, hopefully, (obviously, certainly, definitely, surely, absolutely, indeed, clearly, undoubtedly, naturally, definitely, absolutely, definitly)
# no: no, not, n't
# dunno: actually, answer, (maybe, probably, possibly, perhaps)

# POS
yes_no_features._calculate_bigram()

# TODO: tokenizer, lemma/stemma,
# TODO: compositiions: "surely not", "obviously not"
