
# YouTube End to End Data Engineering Project

This is an End to End Data Engineering Project that helps imaginary client who is going to put Ad-Campaign online for thier product/services. My job is help them where to place their ads in the social media platforms to get better reach for thier products/services.
I used YouTube dataset from Kaggle for my analysis and to build End to End ETL Pipeline.

#### [Pipeline Image]
## Project Implementation

### Dataset Download
The link of the Youtube Dataset from Kaggle is attached below. Before that, why I chose Youtube for the analysis ? Because, it is the 2nd most viewed website and a video-sharing platform where our client's product/service gets more attention.

Check out the Youtube Kaggle Dataset [here](https://www.kaggle.com/datasets/datasnaek/youtube-new).

I downloaded the data as zip file and extracted into a folder.


### Creating AWS account
For storage, processing, and analysing, AWS Cloud will be used. I created a account with AWS free trial and also an IAM account for this project as a better AWS practice.

### Uploading the Dataset to S3
Before uploading the dataset to the AWS s3, We have to do two things

    1. AWS S3 bucket creation
    2. Installing AWS CLI in Ubuntu and upload (My personal Desktop)

#### AWS S3 Bucket creation
In AWS Console page, navigated to S3, and created a new bucket. Next step is uploading the files to the S3 bucket.

#### AWS CLI
Use the following command to install the AWS CLI in Ubuntu
```bash
  sudo snap install aws-cli --channel=v1/stable --clasic
```

The dataset contain two types of data .

JSON -> Data about the video categories that ranks the top for countries

CSV -> Data about Youtube Videos. 

The JSON dataset are uploaded directly to S3 bucket with the following command

```bash
aws s3 cp . s3://youtube-data-project-raw-useast1-dev-952689119273/youtube/raw_statistics_reference_data/ --recursive --exclude "*" --include "*.json"
```

The CSV data files are uploaded to S3 bucket under their country named folder with the following command.

```bash 
aws s3 cp CAvideos.csv s3://youtube-data-project-raw-useast1-dev-952689119273/youtube/raw_statistics/region=ca/
aws s3 cp DEvideos.csv s3://youtube-data-project-raw-useast1-dev-952689119273/youtube/raw_statistics/region=de/
aws s3 cp FRvideos.csv s3://youtube-data-project-raw-useast1-dev-952689119273/youtube/raw_statistics/region=fr/
aws s3 cp GBvideos.csv s3://youtube-data-project-raw-useast1-dev-952689119273/youtube/raw_statistics/region=gb/
aws s3 cp INvideos.csv s3://youtube-data-project-raw-useast1-dev-952689119273/youtube/raw_statistics/region=in/
aws s3 cp JPvideos.csv s3://youtube-data-project-raw-useast1-dev-952689119273/youtube/raw_statistics/region=jp/
aws s3 cp KRvideos.csv s3://youtube-data-project-raw-useast1-dev-952689119273/youtube/raw_statistics/region=kr/
aws s3 cp MXvideos.csv s3://youtube-data-project-raw-useast1-dev-952689119273/youtube/raw_statistics/region=mx/
aws s3 cp RUvideos.csv s3://youtube-data-project-raw-useast1-dev-952689119273/youtube/raw_statistics/region=ru/
aws s3 cp USvideos.csv s3://youtube-data-project-raw-useast1-dev-952689119273/youtube/raw_statistics/region=us/
```

Hurray!!! The file uploading part is done. Next step is using Glue Crawler in AWS Glue to go through our data and create a data catalog which act as a metadata for our data which is very helpful for us to query the data using AWS Athena.

### Glue data catalog using Glue Crawler
Before that, IAM role for Glue catalog with respective policies to read S3 buckets was created and assigned in IAM console.
Then under Glue servicein AWS, an crawler was created to go through the data (Source: S3 bucket -> This was done is the configuration of the crawler) and the metadata was fetched.

The data catalog was stored under a table in a database. That was created before the process.

What next ??? Querying the data in Athena!!!!!!


### Data Querying in Athena
Then, Attempt to query the json file data was done. But, the following error was happened :(.
This error occurs due to the improper format of the json datasets. 

#### [Error Image Placeholder]

The Athena uses the inbuilt Json SerDe to serialise and deserialise the json for processing and querying. The library expects the json dataset to be in single line format like the 

#### [Single line format image]

But the error was removed by using one of the AWS service. Let's see what was that !.

### Solving error using Lambda
AWS Lambda is a service where we can write code for processing the data in any language and make it to run when any event happens.
So, a small ETL will be done here to process th data into correct format and store the dataset into parquet format into another S3 bucket (Cleaned data).

#### [Small ETL Pipeline Image]

The code and configurations including environmental variables and creating layers were done.The code was made to run with an test event with an S3 put event. This was done to ensure and test whether the Lambda function code works correctly.The glue catalog along with the table was created itself by the code. But, the database was created to stored the table of the cleaned data.

#### What does the lambda function code do ? 
    1. Read the uploaded json file in the S3 bucket.
    2. Normalised the json file into flat dataframe (took only required json objects) using the pandas.
    3. Turned the data into parquet format and written into the another S3 bucket.
    4. Along with this, glue data catalog was created for the data for querying in Athena.

After this, the Athena query gave the results from the parquet dataset using the glue data catalog.

#### [Image of Athena test query]

Note: Glue data catalog is like a metadata to raw data stored in the S3. Athena can't directly use query to get the respective data from the S3 buckets.

### Then What next ??
The entire processs was not done. Testing was done on a single file. 



