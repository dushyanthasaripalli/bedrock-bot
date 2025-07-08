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
from pyspark.types import * 
from pyspark.context import SparkContext 
from pyspark.sql import SQLContext, SparkSession 
from pyspark.sql.window import Window
from pyspark.sql import functions as F 
from functools import reduce 
from pyspark.sql import Row 
# from cei _common_reusable_functions import * 

#---- Setting up loggers 
logging.basicConfig(format= '%(asctime)s %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S' ) 
root = logging.getLogger(__name__)
root.setLevel(logging.DEBUG) 

####Spark set up －#### 
# sc = SparkContext.getOrCreate() 
# glueContext = GlueContext(sc) 
# spark = glueContext.spark_session 
spark = SparkSession.builder.appName('PySpark DataFrame').getOrCreate()

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
ct = ct.strftime("%Y-%m-%d-%H-%M-%s")