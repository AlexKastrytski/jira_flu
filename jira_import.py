from jira import JIRA
jira_options = {'server': 'http://10.254.5.199:8080'}
jira = JIRA(options=jira_options, basic_auth=("man_it", "3>dUk${HkqMLa019"))
import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
token = '2Ps15FgGMfSW48O5E5-C3plGAgtv0_GoYQU2_pW0iWexTsnUjWNRRPNSmCQZKQqup80-jw5neXzZ2VRfL5qPDA=='
org = "A1_IKT"
url = "https://influxdb.managed-it.a1.by"
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
def writeJSDBySystem(listToWrite):
# Write script
    try:
        write_api = write_client.write_api(write_options=SYNCHRONOUS)
        print("Writting By system")
        for key in listToWrite:
            p = influxdb_client.Point("ManagedIT").tag("JSD", "BySystem").field('Task',key)
            write_api.write(bucket="Trans_DB_Jira", org=org, record=p)
    except Exception as e:
            print(e)
            
def getJSDData(writeToInflux = False):
    try:
        dt = datetime.datetime.now()	

        jqlCreatedToday = 'project in (ManagedIT, DCSD) AND assignee in (vladimir_shevc, sergey_shev, kanstantsin_ma, Kirill_D1, aliaksandr_kast, dzmitry_ye) AND resolved >= startOfMonth() AND "Customer Request Type" != "Monitoring (MNGIT)"'
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
        createdtoday = jira.search_issues(jqlCreatedToday,  fields= 'key, created', maxResults =2000)
        createdweek = jira.search_issues(jqlCreatedWeek, fields = 'key, created', maxResults = 0).total
        createdMonth = jira.search_issues(jqlCreatedMonth, fields = 'key, created', maxResults = 0).total
        resolved = jira.search_issues(jqlResolved, fields = 'key, resolutiondate, customfield_14003', maxResults = 3000)
        resolvedBySystem = jira.search_issues(jqlResolvedBySystem, fields = 'key, resolutiondate, customfield_14003', maxResults = 3000)
        systemsCount = []
        for item in createdtoday:
            systemsCount.append(item.key)
        print(systemsCount)
        print("Calling write method")
        #__CsvWritter(systemsCountList, createdtoday, createdweek, createdMonth, resolved.total)
        if writeToInflux == True:
            writeJSDBySystem(systemsCount)
    except Exception as e:
        print(e)
getJSDData(True)