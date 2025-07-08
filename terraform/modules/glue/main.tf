# ############################井################＃###＃＃###将#＃####我#####
######## AWS GLUE SERVICE:: JOBS, CRAWLERS, CATALOG DATABASES#将######
#########＃#井＃＃并##并护#种#护##苻井#####井###############＃########＃##接####

####### GLUE JOBS ###井井######
# GLUE JOB ADHOC

resource "aws_glue_job" "fearless-birds-quickops-job" {
    name                = "FearlessBirds_QuickOps"
    role_arn            = var.glue_etl_role_arn
    glue_version        = "4.0"
    number_of_workers   = 10
    worker_type         = "G.2X"
    #connections        = [ "$[var-glue_connection_reshift}" ]
    tags                = var.tags

    command {
        script_location = "s3://${var.s3_script_bucket}/tfe_upload/FearlessBirds_QuickOps.py"
    }

    default_arguments = {
        "--JOB_NAME"                = "FearlessBirds_QuickOps"
        "--BUCKET_NAME"             = "${var.s3_results_bucket}"
        "--REGION"                  = "${var.region}"
        "--rs_account_id"           = "${var.rs_account_id_clm}"
        "--rs_cluster_id"           = "${var.rs_cluster_id_clm}"
        "--rs_db"                   = "${var.rs_db_clm}"
        "--rs_db_user"              = "${var.rs_db_user_clm}"
        "--rs_edla_role"            = "${var.rs_edla_role_clm}"
        "--script_bucket"           = "${var.s3_script_bucket}"
        "--enable-glue-datacatalog" = "true"
        "--enable-auto-scaling"     = "true"
        "--enable-spark-ui"         = "true"
        "--spark-event-logs-path"   = "s3://${var.s3_results_bucket}/sparkout/FearlessBirds_QuickOps/"

    }
}

resource "aws_glue_job" "fearless-birds-idconversion-job" {
    name                = "FearlessBirds_SecureIdEncryption"
    role_arn            = var.glue_etl_role_arn
    glue_version        = "4.0"
    number_of_workers   = 10
    worker_type         = "G.2X"
    #connections        = [ "$[var-glue_connection_reshift}" ]
    tags                = var.tags

    command {
        script_location = "s3://${var.s3_script_bucket}/tfe_upload/FearlessBirds_external_mapper.py"
    }

    default_arguments = {
        "--JOB_NAME"                            = "FearlessBirds_SecureIdEncryption"
        "--BUCKET_NAME"                         = "${var.s3_results_bucket}"
        "--REGION"                              = "${var.region}"
        "--rs_account_id"                       = "${var.rs_account_id_clm}"
        "--rs_cluster_id"                       = "${var.rs_cluster_id_clm}"
        "--rs_db"                               = "${var.rs_db_clm}"
        "--rs_db_user"                          = "${var.rs_db_user_clm}"
        "--rs_edla_role"                        = "${var.rs_edla_role_clm}"
        "--script_bucket"                       = "${var.s3_script_bucket}"
        "--enable-glue-datacatalog"             = "true"
        "--enable-auto-scaling"                 = "true"
        "--enable-spark-ui"                     = "true"
        "--spark-event-logs-path"               = "s3://${var.s3_results_bucket}/sparkout/FearlessBirds_SecureIdEncryption/"
        "--enable-metrics"                      = "true"
        "--enable-continuous-cloudwatch-log"    = "true"
        "--enable-continuous-log-filter"        = "true"
        "--extra-py-files"                      = "s3://${var.s3_script_bucket}/tfe_upload/FearlessBirds_idConversionHandler.py"

    }
}

# resource "aws_glue_job" "claims-bp-dataprep-job" {
#     name                = "FearlessBirds_QuickOps_dummy"
#     role_arn            = var.glueetl_rds_role_arn
#     glue_version        = "4.0"
#     number_of_workers   = 20
#     worker_type         = "G.2X"
#     #connections        = [ "$[var-glue_connection_reshift}" ]
#     tags                = var.tags

#     command {
#         script_location = "s3://${var.s3_script_bucket}-${var.ou}/glue_scripts/FearlessBirds_QuickOps.py"
#     }

#     default_arguments = {
#         "--JOB_NAME"                = "FearlessBirds_QuickOps"
#         "--BUCKET_NAME"             = "${var.s3_results_bucket}-${var.ou}"
#         "--REGION"                  = "${var.region}"
#         "--rs_account_id"           = "${var.rs_account_id_clm}"
#         "--rs_cluster_id"           = "${var.rs_cluster_id_clm}"
#         "--rs_db"                   = "${var.rs_db_clm}"
#         "--rs_db_user"              = "${var.rs_db_user_clm}"
#         "--rs_edla_role"            = "${var.rs_edla_role_clm}"
#         "--script_bucket"           = "${var.s3_script_bucket}-${var.ou}"
#         "--enable-glue-datacatalog" = "true"
#         "--enable-auto-scaling"     = "true"
#         "--enable-spark-ui"         = "true"
#         "--spark-event-logs-path"   = "s3://${var.s3_results_bucket}-${var.ou}/sparkout/FearlessBirds_QuickOps/"
#     }
# }

