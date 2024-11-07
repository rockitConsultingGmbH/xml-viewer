-- Drop dependent tables in reverse order of creation to avoid foreign key conflicts
DROP TABLE IF EXISTS Description;
DROP TABLE IF EXISTS AlternateName;
DROP VIEW IF EXISTS NameListWithCommunication;
DROP TABLE IF EXISTS NameList;
DROP TABLE IF EXISTS CommandParam;
DROP TABLE IF EXISTS Command;
DROP TABLE IF EXISTS Location;
DROP TABLE IF EXISTS Description;
DROP TABLE IF EXISTS Communication;
DROP TABLE IF EXISTS IPQueue;
DROP TABLE IF EXISTS MqTrigger;
DROP TABLE IF EXISTS MqConfig;
DROP TABLE IF EXISTS LzbConfig;
DROP TABLE IF EXISTS BasicConfig;

-- Create BasicConfig table
CREATE TABLE BasicConfig (
    id INTEGER PRIMARY KEY,
    stage VARCHAR(255) NOT NULL,
    tempDir VARCHAR(255) NOT NULL,
    tempDir1 VARCHAR(255) NOT NULL,
    tempDir2 VARCHAR(255) NOT NULL,
    historyFile VARCHAR(255) NOT NULL,
    historyFile1 VARCHAR(255) NOT NULL,
    historyFile2 VARCHAR(255) NOT NULL,
    alreadyTransferedFile VARCHAR(255) NOT NULL,
    historyDays VARCHAR(255) NOT NULL,
    archiverTime VARCHAR(255) NOT NULL,
    watcherEscalationTimeout VARCHAR(255) NOT NULL,
    watcherSleepTime VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    configFilePath VARCHAR(255)
);

-- Create LzbConfig table with reference to BasicConfig
CREATE TABLE LzbConfig (
    id INTEGER PRIMARY KEY,
    basicConfig_id INT NOT NULL,
    encrypt_key VARCHAR(255),
    encrypt_enabled BOOLEAN,
    keystore_path VARCHAR(255),
    keystore_password VARCHAR(255),
    truststore_path VARCHAR(255),
    truststore_password VARCHAR(255),
    ssh_implementation VARCHAR(255),
    dns_timeout VARCHAR(255),
    FOREIGN KEY (basicConfig_id) REFERENCES BasicConfig(id) ON DELETE CASCADE
);

-- Create MqConfig table with reference to BasicConfig
CREATE TABLE MqConfig (
    id INTEGER PRIMARY KEY,
    basicConfig_id INT NOT NULL,
    isRemote BOOLEAN,
    qmgr VARCHAR(255),
    hostname VARCHAR(255),
    port VARCHAR(255),
    channel VARCHAR(255),
    userid VARCHAR(255),
    password VARCHAR(255),
    cipher VARCHAR(255),
    sslPeer VARCHAR(255),
    ccsid VARCHAR(255),
    queue VARCHAR(255),
    numberOfThreads VARCHAR(255),
    errorQueue VARCHAR(255),
    commandQueue VARCHAR(255),
    commandReplyQueue VARCHAR(255),
    waitinterval VARCHAR(255),
    description VARCHAR(255),
    FOREIGN KEY (basicConfig_id) REFERENCES BasicConfig(id) ON DELETE CASCADE
);

-- Create MqTrigger table with reference to MqConfig
CREATE TABLE MqTrigger (
    id INTEGER PRIMARY KEY,
    basicConfig_id INT NOT NULL,
    mqConfig_id INT NOT NULL,
    success_interval VARCHAR(255),
    trigger_interval VARCHAR(255),
    polling VARCHAR(255),
    dynamic_instance_management VARCHAR(255),
    dynamic_success_count VARCHAR(255),
    dynamic_success_interval VARCHAR(255),
    dynamic_max_instances VARCHAR(255),
    FOREIGN KEY (basicConfig_id) REFERENCES BasicConfig(id) ON DELETE CASCADE
    FOREIGN KEY (mqConfig_id) REFERENCES MqConfig(id) ON DELETE CASCADE
);

-- Create IPQueue table with reference to MqConfig
CREATE TABLE IPQueue (
    id INTEGER PRIMARY KEY,
    basicConfig_id INT NOT NULL,
    mqConfig_id INT NOT NULL,
    queue VARCHAR(255) NOT NULL,
    errorQueue VARCHAR(255),
    numberOfThreads VARCHAR(255),
    description VARCHAR(255),
    FOREIGN KEY (basicConfig_id) REFERENCES BasicConfig(id) ON DELETE CASCADE
    FOREIGN KEY (mqConfig_id) REFERENCES MqConfig(id) ON DELETE CASCADE
);

-- Create Communication table with reference to BasicConfig
CREATE TABLE Communication (
    id INTEGER PRIMARY KEY,
    basicConfig_id INT NOT NULL,
    name VARCHAR(255) NOT NULL,
    alternateNameList VARCHAR(255),
    watcherEscalationTimeout VARCHAR(255),
    isToPoll BOOLEAN,
    pollUntilFound BOOLEAN,
    noTransfer BOOLEAN,
    targetMustBeArchived BOOLEAN,
    mustBeArchived BOOLEAN,
    historyDays VARCHAR(255),
    targetHistoryDays VARCHAR(255),
    findPattern VARCHAR(255),
    movPattern VARCHAR(255),
    tmpPattern VARCHAR(255),
    quitPattern VARCHAR(255),
    putPattern VARCHAR(255),
    ackPattern VARCHAR(255),
    rcvPattern VARCHAR(255),
    zipPattern VARCHAR(255),
    befoerderung VARCHAR(255),
    pollInterval VARCHAR(255),
    gueltigAb VARCHAR(255),
    gueltigBis VARCHAR(255),
    befoerderungAb VARCHAR(255),
    befoerderungBis VARCHAR(255),
    befoerderungCron VARCHAR(255),
    preunzip BOOLEAN,
    postzip BOOLEAN,
    renameWithTimestamp BOOLEAN,
    FOREIGN KEY (basicConfig_id) REFERENCES BasicConfig(id)
    --UNIQUE (basicConfig_id, name)
);

-- Create Location table with reference to Communication
CREATE TABLE Location (
    id INTEGER PRIMARY KEY,
    communication_id INT NOT NULL,
    location VARCHAR(255) NOT NULL,
    location_id VARCHAR(255),
    useLocalFilename BOOLEAN,
    usePathFromConfig BOOLEAN,
    targetMustBeArchived BOOLEAN,
    targetHistoryDays BOOLEAN,
    renameExistingFile BOOLEAN,
    userid VARCHAR(255),
    password VARCHAR(255),
    locationType VARCHAR(255) NOT NULL,
    description VARCHAR(255),
    FOREIGN KEY (communication_id) REFERENCES Communication(id) ON DELETE CASCADE
);

-- Create Command table with reference to Communication
CREATE TABLE Command (
    id INTEGER PRIMARY KEY,
    communication_id INT NOT NULL,
    className VARCHAR(255) NOT NULL,
    validForTargetLocations VARCHAR(255),
    userid VARCHAR(255),
    password VARCHAR(255),
    commandType VARCHAR(255) NOT NULL,
    FOREIGN KEY (communication_id) REFERENCES Communication(id) ON DELETE CASCADE
);

-- Create CommandParam table with reference to Command
CREATE TABLE CommandParam (
    id INTEGER PRIMARY KEY,
    command_id INT NOT NULL,
    param VARCHAR(255),
    paramName VARCHAR(255),
    paramOrder INT,
    FOREIGN KEY (command_id) REFERENCES Command(id) ON DELETE CASCADE
    --UNIQUE (command_id, paramName)
);

-- Create NameList table with reference to Communication
CREATE TABLE NameList (
    id INTEGER PRIMARY KEY,
    basicConfig_id INT NOT NULL,
    communication_id INT, --NOT NULL,
    listName VARCHAR(255) NOT NULL,
    FOREIGN KEY (basicConfig_id) REFERENCES BasicConfig(id) ON DELETE CASCADE
    --FOREIGN KEY (communication_id) REFERENCES Communication(id) ON DELETE CASCADE
);

-- Create view NameListWithCommunication
CREATE VIEW NameListWithCommunication AS
SELECT 
    nl.id AS nameList_id,
    nl.listName, 
    nl.communication_id, 
    c.name AS communication_name
FROM 
    NameList nl
JOIN 
    Communication c 
ON 
    nl.communication_id = c.id;

-- Create AlternateName table with reference to NameList
CREATE TABLE AlternateName (
    id INTEGER PRIMARY KEY,
    nameList_id INT,
    entry VARCHAR(255) NOT NULL,
    FOREIGN KEY (nameList_id) REFERENCES NameList(id) ON DELETE CASCADE
);

-- Create Description table with reference to Communication
CREATE TABLE Description (
    id INTEGER PRIMARY KEY,
    communication_id INT  NOT NULL,
    description TEXT,
    descriptionType VARCHAR(255) NOT NULL,
    FOREIGN KEY (communication_id) REFERENCES Communication(id) ON DELETE CASCADE
);