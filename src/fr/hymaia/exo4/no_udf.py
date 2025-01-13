import pyspark.sql.functions as f
from src.fr.hymaia.exo2.spark_session_provider import SparkSessionProvider
from pyspark.sql.window import Window


def main():
    # Obtenir la SparkSession depuis le provider
    spark = SparkSessionProvider.get_spark_session()

    # Charger les données depuis un fichier CSV
    df_sell = spark.read.option("header", True).csv("./src/resources/exo4/sell.csv")

    # Ajouter la colonne `category_name` sans utiliser de UDF
    df_with_category_name = df_sell.withColumn(
        "category_name",
        f.when(f.col("category") < 6, "food").otherwise("furniture")
    )

    # Afficher les résultats
    #df_with_category_name.show()

    sums_1 = True
    sums_2 = False

    if sums_1:
        # Définir la fenêtre pour le calcul des sommes par catégorie et jour
        # Ce n'était pas précisé si c'était category ou category_name, category a donc été choisis*
        window_spec = Window.partitionBy("category", "date")

        # Calculer la somme des prix par jour et catégorie (total_price_per_category_per_day)
        df_with_daily_sum = df_with_category_name.withColumn(
            "total_price_per_category_per_day",
            f.sum("price").over(window_spec)
        )

        # Pour vérifier pour chaque catégorie, utiliez ce df :
        df_with_daily_sum_unique = df_with_daily_sum.dropDuplicates(["date", "category"])

        df_with_daily_sum_unique.show()


    if sums_2:
                  # Convertir price en double
        df = df_with_category_name.withColumn("price", f.col("price").cast("double"))
        
        # Convertir date en type date
        df = df.withColumn("date", f.to_date("date"))

        # Ajouter une colonne avec un timestamp pour plus de contrôle
        df = df.withColumn("timestamp", f.col("date").cast("timestamp"))

        # Fenêtre glissante : utiliser `ROWS BETWEEN` et une jointure sur les 30 derniers jours
        window_spec = Window.partitionBy("category").orderBy("timestamp")

        # **Repartitionner les données avant les transformations**
        df_repart = df.repartition(100)  # Ajuste 200 en fonction de la taille de ton dataset

        # Ajouter une colonne avec les résultats de la somme sur 30 jours (logique explicite)
        df_with_sum = df_repart.withColumn(
            "total_price_per_category_per_day_last_30_days",
            f.sum("price").over(window_spec.rowsBetween(Window.unboundedPreceding, Window.currentRow))
        )

        # Afficher le résultat final
        df_with_sum.orderBy("category", "timestamp").show()
    
    # Nettoyer la SparkSession via le provider
    SparkSessionProvider.reset_session()

