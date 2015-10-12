from __future__ import unicode_literals, division, absolute_import
from datetime import datetime
import logging
import re
import sys
import os

from path import path

from flexget import plugin
from flexget.config_schema import one_or_more
from flexget.event import event
from flexget.entry import Entry

log = logging.getLogger('filesystem')


class Filesystem(object):
    """
    Uses local path content as an input, recurses through directories and creates entries for files that match mask.

    You can specify either the mask key, in shell file matching format, (see python fnmatch module,) or regexp key.

    Example::

      find:
        path: /storage/movies/
        mask: *.avi

    Example::

      find:
        path:
          - /storage/movies/
          - /storage/tv/
        regexp: .*\.(avi|mkv)$

    """
    retrieval_options = ['files', 'dirs', 'symlinks']
    paths = one_or_more({'type': 'string', 'format': 'path'}, unique_items=True)

    schema = {
        'oneOf': [
            paths,
            {'type': 'object',
             'properties': {
                 'path': paths,
                 'mask': {'type': 'string'},
                 'regexp': {'type': 'string', 'format': 'regex'},
                 'recursion': {'oneOf': [{'type': 'integer'}, {'type': 'boolean'}]},
                 'retrieve': one_or_more({'type': 'string', 'enum': retrieval_options}, unique_items=True)
             },
             'required': ['path'],
             'additionalProperties': False}]
    }

    def prepare_config(self, config):
        from fnmatch import translate
        config = config

        # Converts config to a dict with a list of paths
        if not isinstance(config, dict):
            config = {'path': config}
        if not isinstance(config['path'], list):
            config['path'] = [config['path']]

        config.setdefault('recursion', False)
        # If mask was specified, turn it in to a regexp
        if config.get('mask'):
            config['regexp'] = translate(config['mask'])
        # If no mask or regexp specified, accept all files
        config.setdefault('regexp', '.')
        # Sets the default retrieval option to files
        config.setdefault('retrieve', self.retrieval_options)

        return config

    def create_entry(self, filepath, test_mode, type=None):
        """
        Creates a single entry using a filepath and a type (file/dir)
        """
        entry = Entry()
        filepath = path(filepath)

        entry['location'] = filepath
        entry['url'] = 'file://{}'.format(filepath)
        entry['filename'] = filepath.name
        if not type:
            entry['title'] = filepath.namebase
        else:
            entry['title'] = filepath.name
        try:
            entry['timestamp'] = os.path.getmtime(filepath)
        except Exception as e:
            log.warning('Error setting timestamp for %s: %s' % (filepath, e))
            entry['timestamp'] = None
        if entry.isvalid():
            if test_mode:
                log.info("Test mode. Entry includes:")
                log.info("    Title: %s" % entry["title"])
                log.info("    URL: %s" % entry["url"])
                log.info("    Filename: %s" % entry["filename"])
                log.info("    Location: %s" % entry["location"])
                log.info("    Timestamp: %s" % entry["timestamp"])
            return entry
        else:
            log.error('Non valid entry created: {}'.format(entry))
            return

    def get_max_depth(self, recursion, base_depth):
        if recursion is False:
            return base_depth + 1
        elif recursion is True:
            return float('inf')
        else:
            return base_depth + recursion

    def get_folder_objects(self, folder, recursion):
        if recursion is False:
            return folder.listdir()
        else:
            return folder.walk(errors='ignore')

    def get_entries_from_path(self, path_list, match, recursion, test_mode, get_files, get_dirs, get_symlinks):
        entries = []

        for folder in path_list:
            folder = path(folder).expanduser()
            log.debug('Scanning %s' % folder)
            base_depth = len(folder.splitall())
            max_depth = self.get_max_depth(recursion, base_depth)
            folder_objects = self.get_folder_objects(folder, recursion)
            for path_object in folder_objects:
                log.verbose('Checking if {} qualifies to be added as an entry.'.format(path_object))
                try:
                    path_object.exists()
                except UnicodeError:
                    log.error('File %s not decodable with filesystem encoding: {}'.format(path_object))
                    continue
                entry = None
                object_depth = len(path_object.splitall())
                if object_depth <= max_depth:
                    if match(path_object):
                        if (path_object.isdir() and get_dirs) or (path_object.islink() and get_symlinks):
                            entry = self.create_entry(path_object, test_mode, type='dir')
                        elif path_object.isfile() and get_files:
                            entry = self.create_entry(path_object, test_mode)
                        else:
                            log.debug("Path object's {} type doesn't match requested object types.".format(path_object))
                        if entry:
                            entries.append(entry)

        return entries

    def on_task_input(self, task, config):
        config = self.prepare_config(config)

        path_list = config['path']
        test_mode = task.options.test
        match = re.compile(config['regexp'], re.IGNORECASE).match
        recursion = config['recursion']
        get_files = 'files' in config['retrieve']
        get_dirs = 'dirs' in config['retrieve']
        get_symlinks = 'symlinks' in config['retrieve']

        log.info('Starting to scan folders.')
        return self.get_entries_from_path(path_list, match, recursion, test_mode, get_files, get_dirs, get_symlinks)


@event('plugin.register')
def register_plugin():
    plugin.register(Filesystem, 'filesystem', api_ver=2)
