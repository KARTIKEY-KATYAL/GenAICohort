import tiktoken

encoder = tiktoken.encoding_for_model('gpt-4o')

print("vocab size",encoder.n_vocab) #200019 vocab size

tokens = encoder.encode("The Cat Sat On the mat")

print(tokens)

detokens = encoder.decode(tokens)

print(detokens)