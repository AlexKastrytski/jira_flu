from jira import JIRA
jira_options = {'server': 'http://192.168.16.15:8080'}
jira = JIRA(options=jira_options, basic_auth=("alexk", "Qwerty123"))
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
token = os.environ.get("INFLUXDB_TOKEN")
org = "A1_IKT"
url = "http://192.168.16.15:8086"
write_client = influxdb_client.InfluxDBClient(url=url, token=token, org=org)
#from influxdb_client import InfluxDBClient, Point, WritePrecision
#from influxdb_client.client.write_api import SYNCHRONOUS
#client = InfluxDBClient(url="http://192.168.16.15:8086", token="QbbYK3QllZtQa7QLFSe91yFB5d7nfRmEm34cKFTgNnqqXPYuYM3cy0DQOHyE_VDg6jYy2z90F8hyTnNQ-Gvrsg==")
#import influxdb_client
#jira_options = {'server': constants.JIRA_SERVER}
#jira = JIRA(options=jira_options, basic_auth=(constants.JIRA_LOGIN, constants.JIRA_PASS))
import datetime
import json
from collections import Counter
#import influxdbConnector
#import influxdb_client
def getJSDData(writeToInflux = False):
    try:
        dt = datetime.datetime.now()
        jqlCreatedToday = 'project = MNGIT_Demo AND created >= startOfDay()'
        #jqlCreatedWeek = 'project = ITSM AND created >= startOfWeek(-6d) AND created <= startOfWeek("+1d")'
        jqlCreatedMonth = 'project = MNGIT_Demo AND created >= startOfMonth()'
        weekDay = dt.weekday()
        if weekDay == 6:
            jqlCreatedWeek = 'project = MNGIT_Demo AND created >= startofWeek(-6d) AND created <= endOfWeek(-6d) order by created asc'
            jqlResolved = 'project = MNGIT_Demo AND status in (Done) AND resolved >= startOfWeek("-6d") AND resolved <= endOfWeek("-6d")'
            jqlResolvedBySystem = ('project = "ITMG_Demo" AND createdDate >= startOfWeek(-6d) AND createdDate < endOfWeek("-6d") \
                AND status in (Done) AND issuetype in ("Task", "Task") AND resolution in (Done)')
        else:
            jqlCreatedWeek = 'project = MNGIT_Demo AND created >= startofWeek("+1d") and created <= endOfWeek("+1d") order by created asc'
            jqlResolvedBySystem = ('project = "ITMG_Demo" AND createdDate >= startOfWeek(-6d) AND createdDate < startOfWeek("+1d") \
                AND status in (Done) AND issuetype in ("Task", "Task") AND resolution in (Done)')
            jqlResolved = 'project = MNGIT_Demo AND status in (Done) AND resolved >= startOfWeek("+1d") AND resolved <= endOfWeek("+1d")'
        print(jqlCreatedWeek)
        print(f"Weekday - {weekDay}")
        createdtoday = jira.search_issues(jqlCreatedToday,  fields= 'key, created', maxResults = 0).total
        createdweek = jira.search_issues(jqlCreatedWeek, fields = 'key, created', maxResults = 0).total
        createdMonth = jira.search_issues(jqlCreatedMonth, fields = 'key, created', maxResults = 0).total
        resolved = jira.search_issues(jqlResolved, fields = 'key, resolutiondate, customfield_14003', maxResults = 3000)
        resolvedBySystem = jira.search_issues(jqlResolvedBySystem, fields = 'key, resolutiondate, customfield_14003', maxResults = 3000)
        systemsCount = []
        for item in resolvedBySystem:
            if 'customfield_14003' in item.raw['fields']:
                rawIssueJson = json.dumps(item.raw['fields']['customfield_14003'], indent = 4)
                if rawIssueJson != 'null':
                    systemsCount.append(json.loads(rawIssueJson)["value"])
                elif rawIssueJson == 'null':
                    systemsCount.append("Not defined")
        systemsCountList = Counter(systemsCount)
        print(systemsCountList)
        print("Calling write method")
        #__CsvWritter(systemsCountList, createdtoday, createdweek, createdMonth, resolved.total)
        if writeToInflux == True:
            write_client.writeJSDBySystem(systemsCountList)
    except Exception as e:
        print(e)
        
        
getJSDData(True)