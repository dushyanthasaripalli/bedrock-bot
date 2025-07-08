################################################################
### Terraform Variables for Production Environment ###
################################################################

acl                     = "private"
ou                      = "Prod"
region                  = "us-east-1"
account_id              = "589008605989"

tags = {
    Name                = "cappy-ai"
    Environment         = "production"
    Creation            = "Terraform Resource"
}

fb_scripts_bucket       = "cappy-ai-scripts"
fb_results_bucket       = "cappy-ai-results"
fb_adhoc_bucket         = "cappy-ai-adhoc"

cappy_ai_buckets  = ["cappy-ai-results","cappy-ai-scripts","cappy-ai-adhoc"]

fb_scripts_bucket_files = ["FearlessBirds_external_mapper.py","FearlessBirds_QuickOps.py","FearlessBirds_idConversionHandler.py"]

glueetl_rds_role_arn    = "arn:aws:iam::123456789012:role/fb-glue-role"

rs_account_id_clm       = "123456789012"
rs_cluster_id_clm       = "cluster"
rs_db_clm               = "db"
rs_db_user_clm          = "user"
rs_edla_role_clm        = "role"


