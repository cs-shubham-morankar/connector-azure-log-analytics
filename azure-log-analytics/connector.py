"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

from connectors.core.connector import Connector, get_logger, ConnectorError
from .operations import operations, check, list_saved_searches

logger = get_logger('azure-log-analytics')


class AzureLogAnalytics(Connector):
    def execute(self, config, operation, params, **kwargs):
        try:
            config['connector_info'] = {"connector_name": self._info_json.get('name'),
                                        "connector_version": self._info_json.get('version')}
            operation = operations.get(operation)
            if not operation:
                raise ConnectorError("Unsupported Operation")
            return operation(config, params)
        except Exception as err:
            logger.error(str(err))
            raise ConnectorError(str(err))

    def check_health(self, config):
        try:
            connector_info = {"connector_name": self._info_json.get('name'),
                              "connector_version": self._info_json.get('version')}
            config['connector_info'] = connector_info
            check(config, connector_info)
            return True
        except Exception as err:
            logger.error(str(err))
            raise ConnectorError(str(err))
