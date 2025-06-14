import pandas as pd

df = pd.read_csv('stimuli_set.tsv', sep='\t')
df['WAV_Path'] = df['WAV_Path'].apply(lambda x: x if str(x).endswith('.wav') else str(x) + '.wav')
df.to_csv('stimuli_set_updated.tsv', sep='\t', index=False)
