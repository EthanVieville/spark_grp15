from pyspark.sql import SparkSession

class SparkSessionProvider:
    _spark_session = None

    @classmethod
    def get_spark_session(cls):
        if cls._spark_session is None:
            cls._spark_session = SparkSession.builder \
                .appName("Test") \
                .master("local[*]") \
                .config('spark.jars', 'src/resources/exo4/udf.jar') \
                .config("spark.executor.instances", "8") \
                .config("spark.executor.cores", "4") \
                .getOrCreate()
        return cls._spark_session

    @classmethod
    def reset_session(cls):
        if cls._spark_session:
            cls._spark_session.stop()
        cls._spark_session = None  


