
from lxml import etree
import sqlite3
import os
import sql_statements
import dictionaries


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

def print_xml(xml_tree):
    """
    Print the XML content in a formatted way.

    :param xml_tree: Parsed XML tree
    """
    # Convert the XML tree to a pretty-formatted string
    xml_str = etree.tostring(xml_tree, pretty_print=True, encoding='unicode')
    print("\n--- XML Content ---")
    print(xml_str)

def importBasicConfig(cursor, acsfiletransfer):
    return sql_statements.InsertIntoBasicConfig(cursor, dictionaries.createBasicConfigDict(acsfiletransfer, xml_name)).lastrowid

def importLzbConfig(cursor, basicConfig_id, lzb):
    return sql_statements.InsertIntoLzbConfig(cursor, dictionaries.createLzbConfigDict(basicConfig_id, lzb)).lastrowid

def importMqConfig(cursor, basicConfig_id, mq):
    return sql_statements.InsertIntoMqConfig(cursor, dictionaries.createMqConfigDict(basicConfig_id, mq)).lastrowid

def importMqTrigger(cursor, mqConfig_id, mqtrigger):
    return sql_statements.InsertIntoMqTrigger(cursor, dictionaries.createMqTriggerDict(mqConfig_id, mqtrigger)).lastrowid

def importIPQueue(cursor, mqConfig_id, ipqueue):
    return sql_statements.InsertIntoIPQueue(cursor, dictionaries.createIPQueueDict(mqConfig_id, ipqueue)).lastrowid

def importCommunication(cursor, basicConfig_id, communication):
    return sql_statements.InsertIntoCommunication(cursor, dictionaries.createCommunicationDict(basicConfig_id, communication)).lastrowid

def importLocation(cursor, communication_id, location, locationType):
    return sql_statements.InsertIntoLocation(cursor, dictionaries.createLocationDict(communication_id, location, locationType)).lastrowid

def importCommand(cursor, communication_id, command, commandType):
    return sql_statements.InsertIntoCommand(cursor, dictionaries.createCommandDict(communication_id, command, commandType)).lastrowid

def importCommandParam(cursor, command_id, param):
    return sql_statements.InsertIntoCommandParam(cursor, dictionaries.createCommandParamDict(command_id, param)).lastrowid

def importAlternateNameList(cursor, communication_id, listName, alternateName):
    return sql_statements.InsertIntoAlternateNameList(cursor, dictionaries.createAlternateNameListDict(communication_id, listName, alternateName)).lastrowid

def insert_data_into_db(xml_tree, db_path):
    """
    Insert data from the parsed XML tree into the SQLite database.

    :param xml_tree: Parsed XML tree
    :param db_path: Path to the SQLite database
    """
    # Check if the database file exists
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"The specified database file was not found: {db_path}")

    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    rows_created = 0

    root = xml_tree.getroot()

    # Adjust the XPath based on your XML structure
    acsfiletransfer = root.find('.//acsfiletransfer')

    # BasicConfig
    basicConfig_id = importBasicConfig(cursor, acsfiletransfer)
    rows_created = rows_created + cursor.rowcount

    # LzbConfig
    lzb = acsfiletransfer.find('lzb')
    importLzbConfig(cursor, basicConfig_id, lzb)
    rows_created = rows_created + cursor.rowcount

    # MqConfig
    mq = acsfiletransfer.find('mq')
    mqConfig_id = importMqConfig(cursor, basicConfig_id, mq)
    rows_created = rows_created + cursor.rowcount

    # MqTrigger
    mqtrigger = mq.find('trigger')
    importMqTrigger(cursor, mqConfig_id, mqtrigger)
    rows_created = rows_created + cursor.rowcount

    # IPQueue
    for ipqueue in mq.findall('IPQueue'):
        importIPQueue(cursor, mqConfig_id, ipqueue)
        rows_created = rows_created + cursor.rowcount

    # Communication
    for communication in acsfiletransfer.findall('communication'):
        communication_id = importCommunication(cursor, basicConfig_id, communication)
        rows_created = rows_created + cursor.rowcount

        for communicationElement in communication.findall('./*'):            
            match communicationElement.tag:
                case 'sourceLocation' | 'targetLocation':
                    importLocation(cursor, communication_id, communicationElement, communicationElement.tag)
                    rows_created += cursor.rowcount
                    
                case 'preCommand' | 'postCommand':
                    command_id = importCommand(cursor, communication_id, communicationElement, communicationElement.tag)
                    rows_created += cursor.rowcount
                    
                    for commandparam in communicationElement.findall('param'):
                        param = commandparam.text if commandparam.text is not None else ''
                        if param != '':
                            importCommandParam(cursor, command_id, param)
                            rows_created += cursor.rowcount

                case 'alternateNameList' if communicationElement.tag is not None:
                    namelist = acsfiletransfer.find(f".//nameList[@name='{communicationElement.text}']")
                    
                    if namelist is not None:
                        for entry in namelist.findall('entry'):
                            if entry.text is not None:
                                importAlternateNameList(cursor, communication_id, namelist.get('name', ''), entry.text)
                                rows_created += cursor.rowcount

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()
    print(f"Data has been inserted into the database. New rows: {rows_created}")

# Replace these paths with your actual file paths
#xml_path = r"C:/Users/../acsfiletransfer.xml.e"
xml_path = input("Please enter the full 'acsfiletransfer.xml' XML file path: ")
xml_name = os.path.basename(xml_path)
print(f"The XML file name is: {xml_name}")

#xsd_path = r"C:/Users/../acsfiletransfer.xsd"
xsd_path = input("Please enter the full 'acsfiletransfer.xsd' XSD file path: ")
xsd_name = os.path.basename(xsd_path)
print(f"The XSD file name is: {xsd_name}")

#db_path = r"C:/Users/../acsfiletransfer.db"
db_path = input("Please enter the full 'acsfiletransfer.db' DB file path: ")
db_name = os.path.basename(db_path)
print(f"The DB file name is: {db_name}")

# Validate, print, and insert data
try:

    xml_tree = validate_xml(xml_path, xsd_path)
    #print_xml(xml_tree)
    insert_data_into_db(xml_tree, db_path)
except Exception as e:
    print(f"An error occurred: {e}")
