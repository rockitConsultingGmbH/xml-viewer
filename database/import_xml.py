from lxml import etree
import sqlite3
import os
import database.sql_statements as sql_statements
import database.dictionaries as dictionaries

db_path = os.path.join(os.path.dirname(__file__), 'acsfiletransfer.db')

def get_db_connection():
    """
    Get a connection to the SQLite database.

    :return: SQLite connection object
    """
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"The specified database file was not found: {db_path}")

    return sqlite3.connect(db_path)

def validate_xml(xml_path, xsd_path):
    """
    Validate the XML file against the XSD schema.

    :param xml_path: Path to the XML file
    :param xsd_path: Path to the XSD schema file
    :return: Parsed XML tree if valid, raises exception if invalid
    """
    # Check if the XSD file exists
    if not os.path.exists(xsd_path):
        raise FileNotFoundError(f"The specified XSD file was not found: {xsd_path}")

    with open(xsd_path, 'rb') as xsd_file:
        xsd_schema = etree.XMLSchema(etree.parse(xsd_file))

    # Check if the XML file exists
    if not os.path.exists(xml_path):
        raise FileNotFoundError(f"The specified XML file was not found: {xml_path}")

    with open(xml_path, 'rb') as xml_file:
        xml_tree = etree.parse(xml_file)

    # Validate XML against the XSD schema
    if not xsd_schema.validate(xml_tree):
        raise ValueError(f"XML file {xml_path} is invalid:\n{xsd_schema.error_log}")

    print(f"XML file {xml_path} is valid.")
    return xml_tree


def insert_data_into_db(xml_tree, config_file_name):
    """
    Insert data from the parsed XML tree into the SQLite database.

    :param xml_tree: Parsed XML tree
    :param config_file_name: Name of the configuration file
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    rows_created = 0

    root = xml_tree.getroot()

    # Adjust the XPath based on your XML structure
    acsfiletransfer = root.find('.//acsfiletransfer')

    # BasicConfig
    basicConfig_id = sql_statements.InsertIntoBasicConfig(cursor,
                                                          dictionaries.createBasicConfigDict(acsfiletransfer, config_file_name)).lastrowid
    rows_created += cursor.rowcount

    # LzbConfig
    lzb = acsfiletransfer.find('lzb')
    sql_statements.InsertIntoLzbConfig(cursor, dictionaries.createLzbConfigDict(basicConfig_id, lzb))
    rows_created += cursor.rowcount

    # MqConfig
    mq = acsfiletransfer.find('mq')
    mqConfig_id = sql_statements.InsertIntoMqConfig(cursor, dictionaries.createMqConfigDict(basicConfig_id, mq)).lastrowid
    rows_created += cursor.rowcount

    # MqTrigger
    mqtrigger = mq.find('trigger')
    sql_statements.InsertIntoMqTrigger(cursor, dictionaries.createMqTriggerDict(mqConfig_id, mqtrigger))
    rows_created += cursor.rowcount

    # IPQueue
    for ipqueue in mq.findall('IPQueue'):
        sql_statements.InsertIntoIPQueue(cursor, dictionaries.createIPQueueDict(mqConfig_id, ipqueue))
        rows_created += cursor.rowcount

    # Communication
    for communication in acsfiletransfer.findall('communication'):
        communication_id = sql_statements.InsertIntoCommunication(cursor,
                                                                   dictionaries.createCommunicationDict(basicConfig_id,
                                                                                                         communication)).lastrowid
        rows_created += cursor.rowcount

        for communicationElement in communication.findall('./*'):
            match communicationElement.tag:
                case 'sourceLocation' | 'targetLocation':
                    sql_statements.InsertIntoLocation(cursor, dictionaries.createLocationDict(communication_id, communicationElement, communicationElement.tag))
                    rows_created += cursor.rowcount

                case 'preCommand' | 'postCommand':
                    command_id = sql_statements.InsertIntoCommand(cursor, dictionaries.createCommandDict(communication_id, communicationElement, communicationElement.tag)).lastrowid
                    rows_created += cursor.rowcount

                    for commandparam in communicationElement.findall('param'):
                        param = commandparam.text if commandparam.text is not None else ''
                        if param != '':
                            sql_statements.InsertIntoCommandParam(cursor, dictionaries.createCommandParamDict(command_id, param))
                            rows_created += cursor.rowcount

                case 'alternateNameList' if communicationElement.tag is not None:
                    namelist = acsfiletransfer.find(f".//nameList[@name='{communicationElement.text}']")
                    if namelist is not None:
                        for entry in namelist.findall('entry'):
                            if entry.text is not None:
                                sql_statements.InsertIntoAlternateNameList(cursor, dictionaries.createAlternateNameListDict(communication_id, namelist.get('name', ''), entry.text))
                                rows_created += cursor.rowcount

    conn.commit()
    conn.close()
