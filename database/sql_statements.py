# SQL Statements

# BasicConfig
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
        configFilePath
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
        row['configFilePath']
    ))
    return cursor

def UpdateBasicConfig(cursor, row):
    cursor.execute("""
    UPDATE BasicConfig
    SET stage = ?,
        tempDir = ?,
        tempDir1 = ?,
        tempDir2 = ?,
        historyFile = ?,
        historyFile1 = ?,
        historyFile2 = ?,
        alreadyTransferedFile = ?,
        historyDays = ?,
        archiverTime = ?,
        watcherEscalationTimeout = ?,
        watcherSleepTime = ?,
        description = ?,
        configFilePath = ?
    WHERE id = ?
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
        row['configFilePath'],
        row['id']
    ))
    return cursor

def DeleteFromBasicConfig(cursor, id):
    cursor.execute("DELETE FROM BasicConfig WHERE id = ?", (id,))
    return cursor

# LzbConfig
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

def UpdateLzbConfig(cursor, row):
    cursor.execute("""
    UPDATE LzbConfig
    SET encrypt_key = ?,
        encrypt_enabled = ?,
        keystore_path = ?,
        keystore_password = ?,
        truststore_path = ?,
        truststore_password = ?,
        ssh_implementation = ?,
        dns_timeout = ?
    WHERE basicConfig_id = ?
    """, (
        row['encrypt_key'],
        row['encrypt_enabled'],
        row['keystore_path'],
        row['keystore_password'],
        row['truststore_path'],
        row['truststore_password'],
        row['ssh_implementation'],
        row['dns_timeout'],
        row['basicConfig_id']
    ))
    return cursor

def DeleteFromLzbConfig(cursor, basicConfig_id):
    cursor.execute("DELETE FROM LzbConfig WHERE basicConfig_id = ?", (basicConfig_id,))
    return cursor

# MqConfig
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

def UpdateMqConfig(cursor, row):
    cursor.execute("""
    UPDATE MqConfig
    SET isRemote = ?,
        qmgr = ?,
        hostname = ?,
        port = ?,
        channel = ?,
        userid = ?,
        password = ?,
        cipher = ?,
        sslPeer = ?,
        ccsid = ?,
        queue = ?,
        numberOfThreads = ?,
        errorQueue = ?,
        commandQueue = ?,
        commandReplyQueue = ?,
        waitinterval = ?,
        description = ?
    WHERE basicConfig_id = ?
    """, (
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
        row['description'],
        row['basicConfig_id']
    ))
    return cursor

def DeleteFromMqConfig(cursor, basicConfig_id):
    cursor.execute("DELETE FROM MqConfig WHERE basicConfig_id = ?", (basicConfig_id,))
    return cursor

# MqTrigger
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

def UpdateMqTrigger(cursor, row):
    cursor.execute("""
    UPDATE MqTrigger
    SET success_interval = ?,
        trigger_interval = ?,
        polling = ?,
        dynamic_instance_management = ?,
        dynamic_success_count = ?,
        dynamic_success_interval = ?,
        dynamic_max_instances = ?
    WHERE mqConfig_id = ?
    """, (
        row['success_interval'],
        row['trigger_interval'],
        row['polling'],
        row['dynamic_instance_management'],
        row['dynamic_success_count'],
        row['dynamic_success_interval'],
        row['dynamic_max_instances'],
        row['mqConfig_id']
    ))
    return cursor

def DeleteFromMqTrigger(cursor, mqConfig_id):
    cursor.execute("DELETE FROM MqTrigger WHERE mqConfig_id = ?", (mqConfig_id,))
    return cursor

# IPQueue
def InsertIntoIPQueue(cursor, row):
    cursor.execute("""
    INSERT INTO IPQueue (
        mqConfig_id,
        queue,
        errorQueue,
        numberOfThreads,
        description
    )
    VALUES (?, ?, ?, ?, ?)
    """, (
        row['mqConfig_id'],
        row['queue'],
        row['errorQueue'],
        row['numberOfThreads'],
        row['description'],
    ))
    return cursor

def UpdateIPQueue(cursor, row):
    cursor.execute("""
    UPDATE IPQueue
    SET queue = ?,
        errorQueue = ?,
        numberOfThreads = ?,
        description = ?
    WHERE mqConfig_id = ?
    """, (
        row['queue'],
        row['errorQueue'],
        row['numberOfThreads'],
        row['description'],
        row['mqConfig_id']
    ))
    return cursor

def DeleteFromIPQueue(cursor, mqConfig_id):
    cursor.execute("DELETE FROM IPQueue WHERE mqConfig_id = ?", (mqConfig_id,))
    return cursor

# Communication
def InsertIntoCommunication(cursor, row):
    cursor.execute("""
    INSERT INTO Communication (
        basicConfig_id,
        name,
        alternateNameList,
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
        renameWithTimestamp
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row['basicConfig_id'],
        row['name'],
        row['alternateNameList'],
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
        row['renameWithTimestamp']
    ))
    return cursor

def update_communication(cursor, row):
    cursor.execute("""
    UPDATE Communication
    SET name = ?,
        alternateNameList = ?,
        watcherEscalationTimeout = ?,
        isToPoll = ?,
        pollUntilFound = ?,
        noTransfer = ?,
        targetMustBeArchived = ?,
        mustBeArchived = ?,
        historyDays = ?,
        targetHistoryDays = ?,
        findPattern = ?,
        movPattern = ?,
        tmpPattern = ?,
        quitPattern = ?,
        putPattern = ?,
        ackPattern = ?,
        rcvPattern = ?,
        zipPattern = ?,
        befoerderung = ?,
        pollInterval = ?,
        gueltigAb = ?,
        gueltigBis = ?,
        befoerderungAb = ?,
        befoerderungBis = ?,
        befoerderungCron = ?,
        preunzip = ?,
        postzip = ?,
        renameWithTimestamp = ?
    WHERE id = ? AND basicConfig_id = ?
    """, (
        row['name'],
        row['alternateNameList'],
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
        row['communication_id'],
        row['basicConfig_id']
    ))
    return cursor

def DeleteFromCommunication(cursor, basicConfig_id):
    cursor.execute("DELETE FROM Communication WHERE basicConfig_id = ?", (basicConfig_id,))
    return cursor

# Location
def InsertIntoLocation(cursor, row):
    cursor.execute("""
    INSERT INTO Location (
        communication_id,
        location,
        location_id,
        useLocalFilename,
        usePathFromConfig,
        targetMustBeArchived,
        targetHistoryDays,
        renameExistingFile,
        userid,
        password,
        description,
        locationType
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row['communication_id'],
        row['location'],
        row['location_id'],
        row['useLocalFilename'],
        row['usePathFromConfig'],
        row['targetMustBeArchived'],
        row['targetHistoryDays'],
        row['renameExistingFile'],
        row['userid'],
        row['password'],
        row['description'],
        row['locationType']
    ))
    return cursor

def UpdateLocation(cursor, row):
    cursor.execute("""
    UPDATE Location
    SET location = ?,
        location_id = ?,
        useLocalFilename = ?,
        usePathFromConfig = ?,
        targetMustBeArchived = ?,
        targetHistoryDays = ?,
        renameExistingFile = ?,
        userid = ?,
        password = ?,
        description = ?,
        locationType = ?
    WHERE communication_id = ?
    """, (
        row['location'],
        row['location_id'],
        row['useLocalFilename'],
        row['usePathFromConfig'],
        row['targetMustBeArchived'],
        row['targetHistoryDays'],
        row['renameExistingFile'],
        row['userid'],
        row['password'],
        row['description'],
        row['locationType'],
        row['communication_id']
    ))
    return cursor

def DeleteFromLocation(cursor, communication_id):
    cursor.execute("DELETE FROM Location WHERE communication_id = ?", (communication_id,))
    return cursor

# Command
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

def UpdateCommand(cursor, row):
    cursor.execute("""
    UPDATE Command
    SET className = ?,
        validForTargetLocations = ?,
        userid = ?,
        password = ?,
        commandType = ?
    WHERE communication_id = ?
    """, (
        row['className'],
        row['validForTargetLocations'],
        row['userid'],
        row['password'],
        row['commandType'],
        row['communication_id']
    ))
    return cursor

def DeleteFromCommand(cursor, communication_id):
    cursor.execute("DELETE FROM Command WHERE communication_id = ?", (communication_id,))
    return cursor

# Command
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

def UpdateCommandParam(cursor, row):
    cursor.execute("""
    UPDATE CommandParam
    SET param = ?
    WHERE command_id = ?
    """, (
        row['param'],
        row['command_id']
    ))
    return cursor

def DeleteFromCommandParam(cursor, command_id):
    cursor.execute("DELETE FROM CommandParam WHERE command_id = ?", (command_id,))
    return cursor

# NameList
def InsertIntoNameList(cursor, row):
    cursor.execute("""
    INSERT INTO NameList (
        basicConfig_id,
        communication_id,
        listName
    )
    VALUES (?, ?, ?)
    """, (
        row['basicConfig_id'],
        row['communication_id'],
        row['listName']
    ))
    return cursor

def UpdateNameList(cursor, row):
    cursor.execute("""
    UPDATE NameList
    SET listName = ?
    WHERE basicConfig_id = ? AND communication_id = ?
    """, (
        row['listName'],
        row['basicConfig_id'],
        row['communication_id']
    ))
    return cursor

def DeleteFromNameList(cursor, basicConfig_id, communication_id):
    cursor.execute("DELETE FROM NameList WHERE basicConfig_id = ? AND communication_id = ?", (basicConfig_id, communication_id,))
    return cursor

# AlternateName
def InsertIntoAlternateName(cursor, row):
    cursor.execute("""
    INSERT INTO AlternateName (
        nameList_id,
        alternateName
    )
    VALUES (?, ?)
    """, (
        row['nameList_id'],
        row['alternateName']
    ))
    return cursor

def UpdateAlternateName(cursor, row):
    cursor.execute("""
    UPDATE AlternateName
    SET alternateName = ?
    WHERE nameList_id = ?
    """, (
        row['alternateName'],
        row['nameList_id']
    ))
    return cursor

def DeleteFromAlternateName(cursor, nameList_id):
    cursor.execute("DELETE FROM AlternateName WHERE nameList_id = ?", (nameList_id,))
    return cursor

# Description
def InsertIntoDescription(cursor, row):
    cursor.execute("""
    INSERT INTO Description (
        communication_id,
        description,
        descriptionType
    )
    VALUES (?, ?, ?)
    """, (
        row['communication_id'],
        row['description'],
        row['descriptionType']
    ))
    return cursor

def UpdateDescription(cursor, row):
    cursor.execute("""
    UPDATE Description
    SET communication_id = ?,
        description = ?,
        descriptionType = ?
    WHERE communication_id = ? and id = ?
    """, (
        row['communication_id'],
        row['description'],
        row['descriptionType'],
        row['communication_id'],
        row['description_id']
    ))
    return cursor

def DeleteDescription(cursor, description_id):
    cursor.execute("DELETE FROM Description WHERE id = ?", (description_id,))
    return cursor
