# Dictionaries
def createBasicConfigDict(acsfiletransfer, cofigFileName):
    BasicConfigDict = {
        'stage':                        acsfiletransfer.find('stage').text,
        'tempDir':                      acsfiletransfer.find('tempDir').text,
        'tempDir1':                     acsfiletransfer.find('tempDir1').text,
        'tempDir2':                     acsfiletransfer.find('tempDir2').text,
        'historyFile':                  acsfiletransfer.find('historyFile').text,
        'historyFile1':                 acsfiletransfer.find('historyFile1').text,
        'historyFile2':                 acsfiletransfer.find('historyFile2').text,
        'alreadyTransferedFile':        acsfiletransfer.find('alreadyTransferedFile').text,
        'historyDays':                  acsfiletransfer.find('historyDays').text,
        'archiverTime':                 acsfiletransfer.find('archiverTime').text,
        'watcherEscalationTimeout':     acsfiletransfer.find('watcherEscalationTimeout').text,
        'watcherSleepTime':             acsfiletransfer.find('watcherSleepTime').text,
        'description':                  acsfiletransfer.find('description').text            if acsfiletransfer.find('description')              is not None else '',
        'configFileName':               cofigFileName
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
        'numberOfThreads':              mq.find('numberOfThreads').text                     if mq.find('numberOfThreads')                       is not None else '',
        'errorQueue':                   mq.find('errorQueue').text,
        'commandQueue':                 mq.find('commandQueue').text,
        'commandReplyQueue':            mq.find('commandReplyQueue').text,
        'waitinterval':                 mq.find('waitinterval').text,
        'description':                  '' #mq.find('description').text
    }
    return MqConfigDict

def createMqTriggerDict(mqConfig_id, mqtrigger):
    MqTriggerDict = {
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

def createIPQueueDict(mqConfig_id, ipqueue):
    IPQueueDict = {
        'mqConfig_id':                  mqConfig_id,
        'queue':                        ipqueue.find('queue').text,
        'errorQueue':                   ipqueue.find('errorQueue').text,
        'numberOfThreads':              ipqueue.find('numberOfThreads').text,
        #'description':                  ipqueue.find('description').text                    if ipqueue.find('description')                      is not None else ''
        'description':                  ipqueue.getprevious().text                          if ipqueue.getprevious() is not None and ipqueue.getprevious().tag == 'description' else ''
    }
    return IPQueueDict

def createCommunicationDict(basicConfig_id, communication):
    CommunicationDict = {
        'basicConfig_id':               basicConfig_id,
        'name':                         communication.get('name', ''),
        'alternateNameList':            communication.find('alternateNameList').text        if communication.find('alternateNameList')          is not None else '',
        'watcherEscalationTimeout':     communication.find('watcherEscalationTimeout').text if communication.find('watcherEscalationTimeout')   is not None else '',
        'isToPoll':                     communication.find('isToPoll').text                 if communication.find('isToPoll')                   is not None else '',
        'pollUntilFound':               communication.find('pollUntilFound').text           if communication.find('pollUntilFound')             is not None else '',
        'noTransfer':                   communication.find('noTransfer').text               if communication.find('noTransfer')                 is not None else '',
        'targetMustBeArchived':         communication.find('targetMustBeArchived').text     if communication.find('targetMustBeArchived')       is not None else '',
        'mustBeArchived':               communication.find('mustBeArchived').text           if communication.find('mustBeArchived')             is not None else '',
        'historyDays':                  communication.find('historyDays').text              if communication.find('historyDays')                is not None else '',
        'targetHistoryDays':            communication.find('targetHistoryDays').text        if communication.find('targetHistoryDays')          is not None else '',
        'findPattern':                  communication.find('findPattern').text,     
        'movPattern':                   communication.find('movPattern').text,      
        'tmpPattern':                   communication.find('tmpPattern').text               if communication.find('tmpPattern')                 is not None else '',
        'quitPattern':                  communication.find('quitPattern').text              if communication.find('quitPattern')                is not None else '',
        'putPattern':                   communication.find('putPattern').text,      
        'ackPattern':                   communication.find('ackPattern').text,      
        'rcvPattern':                   communication.find('rcvPattern').text               if communication.find('rcvPattern')                 is not None else '',
        'zipPattern':                   communication.find('zipPattern').text               if communication.find('zipPattern')                 is not None else '',
        'befoerderung':                 communication.find('befoerderung').text             if communication.find('befoerderung')               is not None else '',
        'pollInterval':                 communication.find('pollInterval').text             if communication.find('pollInterval')               is not None else '',
        'gueltigAb':                    communication.find('gueltigAb').text                if communication.find('gueltigAb')                  is not None else '',
        'gueltigBis':                   communication.find('gueltigBis').text               if communication.find('gueltigBis')                 is not None else '',
        'befoerderungAb':               communication.find('befoerderungAb').text           if communication.find('befoerderungAb')             is not None else '',
        'befoerderungBis':              communication.find('befoerderungBis').text          if communication.find('befoerderungBis')            is not None else '',
        'befoerderungCron':             communication.find('befoerderungCron').text         if communication.find('befoerderungCron')           is not None else '',
        'preunzip':                     communication.find('preunzip').text                 if communication.find('preunzip')                   is not None else '',
        'postzip':                      communication.find('postzip').text,     
        'renameWithTimestamp':          communication.find('renameWithTimestamp').text
    }
    return CommunicationDict

def createLocationDict(communication_id, location, locationType):
    LocationDict = {
        'communication_id':             communication_id,
        'location':                     location.find('location').text,
        'location_id':                  location.get('id', ''),
        'useLocalFilename':             location.find('useLocalFilename').text              if location.find('useLocalFilename')                is not None else '',
        'usePathFromConfig':            location.find('usePathFromConfig').text             if location.find('usePathFromConfig')               is not None else '',
        'targetMustBeArchived':         location.find('targetMustBeArchived').text          if location.find('targetMustBeArchived')            is not None else '',
        'targetHistoryDays':            location.find('targetHistoryDays').text             if location.find('targetHistoryDays')               is not None else '',
        'renameExistingFile':           location.find('renameExistingFile').text            if location.find('renameExistingFile')              is not None else '',
        'userid':                       location.find('userid').text,
        'password':                     location.find('password').text,
        'description':                  location.find('description').text                   if location.find('description')                     is not None else '',
        'locationType':                 locationType
    }
    return LocationDict

def createCommandDict(communication_id, command, commandType):
    CommandDict = {
        'communication_id':             communication_id,
        'className':                    command.find('className').text,
        'validForTargetLocations':      command.find('validForTargetLocations').text        if command.find('validForTargetLocations')          is not None else '',
        'userid':                       command.find('userid').text                         if command.find('userid')                           is not None else '',
        'password':                     command.find('password').text                       if command.find('password')                         is not None else '',
        'commandType':                  commandType
    }
    return CommandDict

def createCommandParamDict(command_id, param):
    CommandParamDict = {
        'command_id':                   command_id,
        'param':                        param
    }
    return CommandParamDict

def createNameListDict(basicConfig_id, communication_id, listName):
    NameListDict = {
        'basicConfig_id':               basicConfig_id,
        'communication_id':             communication_id,
        'listName':                     listName
    }
    return NameListDict
    
def createAlternateNameDict(nameList_id, alternateName):
    AlternateNameDict = {
        'nameList_id':                  nameList_id,
        'alternateName':                alternateName
    }
    return AlternateNameDict

def createDescriptionDict(communication_id, description, descriptionType):
    DescriptionDict = {
        'communication_id':             communication_id,
        'description':                  description.text,
        'descriptionType':              descriptionType
    }
    return DescriptionDict
