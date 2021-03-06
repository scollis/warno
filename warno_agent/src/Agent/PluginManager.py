import logging
import multiprocessing
from multiprocessing import Queue


class PluginManager(object):
    ''' Plugin manager for the various WARNO plugins

    '''

    white_list = '*'

    def __init__(self, info, instrument=None ):
        """ Initializer for Plugin Manager

        Parameters
        ----------
        config: Plugin Manager configuration.

        Returns
        -------
        PluginManager: class
            Plugin Manager object.

        """
        self.plugin_list = []
        self.msg_queue = Queue()
        self.info = info
        self.site = info['site']
        self.instrument = instrument
        self.instrument_name = instrument['name']
        self.config_id = info['config_id']

        self.event_code_dict = {}

    def add_plugin(self, plugin):
        plugin.config_id= self.config_id
        plugin.instrument = self.instrument
        if plugin.white_list[0] == '*' or self.instrument_name in plugin.white_list:
            self.plugin_list.append({'plugin_handle': plugin,
                                 'status': 'notstarted',
                                 'thread': None,
                                 'ctrl_queue': Queue(),
                                 'plugin_metadata': None,
                                 'event_codes': []},
                                )

    def get_plugin_handle_list(self):
        return [plugin['plugin_handle'] for plugin in self.plugin_list]

    def get_plugin_list(self):
        return self.plugin_list

    def start_plugin(self, plugin):
        """ Starts a plugin.

        Parameters
        ----------
        plugin: plugin dict object
            Plugin to be started.

        Returns
        -------
        plugin: thread_handle
            Running thread for the plugin.

        """
        p = multiprocessing.Process(target=plugin['plugin_handle'].run, args=(
            self.msg_queue, self.info, plugin['ctrl_queue']))
        p.daemon = True
        p.start()
        plugin['thread'] = p
        plugin['status'] = 'started'

        return p

    def start_plugin_by_name(self, name):
        """ Start a plugin with name given by `name`. It must already exist in plugin list.

        Parameters
        ----------
        name: str
            Name of plugin to be started

        Returns
        -------
        None
        """

        for plugin in self.get_plugin_list():
            if plugin['plugin_name'] == name:
                self.start_plugin(plugin)

    def stop_plugin_by_name(self, name):
        """ Stop plugin with name given by `name`

        Parameters
        ----------
        name: str
            Plugin Name to stop.

        Returns
        -------
        None
        """
        for plugin in self.get_plugin_list():
            if plugin['plugin_name'] == name:
                self.stop_plugin(plugin)

    def start_all_plugins(self):
        """ Start all plugins

        Returns
        -------

        """
        for plugin in self.plugin_list:
            self.start_plugin(plugin)

    def stop_plugin(self, plugin):
        """ Stop plugin.

        Parameters
        ----------
        plugin: dict
            Plugin dict object.

        Returns
        -------

        """
        plugin['ctrl_queue'].put({"command":"shutdown"})
        plugin['status'] = 'stopped'

    def register_plugin_events(self, plugin):
        """
        Register a plugin.

        Parameters
        ----------
        plugin: module
            Plugin to be registered.

        Returns
        -------
        """

        logging.info("Registering Plugin %s", plugin)
        registration_info = plugin['plugin_handle'].get_registration_info()

        for event in registration_info['event_code_names']:
            plugin['event_codes'].append(event)

        plugin['plugin_name'] = registration_info['plugin_name']

        logging.debug("Event Codes List: %s", plugin['event_codes'])