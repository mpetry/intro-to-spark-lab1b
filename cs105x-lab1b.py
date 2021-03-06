labVersion = 'cs105x-word-count-df-0.1.0'

# 1a

wordsDF = sqlContext.createDataFrame([('cat',), ('elephant',), ('rat',), ('rat',), ('cat', )], ['word'])
wordsDF.show()
print type(wordsDF)
wordsDF.printSchema()

# 1b

from pyspark.sql.functions import lit, concat

pluralDF = wordsDF.select(concat(wordsDF.word, lit('s')).alias('word'))
pluralDF.show()

# 1c

from pyspark.sql.functions import length
pluralLengthsDF = pluralDF.select(length('word').alias('length'))
pluralLengthsDF.show()

# 2a

wordCountsDF = (wordsDF
                .groupBy('word')
                .count()
                )
wordCountsDF.show()

# 3a

from spark_notebook_helpers import printDataFrames

#This function returns all the DataFrames in the notebook and their corresponding column names.
printDataFrames(True)

uniqueWordsCount = (wordCountsDF
                     .count()
                   )
print uniqueWordsCount

# 3b

averageCount = (wordCountsDF
                  .groupBy()
                  .mean('count')
                  .first()[0]
               )

print averageCount

# 4a

def wordCount(wordListDF):
    """Creates a DataFrame with word counts.

    Args:
        wordListDF (DataFrame of str): A DataFrame consisting of one string column called 'word'.

    Returns:
        DataFrame of (str, int): A DataFrame containing 'word' and 'count' columns.
    """
    
    return (wordListDF.groupBy('word').count())
  
wordCount(wordsDF).show()

# 4b

from pyspark.sql.functions import regexp_replace, trim, col, lower
def removePunctuation(column):
    """Removes punctuation, changes to lower case, and strips leading and trailing spaces.

    Note:
        Only spaces, letters, and numbers should be retained.  Other characters should should be
        eliminated (e.g. it's becomes its).  Leading and trailing spaces should be removed after
        punctuation is removed.

    Args:
        column (Column): A Column containing a sentence.

    Returns:
        Column: A Column named 'sentence' with clean-up operations applied.
    """
  
    return trim(regexp_replace(lower(column), '([^\w\s]|_)', ""))

sentenceDF = sqlContext.createDataFrame([('Hi, you!',),
                                         (' No under_score!',),
                                         (' *      Remove punctuation then spaces  * ',)], ['sentence'])
sentenceDF.show(truncate=False)
(sentenceDF
 .select(removePunctuation(col('sentence')))
 .show(truncate=False))
 
 # 4c
 
 fileName = "dbfs:/databricks-datasets/cs100/lab1/data-001/shakespeare.txt"

shakespeareDF = sqlContext.read.text(fileName).select(removePunctuation(col('value')).alias('sentence'))
shakespeareDF.show(15, truncate=False)

$ 4d

from pyspark.sql.functions import split, explode
shakeWordsDF = shakespeareDF.select(split(shakespeareDF.sentence, ' ').alias('word'))
shakeWordsDF = shakeWordsDF.select(explode(shakeWordsDF.word))
shakeWordsDF = shakeWordsDF.select(col('col').alias('word'))
shakeWordsDF = shakeWordsDF.where(shakeWordsDF.word != '')

shakeWordsDF.show()
shakeWordsDFCount = shakeWordsDF.count()
print shakeWordsDFCount

# 4e

from pyspark.sql.functions import desc
topWordsAndCountsDF = wordCount(shakeWordsDF)
topWordsAndCountsDF = topWordsAndCountsDF.select(col("word").alias("word"), col("count").alias("number"))
topWordsAndCountsDF = topWordsAndCountsDF.orderBy(topWordsAndCountsDF.number.desc())
topWordsAndCountsDF.show()