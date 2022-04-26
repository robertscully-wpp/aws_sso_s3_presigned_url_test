# aws_sso_s3_presigned_url_test
Very simple script for generating a presigned URL, supporting SSO via boto3

Inteded to be used in concert with an SSO enabled AWS account, awscli2, boto3 1.14.0, python3 3.8

Configure the AWS SSO login using:

``` aws sso configure [--profile=<profile_name>]```

Execute the script as follows:

``` python3 presigned_url_sso_test.py <your_bucket_name> <your_file_prefix> [profile_name] ```

There is rudimentary exception trapping only, but this will validate that the profile exists, and if there is a valid SSO session

If there is no valid session, you will be prompted to sign in using the following command:

``` aws sso login [--profile=<profile_name>] ```

Once a valid SSO session has been created, execution of the script with the correct parameters will return a presigned S3 URL for those parameters.
