from controllers.commandparam_map import set_command_param_name


def add_xml_element(root, tag_name):
    value = (
        root.find(tag_name).text if root.find(tag_name) is not None and root.find(tag_name).text else ''
    )
    return value

def add_boolean_xml_element(root, tag_name):
    value = (
        root.find(tag_name).text if root.find(tag_name) is not None and root.find(tag_name).text else 'false'
    )
    return value

# Dictionaries
def createBasicConfigDict(acsfiletransfer, configFilePath):
    BasicConfigDict = {
        'stage':                        add_xml_element(acsfiletransfer, 'stage'),
        'tempDir':                      add_xml_element(acsfiletransfer, 'tempDir'),
        'tempDir1':                     add_xml_element(acsfiletransfer, 'tempDir1'),
        'tempDir2':                     add_xml_element(acsfiletransfer, 'tempDir2'),
        'historyFile':                  add_xml_element(acsfiletransfer, 'historyFile'),
        'historyFile1':                 add_xml_element(acsfiletransfer, 'historyFile1'),
        'historyFile2':                 add_xml_element(acsfiletransfer, 'historyFile2'),
        'alreadyTransferedFile':        add_xml_element(acsfiletransfer, 'alreadyTransferedFile'),
        'historyDays':                  add_xml_element(acsfiletransfer, 'historyDays'),
        'archiverTime':                 add_xml_element(acsfiletransfer, 'archiverTime'),
        'watcherEscalationTimeout':     add_xml_element(acsfiletransfer, 'watcherEscalationTimeout'),
        'watcherSleepTime':             add_xml_element(acsfiletransfer, 'watcherSleepTime'),
        'description':                  add_xml_element(acsfiletransfer, 'description'),
        'configFilePath':               configFilePath
    }
    return BasicConfigDict

def createLzbConfigDict(basicConfig_id, lzb):
    LzbConfigDict = {
        'basicConfig_id':               basicConfig_id,
        'encrypt_key':                  lzb.find('encrypt').find('key').text,
        'encrypt_enabled':              lzb.find('encrypt').find('enabled').text,
        'keystore_path':                lzb.find('ssl').find('keystore').find('path').text,
        'keystore_password':            lzb.find('ssl').find('keystore').find('password').text,
        'truststore_path':              lzb.find('ssl').find('truststore').find('path').text,
        'truststore_password':          lzb.find('ssl').find('truststore').find('password').text,
        'ssh_implementation':           lzb.find('ssh').find('implementation').text,
        'dns_timeout':                  lzb.find('dns').find('timeout').text
    }
    return LzbConfigDict

def createMqConfigDict(basicConfig_id, mq):
    MqConfigDict = {
        'basicConfig_id':               basicConfig_id,
        'isRemote':                     mq.find('isRemote').text,
        'qmgr':                         mq.find('qmgr').text,
        'hostname':                     mq.find('hostname').text,
        'port':                         mq.find('port').text,
        'channel':                      mq.find('channel').text,
        'userid':                       mq.find('userid').text,
        'password':                     mq.find('password').text,
        'cipher':                       mq.find('cipher').text,
        'sslPeer':                      mq.find('sslPeer').text,
        'ccsid':                        mq.find('ccsid').text,
        'queue':                        mq.find('queue').text,
        'numberOfThreads':              add_xml_element(mq, 'numberOfThreads'),
        'errorQueue':                   mq.find('errorQueue').text,
        'commandQueue':                 mq.find('commandQueue').text,
        'commandReplyQueue':            mq.find('commandReplyQueue').text,
        'waitinterval':                 mq.find('waitinterval').text,
        'description':                  '' #mq.find('description').text
    }
    return MqConfigDict

def createMqTriggerDict(basicConfig_id, mqConfig_id, mqtrigger):
    MqTriggerDict = {
        'basicConfig_id':               basicConfig_id,
        'mqConfig_id':                  mqConfig_id,
        'success_interval':             mqtrigger.find('successintervall').text,
        'trigger_interval':             mqtrigger.find('intervall').text,
        'polling':                      mqtrigger.find('polling').text,
        'dynamic_instance_management':  mqtrigger.find('dynamic').find('instance').find('management').text,
        'dynamic_success_count':        mqtrigger.find('dynamic').find('success').find('count').text,
        'dynamic_success_interval':     mqtrigger.find('dynamic').find('success').find('interval').text,
        'dynamic_max_instances':        mqtrigger.find('dynamic').find('max').find('instances').text
    }
    return MqTriggerDict

def createIPQueueDict(basicConfig_id, mqConfig_id, ipqueue):
    IPQueueDict = {
        'basicConfig_id':               basicConfig_id,
        'mqConfig_id':                  mqConfig_id,
        'queue':                        ipqueue.find('queue').text,
        'errorQueue':                   ipqueue.find('errorQueue').text,
        'numberOfThreads':              ipqueue.find('numberOfThreads').text,
        'description':                  (
                                            ipqueue.find('description').text 
                                            if ipqueue.find('description') is not None 
                                            else (
                                                ipqueue.getprevious().text 
                                                if ipqueue.getprevious() is not None and ipqueue.getprevious().tag == 'description' 
                                                else ''
                                            )
                                        )
    }
    return IPQueueDict

def createCommunicationDict(basicConfig_id, communication):
    CommunicationDict = {
        'basicConfig_id':               basicConfig_id,
        'name':                         communication.get('name', ''),
        'alternateNameList':            add_xml_element(communication, 'alternateNameList'),
        'watcherEscalationTimeout':     add_xml_element(communication, 'watcherEscalationTimeout'),
        'isToPoll':                     add_boolean_xml_element(communication, 'isToPoll'),
        'pollUntilFound':               add_boolean_xml_element(communication, 'pollUntilFound'),
        'noTransfer':                   add_boolean_xml_element(communication, 'noTransfer'),
        'targetMustBeArchived':         add_boolean_xml_element(communication, 'targetMustBeArchived'),
        'mustBeArchived':               add_boolean_xml_element(communication, 'mustBeArchived'),
        'historyDays':                  add_xml_element(communication, 'historyDays'),
        'targetHistoryDays':            add_xml_element(communication, 'targetHistoryDays'),
        'findPattern':                  add_xml_element(communication, 'findPattern'),
        'movPattern':                   add_xml_element(communication, 'movPattern'),
        'tmpPattern':                   add_xml_element(communication, 'tmpPattern'),
        'quitPattern':                  add_xml_element(communication, 'quitPattern'),
        'putPattern':                   add_xml_element(communication, 'putPattern'),
        'ackPattern':                   add_xml_element(communication, 'ackPattern'),
        'rcvPattern':                   add_xml_element(communication, 'rcvPattern'),
        'zipPattern':                   add_xml_element(communication, 'zipPattern'),
        'befoerderung':                 add_xml_element(communication, 'befoerderung'),
        'pollInterval':                 add_xml_element(communication, 'pollInterval'),
        'gueltigAb':                    add_xml_element(communication, 'gueltigAb'),
        'gueltigBis':                   add_xml_element(communication, 'gueltigBis'),
        'befoerderungAb':               add_xml_element(communication, 'befoerderungAb'),
        'befoerderungBis':              add_xml_element(communication, 'befoerderungBis'),
        'befoerderungCron':             add_xml_element(communication, 'befoerderungCron'),
        'preunzip':                     add_boolean_xml_element(communication, 'preunzip'),
        'postzip':                      add_boolean_xml_element(communication, 'postzip'),
        'renameWithTimestamp':          add_boolean_xml_element(communication, 'renameWithTimestamp'),
    }
    return CommunicationDict

def createLocationDict(communication_id, location, locationType):
    LocationDict = {
        'communication_id':             communication_id,
        'location':                     add_xml_element(location, 'location'),
        'location_id':                  location.get('id', ''),
        'useLocalFilename':             add_boolean_xml_element(location, 'useLocalFilename'),
        'usePathFromConfig':            add_boolean_xml_element(location, 'usePathFromConfig'),
        'targetMustBeArchived':         add_boolean_xml_element(location, 'targetMustBeArchived'),
        'targetHistoryDays':            add_xml_element(location, 'targetHistoryDays'),
        'renameExistingFile':           add_boolean_xml_element(location, 'renameExistingFile'),
        'userid':                       add_xml_element(location, 'userid'),
        'password':                     add_xml_element(location, 'password'),
        'description':                  add_xml_element(location, 'description'),
        'locationType':                 locationType
    }
    return LocationDict

def createCommandDict(communication_id, command, commandType):
    CommandDict = {
        'communication_id':             communication_id,
        'className':                    add_xml_element(command, 'className'),
        'validForTargetLocations':      add_xml_element(command, 'validForTargetLocations'),
        'userid':                       add_xml_element(command, 'userid'),
        'password':                     add_xml_element(command, 'password'),
        'commandType':                  commandType
    }
    return CommandDict

def createCommandParamDict(command_id, param, paramOrder, className):
    CommandParamDict = {
        'command_id':                   command_id,
        'param':                        param,
        'paramName':                    set_command_param_name(className, paramOrder),
        'paramOrder':                   paramOrder,
    }
    return CommandParamDict

def createNameListDict(basicConfig_id, communication_id, listName):
    NameListDict = {
        'basicConfig_id':               basicConfig_id,
        'communication_id':             communication_id,
        'listName':                     listName
    }
    return NameListDict
    
def createAlternateNameDict(nameList_id, entry):
    AlternateNameDict = {
        'nameList_id':                  nameList_id,
        'entry':                        entry
    }
    return AlternateNameDict

def createDescriptionDict(communication_id, description, descriptionType):
    DescriptionDict = {
        'communication_id':             communication_id,
        'description':                  description.text,
        'descriptionType':              descriptionType
    }
    return DescriptionDict
