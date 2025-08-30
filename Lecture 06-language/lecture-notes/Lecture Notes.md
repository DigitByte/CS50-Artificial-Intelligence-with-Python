## Language

Until now, we shaped data so AI could process it. Today we explore how AI can handle **human language**.

**Natural Language Processing (NLP)** covers tasks where input is human language. Examples:

* **Summarization**: input text → shorter summary.
* **Information extraction**: input corpus → structured data.
* **Language ID**: detect the language.
* **Machine translation**: translate between languages.
* **Named entity recognition (NER)**: detect names (e.g., companies).
* **Speech recognition**: speech → text.
* **Text classification**: e.g., spam vs. not spam.
* **Word sense disambiguation**: pick correct meaning of ambiguous words (e.g., *bank*).

## Syntax and Semantics

* **Syntax**: sentence structure (e.g., word order). A sentence can be grammatical yet ambiguous ("I saw the man with the telescope").
* **Semantics**: meaning. Different wording can convey the same idea. Some sentences may be grammatical but meaningless ("Colorless green ideas sleep furiously").

Both are essential for AI to parse and generate human language.

## Context-Free Grammar

Formal grammar gives structure without focusing on meaning. Example sentence:

* *She saw the city.*

Parts of speech:

* She → Noun (N)
* Saw → Verb (V)
* The → Determiner (D)
* City → Noun (N)

So: **N V D N**. These group into **phrases**:

* NP (noun phrase): *she*, *the city*.
* VP (verb phrase): *saw*, *saw the city*.
* S (sentence): NP + VP.

This abstraction lets AI model sentence structure.

### Example with nltk

```python
import nltk

grammar = nltk.CFG.fromstring("""
    S -> NP VP

    NP -> D N | N
    VP -> V | V NP

    D -> "the" | "a"
    N -> "she" | "city" | "car"
    V -> "saw" | "walked"
""")

parser = nltk.ChartParser(grammar)

sentence = input("Sentence: ").split()
try:
    for tree in parser.parse(sentence):
        tree.pretty_print()
        tree.draw()
except ValueError:
    print("No parse tree possible.")
```

## n-grams

An **n-gram** is a sequence of n items:

* **Unigram** = 1 item
* **Bigram** = 2 items
* **Trigram** = 3 items

Example: “how often have I said…” → “how often have,” “often have I,” “have I said.”

Useful for prediction: your phone suggests next words from probabilities learned from n-grams.

## Tokenization

Splitting text into **tokens** (words or sentences). Challenges:

* Punctuation (e.g., *remains,* vs *remains*).
* Apostrophes, hyphens, abbreviations (e.g., “o’clock,” “Mr.”).

Tokenization is a key preprocessing step for NLP.

## Markov Models

Markov models predict next items from a fixed history. For text:

* Train on corpus.
* Build probabilities of word sequences.
* Generate text one word at a time from distributions.

This produces grammatical, but often meaningless, text.

## Bag-of-Words

Represents text as an **unordered collection of words**, ignoring grammar.

Example: sentiment classification.

* Positive: “loved,” “fun,” “best.”
* Negative: “broke,” “cheap,” “flimsy.”

## Naive Bayes

Uses Bayes’ Rule to classify text sentiment:

We calculate P(sentiment | words). Simplify by assuming **word independence** (the “naive” part). Despite being unrealistic, this works well.

Example: “my grandson loved it” → high probability of positive.

* Uses **additive smoothing** (e.g., Laplace = +1 to counts) to avoid zero probabilities.

## Word Representation

Words must be represented as numbers.

* **One-hot encoding**: each word = long sparse vector (inefficient, no similarity info).
* **Distributed representation**: shorter dense vectors capture semantic similarity.

Example: “king – man + woman ≈ queen.”

## word2vec

**word2vec** generates distributed word vectors via **skip-gram neural networks**:

* Input: target word.
* Output: likely context words.
* Hidden layer → learned embeddings.

Result: semantically similar words have similar vectors.

Example: *book* → closest vectors: book, books, essay, memoir, etc.

## Neural Networks for Sequences

Translation requires mapping sequences to sequences.

* **RNNs (Recurrent Neural Networks)** keep hidden states across steps.
* Problems: storing long sequences in one state, uneven importance of words.

## Attention

Attention lets the model **focus on relevant words** (e.g., “capital” and “Massachusetts” in “What is the capital of Massachusetts?”).

* Context vectors are weighted sums of hidden states.
* Improves translation and comprehension.

## Transformers

**Transformers** process all words in parallel:

* Add **positional encoding** to keep word order.
* Use **self-attention** layers to capture context.
* Encoding + decoding steps with multiple attention layers.

Benefits: faster training, scalable, highly accurate.

## Wrap-up

We’ve seen how AI handles language:

* Syntax & semantics
* Grammars & parsing
* n-grams, tokenization, Markov models
* Bag-of-words, Naive Bayes
* Word embeddings, word2vec
* RNNs, Attention, Transformers

This brings AI closer to truly understanding and producing human language.

