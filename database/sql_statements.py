
def InsertIntoBasicConfig(cursor, row):
    cursor.execute("""
    INSERT INTO BasicConfig (
        stage, 
        tempDir, 
        tempDir1, 
        tempDir2, 
        historyFile, 
        historyFile1, 
        historyFile2, 
        alreadyTransferedFile, 
        historyDays, 
        archiverTime, 
        watcherEscalationTimeout, 
        watcherSleepTime, 
        description,
        configFileName
    ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row['stage'], 
        row['tempDir'], 
        row['tempDir1'], 
        row['tempDir2'], 
        row['historyFile'], 
        row['historyFile1'], 
        row['historyFile2'], 
        row['alreadyTransferedFile'], 
        row['historyDays'], 
        row['archiverTime'], 
        row['watcherEscalationTimeout'], 
        row['watcherSleepTime'], 
        row['description'],
        row['configFileName']
    ))
    return cursor


def InsertIntoLzbConfig(cursor, row):
    cursor.execute("""
    INSERT INTO LzbConfig (
        basicConfig_id, 
        encrypt_key, 
        encrypt_enabled, 
        keystore_path, 
        keystore_password, 
        truststore_path, 
        truststore_password, 
        ssh_implementation, 
        dns_timeout
    ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row['basicConfig_id'], 
        row['encrypt_key'], 
        row['encrypt_enabled'], 
        row['keystore_path'], 
        row['keystore_password'], 
        row['truststore_path'], 
        row['truststore_password'], 
        row['ssh_implementation'], 
        row['dns_timeout']
    ))
    return cursor


def InsertIntoMqConfig(cursor, row):
    cursor.execute("""
    INSERT INTO MqConfig (
        basicConfig_id, 
        isRemote, 
        qmgr, 
        hostname, 
        port, 
        channel, 
        userid, 
        password, 
        cipher, 
        sslPeer, 
        ccsid, 
        queue, 
        numberOfThreads, 
        errorQueue, 
        commandQueue, 
        commandReplyQueue, 
        waitinterval, 
        description
    ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row['basicConfig_id'], 
        row['isRemote'], 
        row['qmgr'], 
        row['hostname'], 
        row['port'], 
        row['channel'], 
        row['userid'], 
        row['password'], 
        row['cipher'], 
        row['sslPeer'], 
        row['ccsid'], 
        row['queue'], 
        row['numberOfThreads'], 
        row['errorQueue'], 
        row['commandQueue'], 
        row['commandReplyQueue'], 
        row['waitinterval'], 
        row['description']
    ))
    return cursor


def InsertIntoMqTrigger(cursor, row):
    cursor.execute("""
    INSERT INTO MqTrigger (
        mqConfig_id, 
        success_interval, 
        trigger_interval, 
        polling, 
        dynamic_instance_management, 
        dynamic_success_count, 
        dynamic_success_interval, 
        dynamic_max_instances
    ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row['mqConfig_id'], 
        row['success_interval'], 
        row['trigger_interval'], 
        row['polling'], 
        row['dynamic_instance_management'], 
        row['dynamic_success_count'], 
        row['dynamic_success_interval'], 
        row['dynamic_max_instances']
    ))
    return cursor


def InsertIntoIPQueue(cursor, row):
    cursor.execute("""
    INSERT INTO IPQueue (
        mqConfig_id, 
        queue, 
        errorQueue, 
        numberOfThreads
    ) 
    VALUES (?, ?, ?, ?)
    """, (
        row['mqConfig_id'], 
        row['queue'], 
        row['errorQueue'], 
        row['numberOfThreads']
    ))
    return cursor


def InsertIntoCommunication(cursor, row):
    cursor.execute("""
    INSERT INTO Communication (
        basicConfig_id, 
        name, 
        watcherEscalationTimeout, 
        isToPoll, 
        pollUntilFound, 
        noTransfer, 
        targetMustBeArchived, 
        mustBeArchived, 
        historyDays, 
        targetHistoryDays, 
        findPattern, 
        movPattern, 
        tmpPattern, 
        quitPattern, 
        putPattern, 
        ackPattern, 
        rcvPattern, 
        zipPattern, 
        befoerderung, 
        pollInterval, 
        gueltigAb, 
        gueltigBis, 
        befoerderungAb, 
        befoerderungBis, 
        befoerderungCron, 
        preunzip, 
        postzip, 
        renameWithTimestamp, 
        description, 
        description1, 
        description2, 
        description3, 
        description4
    ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row['basicConfig_id'], 
        row['name'], 
        row['watcherEscalationTimeout'], 
        row['isToPoll'], 
        row['pollUntilFound'], 
        row['noTransfer'], 
        row['targetMustBeArchived'], 
        row['mustBeArchived'], 
        row['historyDays'], 
        row['targetHistoryDays'], 
        row['findPattern'], 
        row['movPattern'], 
        row['tmpPattern'], 
        row['quitPattern'], 
        row['putPattern'], 
        row['ackPattern'], 
        row['rcvPattern'], 
        row['zipPattern'], 
        row['befoerderung'], 
        row['pollInterval'], 
        row['gueltigAb'], 
        row['gueltigBis'], 
        row['befoerderungAb'], 
        row['befoerderungBis'], 
        row['befoerderungCron'], 
        row['preunzip'], 
        row['postzip'], 
        row['renameWithTimestamp'], 
        row['description'], 
        row['description1'], 
        row['description2'], 
        row['description3'], 
        row['description4']
    ))
    return cursor


def InsertIntoLocation(cursor, row):
    cursor.execute("""
    INSERT INTO Location (
        communication_id, 
        location, 
        useLocalFilename, 
        usePathFromConfig, 
        targetMustBeArchived, 
        targetHistoryDays, 
        renameExistingFile, 
        userid, 
        password, 
        locationType
    ) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row['communication_id'], 
        row['location'], 
        row['useLocalFilename'], 
        row['usePathFromConfig'], 
        row['targetMustBeArchived'], 
        row['targetHistoryDays'], 
        row['renameExistingFile'], 
        row['userid'], 
        row['password'], 
        row['locationType']
    ))
    return cursor


def InsertIntoCommand(cursor, row):
    cursor.execute("""
    INSERT INTO Command (
        communication_id, 
        className, 
        validForTargetLocations, 
        userid, 
        password, 
        commandType
    ) 
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        row['communication_id'], 
        row['className'], 
        row['validForTargetLocations'], 
        row['userid'], 
        row['password'], 
        row['commandType']
    ))
    return cursor


def InsertIntoCommandParam(cursor, row):
    cursor.execute("""
    INSERT INTO CommandParam (
        command_id, 
        param
    ) 
    VALUES (?, ?)
    """, (
        row['command_id'], 
        row['param']
    ))
    return cursor


def InsertIntoAlternateNameList(cursor, row):
    cursor.execute("""
    INSERT INTO AlternateNameList (
        communication_id, 
        listName, 
        alternateName
    ) 
    VALUES (?, ?, ?)
    """, (
        row['communication_id'], 
        row['listName'], 
        row['alternateName']
    ))
    return cursor
