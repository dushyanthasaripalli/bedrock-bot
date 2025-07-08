#########################################################
#####------ Main Terraform Configuration File ------#####
#########################################################



##### Module VPC
# module cappy-ai-vpc{
#     source                    = "./modules/vpc"
# }

# ##### Module IAM
# module cappy-ai-iam{
#     source                    = "./modules/iam"
#     ou                        = var.ou
#     tags                      = var.tags
#     region                    = var.region
#     account_id                = var.account_id
#     fb_results_bucket         = var.fb_results_bucket
#     fb_scripts_bucket         = var.fb_scripts_bucket   
# }

# An example resource that does nothing.
resource "null_resource" "example" {
    triggers = {
    value = "A example resource that does nothing!"
    }
}

# #### Module S3
# module cappy-ai-s3{
#     source                    = "./modules/s3"
#     ou                        = var.ou
#     acl                       = var.acl
#     tags                      = var.tags
#     region                    = var.region
#     account_id                = var.account_id
#     fearless_birds_buckets    = var.fearless_birds_buckets
#     fb_scripts_bucket         = var.fb_scripts_bucket
#     fb_scripts_bucket_files   = var.fb_scripts_bucket_files
# }

# ##### Module Glue
# module cappy-ai-glue{
#     source                    = "./modules/glue"
#     glue_etl_role_arn         = module.cappy-ai-iam.glue_role_arn
#     tags                      = var.tags
#     s3_script_bucket          = var.fb_scripts_bucket
#     ou                        = var.ou
#     s3_results_bucket         = var.fb_results_bucket
#     region                    = var.region
#     rs_account_id_clm         = var.rs_account_id_clm
#     rs_cluster_id_clm         = var.rs_cluster_id_clm
#     rs_db_clm                 = var.rs_db_clm
#     rs_db_user_clm            = var.rs_db_user_clm
#     rs_edla_role_clm          = var.rs_edla_role_clm
# }