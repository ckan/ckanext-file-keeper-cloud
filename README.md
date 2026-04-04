[![Tests](https://github.com/ckan/ckanext-file-keeper-cloud/workflows/Tests/badge.svg?branch=main)](https://github.com/ckan/ckanext-file-keeper-cloud/actions)

# ckanext-file-keeper-cloud

This CKAN extension provides a way to store uploaded files on external cloud
storage services. It extends management functionality introduced in CKAN v2.12
and provides a set of adapters for different cloud storage providers.


## Requirements

Compatibility with core CKAN versions:

| CKAN version | Compatible? |
|--------------|-------------|
| 2.11         | no          |
| 2.12         | yes         |


## Installation

**TODO:** Add any additional install steps to the list below.
   For example installing any non-Python dependencies or adding any required
   config settings.

To install ckanext-file-keeper-cloud:

1. Activate your CKAN virtual environment, for example:
   ```sh
   . /usr/lib/ckan/default/bin/activate
   ```
1. Install the package
   ```sh
   # to install all adapters
   pip install 'ckanext-file-keeper-cloud[all]'

   # or, to install only specific adapter
   pip install 'ckanext-file-keeper-cloud[s3]'
   pip install 'ckanext-file-keeper-cloud[gcs]'
   pip install 'ckanext-file-keeper-cloud[azure]'
   pip install 'ckanext-file-keeper-cloud[libcloud]'
   ```

3. Add `file_keeper_cloud` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN.

## Available adapters

Note, cloud providers can be [emulated using docker
images](https://datashades.github.io/file-keeper/adapters/emulate/). Even
though it these images do not replicate ideally corresponding cloud provider,
generally they are close enough to be used for local development and testing.

### ckan:s3

AWS S3 adapter. Wraps [file-keeper's implementation](https://datashades.github.io/file-keeper/adapters/s3/)

#### Installation:

```sh
pip install 'ckanext-file-keeper-cloud[s3]'
```

#### Configuration example:

```ini
ckan.files.storage.my_cloud.type = ckan:s3
ckan.files.storage.my_cloud.bucket = my_bucket
ckan.files.storage.my_cloud.key = ABC123
ckan.files.storage.my_cloud.secret = 321CBA
```

Only `bucket` option is required as all other parameters can be read from
environment variables:

* `bucket`: name of the storage bucket
* `key`: the AWS Access Key
* `secret`: the AWS Secret Key
* `region`:  the AWS Region of the bucket


### ckan:azure_blob

Microsoft Azure Blob Storage adapter. Wraps [file-keeper's implementation](https://datashades.github.io/file-keeper/adapters/azure_blob/)

#### Installation:

```sh
pip install 'ckanext-file-keeper-cloud[azure]'
```

#### Configuration example:

```ini
ckan.files.storage.my_cloud.type = ckan:azure_blob
ckan.files.storage.my_cloud.container_name = my_container
ckan.files.storage.my_cloud.account_name = ABC123
ckan.files.storage.my_cloud.account_key = 321CBA
```

Recommended options:

* `container_name`: name of the storage container
* `account_name`: name of the Azure account
* `account_key`: key for the Azure account


### ckan:gcs

Google Cloud Storage adapter. Wraps [file-keeper's implementation](https://datashades.github.io/file-keeper/adapters/gcs/)

#### Installation:

```sh
pip install 'ckanext-file-keeper-cloud[gcs]'
```

#### Configuration example:

```ini
ckan.files.storage.my_cloud.type = ckan:gcs
ckan.files.storage.my_cloud.bucket_name = my_bucket
ckan.files.storage.my_cloud.project_id = my-project
ckan.files.storage.my_cloud.credentials_file = /etc/ckan/default/google-cloud-credentials.json
```

Recommended options:

* `bucket_name`: name of the storage bucket
* `credentials_files`: path to the JSON with cloud credentials
* `project_id`: the project which the client acts on behalf of


### ckan:libcloud

[Apache Libcloud](https://libcloud.apache.org/) adapter. Wraps [file-keeper's implementation](https://datashades.github.io/file-keeper/adapters/libcloud/)

#### Installation:

```sh
pip install 'ckanext-file-keeper-cloud[libcloud]'
```

#### Configuration example:

```ini
ckan.files.storage.my_cloud.type = ckan:libcloud
ckan.files.storage.my_cloud.provider = S3
ckan.files.storage.my_cloud.container_name = my_bucket
ckan.files.storage.my_cloud.key = ABC123
ckan.files.storage.my_cloud.secret = 321CBA
```

Requires following options:

* `provider`: one of [Apache Libcloud providers](https://libcloud.readthedocs.io/en/stable/storage/supported_providers.html#provider-matrix)
* `key`: API key or username
* `secret`: Secret password
* `container_name`: Name of the container/bucket

Majority of providers do not support permanent links out of the box. But if the
container supports public anonymous access and all files are available at URL
`https://<PROVIDER>/<CONTAINER>/<FILENAME>`, this shared
`https://<PROVIDER>/<CONTAINER>` part can be specified as `public_prefix`
of the storage. In this case, CKAN will append file's location to the
configured `public_prefix` whenever it needs a permanent public link for the
file.

Files are uploaded to the root of container. To specify nested location for all
uploads, use `path` option.

Any other provider specific option can be added inside `params` option which
expects a valid JSON object


## Use cloud storage for resource uploads

When configuring storage for resource, group, user or admin uploads in CKAN,
keep in mind that CKAN expects correct permissions set on the container. For
example, this is the generic configuration of the AWS S3 bucket for resource
uploads:

```ini
ckan.files.storage.resources.type = ckan:s3
ckan.files.storage.resources.bucket = ckan-resources
ckan.files.storage.resources.key = AWS_S3_KEY
ckan.files.storage.resources.secret = AWS_S3_SECRET
```

CKAN uploads files to bucket and resource's URL points to standard endpoint for
resource downloads:
`<site_url>/dataset/<id>/resource/<resource_id>/download/<filename>`. When user
follows the URL, CKAN emits a redirect to a signed S3 URL:
`http://ckan-resources.s3.us-east.amazonaws.com/131/d3c/42-a2b3-4f03-b85d-73024402d219?AWSAccessKeyId=AWS_S3KEY&Signature=ABC123&Expires=123123123`. This
URL remains valid for the limited amount of time and when user downloads
resource from CKAN's UI, new signed link is created. When link is expired(it
remains valid for 60 seconds), S3 bucket returns 403 response on attempt to use
the link.

But user can remove payload from the link(everything after `?`) and try using
plain URL:
`http://ckan-resources.s3.us-east.amazonaws.com/131/d3c/42-a2b3-4f03-b85d-73024402d219`. Here
configuration of the bucket becomes important:
* if it's a private bucket, user sees 403 error: resource is protected
* if it's a public bucket, user successfully downloads the file: file is not protected

Always use private buckets for resource storage.

This redirect to signed URL differs from the behavior of the `ckan:fs` storage
adapter, which sends file immediately from the download URL. This happens
because resource's download view checks whether user has permission to download
the file and then calls `as_response` method of the storage adapter. This
method returns Flask response which leads to the file content. `ckan:fs`
adapter builds a response that sends static file via flask. `ckan:s3` builds a
signed redirect response to the bucket, because it's much more efficient that
proxifying S3 content through Flask. It's possible to create a new storage
adapter that extends `ckan:s3` and implements `as_response` in different way,
if redirect for some reasons is not acceptable.

## Use cloud storage for user and group uploads

User, group and admin downloads are different from resources. Let's start from the similar
configuration of the storage for the user uploads(avatars):
```ini
ckan.files.storage.users.type = ckan:s3
ckan.files.storage.users.bucket = ckan-users
ckan.files.storage.users.key = AWS_S3_KEY
ckan.files.storage.users.secret = AWS_S3_SECRET
```

Upload an image to user profile. If you check `user_show` output after this,
you'll see that `image_display_url` field points to the cloud bucket, but it's
a plain, not signed URL, with no query parameters:
`http://ckan-users.s3.us-east.amazonaws.com/image.png`. If you open this URL
the following can happen:
* if bucket is public, you'll see the image
* if bucket is private, you'll see 403 response

Ideally, bucket for _public files_, such as user or group images, or site
logos, must be public. In this way all possible problems are solved and no
further actions required. But why image URL is different from resource URL?

Resources historically have separate endpoint where permissions are
checked. It's safe to serve the content of the file by the end of this
endpoint, because user without required permissions is rejected with 403
response in the beginning of the endpoint.

Public images do not have dedicated endpoint where redirect response can be
produced. Instead, CKAN must produce links that will be shown on the page or in
API output and client can use these URLs when required. Because these links can
be stored for a long time before they are accessed, signed URLs will not work
here. The upper bound on lifetime of the signed URL is 7 days which may be not
sufficient if content havested and displayed on a different portal.

Because of this, CKAN uses `permanent_link` method of the storage to build an
image link. This method _makes an assumption_ that bucket is public and builds
URL which will work in this case. But if bucket is misconfigured and has no
public access, URL will be rejected.

If you cannot change visibility of the bucket, images still can be accessed,
but it requires additional steps.

First, you need to prevent creation of `permanent_link`. Storage relies on
"capabilities" when different actions are performed, and `permanent_link` is
bound to capability `LINK_PERMANENT`. If storage has this capability(`ckan:s3`
has it), `permanent_link` will be called and return the link. If storage does
not have this capability, link will not be used.

It's possible to disable any existing capability of the storage using
`ckan.files.storage.users.disabled_capabilities` config option. Add it to the
configuration of the storage and set `LINK_PERMANENT` as its values. Here the
updated configuration:

```ini
ckan.files.storage.users.type = ckan:s3
ckan.files.storage.users.bucket = ckan-users
ckan.files.storage.users.key = AWS_S3_KEY
ckan.files.storage.users.secret = AWS_S3_SECRET
ckan.files.storage.users.disabled_capabilities = LINK_PERMANENT
```

If you check `user_show` output after this change, you'll see that now
`image_display_url` has value `null`. Now invalid URL is not used anymore, but
image is still not accessible. To solve it, we can enable `public` flag of the
storage - for any storage that has `public` flag, CKAN has a fallback URL for
serving files. Add `ckan.files.storage.users.public = true` to the
configuration of the storage and check output of `user_show` once again.

The `image_display_url` looks like
`<site_url>/file/public-download/users/image.png`. If you visit this URL,
you'll be redirected to S3 bucket, which must be familiar after experiments
with the resource. The main difference here is that there is no permission
check here. Any user, even anonymous can access this file. Endpoint that
handles this last URL checks only two things:

* specified file exists in the specified storage
* specified storage has `public` flag enabled

If both conditions are met, anyone can access the file from the
storage. Enabling `public` on storage literally makes it public in terms of
read access, so make sure you mean it when you use it. It always better to use
the initial setup, without `disabled_capabilities` and `public`, and configure
bucket directly, instead of solving misconfiguration via storage settings on
CKAN side. But if bucket cannot be reconfigured, or you want to publicly serve
content from the single folder on otherwise private bucket, this solution can do the trick.

## Developer installation

To install ckanext-file-keeper-cloud for development, activate your CKAN virtualenv and
do:

```sh
git clone https://github.com/ckan/ckanext-file-keeper-cloud.git
cd ckanext-file-keeper-cloud
pip install -e '.[all]'
```

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
