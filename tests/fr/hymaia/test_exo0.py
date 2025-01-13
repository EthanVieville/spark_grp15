from tests.fr.hymaia.spark_test_case import spark
import unittest
from src.fr.hymaia.exo1.main import wordcount
from pyspark.sql import Row

from src.fr.hymaia.exo2.spark_session_provider import SparkSessionProvider


class TestMain(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.spark = SparkSessionProvider.get_spark_session()

    @classmethod
    def tearDownClass(self):
        SparkSessionProvider.reset_session()

    def test_wordcount(self):
    
        input = self.spark.createDataFrame(
            [
                Row(text='bonjour je suis un test unitaire'),
                Row(text='bonjour suis test')
            ]
        )
        expected = self.spark.createDataFrame(
            [
                Row(word='bonjour', count=2),
                Row(word='je', count=1),
                Row(word='suis', count=2),
                Row(word='un', count=1),
                Row(word='test', count=2),
                Row(word='unitaire', count=1),
            ]
        )

        actual = wordcount(input, 'text')

        self.assertCountEqual(actual.collect(), expected.collect())

