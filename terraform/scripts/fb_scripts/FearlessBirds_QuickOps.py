import logging
from pyspark.sql import SparkSession


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Spark session
spark = SparkSession.builder.appName("ReadWritePipeDelimitedCSV").getOrCreate()

# Set log level to INFO
spark.sparkContext.setLogLevel("INFO")

# Define S3 paths
input_path = "s3a://your-bucket/input-file.csv"
output_path = "s3a://your-bucket/output-directory/"

def fearlessBirds_quickOps():
    
    # Read pipe-delimited CSV file from S3
    logger.info("Reading pipe-delimited CSV file from S3")
    df = spark.read.option("delimiter", "|").csv(input_path, header=True, inferSchema=True)

    # Write the DataFrame back to S3 in CSV format
    logger.info("Writing the DataFrame back to S3 in CSV format")
    df.write.option("delimiter", "|").csv(output_path, header=True)

    # Stop the Spark session
    logger.info("Stopping the Spark session")
    spark.stop()
    

if __name__ == "__main__":
    fearlessBirds_quickOps()
