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
1. Clone the source and install it on the virtualenv
   ```sh
   git clone https://github.com/ckan/ckanext-file-keeper-cloud.git
   cd ckanext-file-keeper-cloud

   # to install all adapters
   pip install -e '.[all]'

   # or, to install only specific adapter
   pip install -e '.[s3]'
   pip install -e '.[gcs]'
   pip install -e '.[azure]'
   pip install -e '.[libcloud]'
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
## or, if using development installation, switch to repository folder and
pip install -e '.[s3]'
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
## or, if using development installation, switch to repository folder and
pip install -e '.[azure]'
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
## or, if using development installation, switch to repository folder and
pip install -e '.[gcs]'
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
## or, if using development installation, switch to repository folder and
pip install -e '.[libcloud]'
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
