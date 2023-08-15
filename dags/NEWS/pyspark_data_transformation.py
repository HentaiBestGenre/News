from nltk.tokenize import sent_tokenize, word_tokenize
import pymongo

from pyspark.sql import SparkSession
from pyspark.sql import DataFrame
from pyspark.sql.types import StringType, ArrayType
import pyspark.sql.functions as F
from pyspark.ml import Pipeline
from pyspark.ml import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol


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
        transform_udf = F.udf(lambda x: [word_tokenize(i) for i in x], ArrayType(StringType()))
        return df.withColumn(self.outputCol, transform_udf(df[self.inputCol]))


class BIO(Transformer, HasInputCol, HasOutputCol):
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
                tag = i['type']
                tag_words = i['tokens']
                tag_len = i['l']
                for i in range(len(words) - tag_len + 1):
                    if words[i:i+tag_len] == tag_words:
                        tags[i] = f"B-{tag}"
                        for j in range(1, tag_len):
                            tags[i+j] = f"I-{tag}"

            if tags == ["O"] * len(words):
                continue
            BIO_tags.append(list(zip(words, tags)))
        return BIO_tags

if __name__ == "__main__":
    mongo_client = pymongo.MongoClient("mongodb://localhost:27017")
    db = mongo_client["news_classification"]
    tags = list(db.Tags.find({}).sort('l'))

    spark=SparkSession.builder.master("local[*]").appName('NLP').getOrCreate()
    columns = ["_id", "title", "text"]
    df = spark.read.json("/tmp/new_articles.json").select(columns)
    df = df.rdd.map(
        lambda x: x + (' '.join([f"{x.title}. "] + [i['text'] for i in x.text]).lower(), )
    ).toDF(["_id", "title", "text", 'full_text'])

    sent_transformer = SentTokenizer(inputCol="full_text", outputCol="sentenses")
    word_transformer = WordTokenizer(inputCol="sentenses", outputCol="tokenized_text")
    bio_transformer = BIO(inputCol="tokenized_text", outputCol="BIO", all_tags=tags)
    pipeline = Pipeline(stages=[sent_transformer, word_transformer, bio_transformer])
    results = pipeline.fit(df).transform(df)
    results = results.select('_id', 'BIO')
    results = results.filter(F.size(results.BIO) > 0)
    
    pandas_df = results.toPandas()
    json_array = pandas_df.to_json(path_or_buf='/tmp/clean_articles.json', orient='records')
    