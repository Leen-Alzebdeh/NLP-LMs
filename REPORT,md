
| Model           | Smoothing  | Training set PPL                                            | Dev set PPL                                                 |
| --------------- | ---------- | ----------------------------------------------------------- | ----------------------------------------------------------- |
| unigram         | -          |      34.77                                      |     34.72                                       |
| bigram          | unsmoothed |            12.83                               |                      12.87                     |
| bigram          | Laplace    |        12.88                                   |  12.92                                         |
| trigram         | unsmoothed |      5.40                                      |     5.36                                      |
| trigram         | Laplace    |    5.86                                       |  5.80                                          |
| bigram (KenLM)  | Kneser-Ney | 15.91 (w/ OOVs), 15.91 (w/o OOVs) | 15.90 (w/ OOVs), 15.90 (w/o OOVs) |
| trigram (KenLM) | Kneser-Ney | 8.16 (w/ OOVs), 8.16 (w/o OOVs)     | 8.35 (w/ OOVs), 8.35 (w/o OOVs)   |


# Language Models Task Report

| Decisions Made + Design Choices|Justification |
| ------------------------------ | ------------ |
| Additional cleaning and transformations done to data: No additional cleaning and transformations were done to the data. | We did not require any additional changes to the data, as the data was cleaned/transformed well. <br>This included keeping the lexical markers, as the lexical markers contain additional data to the phenomes that can aid in future analysis of of phenome sequences. The phenomes are also more differentiated with the lexical markers, giving us a wider array of data to train our model with. |


## Evaluation and Error Analysis

**Precision**: ~0.251.
**Recall**: ~0.950. <br>
Values of TP, TN, FP, and FN (respectively): 132, 71, 393, 7

| | 1 (error) | 0 (no error) |
|-|----------| --------------|
|1 (error) | 132 | 393|
|0 (no error)| 7 | 71|

## Reasons for the False Positives
1. Complex sentences: The grammar has limited capability to recognize some complex sentences, such as those with multiple clauses or subordinate clauses. If a user tries to parse a sentence with these structures that aren't addressed in the grammar, it could be erroneously flagged as having a grammatical error.  <br>Example: `102 0 It looks nice and has a good message . PRP VBZ JJ CC VBZ DT JJ NN .`
   * While the grammar can recognize phrases like NP CC NP, VP CC VP, S CC S, and etc (x CC x). It is likely to miss clauses of different phrase types.
2. Lack of flexibility with commas: The grammar recognizes the comma usages “NP, NP” but the language has many varied examples which include: 
   - `435 0 I keep that in my mind , for ever ! PRP VBP DT IN PRP$ NN , IN RB .`
   - `21 0 If not , what do you suggest ? IN RB , WP VBP PRP VB .`
   - `58 0 However, we would like to suggest something: RB , PRP MD VB TO VB NN:`
3. Inability to recognize multiple verbs: In the grammar, there are no rules that account for two or more verbs that directly follow each other in correct sentences. Examples:
   - I have received your letter . PRP VBP VBN PRP$ NN .
   - Your time has been stolen . PRP$ NN VBZ VBN VBN .
## Reasons for the False Negatives
1. Lack of constraints on the relationship between verb and subject: Without specific constraints on the combination of verbs and subjects, the grammar might approve of sequences that are nonsensical in natural language use. An example of this is a personal pronoun directly followed by a gerund verb.<br>Example: `792 1 Be you studing a lot ? VB PRP VBG DT NN .`
   * This has a base verb followed by a personal pronoun at the beginning of the sentence.
2. Lack of constraints on determiners: the grammar does not ensure that determiners are used properly, for example, it does not distinguish indefinite vs definite determiners (they are all given the level DT) and does not check for the different rules of both. <br>Example: `813 1 I have a big news . PRP VBP DT JJ NNS .`
   - This has an indefinite article with a plural noun.


