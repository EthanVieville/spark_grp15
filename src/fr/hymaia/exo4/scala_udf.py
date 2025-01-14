import pyspark.sql.functions as f
from pyspark.sql import SparkSession
from pyspark.sql.column import Column, _to_java_column, _to_seq
from src.fr.hymaia.exo2.spark_session_provider import SparkSessionProvider

def main():
    # get session
    spark = SparkSessionProvider.get_spark_session()

    # Charger les données depuis un fichier CSV
    df_sell = spark.read.option("header", True).csv("./src/resources/exo4/sell.csv")

    # Ajouter une colonne category_name au DataFrame
    df_with_category_name = df_sell.withColumn(
        "category_name",
        addCategoryName(spark, f.col("category"))
    )

    df_with_category_name.show()

    SparkSessionProvider.reset_session()

def addCategoryName(spark, col):
    # get context
    sc = spark.sparkContext
    
    add_category_name_udf = sc._jvm.fr.hymaia.sparkfordev.udf.Exo4.addCategoryNameCol()
    # return
    return Column(add_category_name_udf.apply(_to_seq(sc, [col], _to_java_column)))


