"""
Use this module to setup the backend of your search system.
Use this module to load and push your data into 
Milvus & Postgres db after starting your Milvus and Postgres servers

$ python cli/build.py --data_path "/abs/path/to/data.csv" --model_name "multi-qa-MiniLM-L6-cos-v1"

"""
import pyspark

from src.tasks.build import build


def parse_arguments():
    """
    Use this function to pass the path to the dataset, and the name of the
    NLP model for vector embedding generation

    Returns
    -------
    args : dict
        a dict contaning build paramters
        { "data_path":  "/abs/path/to/data.csv",
          "model_name":  "multi-qa-MiniLM-L6-cos-v1" }

    """
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path",
        type=str,
        required=True,
        help="absolute path to input csv file",
    )
    parser.add_argument(
        "--model_name",
        type=str,
        required=True,
        help="name of the nlp model for embeddings generation",
    )
    args = parser.parse_args()
    return vars(args)


if __name__ == "__main__":
    conf = pyspark.SparkConf().setAppName("bd_project")
    conf.set("spark.driver.memory", "8g")
    conf.set("spark.worker.timeout", "10000000")
    conf.set("spark.driver.maxResultSize", "0")
    conf.set("spark.executor.memory", "8g")
    sc = pyspark.SparkContext(conf=conf)
    spark = pyspark.SQLContext.getOrCreate(sc)

    arguments = parse_arguments()
    build(arguments=arguments, spark_context=sc, spark_sql=spark)
