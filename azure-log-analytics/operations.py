""" Copyright start
  Copyright (C) 2008 - 2021 Fortinet Inc.
  All rights reserved.
  FORTINET CONFIDENTIAL & FORTINET PROPRIETARY SOURCE CODE
  Copyright end """

from requests import request, exceptions as req_exceptions
from .microsoft_api_auth import *

logger = get_logger('azure-log-analytics')

loganalysis_api_endpoint = 'https://api.loganalytics.io/v1'
analytics_api_endpoint = 'https://management.azure.com'


def api_request(method, endpoint, connector_info, config, params=None, data=None, headers={}):
    try:
        ms = MicrosoftAuth(config)
        token = ms.validate_token(config, connector_info)
        headers['Authorization'] = token
        headers['Content-Type'] = 'application/json'
        logger.debug("Endpoint: {0}".format(endpoint))
        try:
            response = request(method, endpoint, headers=headers, params=params, json=data, verify=ms.verify_ssl)
            logger.debug("Response Status Code: {0}".format(response.status_code))
            logger.debug("Response: {0}".format(response.text))
            logger.debug("API Header: {0}".format(response.headers))
            if response.status_code in [200, 201, 204]:
                if response.text != "":
                    return response.json()
                else:
                    return True
            else:
                if response.text != "":
                    err_resp = response.json()
                    failure_msg = err_resp['error']['message']
                    error_msg = 'Response [{0}:{1} Details: {2}]'.format(response.status_code, response.reason,
                                                                         failure_msg if failure_msg else '')
                else:
                    error_msg = 'Response [{0}:{1}]'.format(response.status_code, response.reason)
                logger.error(error_msg)
                raise ConnectorError(error_msg)
        except req_exceptions.SSLError:
            logger.error('An SSL error occurred')
            raise ConnectorError('An SSL error occurred')
        except req_exceptions.ConnectionError:
            logger.error('A connection error occurred')
            raise ConnectorError('A connection error occurred')
        except req_exceptions.Timeout:
            logger.error('The request timed out')
            raise ConnectorError('The request timed out')
        except req_exceptions.RequestException:
            logger.error('There was an error while handling the request')
            raise ConnectorError('There was an error while handling the request')
        except Exception as err:
            raise ConnectorError(str(err))
    except Exception as err:
        raise ConnectorError(str(err))


def check_payload(payload):
    final_payload = {}
    for key, value in payload.items():
        if isinstance(value, dict):
            nested = check_payload(value)
            if len(nested.keys()) > 0:
                final_payload[key] = nested
        elif value:
            final_payload[key] = value
    return final_payload


def build_payload(payload):
    payload = {k: v for k, v in payload.items() if v is not None and v != ''}
    return payload


def execute_query(config, params, connector_info):
    try:
        endpoint = loganalysis_api_endpoint + '/workspaces/{0}/query'.format(params.get('WorkspaceId'))
        workspaces = params.get("workspaces")
        if workspaces:
            workspaces = workspaces.split(",")
        payload = {
            'query': params.get('query'),
            'timespan': params.get('timespan'),
            'workspaces': workspaces
        }
        payload = build_payload(payload)
        logger.debug("Payload: {0}".format(payload))
        response = api_request("POST", endpoint, connector_info, config, data=payload)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def list_saved_searches(config, params, connector_info):
    try:
        endpoint = analytics_api_endpoint + '/subscriptions/{0}/resourcegroups/{1}/providers/Microsoft.OperationalInsights/workspaces/{2}/savedSearches?api-version=2020-08-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('workspaceName'))
        response = api_request("GET", endpoint, connector_info, config)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def get_saved_searches(config, params, connector_info):
    try:
        endpoint = analytics_api_endpoint + '/subscriptions/{0}/resourcegroups/{1}/providers/Microsoft.OperationalInsights/workspaces/{2}/savedSearches/{3}?api-version=2020-08-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('workspaceName'),
            params.get('savedSearchId'))
        response = api_request("GET", endpoint, connector_info, config)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def create_saved_searches(config, params, connector_info):
    try:
        endpoint = analytics_api_endpoint + '/subscriptions/{0}/resourcegroups/{1}/providers/Microsoft.OperationalInsights/workspaces/{2}/savedSearches/{3}?api-version=2020-08-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('workspaceName'),
            params.get('savedSearchId'))
        additional_fields = params.get('additional_fields')
        payload = {
            "etag": params.get('etag'),
            "properties": {
                "category": params.get('category'),
                "displayName": params.get('displayName'),
                "query": params.get('query')
            }
        }
        if additional_fields:
            payload['properties'].update(additional_fields)
        payload = check_payload(payload)
        logger.debug("Payload: {0}".format(payload))
        response = api_request("PUT", endpoint, connector_info, config, data=payload)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def update_saved_searches(config, params, connector_info):
    try:
        endpoint = analytics_api_endpoint + '/subscriptions/{0}/resourcegroups/{1}/providers/Microsoft.OperationalInsights/workspaces/{2}/savedSearches/{3}?api-version=2020-08-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('workspaceName'),
            params.get('savedSearchId'))
        additional_fields = params.get('additional_fields')
        payload = {
            "etag": params.get('etag'),
            "properties": {
                "category": params.get('category'),
                "displayName": params.get('displayName'),
                "query": params.get('query')
            }
        }
        if additional_fields:
            payload['properties'].update(additional_fields)
        payload = check_payload(payload)
        logger.debug("Payload: {0}".format(payload))
        response = api_request("PUT", endpoint, connector_info, config, data=payload)
        return response
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def delete_saved_search(config, params, connector_info):
    try:
        endpoint = analytics_api_endpoint + '/subscriptions/{0}/resourcegroups/{1}/providers/Microsoft.OperationalInsights/workspaces/{2}/savedSearches/{3}?api-version=2020-08-01'.format(
            params.get('subscriptionId'), params.get('resourceGroupName'), params.get('workspaceName'),
            params.get('savedSearchId'))
        response = api_request("DELETE", endpoint, connector_info, config)
        return {'result': 'Deleted Saved Search {0} successfully'.format(params.get('savedSearchId'))}
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


def _check_health(config, connector_info):
    try:
        return check(config, connector_info)
    except Exception as err:
        logger.exception("{0}".format(str(err)))
        raise ConnectorError("{0}".format(str(err)))


operations = {
    'execute_query': execute_query,
    'list_saved_searches': list_saved_searches,
    'get_saved_searches': get_saved_searches,
    'create_saved_searches': create_saved_searches,
    'update_saved_searches': update_saved_searches,
    'delete_saved_search': delete_saved_search
}
