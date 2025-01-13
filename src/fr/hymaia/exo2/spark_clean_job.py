import pyspark.sql.functions as f
from pyspark.sql import SparkSession


def main():

    spark = SparkSession.builder.appName("clean").master("local[*]").getOrCreate()

    df_clients = spark.read.option("header", True).csv("./src/resources/exo2/clients_bdd.csv")

    df_major_clients = filter_major(df_clients)

    df_cities = spark.read.option("header", True).csv("./src/resources/exo2/city_zipcode.csv")

    df_joined = join_clients_cities(df_major_clients, df_cities)

    df_joined_departement = add_departement(df_joined)

    df_joined_departement.write.mode("overwrite").parquet("src/resources/data/exo2/output")

    spark.stop()


def filter_major(df_clients):
    # vérif des âges négatif (pour générer une erreur)
    if df_clients.filter(f.col("age") < 0).count() > 0:
        raise ValueError("age must be > 0 !")

    # Filtre major
    df_filtered = df_clients.withColumn("age", f.col("age").cast("int")).filter(f.col("age") >= 18)
    return df_filtered


def join_clients_cities(df_clients, df_cities):
    return df_clients.join(df_cities, on="zip")

def add_departement(df_joined):
    df_joined_departement = df_joined.withColumn(
        "departement",
        f.when(
            (f.substring(f.col("zip"), 1, 2) == '20') & (f.col("zip").cast("int") <= 20190),
            "2A"
        ).when(
            (f.substring(f.col("zip"), 1, 2) == '20') & (f.col("zip").cast("int") > 20190),
            "2B"
        ).otherwise(f.substring(f.col("zip"), 1, 2))
    )
    return df_joined_departement

def integration_clean_job(df_clients, df_cities):
    df_major_clients = filter_major(df_clients)
    df_joined = join_clients_cities(df_major_clients, df_cities)
    df_joined_departement = add_departement(df_joined)
    return df_joined_departement
   