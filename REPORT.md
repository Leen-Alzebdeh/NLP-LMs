# Language Models Task Report

## Justifications
| Decisions Made + Design Choices|Justification |
| ------------------------------ | ------------ |
| Additional cleaning and transformations done to data: No additional cleaning and transformations were done to the data. | We did not require any additional changes to the data, as the data was cleaned/transformed well. <br>This included keeping the lexical markers, as the lexical markers contain additional data to the phenomes that can aid in future analysis of of phenome sequences. The phenomes are also more differentiated with the lexical markers, giving us a wider array of data to train our model with. |
| How are begin-of-utterance and end-of-utterance identified: | The original data is organized per utterance sequence. The `<s>` symbol is added to the beginning of an utterance (at the start of a new data line), and the </s> symbol is added to the end of an utterance (at the end of that line). The “tokenize_sentences” function iterates through the data file, tokenizing each line. |
|How OOV words are handled: Excluded from training. | Excluding OOV words instead of using alternatives such as UNK tokens and Backoff can result in faster performance and a more simplified language model for our purposes. This helps us build a more meaningful language model.<br> Because the training set and dev set are both made up of ARPAbet sequences, there should not be a large number of unknown words, as even unknown or pseudo words reuse the same ARPAbet phenomes in a rearranged manner. ARPAbet sequences are intentionally well structured for linguistic purposes, and through training can inherently aid in limiting the probabilities of OOV utterances. <br>For data cleaning, we decided to include non-word utterances if they were able to be broken down into relevant ARPAbet phenomes. If they were not, they were excluded. To exclude pseudowords and unknown words, would be the most appropriate choice as it ensures our data training is not producing inaccurate perplexities.|

## Results

| Model           | Smoothing  | Training set PPL                                            | Dev set PPL                                                 |
| --------------- | ---------- | ----------------------------------------------------------- | ----------------------------------------------------------- |
| unigram         | -          |      34.77                                      |     34.72                                       |
| bigram          | unsmoothed |            12.83                               |                      12.87                     |
| bigram          | Laplace    |        12.88                                   |  12.92                                         |
| trigram         | unsmoothed |      5.40                                      |     5.36                                      |
| trigram         | Laplace    |    5.86                                       |  5.80                                          |
| bigram (KenLM)  | Kneser-Ney | 15.91 (w/ OOVs), 15.91 (w/o OOVs) | 15.90 (w/ OOVs), 15.90 (w/o OOVs) |
| trigram (KenLM) | Kneser-Ney | 8.16 (w/ OOVs), 8.16 (w/o OOVs)     | 8.35 (w/ OOVs), 8.35 (w/o OOVs)   |

