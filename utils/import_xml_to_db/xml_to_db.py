from lxml import etree
import sqlite3
import os
from common.connection_manager import ConnectionManager
import database.utils as utils
import utils.import_xml_to_db.dictionaries as dictionaries

# DB file path
db_path = os.path.join(os.path.dirname(__file__), 'database.db')

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
    return utils.insert_into_basicconfig(cursor,
                                                dictionaries.createBasicConfigDict(acsfiletransfer, config_file_path))

# Lzb
def insert_lzb_config(cursor, basicConfig_id, lzb):
    return utils.insert_into_lzbconfig(cursor, dictionaries.createLzbConfigDict(basicConfig_id, lzb))

# Mq
def insert_mq_config(cursor, basicConfig_id, mq):
    return utils.insert_into_mqconfig(cursor, dictionaries.createMqConfigDict(basicConfig_id, mq))

# MqTrigger
def insert_mq_trigger(cursor, basicConfig_id, mqConfig_id, mqtrigger):
    return utils.insert_into_mqtrigger(cursor, dictionaries.createMqTriggerDict(basicConfig_id, mqConfig_id, mqtrigger))

# IPQueue
def insert_ip_queue(cursor,basicConfig_id,  mqConfig_id, ipqueue):
    return utils.insert_into_ipqueue(cursor, dictionaries.createIPQueueDict(basicConfig_id, mqConfig_id, ipqueue))

# Communication
def insert_communication(cursor, basicConfig_id, communication):
    return utils.insert_into_communication(cursor, dictionaries.createCommunicationDict(basicConfig_id,
                                                                                               communication))
# Location
def insert_location(cursor, communication_id, location, locationType):
    return utils.insert_into_location(cursor, dictionaries.createLocationDict(communication_id, location,
                                                                                     locationType))
# Command
def insert_command(cursor, communication_id, command, commandType):
    return utils.InsertIntoCommand(cursor, dictionaries.createCommandDict(communication_id, command,
                                                                                   commandType))
# CommandParam
def insert_command_param(cursor, command_id, param):
    return utils.InsertIntoCommandParam(cursor, dictionaries.createCommandParamDict(command_id, param))
# CommandParam

def insert_name_list(cursor, basicConfig_id, communication_id, listName):
    return utils.insert_into_namelist(cursor, dictionaries.createNameListDict(basicConfig_id, communication_id, listName))

# NameList
def insert_alternate_name(cursor, nameList_id, entry):
    return utils.insert_into_alternatename(cursor, dictionaries.createAlternateNameDict(nameList_id, entry))

# Description
def insert_description(cursor, communication_id, description, descriptionType):
    return utils.insert_into_description(cursor, dictionaries.createDescriptionDict(communication_id, description, descriptionType))

# Insert data into the database
def insert_data_into_db(xml_tree, config_file_path):
    """
    Insert data from the parsed XML tree into the SQLite database.

    :param xml_tree: Parsed XML tree
    :param config_file_path: Path of the configuration file
    """
    conn_manager = ConnectionManager().get_instance()
    conn = conn_manager.get_db_connection()
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
        insert_mq_trigger(cursor, basicConfig_id, mqConfig_id, mqtrigger)
        rows_created += cursor.rowcount

        for ipqueue in mq.findall('IPQueue'):
            insert_ip_queue(cursor, basicConfig_id, mqConfig_id, ipqueue)
            rows_created += cursor.rowcount

        for communication in acsfiletransfer.findall('communication'):
            communication_id = insert_communication(cursor, basicConfig_id, communication).lastrowid
            rows_created += cursor.rowcount

            for communicationElement in communication.findall('./*'):
                if communicationElement.tag in ['description', 'description1', 'description2', 'description3', 'description4', 'description5', 'description6']:
                    insert_description(cursor, communication_id, communicationElement, communicationElement.tag)
                    rows_created += cursor.rowcount
                
                elif communicationElement.tag in ['sourceLocation', 'targetLocation']:
                    insert_location(cursor, communication_id, communicationElement, communicationElement.tag)
                    rows_created += cursor.rowcount

                elif communicationElement.tag in ['preCommand', 'postCommand']:
                    command_id = insert_command(cursor, communication_id, communicationElement, communicationElement.tag).lastrowid
                    rows_created += cursor.rowcount

                    for commandparam in communicationElement.findall('param'):
                        param = commandparam.text if commandparam.text is not None else ''
                        if param != '':
                            insert_command_param(cursor, command_id, param)
                            rows_created += cursor.rowcount

                        rows_created += cursor.rowcount

                elif communicationElement.tag == 'alternateNameList' and communicationElement.tag is not None:
                    namelist = acsfiletransfer.find(f".//nameList[@name='{communicationElement.text}']")
                    if namelist is not None:
                        nameList_id = insert_name_list(cursor, basicConfig_id, communication_id, namelist.get('name', '')).lastrowid
                        rows_created += cursor.rowcount
                        for entry in namelist.findall('entry'):
                            if entry.text is not None:
                                insert_alternate_name(cursor, nameList_id, entry.text)
                                rows_created += cursor.rowcount

        # Save the changes to the database
        conn.commit()
        return basicConfig_id

    except Exception as e:
        conn.rollback()
        raise e

    finally:
        conn.close()
