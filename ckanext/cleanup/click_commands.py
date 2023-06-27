import os
import click
import logging

from ckan.common import config
from ckan import model

from pathlib import Path

# create logger
logger = logging.getLogger("Migration_log")
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)

@click.command(u'check-resource',
               short_help=u'Checks for all resources by id from databese '
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
    
    resource_id_url = model.Session.execute("select id, url from resource where state = 'active' and url_type = 'upload'")
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