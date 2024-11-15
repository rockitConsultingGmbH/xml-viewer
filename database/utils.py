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

def select_from_basicconfig(cursor, basicConfig_id):
    cursor.execute("""
    SELECT
        id,
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
    FROM BasicConfig
    WHERE id = ?
    """, (basicConfig_id,))
    return cursor

def get_basic_configs(cursor, text):
    query = """
    SELECT id, 'BasicConfig' as table_name, stage, tempDir, tempDir1, tempDir2, historyFile,
           historyFile1, historyFile2, historyDays, archiverTime, watcherEscalationTimeout,
           watcherSleepTime,
    CASE
        WHEN stage LIKE ? THEN 'stage'
        WHEN tempDir LIKE ? THEN 'tempDir'
        WHEN tempDir1 LIKE ? THEN 'tempDir1'
        WHEN tempDir2 LIKE ? THEN 'tempDir2'
        WHEN historyFile LIKE ? THEN 'historyFile'
        WHEN historyFile1 LIKE ? THEN 'historyFile1'
        WHEN historyFile2 LIKE ? THEN 'historyFile2'
        WHEN historyDays LIKE ? THEN 'historyDays'
        WHEN archiverTime LIKE ? THEN 'archiverTime'
        WHEN watcherEscalationTimeout LIKE ? THEN 'watcherEscalationTimeout'
        WHEN watcherSleepTime LIKE ? THEN 'watcherSleepTime'
    END as source
    FROM BasicConfig
    WHERE stage LIKE ? OR tempDir LIKE ? OR tempDir1 LIKE ? OR tempDir2 LIKE ? OR
          historyFile LIKE ? OR historyFile1 LIKE ? OR historyFile2 LIKE ? OR
          historyDays LIKE ? OR archiverTime LIKE ? OR watcherEscalationTimeout LIKE ?
          OR watcherSleepTime LIKE ?
    """
    params = [f'%{text}%'] * 22
    cursor.execute(query, params)
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
        watcherSleepTime = ?
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

def select_from_lzbconfig(cursor, basicConfig_id):
    cursor.execute("""
    SELECT
        id,
        basicConfig_id,
        encrypt_key,
        encrypt_enabled,
        keystore_path,
        keystore_password,
        truststore_path,
        truststore_password,
        ssh_implementation,
        dns_timeout
    FROM LzbConfig
    WHERE basicConfig_id = ?
    """, (basicConfig_id,))
    return cursor

def get_lzb_configs(cursor, text):
    query = """
    SELECT id, 'LzbConfig' as table_name, encrypt_key, encrypt_enabled, keystore_path, keystore_password, 
           truststore_path, truststore_password, ssh_implementation, dns_timeout,
    CASE
        WHEN encrypt_key LIKE ? THEN 'encrypt_key'
        WHEN keystore_path LIKE ? THEN 'keystore_path'
        WHEN keystore_password LIKE ? THEN 'keystore_password'
        WHEN truststore_path LIKE ? THEN 'truststore_path'
        WHEN truststore_password LIKE ? THEN 'truststore_password'
        WHEN ssh_implementation LIKE ? THEN 'ssh_implementation'
        WHEN dns_timeout LIKE ? THEN 'dns_timeout'
    END as source
    FROM LzbConfig
    WHERE encrypt_key LIKE ? OR keystore_path LIKE ? OR keystore_password LIKE ? OR 
          truststore_path LIKE ? OR truststore_password LIKE ? OR 
          ssh_implementation LIKE ? OR dns_timeout LIKE ?
    """
    params = [f'%{text}%'] * 14
    cursor.execute(query, params)
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
        id,
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

def get_mq_configs(cursor, text):
    query = """
    SELECT id, 'MqConfig' as table_name, isRemote, qmgr, hostname, port, channel, userid, password, cipher, 
           sslPeer, ccsid, queue, numberOfThreads, errorQueue, commandQueue, commandReplyQueue, waitinterval, 
           description,
    CASE
        WHEN qmgr LIKE ? THEN 'qmgr'
        WHEN hostname LIKE ? THEN 'hostname'
        WHEN port LIKE ? THEN 'port'
        WHEN channel LIKE ? THEN 'channel'
        WHEN userid LIKE ? THEN 'userid'
        WHEN password LIKE ? THEN 'password'
        WHEN cipher LIKE ? THEN 'cipher'
        WHEN sslPeer LIKE ? THEN 'sslPeer'
        WHEN ccsid LIKE ? THEN 'ccsid'
        WHEN queue LIKE ? THEN 'queue'
        WHEN numberOfThreads LIKE ? THEN 'numberOfThreads'
        WHEN errorQueue LIKE ? THEN 'errorQueue'
        WHEN commandQueue LIKE ? THEN 'commandQueue'
        WHEN commandReplyQueue LIKE ? THEN 'commandReplyQueue'
        WHEN waitinterval LIKE ? THEN 'waitinterval'
    END as source
    FROM MqConfig
    WHERE qmgr LIKE ? OR hostname LIKE ? OR port LIKE ? OR channel LIKE ? OR userid LIKE ? OR password LIKE ? OR 
          cipher LIKE ? OR sslPeer LIKE ? OR ccsid LIKE ? OR queue LIKE ? OR numberOfThreads LIKE ? OR 
          errorQueue LIKE ? OR commandQueue LIKE ? OR commandReplyQueue LIKE ? OR waitinterval LIKE ?
    """
    params = [f'%{text}%'] * 30
    cursor.execute(query, params)
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
        waitinterval = ?
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

def get_mq_trigger(cursor, text):
    query = """
    SELECT id, 'MqTrigger' as table_name, success_interval, trigger_interval, polling, dynamic_instance_management, dynamic_success_count, dynamic_success_interval, dynamic_max_instances,
    CASE
        WHEN success_interval LIKE ? THEN 'success_interval'
        WHEN trigger_interval LIKE ? THEN 'trigger_interval'
        WHEN polling LIKE ? THEN 'polling'
        WHEN dynamic_instance_management LIKE ? THEN 'dynamic_instance_management'
        WHEN dynamic_success_count LIKE ? THEN 'dynamic_success_count'
        WHEN dynamic_success_interval LIKE ? THEN 'dynamic_success_interval'
        WHEN dynamic_max_instances LIKE ? THEN 'dynamic_max_instances'
    END as source
    FROM MqTrigger
    WHERE success_interval LIKE ? OR trigger_interval LIKE ? OR polling LIKE ? OR dynamic_instance_management LIKE ? OR dynamic_success_count LIKE ? OR dynamic_success_interval LIKE ? OR dynamic_max_instances LIKE ?
    """
    params = [f'%{text}%'] * 14
    cursor.execute(query, params)
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

def get_ip_queue(cursor, text):
    query = """
    SELECT id, 'IPQueue' as table_name, queue, errorQueue, numberOfThreads, description,
    CASE
        WHEN queue LIKE ? THEN 'queue'
        WHEN errorQueue LIKE ? THEN 'errorQueue'
        WHEN numberOfThreads LIKE ? THEN 'numberOfThreads'
        WHEN description LIKE ? THEN 'description'
    END as source
    FROM IPQueue
    WHERE queue LIKE ? OR errorQueue LIKE ? OR numberOfThreads LIKE ? OR description LIKE ?
    """
    params = [f'%{text}%'] * 8
    cursor.execute(query, params)
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
        row['id']
    ))
    return cursor

def delete_from_ipqueue(cursor, ipqueue_id):
    cursor.execute("DELETE FROM IPQueue WHERE id = ?", (ipqueue_id,))
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
        id,
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
    FROM Communication
    WHERE id = ? AND basicConfig_id = ?
    """,
                   (communication_id, basicConfig_id))
    return cursor

def get_communication_names(cursor, communication_id, basicConfig_id):
    cursor.execute("""
    SELECT name FROM Communication WHERE id = ? AND basicConfig_id = ?
    """,
                   (communication_id, basicConfig_id))
    return cursor

def get_communications(cursor, config_id, text):
    query = """
    SELECT id, 'Communication' as table_name, name as communication_name,
    CASE
        WHEN name LIKE ? THEN 'name'
        WHEN alternateNameList LIKE ? THEN 'alternateNameList'
        WHEN gueltigAb LIKE ? THEN 'gueltigAb'
        WHEN gueltigBis LIKE ? THEN 'gueltigBis'
        WHEN befoerderungAb LIKE ? THEN 'befoerderungAb'
        WHEN befoerderungBis LIKE ? THEN 'befoerderungBis'
        WHEN pollInterval LIKE ? THEN 'pollInterval'
        WHEN watcherEscalationTimeout LIKE ? THEN 'watcherEscalationTimeout'
        WHEN findPattern LIKE ? THEN 'findPattern'
        WHEN movPattern LIKE ? THEN 'movPattern'
        WHEN quitPattern LIKE ? THEN 'quitPattern'
        WHEN putPattern LIKE ? THEN 'putPattern'
        WHEN ackPattern LIKE ? THEN 'ackPattern'
        WHEN rcvPattern LIKE ? THEN 'rcvPattern'
        WHEN zipPattern LIKE ? THEN 'zipPattern'
        WHEN tmpPattern LIKE ? THEN 'tmpPattern'
    END as source
    FROM Communication
    WHERE basicConfig_id = ?
    AND (name LIKE ? OR alternateNameList LIKE ? OR gueltigAb LIKE ? OR gueltigBis LIKE ?
    OR befoerderungAb LIKE ? OR befoerderungBis LIKE ? OR pollInterval LIKE ?
    OR watcherEscalationTimeout LIKE ? OR findPattern LIKE ?
    OR movPattern LIKE ? OR quitPattern LIKE ? OR putPattern LIKE ?
    OR ackPattern LIKE ? OR rcvPattern LIKE ? OR zipPattern LIKE ?
    OR tmpPattern LIKE ?)
    """
    params = [f'%{text}%'] * 16 + [config_id] + [f'%{text}%'] * 16
    cursor.execute(query, params)
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

def update_communication_column(cursor, column_name, column_value, id):
    # List of allowed column names
    valid_columns = ['name', 'alternateNameList', 'watcherEscalationTimeout', 'isToPoll',
                     'pollUntilFound', 'noTransfer', 'targetMustBeArchived', 'mustBeArchived',
                     'historyDays', 'targetHistoryDays', 'findPattern', 'movPattern',
                     'tmpPattern', 'quitPattern', 'putPattern', 'ackPattern', 'rcvPattern',
                     'zipPattern', 'befoerderung', 'pollInterval', 'gueltigAb', 'gueltigBis',
                     'befoerderungAb', 'befoerderungBis', 'befoerderungCron', 'preunzip', 'postzip',
                     'renameWithTimestamp']

    if column_name not in valid_columns:
        raise ValueError(f"Invalid column name: {column_name}")

    query = f"""
    UPDATE Communication
    SET {column_name} = ?
    WHERE id = ?
    """
    cursor.execute(query, (column_value, id,))
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
        renameExistingFile,
        userid,
        password,
        description,
        locationType
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        row['communication_id'],
        row['location'],
        row['location_id'],
        row['useLocalFilename'],
        row['usePathFromConfig'],
        row['renameExistingFile'],
        row['userid'],
        row['password'],
        row['description'],
        row['locationType']
    ))
    return cursor

def select_from_location(cursor, communication_id, locationType=None):
    query = """
    SELECT
        id,
        communication_id,
        location,
        location_id,
        useLocalFilename,
        usePathFromConfig,
        renameExistingFile,
        userid,
        password,
        description,
        locationType
    FROM Location
    WHERE communication_id = ?
    """
    params = [communication_id]
    if locationType is not None:
        query += " AND locationType = ?"
        params.append(locationType)
    cursor.execute(query, params)
    return cursor

def get_locations(cursor, text):
    query = """
    SELECT l.id, 'Location' as table_name, l.location, l.communication_id, l.password, l.description,
    CASE
        WHEN l.location LIKE ? THEN 'location'
        WHEN l.location_id LIKE ? THEN 'location_id'
        WHEN l.userid LIKE ? THEN 'userid'
        WHEN l.locationType LIKE ? THEN 'locationType'
        WHEN l.description LIKE ? THEN 'description'
        WHEN l.password LIKE ? THEN 'password'
    END as source,
    c.name as communication_name
    FROM Location l
    JOIN Communication c ON l.communication_id = c.id
    WHERE l.location LIKE ? OR l.location_id LIKE ? OR l.userid LIKE ?
    OR l.locationType LIKE ? OR l.description LIKE ? OR l.password LIKE ?
    """
    params = [f'%{text}%'] * 6 + [f'%{text}%'] * 6
    cursor.execute(query, params)
    return cursor

def update_location(cursor, row):
    cursor.execute("""
    UPDATE Location
    SET location = ?,
        location_id = ?,
        useLocalFilename = ?,
        usePathFromConfig = ?,
        renameExistingFile = ?,
        userid = ?,
        password = ?,
        description = ?
    WHERE id = ?  
    """, (
        row['location'],
        row['location_id'],
        row['useLocalFilename'],
        row['usePathFromConfig'],
        row['renameExistingFile'],
        row['userid'],
        row['password'],
        row['description'],
        row['id']
    ))
    return cursor

def delete_from_location(cursor, location_id):
    cursor.execute("DELETE FROM Location WHERE id = ?", (location_id,))
    return cursor

# Command
def insert_into_command(cursor, row):
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

def select_from_command(cursor, communication_id):
    cursor.execute("""
    SELECT
        id,
        className,
        validForTargetLocations,
        userid,
        password,
        commandType
    FROM Command
    WHERE communication_id = ?
    """,
                   (communication_id,))
    return cursor

def get_command(cursor, text):
    query = """
    SELECT c.id, 'Command' as table_name, c.className, c.validForTargetLocations, c.userid, c.password, c.commandType,
    CASE
        WHEN c.className LIKE ? THEN 'className'
        WHEN c.validForTargetLocations LIKE ? THEN 'validForTargetLocations'
        WHEN c.userid LIKE ? THEN 'userid'
        WHEN c.password LIKE ? THEN 'password'
        WHEN c.commandType LIKE ? THEN 'commandType'
    END as source
    FROM Command c
    WHERE c.className LIKE ? OR c.validForTargetLocations LIKE ? OR c.userid LIKE ? OR c.password LIKE ? OR c.commandType LIKE ?
    """
    params = [f'%{text}%'] * 10
    cursor.execute(query, params)
    return cursor

def update_command(cursor, row):
    cursor.execute("""
    UPDATE Command
    SET className = ?,
        validForTargetLocations = ?,
        userid = ?,
        password = ?,
        commandType = ?
    WHERE id = ?
    """, (
        row['className'],
        row['validForTargetLocations'],
        row['userid'],
        row['password'],
        row['commandType'],
        row['command_id']
    ))
    return cursor

def delete_from_command(cursor, command_id):
    cursor.execute("DELETE FROM Command WHERE id = ?", (command_id,))
    return cursor

# CommandParam
def insert_into_commandparam(cursor, row):
    cursor.execute("""
    INSERT INTO CommandParam (
        command_id,
        param,
        paramName,
        paramOrder
    )
    VALUES (?, ?, ?, ?)
    """, (
        row['command_id'],
        row['param'],
        row['paramName'],
        row['paramOrder']
    ))
    return cursor

def select_from_commandparam(cursor, command_id):
    cursor.execute("""
    SELECT
        id,
        param,
        paramName,
        paramOrder
    FROM CommandParam
    WHERE command_id = ?
    """,
                   (command_id,))
    return cursor

def get_command_param(cursor, text):
    query = """
    SELECT cp.id, 'CommandParam' as table_name, cp.param, cp.paramName, cp.paramOrder,
    CASE
        WHEN cp.param LIKE ? THEN 'param'
        WHEN cp.paramName LIKE ? THEN 'paramName'
        WHEN cp.paramOrder LIKE ? THEN 'paramOrder'
    END as source
    FROM CommandParam cp
    WHERE cp.param LIKE ? OR cp.paramName LIKE ? OR cp.paramOrder LIKE ?
    """
    params = [f'%{text}%'] * 6
    cursor.execute(query, params)
    return cursor

def update_commandparam(cursor, row):
    cursor.execute("""
    UPDATE CommandParam
    SET param = ?
    WHERE command_id = ? AND paramName = ?
    """, (
        row['param'],
        row['command_id'],
        row['paramName']
    ))
    return cursor

def delete_from_commandparam(cursor, command_id):
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

def select_from_namelist_w_communication_id(cursor, communication_id):
    cursor.execute("""
    SELECT
        id,
        basicConfig_id,
        communication_id,
        listName
    FROM NameList
    WHERE communication_id = ?
    """,
                   (communication_id,))
    return cursor

def update_namelist(cursor, row):
    cursor.execute("""
    UPDATE NameList
    SET listName = ?
    WHERE id = ?
    """, (
        row['listName'],
        row['id']
    ))
    return cursor

def delete_from_namelist(cursor, id):
    cursor.execute("DELETE FROM NameList WHERE id = ?",
                   (id,))
    return cursor

def select_from_namelist_with_communication(cursor, nameList_id):
    cursor.execute("""
    SELECT 
        nameList_id, 
        listName, 
        communication_id, 
        communication_name
    FROM NameListWithCommunication
    WHERE nameList_id = ?
    """,
                   (nameList_id,))
    return cursor

def get_namelist(cursor, text):
    query = """
    SELECT nl.id, 'NameList' as table_name, nl.listName, nl.basicConfig_id, nl.communication_id,
    CASE
        WHEN nl.listName LIKE ? THEN 'listName'
    END as source,
    c.name as communication_name
    FROM NameList nl
    JOIN Communication c ON nl.communication_id = c.id
    WHERE nl.listName LIKE ?
    """
    params = [f'%{text}%'] * 2
    cursor.execute(query, params)
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

def get_alternatenames(cursor, text):
    query = """
    SELECT an.id, 'AlternateName' as table_name, an.entry, an.nameList_id, nl.listName,
    CASE
        WHEN an.entry LIKE ? THEN 'entry'
    END as source
    FROM AlternateName an
    JOIN NameList nl ON an.nameList_id = nl.id
    WHERE an.entry LIKE ?
    """
    params = [f'%{text}%'] * 2
    cursor.execute(query, params)
    return cursor

def update_alternatename(cursor, row):
    cursor.execute("""
    UPDATE AlternateName
    SET entry = ?
    WHERE id = ?
    """, (
        row['entry'],
        row['id']
    ))
    return cursor

def delete_from_alternatename(cursor, id):
    cursor.execute("DELETE FROM AlternateName WHERE id = ?", (id,))
    return cursor

def delete_from_alternatename_w_nameList_id(cursor, nameList_id):
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

def select_from_description(cursor, communication_id, description_id=None):
    if description_id is not None:
        cursor.execute("""
        SELECT
            id,
            communication_id,
            description,
            descriptionType
        FROM Description
        WHERE communication_id = ? AND id = ?
        """, (communication_id, description_id))
    else:
        cursor.execute("""
        SELECT
            id,
            communication_id,
            description,
            descriptionType
        FROM Description
        WHERE communication_id = ?
        """, (communication_id,))
    return cursor

def get_descriptions(cursor, text):
    query = """
    SELECT d.id, 'Description' as table_name, d.description, d.communication_id, d.descriptionType,
    CASE
        WHEN d.description LIKE ? THEN 'description'
        WHEN d.descriptionType LIKE ? THEN 'descriptionType'
    END as source,
    c.name as communication_name
    FROM Description d
    JOIN Communication c ON d.communication_id = c.id
    WHERE d.description LIKE ? OR d.descriptionType LIKE ?
    """
    params = [f'%{text}%'] * 4
    cursor.execute(query, params)
    return cursor

def update_description(cursor, row):
    cursor.execute("""
    UPDATE Description
    SET description = ?
    WHERE id = ?
    """, (
        row['description'],
        row['description_id'],
    ))
    return cursor

def delete_from_description(cursor, description_id):
    cursor.execute("DELETE FROM Description WHERE id = ?", (description_id,))
    return cursor
