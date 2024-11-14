from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem, QApplication, QMessageBox

from common.resource_manager import ResourceManager
from database.utils import get_communications, get_locations, get_descriptions, get_basic_configs, get_lzb_configs, \
    get_mq_configs, get_mq_trigger, get_ip_queue, get_namelist, get_alternatenames, get_command, get_command_param
from common.connection_manager import ConnectionManager
from common.config_manager import ConfigManager
from gui.common_components.icons import search_icon


class SearchResultsWindow(QWidget):
    communication_selected = pyqtSignal(int)

    def __init__(self, results, search_query):
        super().__init__()
        self.resource_manager = ResourceManager()
        self.setWindowTitle("Search Results")
        self.setGeometry(100, 100, 800, 400)
        self.setWindowIcon(search_icon)
        layout = QVBoxLayout()
        self.results_tree = QTreeWidget()
        self.results_tree.setHeaderLabels(["Found", "Configuration", "Source", "Name"])
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
            name = result['table_name'] if 'table_name' in result.keys() else 'Unknown'
            source = result['source'] if 'source' in result.keys() else 'Unknown'
            communication_name = result['communication_name'] if 'communication_id' in result.keys() else ''
            item = QTreeWidgetItem([search_query, name, source, communication_name])
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
    def __init__(self):
        self.conn_manager = ConnectionManager()
        self.config_manager = ConfigManager()

    def search(self, text):
        conn = None
        try:
            conn = self.conn_manager.get_db_connection()
            cursor = conn.cursor()

            communication_results = get_communications(cursor, self.config_manager.config_id, text).fetchall()
            location_results = get_locations(cursor, text).fetchall()
            description_results = get_descriptions(cursor, text).fetchall()
            basic_config_results = get_basic_configs(cursor, text).fetchall()
            lzb_config_results = get_lzb_configs(cursor, text).fetchall()
            mq_config_results = get_mq_configs(cursor, text).fetchall()
            mq_trigger_results = get_mq_trigger(cursor, text).fetchall()
            ip_queue_results = get_ip_queue(cursor, text).fetchall()
            namelist_results = get_namelist(cursor, text).fetchall() + get_alternatenames(cursor, text).fetchall()
            command_results = get_command(cursor, text).fetchall() + get_command_param(cursor, text).fetchall()
            results = (communication_results + location_results + description_results + basic_config_results +
                       lzb_config_results + mq_config_results + mq_trigger_results + ip_queue_results +
                       namelist_results + command_results)
            return results
        except Exception as e:
            QMessageBox.critical(None, "Search Error", f"An error occurred during the search: {str(e)}")
            return []
        finally:
            if conn:
                conn.close()

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
