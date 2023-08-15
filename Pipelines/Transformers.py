from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
from pyspark.sql.types import StringType, ArrayType

from pyspark.ml import Pipeline, Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol, Param, Params, TypeConverters
from pyspark.ml.feature import Bucketizer

spark = SparkSession.builder.appName('NLP').getOrCreate()
spark

import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize, word_tokenize

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import contractions

import json
from datetime import datetime


class SentTokenizer(Transformer, HasInputCol, HasOutputCol):
    def __init__(self, inputCol=None, outputCol=None):
        super(SentTokenizer, self).__init__()
        self.inputCol = inputCol
        self.outputCol = outputCol

    def _transform(self, df: DataFrame) -> DataFrame:
        transform_udf = F.udf(lambda x: sent_tokenize(x), ArrayType(StringType()))
        return df.withColumn(self.outputCol, transform_udf(df[self.inputCol]))
    

class WordTokenizer(Transformer, HasInputCol, HasOutputCol):
    def __init__(self, inputCol: str = "input", outputCol: str = "output"):
        super(WordTokenizer, self).__init__()
        self.inputCol = inputCol
        self.outputCol = outputCol

    def _transform(self, df: DataFrame) -> DataFrame:
        transform_udf = F.udf(lambda x: [word_tokenize(i.lower()) for i in x], ArrayType(ArrayType(StringType())))
        return df.withColumn(self.outputCol, transform_udf(df[self.inputCol]))
    

class BIO(Transformer, HasInputCol, HasOutputCol):
    TYPE_FIELD = 'type'
    TOCKEN_FIELD = 'tokens'
    LENGTH_FIELD = 'l'
    
    def __init__(self, inputCol: str = "input", outputCol: str = "output", all_tags: list = []):
        super(BIO, self).__init__()
        self.inputCol = inputCol
        self.outputCol = outputCol
        self.all_tags = all_tags

    def _transform(self, df: DataFrame) -> DataFrame:
        transform_udf = F.udf(self.BIO_format, ArrayType(ArrayType(ArrayType(StringType()))))
        return df.withColumn(self.outputCol, transform_udf(df[self.inputCol]))
    
    def BIO_format(self, sentenses):
        BIO_tags = []
        for words in sentenses:
            tags = ["O"] * len(words)
            for i in self.all_tags:
                tag = i[self.TYPE_FIELD]
                tag_words = i[self.TOCKEN_FIELD]
                tag_len = i[self.LENGTH_FIELD]
                for i in range(len(words) - tag_len + 1):
                    if words[i:i+tag_len] == tag_words:
                        tags[i] = f"B-{tag}"
                        for j in range(1, tag_len):
                            tags[i+j] = f"I-{tag}"

            if tags == ["O"] * len(words):
                continue
            BIO_tags.append(list(zip(words, tags)))
        return BIO_tags
    

class Contractions(Transformer, HasInputCol, HasOutputCol):    
    def __init__(self, inputCol: str = "input", outputCol: str = "output"):
        super(Contractions, self).__init__()
        self.inputCol = inputCol
        self.outputCol = outputCol

    def _transform(self, df: DataFrame) -> DataFrame:
        transform_udf = F.udf(lambda x: contractions.fix(x), StringType())
        return df.withColumn(self.outputCol, transform_udf(df[self.inputCol]))
    
class DeletePunct(Transformer, HasInputCol, HasOutputCol):    
    def __init__(self, inputCol: str = "input", outputCol: str = "output"):
        super(DeletePunct, self).__init__()
        self.inputCol = inputCol
        self.outputCol = outputCol

    def _transform(self, df: DataFrame) -> DataFrame:
        return df.withColumn(
            self.outputCol, 
            F.regexp_replace(
                self.inputCol,
                r"""[!\"#$%&'()*+,\-.\/:;<=>?@\[\\\]^_`{|}~]""",
                " "
            )
        )