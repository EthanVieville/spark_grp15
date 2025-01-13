import pyspark.sql.functions as f
from pyspark.sql import SparkSession


def main():

    spark = SparkSession.builder.appName("python_udf").master("local[*]").getOrCreate().config('spark.jars', 'src/resources/exo4/udf.jar') \

    df_sell = spark.read.option("header", True).csv("./src/resources/exo4/sell.csv")

    df_major_clients = add_category_name(df_sell).show()

    spark.stop()


def add_category_name(df_sell):
    # Ajouter la colonne category_name en fonction de la valeur de category
    df_sell_with_category_name = df_sell.withColumn(
        "category_name",
        f.when(f.col("category") < 6, "food").otherwise("furniture")
    )
    return df_sell_with_category_name
