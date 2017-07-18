# slp

Subregular toolkit for language processing. Run _main.py_ to gain access to the functions.

#### Extraction of Strictly k-Local (k-SL) grammar from the input data

    --- find_sl(data, n, polar, param) ---
    Extracts strictly local grammar from the given data set.
    Arguments:
    * data (any iterable or a filename) -- data to be analyzed
    * polar (True or False) -- positive/negative grammar to be extracted
    * n (integer) -- length of ngrams to be constructed
    * param ("s", "m", "w") -- type of the data: symbols, morphemes, or words



#### Extraction of Tier-based Strictly k-Local (k-TSL) grammar from the input data

    --- find_tsl(data, n, polar, param) ---
    Extracts tier-based strictly local grammar from the given
    data set. Follows the algorithm provided in (Jardine and
    McMullin in prep.) with small modifications.
    Arguments: see find_sl function.

#### Extraction of the alphabet from the input data

    --- alphabet(data, param) ---
    Collects alphabet based on the input data type ("s", "m", "w")
    Arguments:
    * data (any iterable) -- data to be analyzed
    * param ("s", "m", "w") -- type of the data, symbols, morphemes, or words
