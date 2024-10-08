from lxml import etree

excluded_columns = ['id', 'configFileName', 'basicConfig_id', 'mqConfig_id', 'communication_id', 'command_id', 'location_id', 'locationType', 'commandType', 'nameList_id']

def add_xml_element_if_not_empty(xml_element, tag_name, value):
    if value:
        etree.SubElement(xml_element, tag_name).text = str(value)
    return etree

def add_xml_element(xml_element, tag_name, value):
    element = etree.SubElement(xml_element, tag_name)
    if value:
        element.text = str(value)
    return etree

def add_xml_element_if_not_emptys_for_row(xml_element, row, columns):
    for col in columns:
        if col in excluded_columns:
            continue
        add_xml_element_if_not_empty(xml_element, col, row[col])
    return etree

# BasicConfig
def create_xml_from_basic_config(root, row, columns):
    xml_element = etree.SubElement(root, 'acsfiletransfer')
    add_xml_element_if_not_emptys_for_row(xml_element, row, columns)

    # add_xml_element_if_not_empty(xml_element, 'stage',                    row['stage'])
    # add_xml_element_if_not_empty(xml_element, 'tempDir',                  row['tempDir'])
    # add_xml_element_if_not_empty(xml_element, 'tempDir1',                 row['tempDir1'])
    # add_xml_element_if_not_empty(xml_element, 'tempDir2',                 row['tempDir2'])
    # add_xml_element_if_not_empty(xml_element, 'historyFile',              row['historyFile'])
    # add_xml_element_if_not_empty(xml_element, 'historyFile1',             row['historyFile1'])
    # add_xml_element_if_not_empty(xml_element, 'historyFile2',             row['historyFile2'])
    # add_xml_element_if_not_empty(xml_element, 'alreadyTransferedFile',    row['alreadyTransferedFile'])
    # add_xml_element_if_not_empty(xml_element, 'historyDays',              row['historyDays'])
    # add_xml_element_if_not_empty(xml_element, 'archiverTime',             row['archiverTime'])
    # add_xml_element_if_not_empty(xml_element, 'watcherEscalationTimeout', row['watcherEscalationTimeout'])
    # add_xml_element_if_not_empty(xml_element, 'watcherSleepTime',         row['watcherSleepTime'])
    # add_xml_element_if_not_empty(xml_element, 'description',              row['description'])
    return etree, xml_element

# LzbConfig
def create_xml_from_basic_lzb(root, row):
    xml_element = etree.SubElement(root, 'lzb')
    encrypt = etree.SubElement(xml_element, 'encrypt')
    add_xml_element_if_not_empty(encrypt, 'enabled',                        row['encrypt_enabled'])
    add_xml_element_if_not_empty(encrypt, 'key',                            row['encrypt_key'])
    ssl = etree.SubElement(xml_element, 'ssl')
    keystore = etree.SubElement(ssl, 'keystore')
    add_xml_element_if_not_empty(keystore, 'path',                          row['keystore_path'])
    add_xml_element_if_not_empty(keystore, 'password',                      row['keystore_password'])
    truststore = etree.SubElement(ssl, 'truststore')
    add_xml_element_if_not_empty(truststore, 'path',                        row['truststore_path'])
    add_xml_element_if_not_empty(truststore, 'password',                    row['truststore_password'])
    ssh = etree.SubElement(xml_element, 'ssh')
    add_xml_element_if_not_empty(ssh, 'implementation',                     row['ssh_implementation'])
    dns = etree.SubElement(xml_element, 'dns')
    add_xml_element_if_not_empty(dns, 'timeout',                            row['dns_timeout'])
    return etree, xml_element

# MqConfig
def create_xml_from_mqconfig(root, row, columns):
    xml_element = etree.SubElement(root, 'mq')
    add_xml_element_if_not_emptys_for_row(xml_element, row, columns)

    # add_xml_element_if_not_empty(xml_element, 'isRemote',                 row['isRemote'])
    # add_xml_element_if_not_empty(xml_element, 'qmgr',                     row['qmgr'])
    # add_xml_element_if_not_empty(xml_element, 'hostname',                 row['hostname'])
    # add_xml_element_if_not_empty(xml_element, 'port',                     row['port'])
    # add_xml_element_if_not_empty(xml_element, 'channel',                  row['channel'])
    # add_xml_element_if_not_empty(xml_element, 'userid',                   row['userid'])
    # add_xml_element_if_not_empty(xml_element, 'password',                 row['password'])
    # add_xml_element_if_not_empty(xml_element, 'cipher',                   row['cipher'])
    # add_xml_element_if_not_empty(xml_element, 'sslPeer',                  row['sslPeer'])
    # add_xml_element_if_not_empty(xml_element, 'ccsid',                    row['ccsid'])
    # add_xml_element_if_not_empty(xml_element, 'queue',                    row['queue'])
    # add_xml_element_if_not_empty(xml_element, 'numberOfThreads',          row['numberOfThreads'])
    # add_xml_element_if_not_empty(xml_element, 'errorQueue',               row['errorQueue'])
    # add_xml_element_if_not_empty(xml_element, 'commandQueue',             row['commandQueue'])
    # add_xml_element_if_not_empty(xml_element, 'commandReplyQueue',        row['commandReplyQueue'])
    # add_xml_element_if_not_empty(xml_element, 'waitinterval',             row['waitinterval'])
    # add_xml_element_if_not_empty(xml_element, 'description',              row['description'])
    return etree, xml_element

# MqTrigger
def create_xml_from_mqtrigger(root, row):
    xml_element = etree.SubElement(root, 'trigger')
    add_xml_element_if_not_empty(xml_element, 'successintervall',           row['success_interval'])
    add_xml_element_if_not_empty(xml_element, 'intervall',                  row['trigger_interval'])
    add_xml_element_if_not_empty(xml_element, 'polling',                    row['polling'])
    dynamic = etree.SubElement(xml_element, 'dynamic')
    instance = etree.SubElement(dynamic, 'instance')
    add_xml_element_if_not_empty(instance, 'management',                    row['dynamic_instance_management'])
    success = etree.SubElement(dynamic, 'success')
    add_xml_element_if_not_empty(success, 'count',                          row['dynamic_success_count'])
    add_xml_element_if_not_empty(success, 'interval',                       row['dynamic_success_interval'])
    max = etree.SubElement(dynamic, 'max')
    add_xml_element_if_not_empty(max, 'instances', row['dynamic_max_instances'])
    return etree, xml_element

# IPQueue
def create_xml_from_ipqueue(root, row):
    etree.SubElement(root, 'description').text = str(row['description'])
    xml_element = etree.SubElement(root, 'IPQueue')
    add_xml_element_if_not_empty(xml_element, 'queue',                      row['queue'])
    add_xml_element_if_not_empty(xml_element, 'errorQueue',                 row['errorQueue'])
    add_xml_element_if_not_empty(xml_element, 'numberOfThreads',            row['numberOfThreads'])
    return etree, xml_element

# Communication
def create_xml_from_communication(root, row):
    #xml_element = etree.SubElement(root, 'communication')
    xml_element = root
    xml_element.set('name', row['name'])

    add_xml_element_if_not_empty(xml_element, 'alternateNameList',          row['alternateNameList'])
    add_xml_element_if_not_empty(xml_element, 'watcherEscalationTimeout',   row['watcherEscalationTimeout'])
    add_xml_element_if_not_empty(xml_element, 'isToPoll',                   row['isToPoll'])
    add_xml_element_if_not_empty(xml_element, 'pollUntilFound',             row['pollUntilFound'])
    add_xml_element_if_not_empty(xml_element, 'noTransfer',                 row['noTransfer'])
    add_xml_element_if_not_empty(xml_element, 'targetMustBeArchived',       row['targetMustBeArchived'])
    add_xml_element_if_not_empty(xml_element, 'mustBeArchived',             row['mustBeArchived'])
    add_xml_element_if_not_empty(xml_element, 'historyDays',                row['historyDays'])
    add_xml_element_if_not_empty(xml_element, 'targetHistoryDays',          row['targetHistoryDays'])
    add_xml_element(xml_element, 'findPattern',                             row['findPattern'])
    add_xml_element(xml_element, 'movPattern',                              row['movPattern'])
    add_xml_element(xml_element, 'tmpPattern',                              row['tmpPattern'])
    add_xml_element(xml_element, 'quitPattern',                             row['quitPattern'])
    add_xml_element(xml_element, 'putPattern',                              row['putPattern'])
    add_xml_element(xml_element, 'ackPattern',                              row['ackPattern'])
    add_xml_element(xml_element, 'rcvPattern',                              row['rcvPattern'])
    add_xml_element(xml_element, 'zipPattern',                              row['zipPattern'])
    add_xml_element_if_not_empty(xml_element, 'befoerderung',               row['befoerderung'])
    add_xml_element_if_not_empty(xml_element, 'pollInterval',               row['pollInterval'])
    add_xml_element(xml_element, 'gueltigAb',                               row['gueltigAb'])
    add_xml_element(xml_element, 'gueltigBis',                              row['gueltigBis'])
    add_xml_element(xml_element, 'befoerderungAb',                          row['befoerderungAb'])
    add_xml_element(xml_element, 'befoerderungBis',                         row['befoerderungBis'])
    add_xml_element(xml_element, 'befoerderungCron',                        row['befoerderungCron'])
    add_xml_element(xml_element, 'preunzip',                                row['preunzip'])
    add_xml_element(xml_element, 'postzip',                                 row['postzip'])
    add_xml_element_if_not_empty(xml_element, 'renameWithTimestamp',        row['renameWithTimestamp'])
    return etree

# Location
def create_xml_from_location(root, row, columns):
    xml_element = etree.SubElement(root, row['locationType'])
    if row['location_id']:
        xml_element.set('id', row['location_id'])
    add_xml_element_if_not_emptys_for_row(xml_element, row, columns)

    # add_xml_element_if_not_empty(xml_element, 'location',                   row['location'])
    # add_xml_element_if_not_empty(xml_element, 'useLocalFilename',           row['useLocalFilename'])
    # add_xml_element_if_not_empty(xml_element, 'usePathFromConfig',          row['usePathFromConfig'])
    # add_xml_element_if_not_empty(xml_element, 'targetMustBeArchived',       row['targetMustBeArchived'])
    # add_xml_element_if_not_empty(xml_element, 'targetHistoryDays',          row['targetHistoryDays'])
    # add_xml_element_if_not_empty(xml_element, 'renameExistingFile',         row['renameExistingFile'])
    # add_xml_element_if_not_empty(xml_element, 'userid',                     row['userid'])
    # add_xml_element_if_not_empty(xml_element, 'password',                   row['password'])
    # add_xml_element_if_not_empty(xml_element, 'description',                row['description'])
    return etree, xml_element

# Command
def create_xml_from_command(root, row):
    xml_element = etree.SubElement(root, row['commandType'])
    add_xml_element_if_not_empty(xml_element, 'className',                  row['className'])
    add_xml_element_if_not_empty(xml_element, 'validForTargetLocations',    row['validForTargetLocations'])
    add_xml_element_if_not_empty(xml_element, 'userid',                     row['userid'])
    add_xml_element_if_not_empty(xml_element, 'password',                   row['password'])
    return etree, xml_element

# CommandParam
def create_xml_from_commandparam(root, row):
    xml_element = add_xml_element(root, 'param',                            row['param'])
    return etree, xml_element

# NameList
def create_xml_from_namelist(root, row):
    xml_element = etree.SubElement(root, 'nameList')
    xml_element.set('name', row['listName'])
    return etree, xml_element

# AlternateName
def create_xml_from_alternatename(root, row):
    xml_element = add_xml_element_if_not_empty(root, 'entry',                row['alternateName'])
    return etree, xml_element

# Description
def create_xml_from_description(root, row):
    #xml_element = add_xml_element_if_not_empty(root, 'description',          row['description'])
    xml_element = add_xml_element_if_not_empty(root, row['descriptionType'],          row['description'])
    return etree, xml_element

