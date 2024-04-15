from jira import JIRA
jira_options = {'server': 'http://192.168.16.15'}
jira = JIRA(options=jira_options, basic_auth=("alexk", "Qwerty123"))
#import influxdb_client
#from influxdb_client.client.write_api import SYNCHRONOUS
#jira_options = {'server': constants.JIRA_SERVER}
#jira = JIRA(options=jira_options, basic_auth=(constants.JIRA_LOGIN, constants.JIRA_PASS))

def getJSDData(writeToInflux = False):
    try:
        dt = datetime.now()
        jqlCreatedToday = 'project = ITSM AND created >= startOfDay()'
        #jqlCreatedWeek = 'project = ITSM AND created >= startOfWeek(-6d) AND created <= startOfWeek("+1d")'
        jqlCreatedMonth = 'project = ITSM AND created >= startOfMonth()'
        weekDay = dt.weekday()
        if weekDay == 6:
            jqlCreatedWeek = 'project = MNGIT_Demo AND created >= startofWeek(-6d) AND created <= endOfWeek(-6d) order by created asc'
            jqlResolved = 'project = MNGIT_Demo AND status in (Resolved, Closed) AND resolved >= startOfWeek("-6d") AND resolved <= endOfWeek("-6d")'
            jqlResolvedBySystem = ('project = "ITMG_Demo" AND createdDate >= startOfWeek(-6d) AND createdDate < endOfWeek("-6d") \
                AND status in (Resolved, Closed) AND issuetype in ("Task", "Task") AND resolution in (Resolved, Done) AND "System Type" is not EMPTY')
        else:
            jqlCreatedWeek = 'project = MNGIT_Demo AND created >= startofWeek("+1d") and created <= endOfWeek("+1d") order by created asc'
            jqlResolvedBySystem = ('project = "ITMG_Demo" AND createdDate >= startOfWeek(-6d) AND createdDate < startOfWeek("+1d") \
                AND status in (Resolved, Closed) AND issuetype in ("Task", "Task") AND resolution in (Resolved, Done)AND "System Type" is not EMPTY')
            jqlResolved = 'project = MNGIT_Demo AND status in (Resolved, Closed) AND resolved >= startOfWeek("+1d") AND resolved <= endOfWeek("+1d")'
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
            influxdbConnector.writeJSDBySystem(systemsCountList)
    except Exception as e:
        print(e)
        
        
def writeJSDBySystem(listToWrite):
# Write script
    try:
        write_api = client.write_api(write_options=SYNCHRONOUS)
        print("Writting By system")
        for key, c in listToWrite.most_common():
            p = influxdb_client.Point("ITSM").tag("JSD", "BySystem").field(key, c)
            write_api.write(bucket=constants.IF_BUCKET, org=constants.IF_ORG, record=p)
    except Exception as e:
            print("Exception occurred")
            
getJSDData(True)