#importing libraries
import awswrangler as wr
import pandas as pd
import urllib.parse
import os

#defining environment variables
os_input_s3_cleaned_layer = os.environ['s3_cleaned_layer']
os_input_glue_catalog_db_name = os.environ['glue_catalog_db_name']
os_input_glue_catalog_table_name = os.environ['glue_catalog_table_name']
os_input_write_data_operation = os.environ['write_data_operation']


#Function that cleans and write the data into parquet format
def lambda_handler(event, context):

    #bucket and key
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'], encoding='utf-8')

    try:
        #creating dataframe from the s3
        df_raw = wr.s3.read_json(f's3://{bucket}/{key}')

        #flattening the json
        df_new = pd.json_normalize(df_raw['items'])
        df_new['id'] = df_new['id'].astype('int64')  # This converts the column to proper bigint

        wr_response = wr.s3.to_parquet(
            df=df_new,
            path=os_input_s3_cleaned_layer,
            dataset=True,
            database=os_input_glue_catalog_db_name,
            table=os_input_glue_catalog_table_name,
            mode=os_input_write_data_operation
        )

        return wr_response

    except Exception as e:
        print(e)
        print(f"Error getting object {object} from key {key}")
        raise e
