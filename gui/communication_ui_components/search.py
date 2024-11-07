from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QApplication, QMessageBox

from common.resource_manager import ResourceManager
from database.utils import get_communications, get_locations, get_descriptions, get_basic_configs, get_lzb_configs, \
    get_mq_configs, get_mq_trigger, get_ip_queue, get_namelist, get_alternatenames, get_command, get_command_param


class SearchResultsWindow(QWidget):
    communication_selected = pyqtSignal(int)

    def __init__(self, results, search_query):
        super().__init__()
        self.resource_manager = ResourceManager()
        self.setWindowTitle("Search Results")
        self.setGeometry(100, 100, 800, 400)
        search_icon =  self.resource_manager.get_resource_path('gui/icon/search.svg')
        self.setWindowIcon(QIcon(search_icon))
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


class Search:
    def __init__(self, conn_manager, config_manager):
        self.conn_manager = conn_manager
        self.config_manager = config_manager
        self.conn = self.conn_manager.get_db_connection()
        self.cursor = self.conn.cursor()

    def search(self, text):
        communication_results = filter_communications(self.cursor, self.config_manager, text)
        location_results = filter_locations(self.cursor, text)
        description_results = filter_descriptions(self.cursor, text)
        basic_config_results = filter_basic_configs(self.cursor, text)
        lzb_config_results = filter_lzb_configs(self.cursor, text)
        mq_config_results = filter_mq_configs(self.cursor, text)
        mq_trigger_results = filter_mq_trigger(self.cursor, text)
        ip_queue_results = filter_ip_queue(self.cursor, text)
        namelist_results = filter_namelists(self.cursor, text)
        command_results = filter_command(self.cursor, text)
        results = (communication_results + location_results + description_results + basic_config_results +
                   lzb_config_results + mq_config_results + mq_trigger_results + ip_queue_results +
                   namelist_results + command_results)
        return results

    def create_result_window(self, main_window, results, text):
        if not results:
            QMessageBox.information(main_window, "No Results", "No search results found.")
        else:
            main_window.results_window = SearchResultsWindow(results, text)
            main_window.results_window.communication_selected.connect(
                lambda communication_id: self.navigate_to_communication(main_window, communication_id))
            main_window.results_window.show()

    def on_search(self, main_window):
        text = main_window.search_field.text().strip()
        if text:
            results = self.search(text)
            self.create_result_window(main_window, results, text)

    @staticmethod
    def navigate_to_communication(main_window, communication_id):
        tree_widget = main_window.left_widget.layout().itemAt(0).widget()
        for i in range(main_window.communication_config_item.childCount()):
            child_item = main_window.communication_config_item.child(i)
            if child_item.data(0, Qt.UserRole) == communication_id:
                tree_widget.setCurrentItem(child_item)
                main_window.on_item_clicked(child_item)
                main_window.results_window.close()
                break


def filter_communications(cursor, config_manager, text):
    cursor = get_communications(cursor, config_manager.config_id, text)
    rows = cursor.fetchall()
    return rows


def filter_locations(cursor, text):
    cursor = get_locations(cursor, text)
    rows = cursor.fetchall()
    return rows


def filter_descriptions(cursor, text):
    cursor = get_descriptions(cursor, text)
    rows = cursor.fetchall()
    return rows


def filter_basic_configs(cursor, text):
    cursor = get_basic_configs(cursor, text)
    rows = cursor.fetchall()
    return rows


def filter_lzb_configs(cursor, text):
    cursor = get_lzb_configs(cursor, text)
    rows = cursor.fetchall()
    return rows


def filter_mq_configs(cursor, text):
    cursor = get_mq_configs(cursor, text)
    rows = cursor.fetchall()
    return rows


def filter_mq_trigger(cursor, text):
    cursor = get_mq_trigger(cursor, text)
    rows = cursor.fetchall()
    return rows


def filter_ip_queue(cursor, text):
    cursor = get_ip_queue(cursor, text)
    rows = cursor.fetchall()
    return rows


def filter_namelists(cursor, text):
    namelist_cursor = get_namelist(cursor, text)
    alternatename_cursor = get_alternatenames(cursor, text)
    rows = namelist_cursor.fetchall() + alternatename_cursor.fetchall()
    return rows


def filter_command(cursor, text):
    command_cursor = get_command(cursor, text)
    command_rows = command_cursor.fetchall()

    command_param_cursor = get_command_param(cursor, text)
    command_param_rows = command_param_cursor.fetchall()

    rows = command_rows + command_param_rows
    return rows
