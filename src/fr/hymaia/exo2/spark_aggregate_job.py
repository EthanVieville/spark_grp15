import pyspark.sql.functions as f
from pyspark.sql import SparkSession

def main():

    spark = SparkSession.builder.appName("aggregate").master("local[*]").getOrCreate()

    df_clean = spark.read.parquet("./src/resources/data/exo2/output")

    df_clean_population = population_by_departement(df_clean).show()

    df_clean_population.write.option("header", True).csv("src/resources/data/exo2/aggregate")

    spark.stop()

def population_by_departement(df_clean):
    def_population = df_clean.groupBy("departement").agg(f.count("*").alias("population")) \
        .orderBy(f.col("population").desc(), f.col("departement").asc())
    return def_population