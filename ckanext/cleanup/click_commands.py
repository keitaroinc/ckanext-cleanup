import os
import click
import logging

from ckan.common import config
from ckan import model

from pathlib import Path

# create logger
logger = logging.getLogger("Check_and_cleanup_log")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)


@click.command(u'check-resource',
               short_help=u'Checks for all resources by id from database '
                          u'exists resource file in storage')
def check_resource():

    # Checks for all resources by id from databese
    # exists resource file in storage

    fh = logging.FileHandler(r'resource_exists.log', 'w+')
    logger.addHandler(fh)
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)

    storage_path = config.get('ckan.storage_path',
                            '/var/lib/ckan/default/resources')
    count = 0
    
    resource_id_url = model.Session.execute("""
                                                select id, url from resource
                                                where state = 'active'
                                                and url_type = 'upload'""")
    resultDictionary = dict((x, y) for x, y in resource_id_url)
    logger.info(f'Number of total active resources in database is {len(resultDictionary)}')
    for resource_id in resultDictionary:

        path_to_resource = storage_path + "/resources" + "/" + resource_id[0:3] + "/" + resource_id[3:6] + "/" + resource_id[6:]
        my_file = Path(path_to_resource)   
        if my_file.is_file():
            continue
            # logger.info("resource exists on local storage")
        else:
            count += 1
            logger.warn(f'{path_to_resource} is missing')
    if count == 0:
        logger.info("No resource is missing in filestore")


@click.command(u'resource-table-cleanup',
               short_help=u'Checks resources by id and state '
                          u'and deletes the rows where state is deleted '
                          u'and there is no dataset for that resource')
@click.option("--cleanup", 
              prompt=u'Cleanup resource rows (N will just list the notactive rows)', 
              help=u'Yes or No')
def resource_table_cleanup(cleanup):

    # Checks for all resources by id from databese
    # exists resource file in storage
    fh = logging.FileHandler(r'resource_rows_check.log', 'w+')
    logger.addHandler(fh)
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)

    resource_id_url = model.Session.execute("""
                                            select r.id, r.url from resource r 
                                            where r.state ='deleted'
                                            and not exists (
                                            select id from package p
                                            where p.id = r.package_id)""")
    resultDictionary = dict((x, y) for x, y in resource_id_url)
    logger.info(f'There are {len(resultDictionary)} not active rows in resources table')
    if cleanup == 'Y':
        delete_resource_row = model.Session.execute("""
                                                    delete from resource r
                                                    where r.state ='deleted'
                                                    and not exists (
                                                    select id from package p
                                                    where p.id = r.package_id)
                                                    """)
        logger.info('Not active rows from resource tabel were deleted')
    else:
        logger.info('Delete operation was skipped')
     
    logger.info("Resource table cleanup end")


@click.command(u'resource-filestore-cleanup',
               short_help=u'Checks for resource in filestore '
                          u'exists row in resource table '
                          u'and deletes the resource if no row is found')
@click.option('--delete', is_flag=True, default=False,
              help='Use --delete to delete the resources, otherwise it just lists them')
@click.option('--list-deleted', 'list_deleted', is_flag=True, default=False,
              help='Use --list-deleted to list only resources to be the deleted/deleted)')
def resource_filestore_cleanup(delete, list_deleted):
    fh = logging.FileHandler(r'filestore_cleanup.log', 'w+')
    logger.addHandler(fh)
    fh.setFormatter(formatter)
    fh.setLevel(logging.DEBUG)
    
    storage_path = config.get('ckan.storage_path',
                            '/var/lib/ckan/default/resources')
    resource_ids_and_paths = {}
    resource_ids =  model.Session.execute("select id, url from resource r")
    resource_ids_dict = dict((x, y) for x, y in resource_ids)
    for root, dirs, files in os.walk(storage_path):
        if root[-17:-8] == 'resources':
            for idx, resource_file in enumerate(files):
                resource_ids_and_paths[resource_file] = os.path.join(
                    root, files[idx])
              
                full_id = resource_ids_and_paths[resource_file][-38:-35] + resource_ids_and_paths[resource_file][-34:-31] + resource_file
               
                if resource_ids_dict.get(full_id):
                    if list_deleted:
                        pass
                    else:
                        logger.info(f'{resource_file} exists in resources table')
                else:
                    if delete:
                        logger.warn(f'{resource_file} does not exists in resources table')
                        os.remove(resource_ids_and_paths[resource_file])
                        logger.warn(f'{resource_ids_and_paths[resource_file]} is deleted')
                    else:
                        logger.warn(f'{resource_ids_and_paths[resource_file]} does not exists in resources table')

    click.secho('Found {0} resource files in the file system'.format(
        len(resource_ids_and_paths)),
        fg=u'green',
        bold=True)

    logger.info('resource cleanup end')
