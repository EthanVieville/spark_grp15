import unittest
import pyspark.sql.functions as f
from pyspark.sql import Row
from src.fr.hymaia.exo2.spark_clean_job import integration_clean_job
from src.fr.hymaia.exo2.spark_aggregate_job import population_by_departement
from src.fr.hymaia.exo2.spark_session_provider import SparkSessionProvider


class TestClientFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSessionProvider.get_spark_session()

    @classmethod
    def tearDownClass(self):
        SparkSessionProvider.reset_session()

    def test_integration_clean_job(self):
        # given
        df_clients = self.spark.createDataFrame([
            Row(name="Alice", age=25, zip="75010"),
            Row(name="Bob", age=17, zip="75012"),  # minor
            Row(name="Charlie", age=30, zip="20115"),  # Corse 2A
            Row(name="David", age=35, zip="20200"),    # Corse 2B
        ])

        df_cities = self.spark.createDataFrame([
            Row(zip="75010", city="Paris"),
            Row(zip="75012", city="Paris"),
            Row(zip="20115", city="Ajaccio"),
            Row(zip="20200", city="Bastia"),
        ])

        # when
        df_cleaned = integration_clean_job(df_clients, df_cities)

        # then
        result = df_cleaned.collect()
        expected = [
            Row(zip="75010", name="Alice", age=25, city="Paris", departement="75"),
            Row(zip="20115",name="Charlie", age=30, city="Ajaccio", departement="2A"),
            Row(zip="20200",name="David", age=35, city="Bastia", departement="2B")
        ]

        self.assertEqual(result, expected)


        

    def test_integration_aggregate_job(self):
        # given
        df_clean = self.spark.createDataFrame([
            Row(name="Alice", departement="75"),
            Row(name="Bob", departement="75"),
            Row(name="Charlie", departement="13"),
            Row(name="David", departement="13"),
            Row(name="Eve", departement="75"),
            Row(name="Frank", departement="93"),
        ])

        # when
        df_population = population_by_departement(df_clean)

        # then 
        result = df_population.collect()
        expected = [
            Row(departement="75", population=3),  
            Row(departement="13", population=2),  
            Row(departement="93", population=1)   
        ]

        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()