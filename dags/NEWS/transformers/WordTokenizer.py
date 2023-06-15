from nltk.tokenize import word_tokenize

import pyspark.sql.functions as F
from pyspark.ml import Transformer
from pyspark.ml.param.shared import HasInputCol, HasOutputCol
from pyspark.sql import DataFrame
from pyspark.sql.types import StringType, ArrayType
    
    
class WordTokenizer(Transformer, HasInputCol, HasOutputCol):
    def __init__(self, inputCol: str = "input", outputCol: str = "output"):
        super(WordTokenizer, self).__init__()
        self.inputCol = inputCol
        self.outputCol = outputCol

    def _transform(self, df: DataFrame) -> DataFrame:
        transform_udf = F.udf(lambda x: [word_tokenize(i) for i in x], ArrayType(StringType()))
        return df.withColumn(self.outputCol, transform_udf(df[self.inputCol]))
