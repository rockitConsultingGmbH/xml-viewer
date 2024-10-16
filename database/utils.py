# SQL Statements

# Common
def select_all_tablenames_from_db(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return cursor
                   
# BasicConfig
def insert_into_basicconfig(cursor, row):
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

def update_basicconfig(cursor, row):
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

def delete_from_basicconfig(cursor, id):
    cursor.execute("DELETE FROM BasicConfig WHERE id = ?", (id,))
    return cursor

# LzbConfig
def insert_into_lzbconfig(cursor, row):
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

def update_lzbconfig(cursor, row):
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

def delete_from_lzbconfig(cursor, basic_config_id):
    cursor.execute("DELETE FROM LzbConfig WHERE basic_config_id = ?", (basic_config_id,))
    return cursor

# MqConfig
def insert_into_mqconfig(cursor, row):
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

def select_from_mqconfig(cursor, basicConfig_id):
    cursor.execute("""
    SELECT
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
    FROM MqConfig
    WHERE basicConfig_id = ?
    """, (basicConfig_id,))
    return cursor

def update_mqconfig(cursor, row):
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

def delete_from_mqconfig(cursor, basicConfig_id):
    cursor.execute("DELETE FROM MqConfig WHERE basicConfig_id = ?", (basicConfig_id,))
    return cursor

# MqTrigger
def insert_into_mqtrigger(cursor, row):
    cursor.execute("""
    INSERT INTO MqTrigger (
        basicConfig_id,
        mqConfig_id,
        success_interval,
        trigger_interval,
        polling,
        dynamic_instance_management,
        dynamic_success_count,
        dynamic_success_interval,
        dynamic_max_instances
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row['basicConfig_id'],
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

def select_from_mqtrigger(cursor, basicConfig_id):
    cursor.execute("""
    SELECT
        basicConfig_id,
        mqConfig_id,
        success_interval,
        trigger_interval,
        polling,
        dynamic_instance_management,
        dynamic_success_count,
        dynamic_success_interval,
        dynamic_max_instances
    FROM MqTrigger
    WHERE basicConfig_id = ?
    """, (basicConfig_id,))
    return cursor

def update_mqtrigger(cursor, row):
    cursor.execute("""
    UPDATE MqTrigger
    SET success_interval = ?,
        trigger_interval = ?,
        polling = ?,
        dynamic_instance_management = ?,
        dynamic_success_count = ?,
        dynamic_success_interval = ?,
        dynamic_max_instances = ?
    WHERE basicConfig_id = ?
    """, (
        row['success_interval'],
        row['trigger_interval'],
        row['polling'],
        row['dynamic_instance_management'],
        row['dynamic_success_count'],
        row['dynamic_success_interval'],
        row['dynamic_max_instances'],
        row['basicConfig_id']
    ))
    return cursor

def delete_from_mqtrigger(cursor, mqTrigger_id):
    cursor.execute("DELETE FROM MqTrigger WHERE id = ?", (mqTrigger_id,))
    return cursor

# IPQueue
def insert_into_ipqueue(cursor, row):
    cursor.execute("""
    INSERT INTO IPQueue (
        basicConfig_id,
        mqConfig_id,
        queue,
        errorQueue,
        numberOfThreads,
        description
    )
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        row['basicConfig_id'],
        row['mqConfig_id'],
        row['queue'],
        row['errorQueue'],
        row['numberOfThreads'],
        row['description'],
    ))
    return cursor

def select_from_ipqueue(cursor, basicConfig_id):
    cursor.execute("""
    SELECT
        id,
        basicConfig_id,
        mqConfig_id,
        queue,
        errorQueue,
        numberOfThreads,
        description
    FROM IPQueue
    WHERE basicConfig_id = ?
    """, (basicConfig_id,))
    return cursor

def update_ipqueue(cursor, row):
    cursor.execute("""
    UPDATE IPQueue
    SET queue = ?,
        errorQueue = ?,
        numberOfThreads = ?,
        description = ?
    WHERE basicConfig_id = ? AND id = ?
    """, (
        row['queue'],
        row['errorQueue'],
        row['numberOfThreads'],
        row['description'],
        row['basicConfig_id'],
        row['ipqueue_id']
    ))
    return cursor

def delete_from_ipqueue(cursor, ipqueue_id):
    cursor.execute("DELETE FROM IPQueue WHERE ipqueue_id = ? AND ", (ipqueue_id,))
    return cursor

# Communication
def insert_into_communication(cursor, row):
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

def select_from_communication(cursor, communication_id, basicConfig_id):
    cursor.execute("""
    SELECT 
        name, 
        isToPoll, 
        pollUntilFound, 
        noTransfer, 
        befoerderungAb, 
        befoerderungBis,
        pollInterval, 
        watcherEscalationTimeout, 
        preunzip, 
        postzip,
        renameWithTimestamp, 
        gueltigAb, 
        gueltigBis, 
        findPattern, 
        quitPattern,
        ackPattern,
        zipPattern,
        movPattern,
        putPattern, 
        rcvPattern, 
        alternateNameList
    FROM Communication
    WHERE id = ? AND basicConfig_id = ?
    """,
    (communication_id, basicConfig_id))
    return cursor.fetchone()

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

def delete_from_communication(cursor, basicConfig_id):
    cursor.execute("DELETE FROM Communication WHERE basicConfig_id = ?", (basicConfig_id,))
    return cursor

# Location
def insert_into_location(cursor, row):
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

def select_from_location(cursor, communication_id, locationType):
    cursor.execute("""
    SELECT
		id,
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
    FROM Location
    WHERE communication_id = ? AND locationType = ?
    """,
    (communication_id,locationType))
    return cursor.fetchone()

def update_location(cursor, row):
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

def delete_from_location(cursor, communication_id):
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

# CommandParam
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
def insert_into_namelist(cursor, row):
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

def select_from_namelist(cursor, nameList_id):
    cursor.execute("""
    SELECT
        basicConfig_id,
        communication_id,
        listName
    FROM NameList
    WHERE id = ?
    """,
    (nameList_id,))
    return cursor

def update_namelist(cursor, row):
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

def delete_from_namelist(cursor, basicConfig_id, communication_id):
    cursor.execute("DELETE FROM NameList WHERE basicConfig_id = ? AND communication_id = ?", (basicConfig_id, communication_id,))
    return cursor

# AlternateName
def insert_into_alternatename(cursor, row):
    cursor.execute("""
    INSERT INTO AlternateName (
        nameList_id,
        entry
    )
    VALUES (?, ?)
    """, (
        row['nameList_id'],
        row['entry']
    ))
    return cursor

def select_from_alternatename(cursor, nameList_id):
    cursor.execute("""
    SELECT
        id,
        nameList_id,
        entry
    FROM AlternateName
    WHERE nameList_id = ?
    """,
    (nameList_id,))
    return cursor

def update_alternatename(cursor, row):
    cursor.execute("""
    UPDATE AlternateName
    SET entry = ?
    WHERE nameList_id = ?
    """, (
        row['entry'],
        row['nameList_id']
    ))
    return cursor

def delete_from_alternatename(cursor, nameList_id):
    cursor.execute("DELETE FROM AlternateName WHERE nameList_id = ?", (nameList_id,))
    return cursor

# Description
def insert_into_description(cursor, row):
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

def select_from_description(cursor, communication_id, descriptionType):
    cursor.execute("""
    SELECT
        id,
        communication_id,
        description,
        descriptionType
    FROM Description
    WHERE communication_id = ? AND descriptionType = ?
    """,
    (communication_id, descriptionType))
    return cursor.fetchone()

def update_description(cursor, row):
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

def delete_from_description(cursor, description_id):
    cursor.execute("DELETE FROM Description WHERE id = ?", (description_id,))
    return cursor