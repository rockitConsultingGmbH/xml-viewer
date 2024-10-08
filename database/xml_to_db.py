from lxml import etree
import sqlite3
import os
import database.sql_statements as sql_statements
import database.dictionaries as dictionaries

# DB file path
db_path = os.path.join(os.path.dirname(__file__), 'database.db')


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

    # Validate the XML file against the XSD schema
    if not xsd_schema.validate(xml_tree):
        raise ValueError(f"XML file {xml_path} is invalid:\n{xsd_schema.error_log}")

    print(f"XML file {xml_path} is valid.")
    return xml_tree

# BasicConfiguration
def insert_basic_config(cursor, acsfiletransfer, config_file_path):
    return sql_statements.InsertIntoBasicConfig(cursor,
                                                dictionaries.createBasicConfigDict(acsfiletransfer, config_file_path))

# Lzb
def insert_lzb_config(cursor, basicConfig_id, lzb):
    return sql_statements.InsertIntoLzbConfig(cursor, dictionaries.createLzbConfigDict(basicConfig_id, lzb))

# Mq
def insert_mq_config(cursor, basicConfig_id, mq):
    return sql_statements.InsertIntoMqConfig(cursor, dictionaries.createMqConfigDict(basicConfig_id, mq))

# MqTrigger
def insert_mq_trigger(cursor, mqConfig_id, mqtrigger):
    return sql_statements.InsertIntoMqTrigger(cursor, dictionaries.createMqTriggerDict(mqConfig_id, mqtrigger))

# IPQueue
def insert_ip_queue(cursor, mqConfig_id, ipqueue):
    return sql_statements.InsertIntoIPQueue(cursor, dictionaries.createIPQueueDict(mqConfig_id, ipqueue))

# Communication
def insert_communication(cursor, basicConfig_id, communication):
    return sql_statements.InsertIntoCommunication(cursor, dictionaries.createCommunicationDict(basicConfig_id,
                                                                                               communication))
# Location
def insert_location(cursor, communication_id, location, locationType):
    return sql_statements.InsertIntoLocation(cursor, dictionaries.createLocationDict(communication_id, location,
                                                                                     locationType))
# Command
def insert_command(cursor, communication_id, command, commandType):
    return sql_statements.InsertIntoCommand(cursor, dictionaries.createCommandDict(communication_id, command,
                                                                                   commandType))
# CommandParam
def insert_command_param(cursor, command_id, param):
    return sql_statements.InsertIntoCommandParam(cursor, dictionaries.createCommandParamDict(command_id, param))
# CommandParam

def insert_name_list(cursor, basicConfig_id, communication_id, listName):
    return sql_statements.InsertIntoNameList(cursor, dictionaries.createNameListDict(basicConfig_id, communication_id, listName))

# NameList
def insert_alternate_name(cursor, nameList_id, alternateName):
    return sql_statements.InsertIntoAlternateName(cursor, dictionaries.createAlternateNameDict(nameList_id, alternateName))

# Description
def insert_description(cursor, communication_id, description, descriptionType):
    return sql_statements.InsertIntoDescription(cursor, dictionaries.createDescriptionDict(communication_id, description, descriptionType))

# Insert data into the database
def insert_data_into_db(xml_tree, config_file_path):
    """
    Insert data from the parsed XML tree into the SQLite database.

    :param xml_tree: Parsed XML tree
    :param config_file_path: Path of the configuration file
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    rows_created = 0

    try:
        root = xml_tree.getroot()
        acsfiletransfer = root.find('.//acsfiletransfer')

        basicConfig_id = insert_basic_config(cursor, acsfiletransfer, config_file_path).lastrowid
        rows_created += cursor.rowcount

        lzb = acsfiletransfer.find('lzb')
        insert_lzb_config(cursor, basicConfig_id, lzb)
        rows_created += cursor.rowcount

        mq = acsfiletransfer.find('mq')
        mqConfig_id = insert_mq_config(cursor, basicConfig_id, mq).lastrowid
        rows_created += cursor.rowcount

        mqtrigger = mq.find('trigger')
        insert_mq_trigger(cursor, mqConfig_id, mqtrigger)
        rows_created += cursor.rowcount

        for ipqueue in mq.findall('IPQueue'):
            insert_ip_queue(cursor, mqConfig_id, ipqueue)
            rows_created += cursor.rowcount

        for communication in acsfiletransfer.findall('communication'):
            communication_id = insert_communication(cursor, basicConfig_id, communication).lastrowid
            rows_created += cursor.rowcount

            for communicationElement in communication.findall('./*'):
                if communicationElement.tag in ['description', 'description1', 'description2', 'description3', 'description4', 'description5', 'description6']:
                    #insert_description(cursor, communication_id, communicationElement, communicationElement.tag)
                    rows_created += cursor.rowcount
                
                elif communicationElement.tag in ['sourceLocation', 'targetLocation']:
                    #insert_location(cursor, communication_id, communicationElement, communicationElement.tag)
                    rows_created += cursor.rowcount

                elif communicationElement.tag in ['preCommand', 'postCommand']:
                    #command_id = insert_command(cursor, communication_id, communicationElement, communicationElement.tag).lastrowid
                    rows_created += cursor.rowcount

                    for commandparam in communicationElement.findall('param'):
                        param = commandparam.text if commandparam.text is not None else ''
                        if param != '':
                           # insert_command_param(cursor, command_id, param)
                            rows_created += cursor.rowcount

                        rows_created += cursor.rowcount

                elif communicationElement.tag == 'alternateNameList' and communicationElement.tag is not None:
                    namelist = acsfiletransfer.find(f".//nameList[@name='{communicationElement.text}']")
                    if namelist is not None:
                        #nameList_id = insert_name_list(cursor, basicConfig_id, communication_id, namelist.get('name', '')).lastrowid
                        rows_created += cursor.rowcount
                        for entry in namelist.findall('entry'):
                            if entry.text is not None:
                                #insert_alternate_name(cursor, nameList_id, entry.text)
                                rows_created += cursor.rowcount

        # Save the changes to the database
        conn.commit()
        return basicConfig_id

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()
