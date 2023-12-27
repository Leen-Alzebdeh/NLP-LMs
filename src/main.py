# This program should loop over the files listed in the input file directory,
# assign perplexity with each language model,
# and produce the output as described in the assignment description.

import argparse
import itertools
from itertools import tee
import os
import random
import math
import sys


def main():

    # (1) one positional argument for model type (unigram/bigram/trigram),
    # (2) one argument for the path to the training data,
    # (3) one argument for the path to the data for which perplexity will be computed. In addition,
    # (4) one optional argument for smoothing (--laplace) could be present.

    parser = argparse.ArgumentParser()

    # Create positional (mandatory) arguments
    parser.add_argument("model")
    parser.add_argument("train_path")
    parser.add_argument("ppl_path")
    parser.add_argument("-l", "--laplace", action="store_true")

    # Get the argument list
    args = parser.parse_args()

    # Define dictionaries to store model and smoothing information
    model_info = {
        "unigram": "Unigram",
        "bigram": "Bigram",
        "trigram": "Trigram"
    }
    smoothing_info = {
        True: "Yes",
        False: "No"
    }

    # Determine model and smoothing information
    model = model_info.get(args.model, "Unknown Model")
    smoothing = smoothing_info[args.laplace]

    # Determine data set information
    if args.ppl_path == "data/training.txt":
        dataset = "Training"
    elif args.ppl_path == "data/dev.txt":
        dataset = "Dev"
    else:
        dataset = "Invalid entry. Please enter a valid data set."

    # Print the information
    print(f"Model: {model}")
    print(f"Smoothing: {smoothing}")
    print(f"Set: {dataset}")


    # If transformed directory exists, combine all the files into one training file
    if os.path.exists('transformed'):
        combined_text = []
        combine_transformed_files(combined_text, 'transformed')
        create_files(combined_text, args.train_path)
    
    # tokenize training data
    dataset = tokenize_sentences(args.train_path)
    # get vocab size
    vocab_size = count_unique_words(dataset)
    # get probability table from training
    prob_table = train_ngram_model(args.model, dataset, args.laplace, k=0, vocab_size=vocab_size)
    # evaulate preplixity
    if args.train_path != args.ppl_path:
        dataset = tokenize_sentences(args.ppl_path)
    ppl = eval_ppl(args.model, prob_table, dataset)
    print("Perplexity: " + str(ppl))


def combine_transformed_files(combined_text, root):
    """
    Function combines the text from all the transformed files into one python list
    root (string): name of the directory which we're retrieving files from.
    combined_text (list): python list with all the combined text
    Return None
    """
    data_dir = os.listdir(root)  # list all subdirectories in path
    for dir in data_dir:
        sub_root = os.path.join(root, dir)
        if not dir.endswith(".txt"):
            # list all subdirectories in path
            combine_transformed_files(combined_text, sub_root)
        else:
            if dir != "0metadata.txt" and dir != "0types.txt":
                f = open(sub_root, "r")
                # reading the file
                data = f.read()
                data = [i for i in data.split("\n") if i]
                combined_text.extend(data)
                f.close()


def create_files(combined_text, train_path='data/training.txt'):
    """
    Function creates the training and dev files in given directory
    combined_text (list) python list with all the combined text.
    train_path (string): path where training file will go.
    Return none
    """
    random.shuffle(combined_text)
    split_length = round(0.8*len(combined_text))
    os.makedirs(train_path.split('/')[0], exist_ok=True)

    # create training file in given path
    file = open(train_path, 'w')
    for line in (combined_text[:split_length]):
        file.write("%s\n" % line)
    file.close()

    # creates dev file in the same directory
    dev_path = train_path.split('/')[0]+'/dev.txt'
    file = open(dev_path, 'w')
    for line in (combined_text[split_length:]):
        file.write("%s\n" % line)
    file.close()


def tokenize_sentences(path):
    """
    Function tokenizes sentences in given file (strips lines, and adds begin and end of utterance symbols)
    path (string): path to txt file.
    Returns:
    lines (list): lines of file
    """
    file = open(path, 'r')
    lines = file.readlines()
    lines = [(("<s> " + i).strip().strip("''") + " </s>").split(" ")
             for i in lines]
    return lines


def count_words_freq(model, dataset):
    """
    Function counts the frequencies of words given a model and a dataset of text
    model (string): type of model.
    dataset (list): list of sentences (list of lists)
    Return:
    ngram table (dict): dictionary where keys are each word(s) and values are their counts
    """
    ngram_table = {}
    for sentence in dataset:
        first_word = None
        second_word = None
        for word in sentence:
            if model == 'unigram':
                ngram_table[word] = ngram_table.get(word, 0) + 1
            if model == 'bigram':
                if first_word:
                    ngram_table[(first_word, word)] = ngram_table.get(
                        (first_word, word), 0) + 1
                first_word = word
            if model == 'trigram':
                if first_word:
                    if second_word:
                        ngram_table[(first_word, second_word, word)] = ngram_table.get(
                            (first_word, second_word, word), 0) + 1
                        first_word = second_word
                        second_word = word
                    else:
                        second_word = word
                else:
                    first_word = word
    # print(ngram_table)
    return ngram_table

def count_unique_words(dataset):
    """
    Function counts the number of unique words in a dataset
    dataset (list): list of sentences (list of lists)
    Return:
    len(unique_words) (int): number of unique words in dataset
    """
    unique_words = set()
    for sentence in dataset:
        for word in sentence:
            unique_words.add(word)
    return len(unique_words)

def train_ngram_model(model, dataset, laplace=False, k=0, vocab_size=None):
    """
    Function trains n gram model on the text dataset
    model (string): type of model.
    dataset (list): list of sentences (list of lists)
    laplace (boolean): whether or not to apply laplace smoothing
    k (int): smoothing constant
    vocab_size (int): number of unique words in dataset
    Returns:
    prob_table (dict): dictionary where keys are each word(s) and values are their probabilities
    """

    # Apply Laplace smoothing if laplace argument is true
    if laplace:
        k = 1
    elif not laplace:
        vocab_size = 1 # if no smoothing, set vocab size to 1 to ignore laplace smoothing calculation

    tokens_len = sum([len(word) for word in dataset])

    prob_table = {}
    # if laplace is true, state invalid entry
    if model == 'unigram' and laplace:
        print ("Invalid entry. Laplace smoothing not applicable to unigram model.")
        sys.exit()
    if model == 'unigram':
        word_table = count_words_freq(model, dataset)
        for word in word_table:
            prob_table[word] = word_table[word]/tokens_len
        return prob_table

    # needed for both bigrams and unigrams
    bigram_count_table = count_words_freq('bigram', dataset)

    if model == 'bigram':
        word_table = count_words_freq('unigram', dataset)
        for (first_word, second_word) in bigram_count_table:
            numerator = bigram_count_table[(first_word, second_word)]
            denominator = word_table[first_word] + k * vocab_size # Apply Laplace smoothing
            if not numerator or not denominator:
                prob_table[(first_word, second_word)] = k / vocab_size
            else:
                prob_table[(first_word, second_word)] = (numerator+k)/denominator
        return prob_table

    if model == 'trigram':
        trigram_count_table = count_words_freq(model, dataset)
        for (first_word, second_word, third_word) in trigram_count_table:
            numerator = trigram_count_table[(
                first_word, second_word, third_word)]
            denominator = bigram_count_table[(first_word, second_word)] + k * vocab_size # Apply Laplace smoothing
            if not numerator or not denominator:
                prob_table[(first_word, second_word, third_word)] = k / vocab_size
            else:
                prob_table[(first_word, second_word, third_word)
                           ] = (numerator+k)/denominator
    return prob_table


def eval_ppl(model, prob_table, dataset):
    """
    Function evaluates the preplexity of a text file at the given path
    model (string): type of model.
    prob_table (dict): dictionary where keys are each word(s) and values are their probabilities
    dataset (list): list of sentences (list of lists)
    Return 
    ppl (float): preplexity
    """

    tokens_len = sum([len(word) for word in dataset])

    log_probs = []
    for sentence in dataset:
        log_probs.append(math.fsum([math.log(prob_table[x])
                         for x in pairwise(model, sentence) if x in prob_table]))

    avg_log_prob = -math.fsum(log_probs)/tokens_len
    ppl = math.exp(avg_log_prob)
    return ppl


def pairwise(model, sentence_list):
    """
    Function iterates over word list n elements at a time, overlapping
    model (string): type of model.
    sentence_list (list): list of words to iterate through
    Return 
    ppl (float): preplexity
    """
    # resource: https://stackoverflow.com/questions/38151445/iterate-over-n-successive-elements-of-list-with-overlapping
    "s -> (s0, s1), (s2, s3), (s4, s5), ..."
    if model == 'unigram':
        return sentence_list
    if model == 'bigram':
        a, b = tee(sentence_list)
        next(b, None)
        return zip(a, b)
    if model == 'trigram':
        a, b, c = tee(sentence_list, 3)
        next(b, None)
        next(c, None)
        next(c, None)
        return zip(a, b, c)


main()
