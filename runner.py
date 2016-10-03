import time
import os
import read_training as rt
import distribution_calculator as dc


corpus_file = os.path.join(os.path.dirname(__file__), 'data/sentences/cw_1_sentences.tsv')
new_corpus_file = os.path.join(os.path.dirname(__file__), 'data/replaced/cw_1_sentences_100k.tsv')
training_file = os.path.join(os.path.dirname(__file__), 'data/training/training.tsv')

start = time.clock()
# print(start)

# substitute_midnames()
# substitute_midnames_partial()
# substitute_midnames_in_memory()
# print get_id_by_token('{m.03cd5dk:45037:45040}')
# print rt.get_all_entity_properties_by_id('m.0c3dqq3')
# print search_midname('m.01000036')
# print dc.count_types()
print rt.substitute_midnames(corpus_file, new_corpus_file, 100000)
# rt.create_training_from_dataset(corpus_file, training_file, 1000)

end = time.clock()
# print(end)

print(str(end - start) + ' seconds')
