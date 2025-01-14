import sys

from awsglue.context import GlueContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql import SparkSession
# TODO : import custom spark code dependencies

if __name__ == '__main__':
    spark = SparkSession.builder.getOrCreate()
    glueContext = GlueContext(spark.sparkContext)
    job = Job(glueContext)
    args = getResolvedOptions(sys.argv, ["JOB_NAME", "PARAM_1", "PARAM_2"])
    job.init(args['JOB_NAME'], args)

    param1 = args["PARAM_1"]
    param2 = args["PARAM_2"]

    # Récupère les paramètres (des input et output vers S3 en temps normal ?)
    input_path = args["PARAM_1"]  
    output_path = args["PARAM_2"] 

    # SIMULATION : 

    # "Charger des donneés depuis S3"
    df = spark.read.csv(input_path, header=True, inferSchema=True)  # (CSV ici)

    # On applique une transformation simple
    df_transformed = df.filter(df["value"] > 100)  

    # On affiche (CAR SPARK EST LAZY)
    df_transformed.show()

    # Save les donneés sur S3
    df_transformed.write.csv(output_path, header=True, mode="overwrite")

    job.commit()