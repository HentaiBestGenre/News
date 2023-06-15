import pyspark.sql.functions as F
from pyspark.ml import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol
from pyspark.sql import DataFrame
from pyspark.sql.types import StringType, ArrayType


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
    