[![Tests](https://github.com/Keitaro/ckanext-cleanup/workflows/Tests/badge.svg?branch=main)](https://github.com/Keitaro/ckanext-cleanup/actions)

# ckanext-cleanup

A CKAN extension that checks and cleans the FileStore.


## Requirements

Compatibility with core CKAN versions:

| CKAN version    | Compatible?   |
| --------------- | ------------- |
| 2.6 and earlier | not tested    |
| 2.7             | not tested    |
| 2.8             | not tested    |
| 2.9             | Yes           |
| 2.10            | not tested    |



## Installation

To install ckanext-cleanup:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/Keitaro/ckanext-cleanup.git
    cd ckanext-cleanup
    pip install -e .
	pip install -r requirements.txt

3. Add `cleanup` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

None at present


## Developer installation

To install ckanext-cleanup for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/Keitaro/ckanext-cleanup.git
    cd ckanext-cleanup
    python setup.py develop
    pip install -r dev-requirements.txt


## List of cli commands

1. Check-resource - Checks if for all resources by id from database exists resource file in storage

```
    ckan -c ../ckan/production.ini check-resource
```

2. Resource-table-cleanup - Checks resources by id and state and deletes the rows where state is deleted and there is no dataset for that resource

```
    ckan -c ../ckan/production.ini resource-table-cleanup
```

3. Resource-filestore-cleanup - Checks for resource in filestore exists row in resource table and deletes the resource if no row is found. When used without arguments it just lists the files and creates log file containing the list. Use --delete to actually delete the resources

```
    ckan -c ../ckan/production.ini resource-filestore-cleanup
```


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## Releasing a new version of ckanext-cleanup

If ckanext-cleanup should be available on PyPI you can follow these steps to publish a new version:

1. Update the version number in the `setup.py` file. See [PEP 440](http://legacy.python.org/dev/peps/pep-0440/#public-version-identifiers) for how to choose version numbers.

2. Make sure you have the latest version of necessary packages:

    pip install --upgrade setuptools wheel twine

3. Create a source and binary distributions of the new version:

       python setup.py sdist bdist_wheel && twine check dist/*

   Fix any errors you get.

4. Upload the source distribution to PyPI:

       twine upload dist/*

5. Commit any outstanding changes:

       git commit -a
       git push

6. Tag the new release of the project on GitHub with the version number from
   the `setup.py` file. For example if the version number in `setup.py` is
   0.0.1 then do:

       git tag 0.0.1
       git push --tags

## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
