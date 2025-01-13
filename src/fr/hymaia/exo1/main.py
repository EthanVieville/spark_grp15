import pyspark.sql.functions as f
from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder.appName("wordcount").master("local[*]").getOrCreate()

    df = spark.read.option("header", True).csv("./src/resources/exo1/data.csv")

    df_out = wordcount(df, "text")

    df_out.write.mode("overwrite").partitionBy("count").parquet("src/resources/data/exo1/output")

    spark.stop()


def wordcount(df, col_name):
    return df.withColumn('word', f.explode(f.split(f.col(col_name), ' '))) \
        .groupBy('word') \
        .count()
