
-- Insert data into BasicConfig table
INSERT INTO BasicConfig (stage, tempDir, tempDir1, tempDir2, historyFile, historyFile1, historyFile2, alreadyTransferedFile, historyDays, archiverTime, watcherEscalationTimeout, watcherSleepTime, description) VALUES
('Stage 1', '/tmp/dir1', '/tmp/dir1_1', '/tmp/dir1_2', '/history/file1', '/history/file1_1', '/history/file1_2', '/transfered/file1', '10', '12:00', '60', '5', 'Config 1'),
('Stage 2', '/tmp/dir2', '/tmp/dir2_1', '/tmp/dir2_2', '/history/file2', '/history/file2_1', '/history/file2_2', '/transfered/file2', '20', '15:00', '120', '10', 'Config 2');

-- Insert data into LzbConfig table
INSERT INTO LzbConfig (basicConfig_id, encrypt_key, encrypt_enabled, keystore_path, keystore_password, truststore_path, truststore_password, ssh_implementation, dns_timeout) VALUES
(1, 'key123', 'TRUE', '/path/to/keystore', 'keystorepass', '/path/to/truststore', 'truststorepass', 'OpenSSH', '30'),
(2, 'key456', 'FALSE', '/path/to/keystore2', 'keystorepass2', '/path/to/truststore2', 'truststorepass2', 'PuTTY', '40');

-- Insert data into MqConfig table
INSERT INTO MqConfig (basicConfig_id, isRemote, qmgr, hostname, port, channel, userid, password, cipher, sslPeer, ccsid, queue, numberOfThreads, errorQueue, commandQueue, commandReplyQueue, waitinterval, description) VALUES
(1, 'TRUE', 'QMGR1', 'hostname1', '1414', 'CHANNEL1', 'user1', 'pass1', 'TLS_RSA_WITH_AES_128_CBC_SHA', 'CN=SSLPeer1', '1208', 'QUEUE1', '5', 'ERROR_QUEUE1', 'COMMAND_QUEUE1', 'COMMAND_REPLY_QUEUE1', '60', 'MQ Config 1'),
(2, 'FALSE', 'QMGR2', 'hostname2', '1415', 'CHANNEL2', 'user2', 'pass2', 'TLS_RSA_WITH_AES_256_CBC_SHA', 'CN=SSLPeer2', '819', 'QUEUE2', '10', 'ERROR_QUEUE2', 'COMMAND_QUEUE2', 'COMMAND_REPLY_QUEUE2', '60', 'MQ Config 2');

-- Insert data into MqTrigger table
INSERT INTO MqTrigger (mqConfig_id, success_interval, trigger_interval, polling, dynamic_instance_management, dynamic_success_count, dynamic_success_interval, dynamic_max_instances) VALUES
(1, '5', '10', 'Yes', 'Auto', '3', '20', '5'),
(2, '10', '15', 'No', 'Manual', '2', '25', '10');

-- Insert data into IPQueue table
INSERT INTO IPQueue (mqConfig_id, queue, errorQueue, numberOfThreads) VALUES
(1, 'IP_QUEUE1', 'IP_ERROR_QUEUE1', '3'),
(2, 'IP_QUEUE2', 'IP_ERROR_QUEUE2', '7');

-- Insert data into Communication table
INSERT INTO Communication (basicConfig_id, name, alternateNameList, watcherEscalationTimeout, isToPoll, pollUntilFound, noTransfer, targetMustBeArchived, mustBeArchived, historyDays, targetHistoryDays, findPattern, movPattern, tmpPattern, quitPattern, putPattern, ackPattern, rcvPattern, zipPattern, befoerderung, pollInterval, gueltigAb, gueltigBis, befoerderungAb, befoerderungBis, befoerderungCron, preunzip, postzip, renameWithTimestamp, description, description1, description2, description3, description4) VALUES
(1, 'AltList1', '30', 'TRUE', 'TRUE', 'FALSE', 'TRUE', 'TRUE', '15', '20', '*.txt', '*.mov', '*.tmp', '*.quit', '*.put', '*.ack', '*.rcv', '*.zip', 'B1', '10', '2024-01-01', '2024-12-31', '2024-02-01', '2024-11-30', '0 0 * * *', 'TRUE', 'FALSE', 'TRUE', 'Name 1', 'Comm 1', 'Desc 1.1', 'Desc 1.2', 'Desc 1.3', 'Desc 1.4'),
(2, 'AltList2', '60', 'FALSE', 'FALSE', 'TRUE', 'FALSE', 'FALSE', '30', '40', '*.log', '*.mov', '*.tmp', '*.quit', '*.put', '*.ack', '*.rcv', '*.zip', 'B2', '20', '2025-01-01', '2025-12-31', '2025-02-01', '2025-11-30', '0 12 * * *', 'FALSE', 'TRUE', 'FALSE', 'Name 2', 'Comm 2', 'Desc 2.1', 'Desc 2.2', 'Desc 2.3', 'Desc 2.4');

-- Insert data into Description table
/*INSERT INTO Description (communication_id, description) VALUES
(1, 'This is the first description.'),
(2, 'This is the second description.');
*/

-- Insert data into Location table
INSERT INTO Location (communication_id, location, location_id, useLocalFilename, usePathFromConfig, targetMustBeArchived, targetHistoryDays, renameExistingFile, userid, password, locationType) VALUES
(1, '/path/to/location1', 't1', 'TRUE', 'FALSE', 'TRUE', 'TRUE', 'FALSE', 'user1', 'pass1', 'sourceLocation'),
(2, '/path/to/location2', '', 'FALSE', 'TRUE', 'FALSE', 'FALSE', 'TRUE', 'user2', 'pass2', 'sourceLocation');

-- Insert data into Command table
INSERT INTO Command (communication_id, className, validForTargetLocations, userid, password, commandType) VALUES
(1, 'com.example.CommandClass1', 'Location1', 'user1', 'pass1', 'preCommand'),
(2, 'com.example.CommandClass2', 'Location2', 'user2', 'pass2', 'postCommand');

-- Insert data into CommandParam table
INSERT INTO CommandParam (command_id, param) VALUES
(1, 'param1'),
(1, 'param2'),
(2, 'param3'),
(2, 'param4');

-- Insert data into NameList table
INSERT INTO NameList (basicConfig_id, communication_id, listName) VALUES
(1, 1, 'NameList1'),
(2, 2, 'NameList2');

-- Insert data into AlternateNameList table
INSERT INTO AlternateName (nameList_id, alternateName) VALUES
(1, 'AlternateName1'),
(1, 'AlternateName2'),
(2, 'AlternateName3'),
(2, 'AlternateName4');
