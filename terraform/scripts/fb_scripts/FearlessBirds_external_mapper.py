import sys
import uuid 
import math 
import pytz 
import boto3
import logging 
#import datetime 
from datetime import datetime, date, timedelta 
from awsglue.utils import getResolvedOptions 
from awsglue.context import GlueContext 
from awsglue.transforms import * 
from pyspark.sql.functions import *
from pyspark.sql.types import *
# from pyspark.context import SparkContext 
from pyspark.sql import SparkSession
# from pyspark.sql import SQLContext, SparkSession 
from pyspark.sql.window import Window
from pyspark.sql import functions as F 
from functools import reduce 
from pyspark.sql import Row 
# from cei _common_reusable_functions import * 
from FearlessBirds_idConversionHandler import idMappingHandler

# Initialize GlueContext
spark = SparkSession.builder.appName("GlueJob").getOrCreate()
glueContext = GlueContext(spark.sparkContext)

#---- Setting up loggers 
logging.basicConfig(format= '%(asctime)s %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S' ) 
root = logging.getLogger(__name__)
root.setLevel(logging.DEBUG) 

####--- Glue Arguments ＃井井井 # 
# args = getResolvedOptions (sys.argv, ["process", "results_bucket", "scripts_bucket", "region"]) 
process = ""
region = "us-east-1" 
results_bucket = "fearless-birds-results"
scripts_bucket = "fearless-birds-scripts" 

###-－・・－-Date  一并井井 
local_timezone = pytz.timezone('America/Chicago')
ct = datetime.now(local_timezone)
current_date = ct.strftime ("%Y-%m-%d") 
date_str = ct.strftime ("%m-%d-%Y")
ct = ct.strftime("%Y-%m-%d-%H-%M-%s")
journey = "adhoc"

def idMapper(flag,output_file_path,input_file_path,sensitiveFieldList):

    sensitive_data_df = spark.read.format("csv").option("header",True).option("sep", "|").load(input_file_path)
    
    if flag == "external":
        secure_data_df = idMappingHandler().translateToExternalId(sensitive_data_df,results_bucket,date_str,journey,sensitiveFieldList)
    elif flag == "internal":
        secure_data_df - idMappingHandler().translateToInternalId(sensitive_data_df,results_bucket,sensitiveFieldList)
    
    secure_data_df.repartition(1).write.option("header",True).option("delimiter", "|").mode("append").csv(output_file_path)


if __name__ == "__main__":
    
    ### Pipe delimited cs sensitive data file(with header) directory in 53 bucket.
    # input_file_path = "s3://"+results_bucket+"/folder name/file name.csv"
    input_file_path ="s3://fearless-birds-results/test_data_encryption.csv"
    
    ### S3 directory to write resultant file Pipe delimited sv with header). 
    # output_file_path = "s3://"+results_bucket+"/folder _name/"
    output_file_path = "s3://fearless-birds-results/"
    
    ### List of columns/fields that requires masking/unmasking. must be one or more of ["claim_id", "bob_id", "assoc_id"]. 
    # sensitiveFieldList = ["field1", "field2", "fei1d3"]
    sensitiveFieldList = ["bob_id"]
    
    
    ### set flag variable to call translateToExternalId/translateToInternalId function.
    flag = "external" ### "external" (or) "internal".
    
    idMapper(flag,output_file_path,input_file_path,sensitiveFieldList)
    
    spark.stop()