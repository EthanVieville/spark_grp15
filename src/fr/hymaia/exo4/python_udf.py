import pyspark.sql.functions as f
from pyspark.sql import SparkSession
from src.fr.hymaia.exo2.spark_session_provider import SparkSessionProvider


def main():

    spark = SparkSessionProvider.get_spark_session()

    df_sell = spark.read.option("header", True).csv("./src/resources/exo4/sell.csv")

    df_major_clients = add_category_name(df_sell)

    df_major_clients.show()

    SparkSessionProvider.reset_session()


def add_category_name(df_sell):
    # Ajouter la colonne category_name en fonction de la valeur de category
    df_sell_with_category_name = df_sell.withColumn(
        "category_name",
        f.when(f.col("category") < 6, "food").otherwise("furniture")
    )
    return df_sell_with_category_name
