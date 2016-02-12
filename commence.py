import argparse, boto3, sys, time, uuid, webbrowser

INDEX_DOCUMENT = 'index.html'
ERROR_DOCUMENT = 'error.html'

# Parse command line arguments
parser = argparse.ArgumentParser(description='Create an S3 static site.')
parser.add_argument('sitename', metavar='name', nargs=1, help='the domain name for your new static site')
sitename = parser.parse_args().sitename[0]
site_url = 'http://' + sitename

# Sanity checks
if '.' not in sitename:
    sys.exit('Error: No dot in the provided name. The name of the bucket must be the domain name of the site.')

print 'Creating site', sitename + '...'

client = boto3.client('s3')

bucket_policy = '''{
	"Id": "''' + str(uuid.uuid4()) + '''",
	"Statement": [
		{
			"Sid": "CommenceStaticSiteStatement1",
			"Effect": "Allow",
			"Principal": "*",
			"Action": "s3:GetObject",
			"Resource": "arn:aws:s3:::''' + sitename + '''/*"
		}
	]
}'''

client.create_bucket(
    ACL='public-read',
    Bucket=sitename
)

client.put_bucket_policy(
	Bucket=sitename,
	Policy=bucket_policy
)

client.put_bucket_website(
	Bucket=sitename,
	WebsiteConfiguration={
        'ErrorDocument': {
            'Key': ERROR_DOCUMENT
        },
        'IndexDocument': {
            'Suffix': INDEX_DOCUMENT
        }
    }
)

endpoint = sitename + '.s3-website-us-east-1.amazonaws.com'
endpoint_url = 'http://' + endpoint

client.put_object(
	Bucket=sitename,
	Key=INDEX_DOCUMENT,
	ContentType='text/html',
	Body='''
		<h2>Hello world! Here\'s your CNAME:</h2>
		<h2><code>''' + endpoint + '''</code></h2>
		<h2><a href="''' + site_url + '''">Go to actual site URL ></a></h2>
	'''
)

client.put_object(
	Bucket=sitename,
	Key=ERROR_DOCUMENT,
	ContentType='text/html',
	Body='Error'
)

print 'Done! Your endpoint is:', endpoint

webbrowser.open_new_tab(endpoint_url)
