from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QApplication

from database.utils import get_communications, get_locations, get_descriptions, get_basic_configs, get_lzb_configs, \
    get_mq_configs, get_mq_trigger, get_ip_queue, get_namelist, get_alternatenames


class SearchResultsWindow(QWidget):
    communication_selected = pyqtSignal(int)

    def __init__(self, results, search_query):
        super().__init__()
        self.setWindowTitle("Search Results")
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(QIcon('gui/icon/search.svg'))
        layout = QVBoxLayout()
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(["Found", "Name", "Source"])
        self.results_tree.setColumnWidth(0, 250)
        self.results_tree.setColumnWidth(1, 200)
        self.results_tree.setColumnWidth(2, 200)
        layout.addWidget(self.results_tree)
        self.setLayout(layout)
        self.populate_results(results, search_query)
        self.center_window()
        self.results_tree.itemClicked.connect(self.on_item_clicked)

    def populate_results(self, results, search_query):
        for result in results:
            if 'table_name' in result.keys():
                name = result['table_name']
            else:
                name = result['communication_name'] if 'communication_name' in result.keys() else 'Unknown'
            source = result['source'] if 'source' in result.keys() else 'Unknown'
            item = QTreeWidgetItem([search_query, name, source])
            communication_id = result['communication_id'] if 'communication_id' in result.keys() else result['id']
            item.setData(0, Qt.UserRole, communication_id)
            self.results_tree.addTopLevelItem(item)

    def center_window(self):
        screen_geometry = QApplication.primaryScreen().availableGeometry()
        window_geometry = self.frameGeometry()
        center_point = screen_geometry.center()
        window_geometry.moveCenter(center_point)
        self.move(window_geometry.topLeft())

    def on_item_clicked(self, item):
        communication_id = item.data(0, Qt.UserRole)
        self.communication_selected.emit(communication_id)

def filter_communications(conn_manager, config_manager, text):
    conn = conn_manager.get_db_connection()
    rows = get_communications(conn, config_manager.config_id, text)
    conn.close()
    return rows

def filter_locations(conn_manager, text):
    conn = conn_manager.get_db_connection()
    rows = get_locations(conn, text)
    conn.close()
    return rows

def filter_descriptions(conn_manager, text):
    conn = conn_manager.get_db_connection()
    rows = get_descriptions(conn, text)
    conn.close()
    return rows

def filter_basic_configs(conn_manager, text):
    conn = conn_manager.get_db_connection()
    rows = get_basic_configs(conn, text)
    conn.close()
    return rows

def filter_lzb_configs(conn_manager, text):
    conn = conn_manager.get_db_connection()
    rows = get_lzb_configs(conn, text)
    conn.close()
    return rows

def filter_mq_configs(conn_manager, text):
    conn = conn_manager.get_db_connection()
    rows = get_mq_configs(conn, text)
    conn.close()
    return rows

def filter_mq_trigger(conn_manager, text):
    conn = conn_manager.get_db_connection()
    rows = get_mq_trigger(conn, text)
    conn.close()
    return rows

def filter_ip_queue(conn_manager, text):
    conn = conn_manager.get_db_connection()
    rows = get_ip_queue(conn, text)
    conn.close()
    return rows

def filter_namelists(conn_manager, text):
    conn = conn_manager.get_db_connection()
    namelist_rows = get_namelist(conn, text)
    alternatename_rows = get_alternatenames(conn, text)
    rows = namelist_rows + alternatename_rows
    return rows