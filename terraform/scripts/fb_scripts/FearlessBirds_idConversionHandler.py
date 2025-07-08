"""
-> idMappingHandler is created for the purpose of Anonymization for any Classified Fields present in Sensitive Data Files.
-> Classified Field Anonymization Function in this library considers files present in AWS S3 bucket prefix("s3://bucket_name/external_id_mapper/) as Mapper DB.
-> Data stored in Mapper DB are in format of pipe delimited csv files.
"""

import logging,sys
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from functools import reduce
from pyspark.sql import Row
from awsglue.transforms import *
from pyspark.sql.functions import *
from pyspark.sql.types import *

class idMappingHandler():

    def __init__(self):
        self.spark = SparkSession.builder.appName('Classified Fields Anonymization').getOrCreate()
        logging.basicConfig(format='%(asctime)s %(levelname)s %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.root = logging.getLogger(__name__) 
        self.root.setLevel(logging.DEBUG)

    ### Store ID Mappings into S3 Directory.
    def storeMaskedIdDataMappings(self,sensitiveFieldList,sensitive_data_df,mapper_db_internal_id_list,results_bucket,date_str,journey):
        self.root.info("==== storeMaskedIdDataMappings Function Initiated ======")
        accumulator_df = [] 
    
        for classifiedField in range(len(sensitiveFieldList)):
            sensitive_data_df = sensitive_data_df.withColumn("type", lit(sensitiveFieldList[classifiedField]))\
                                                 .withColumn("internal_id",col(sensitiveFieldList[classifiedField]))\
                                                 .withColumn("external_id",col('external_id_'+str(sensitiveFieldList[classifiedField])))
            accumulator_df.append(sensitive_data_df)
        
        sensitive_data_df = reduce(DataFrame.union, accumulator_df)
        sensitive_data_df = sensitive_data_df.withColumn("creation_timestamp", date_format(current_timestamp(),"MM-dd-yyyy HH:mm:ss"))
        
        sensitive_data_df = sensitive_data_df.select("internal_id", "external_id", "creation_timestamp", "type")
        sensitive_data_df_db_data = sensitive_data_df.join( F.broadcast( self.spark.createDataFrame( [(ID,) for ID in mapper_db_internal_id_list],["internal_id"])),["internal_id"],"leftanti")
        
        sensitive_data_df_db_data = sensitive_data_df_db_data.filter( (sensitive_data_df_db_data.internal_id.isNotNull()) & (sensitive_data_df_db_data.internal_id != "" ) )
        
        self.root.info("===== Records generated with new extrnl_id in current run: {} ======".format(sensitive_data_df_db_data.distinct().count())) 
        
        sensitive_data_df_db_data.distinct().repartition(1).write.option ("header",True).option("delimiter","|").mode("append").csv("s3://"+results_bucket+"/external_id_mapper/"+date_str+"_"+journey+"/") if sensitive_data_df_db_data.count()>0 else self.root.info(" -======= No New Records generated to store into Mapper DB =======")

        self.root.info("======= storeMaskedIdDataMappings Function Completed =======")


    ### Conversion of Sensitive fields to Universally Unique Identifiers. translateToExternalId
    def translateToExternalId(self,sensitive_data_df_input,results_bucket,date_str,journey,sensitiveFieldList):
        self.root.info("======== translateToExternalId Function Initiated ========")
        self.root.info("====== Records_count_from_input data received: {} ===-==".format(sensitive_data_df_input.count()))

        ### Restricting conversion for mentioned fields. 
        
        allowed_field_list = ["claim_id", "bob_id", "assoc_id"] 
        if all(item in allowed_field_list for item in sensitiveFieldList):
            self.root.info("======== fields provided in sensitiveFieldList are in allowed range for conversion ========")
        else:
            sys.exit("========= Error: One or more fields provided in sensitiveFieldlist is out of allowed fileds for conversion, accepted fields are [ claim id','bob_id','assoc_id' ] ====")

        df_external_id_mapper_db = self.spark.read.format("csv").option ("header",True).option("sep","|").load("s3://"+results_bucket+"/external_id_mapper/*") 
        df_external_id_mapper_db = df_external_id_mapper_db.select ("internal_id", "external_id").distinct() 
        
        columns = sensitive_data_df_input.columns
        sensitive_data_df = sensitive_data_df_input.select(*sensitiveFieldList)
        sensitive_data_df = sensitive_data_df.dropDuplicates([*sensitiveFieldList])
        mapper_db_internal_id_list = df_external_id_mapper_db.select("internal_id").rdd.flatMap(lambda x: x).collect()
        
        placeholder = "external_id_generator"
        accumulator_df = self.spark.createDataFrame([ Row(placeholder=placeholder) ])
        accumulator_df_external_data = accumulator_df

        ### Collection of masked data for any matched pre-existing sensitive data from Mapper_DB. 
        for classifiedField in range(len(sensitiveFieldList)):
            sensitive_data_df_filtered = sensitive_data_df.filter((sensitive_data_df[sensitiveFieldList[classifiedField]].isNotNull())&(sensitive_data_df[sensitiveFieldList[classifiedField]] != "" ))
            df_selected_field = sensitive_data_df_filtered.select(sensitiveFieldList[classifiedField])
            
            sensitive_data_df_matched_with_mapper_db = df_selected_field.join( F.broadcast( self.spark.createDataFrame( [(ID,) for ID in mapper_db_internal_id_list],[sensitiveFieldList[classifiedField]])),on=sensitiveFieldList[classifiedField],)
            
            sensitive_data_df_matched_with_mapper_db = sensitive_data_df_matched_with_mapper_db.withColumnRenamed(sensitiveFieldList[classifiedField], "matched_internal_id")
            
            accumulator_df = accumulator_df.unionByName(sensitive_data_df_matched_with_mapper_db, allowMissingColumns=True)
        
        sensitive_data_df_matched_with_mapper_db = accumulator_df.drop("placeholder")
        sensitive_data_df_matched_with_mapper_db = sensitive_data_df_matched_with_mapper_db.join(df_external_id_mapper_db, [sensitive_data_df_matched_with_mapper_db["matched_internal_id"] == df_external_id_mapper_db["internal_id"] ],"left")

        ### Generation of masked data for classifiedFields using UUID python function. 
        for classifiedField in range(len(sensitiveFieldList)):
            
            sensitive_data_df_selected = sensitive_data_df.select(sensitiveFieldList[classifiedField])
            
            sensitive_data_df_selected = sensitive_data_df_selected.join(sensitive_data_df_matched_with_mapper_db,[ sensitive_data_df_selected[sensitiveFieldList[classifiedField]] == sensitive_data_df_matched_with_mapper_db["matched_internal_id"] ],"left")

            sensitive_data_df_selected = sensitive_data_df_selected\
                                    .withColumnRenamed("matched_internal_id", 'matched_internal_id_'+str(sensitiveFieldList[classifiedField]))\
                                    .withColumnRenamed("internal_id", 'internal_id_'+str(sensitiveFieldList[classifiedField]))\
                                    .withColumnRenamed("external_id", 'external_id_'+str(sensitiveFieldList[classifiedField]))
            
            sensitive_data_df_db_extract_records = sensitive_data_df_selected.filter( ( sensitive_data_df_selected["external_id_"+str(sensitiveFieldList[classifiedField])].isNotNull() ) & ( trim(sensitive_data_df_selected["external_id_"+str(sensitiveFieldList[classifiedField])]) !=""  ) )

            sensitive_data_df_selected = sensitive_data_df_selected.filter( sensitive_data_df_selected["external_id_"+str(sensitiveFieldList[classifiedField])].isNull() )

            sensitive_data_df_selected = sensitive_data_df_selected.filter( ( sensitive_data_df_selected[sensitiveFieldList[classifiedField]].isNotNull() ) & ( trim(sensitive_data_df_selected[sensitiveFieldList[classifiedField]]) !="" ) )
            

            sensitive_data_df_selected = sensitive_data_df_selected.withColumn("external_id_"+str(sensitiveFieldList[classifiedField]),F.expr("uuid()"))
            sensitive_data_df_selected = sensitive_data_df_selected.withColumn("internal_id_"+str(sensitiveFieldList[classifiedField]),sensitive_data_df_selected[sensitiveFieldList[classifiedField]])


            sensitive_data_df_selected = sensitive_data_df_selected.union(sensitive_data_df_db_extract_records)
            accumulator_df_external_data = accumulator_df_external_data.unionByName(sensitive_data_df_selected, allowMissingColumns=True)
            
            self.root.info("===== classifiedField: [{}] <-> Records_to_be_masked_from_input _data: {} ========".format(sensitiveFieldList[classifiedField], accumulator_df_external_data.select(sensitiveFieldList[classifiedField]).filter( (accumulator_df_external_data[sensitiveFieldList[classifiedField]].isNotNull()) & (accumulator_df_external_data[sensitiveFieldList[classifiedField]] != "")).distinct().count()))
        
        
        sensitive_data_df = accumulator_df_external_data.drop("placeholder")
        self.storeMaskedIdDataMappings(sensitiveFieldList,sensitive_data_df,mapper_db_internal_id_list,results_bucket,date_str,journey)
        
        
        ### Reconstruction of input sensitive_data_df with masked_data in classifiedFields. 
        for classifiedField in range(len(sensitiveFieldList)):
            df_extrnl_intrnl_data_selected = sensitive_data_df.select(str(sensitiveFieldList[classifiedField]), 'external_id_'+str(sensitiveFieldList[classifiedField]))
            sensitive_data_df_input = sensitive_data_df_input.join(df_extrnl_intrnl_data_selected,[sensitiveFieldList[classifiedField]],"left")
            sensitive_data_df_input = sensitive_data_df_input.withColumn(sensitiveFieldList[classifiedField],col('external_id_'+str(sensitiveFieldList[classifiedField])))
            sensitive_data_df_input = sensitive_data_df_input.drop('external_id_'+str(sensitiveFieldList[classifiedField]))
        
        sensitive_data_df_input = sensitive_data_df_input.select(*columns)
        self.root.info("======== Records_count_after_translateToExternalId_function_execution: {} ========".format(sensitive_data_df_input.distinct().count()))
        self.root.info("======== translateToExternalId Function Completed Successfully ========")
        return sensitive_data_df_input.distinct()
        
    ### Retreival of Sensitive data from UUIDs of Mapper_DB. for classifiedField in range(len(sensitiveFieldList)):
    def translateToInternalId(self, mapper_input_df,results_bucket,sensitiveFieldList):
        
        ### Restricting conversion for mentioned fields.
        allowed_field_list = ["claim_id", "bob_id", "assoc_id"] 
        if all(item in allowed_field_list for item in sensitiveFieldList):
            self.root.info("======== fields provided in sensitiveFieldList are in allowed range for conversion =======-")
        else:
            sys.exit("-====== Error: One or more fields provided in sensitiveFieldList is out of allowed fileds for conversion, accepted fields are [ 'claim_id', 'bob_id','assoc_id' ] ========")
        
        df_external_id_mapper_db = self.spark.read.format("csv").option("header",True).option("sep","|").load("s3://"+results_bucket+"/external_id_mapper/*")
        df_external_id_mapper_db = df_external_id_mapper_db.select("internal_id", "external_id", "type").distinct()
        
        
        ### Retreival of classifiedField for maskedField from Mapper_DB.
        columns = mapper_input_df.columns
        for classifiedField in range(len(sensitiveFieldList)):
            
            df_external_id_mapper_db_filtered = df_external_id_mapper_db.filter(df_external_id_mapper_db["type"] == sensitiveFieldList[classifiedField] ).drop(df_external_id_mapper_db["type"])

            df_external_id_mapper_db_renamed = df_external_id_mapper_db_filtered.withColumnRenamed("internal_id", "internal_id_"+str(sensitiveFieldList[classifiedField])).withColumnRenamed("external_id", "external_id_"+str(sensitiveFieldList[classifiedField]))
            
            mapper_input_df = mapper_input_df.join(df_external_id_mapper_db_renamed,[ mapper_input_df[sensitiveFieldList[classifiedField]] == df_external_id_mapper_db_renamed["external_id_"+str(sensitiveFieldList[classifiedField])] ], "left")

            mapper_input_df = mapper_input_df.withColumn(sensitiveFieldList[classifiedField], when(mapper_input_df[sensitiveFieldList[classifiedField]] == mapper_input_df["external_id_"+str(sensitiveFieldList[classifiedField])], mapper_input_df["internal_id_"+str(sensitiveFieldList[classifiedField])]).otherwise(lit('')))

            mapper_input_df = mapper_input_df.drop("external_id_"+str(sensitiveFieldList[classifiedField]), "internal_id_"+str(sensitiveFieldList[classifiedField]))
        
        
        mapper_input_df = mapper_input_df.select(*columns)
        self.root.info("======== Records_count_after_translateToInternalId_function _execution: {} =======".format(mapper_input_df.count()))
        self.root.info("======== translateToInternalId Function Completed Successfully =======")
        return mapper_input_df.distinct()