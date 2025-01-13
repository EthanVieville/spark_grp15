import unittest
import pyspark.sql.functions as f
from pyspark.sql import Row
from src.fr.hymaia.exo2.spark_clean_job import filter_major, join_clients_cities, add_departement 
from src.fr.hymaia.exo2.spark_aggregate_job import population_by_departement 
from src.fr.hymaia.exo2.spark_session_provider import SparkSessionProvider


class TestClientFunctions(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSessionProvider.get_spark_session()

    @classmethod
    def tearDownClass(self):
        SparkSessionProvider.reset_session()

    def test_filter_major(self):
        # given
        df_clients = self.spark.createDataFrame([
            Row(name="Oui", age=12, zip="17540"),
            Row(name="AhOui", age=88, zip="11410"),
            Row(name="Non", age=23, zip="61570"),
            Row(name="AhNon", age=2, zip="62310")
        ])

        # when
        df_major_clients = filter_major(df_clients)

        # then
        result = df_major_clients.collect()
        expected = [
            Row(naame="AhOui", age=88, zip="11410"),
            Row(naame="Non", age=23, zip="61570")
        ]

        self.assertEqual(result, expected)
        
    
    def test_filter_major_invalid_age(self):
        # given
        df_clients = self.spark.createDataFrame([
            Row(name="Alice", age=-5, zip="17540"),  # Âge invalide
            Row(name="Bob", age=25, zip="11410"),
        ])

        # when (*n then)
        with self.assertRaises(ValueError) as error:
            filter_major(df_clients)
        
        # on verifie le contenu de l'exception catcher (dnc que le msg récupérer est le bon)
        self.assertEqual(str(error.exception), "age must be > 0 !")


    def test_join_clients_cities(self):
        # given
        df_clients = self.spark.createDataFrame([
            Row(name="AhOui", age=88, zip="11410"),
            Row(name="Non", age=23, zip="61570"),
        ])

        df_cities = self.spark.createDataFrame([
            Row(zip="11410", city="PAYRA SUR L HERS"),
            Row(zip="61570", city="MEDAVY")
        ])

        # when
        df_joined = join_clients_cities(df_clients, df_cities)

        # then
        result = df_joined.collect()
        expected = [
            Row(zip="11410", name="AhOui", age=88, city="PAYRA SUR L HERS"),
            Row(zip="61570", name="Non", age=23, city="MEDAVY")
        ]

        self.assertEqual(result, expected)

    def test_add_departement(self):
        # given
        df_joined = self.spark.createDataFrame([
            Row(name="AhOui", age=46, zip="11410", city="PAYRA SUR L HERS"),
            Row(name="AhPeutEtre", age=24, zip="20167", city="AJACCIO"),  # Corse 2A
            Row(name="AhJePensePas", age=39, zip="20200", city="BASTIA")     # Corse 2B
        ])

        # when
        df_with_dept = add_departement(df_joined)

        # then
        result = df_with_dept.collect()
        expected = [
            Row(name="AhOui", age=46, zip="11410", city="PAYRA SUR L HERS", departement="11"),
            Row(name="AhPeutEtre", age=24, zip="20167", city="AJACCIO", departement="2A"),
            Row(name="AhJePensePas", age=39, zip="20200", city="BASTIA", departement="2B")
        ]

        self.assertEqual(result, expected)

    def test_count_population_by_departement(self):
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
            Row(departement="75", population=3),  # 3 / 75
            Row(departement="13", population=2),  # 2 / 13
            Row(departement="93", population=1)   # 1 / 93
        ]
        

        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
