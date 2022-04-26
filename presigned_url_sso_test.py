#! /usr/bin/env python3
import sys
import logging
import boto3
from botocore.exceptions import ClientError, ProfileNotFound, SSOTokenLoadError

def create_presigned_url(bucket_name, object_name, profile_name='default', expiration=3600 ):
    """Generate a presigned URL to share an S3 object
    :param bucket_name: string
    :param object_name: string
    :param expiration: Time in seconds for the presigned URL to remain valid
    :return: Presigned URL as string. If error, returns None.
    """
    # Set the session credentials for boto3 to use a specific profile.
    # If the session has already been signed in to via the command line it will use the signed in session
    boto3.setup_default_session(profile_name=profile_name)
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        print('abc')
        logging.error(e)
        return None
    # The response contains the presigned URL
    return response


class safelist(list):
    def get(self, index, default=None):
        try:
            return self.__getitem__(index)
        except IndexError:
            return default


def main():
    print("*** START ***")
    if (len(sys.argv) <3):
        print("Usage: python3 presigned_url_sso_test.py <bucket_name> <prefix_name> [profile_name]")
        exit(1)
    else:
        args=safelist(sys.argv)

    bucket_name=args.get(1)
    prefix_name=args.get(2)
    profile_name=args.get(3, 'default')

    print("Attempting to get a presigned URL for s3://{0}/{1} using the {2} profile".format(bucket_name, prefix_name, profile_name))

    try:
        response=create_presigned_url(bucket_name,prefix_name,profile_name=profile_name)
    except ProfileNotFound as e:
        print("*** ERROR ***")
        print(e)
        exit(2)
    except SSOTokenLoadError as e:
        print("*** ERROR ***")
        print(e)
        print("Please execute 'aws sso login --profile={0}' and try again".format(profile_name))
        exit(3)

    print(response)

if __name__ == "__main__":
    main()