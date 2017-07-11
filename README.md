# slp

Subregular toolkit for language processing.

Run _main.py_ to gain access to the functions.

### Extraction of Strictly k-Local (k-SL) grammar from the input data

   --- alphabet(data, text) ---
   find_sl collects _n_-grams that input data consists of.
   Arguments:
       * data (any iterable) -- data to be analyzed
       * n (integer) -- length of ngrams to be constructed
       * text (boolean) -- type of the data, symbols or text

### Extraction of Tier-based Strictly k-Local (k-TSL) grammar from the input data
**find_tsl** extracts tier-based strictly local grammar from the given data set. Follows the algorithm provided in (Jardine and McMullin in prep.)

Arguments: see _find_sl_ function.

    --- alphabet(data, text) ---
    Collects alphabet based on the input data. If text=False,
    considers words to be alphabet units.
    Arguments:
    * data (any iterable) -- data to be analyzed
    * text (boolean) -- type of the data, symbols or text
