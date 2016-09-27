import read_training as rt

phrase1 = "I'm {Kevin John} president of Kevin medical Supplies Limited our company was located at {m.0cr3d:31053:31061} in {m.02_286:31065:31073} and we have client in {m.07y2s:31096:31102} state , {m.02j9z:31111:31117} and {m.0dg3n1:31122:31128} ."

print rt.get_tokens_in_phrase(phrase1)

print rt.get_types_in_phrase(phrase1)
