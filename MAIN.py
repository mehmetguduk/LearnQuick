# © Designed and Developed by Mehmet Güdük.
# © Licensed with GPL-3.0 License, Author is Mehmet Güdük.



import re
import sys
import random
from datetime import datetime 
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QInputDialog
from PyQt5.QtCore import QTimer, QDate
from interface import Ui_MainWindow
from database_functions import *
from default_deck import *

class myApp(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # We are connecting to the necessary databases here.
        DATABASE_CONNECT()
        DATABASE_CONNECT_for_logs()

        "__________CREATING_DEFAULT_DECK__________"
        """This section includes commands that creates a default deck for first start."""
        if DATABASE_user_deleted_default_tool() != "DELETED" and DATABASE_is_default_created() != True:
            DATABASE_create_deck("German Top200 Words (Default Deck)")
            for item in default_list:
                card = item.split("-")
                DATABASE_inserting_default_list(card[0], card[1])
        
        "__________STARTING_WITH_APP__________"
        """This section includes commands that should start with application."""
        self.ui.tableCards.horizontalHeader().setSectionResizeMode(1)
        
        self.ui.tableWidget_creation_card_list.horizontalHeader().setSectionResizeMode(1)
        self.ui.tableWidget_creation_card_list.setHorizontalHeaderLabels(["Front","Back"])
        self.ui.tableWidget_for_total_studied.horizontalHeader().setSectionResizeMode(1)
        self.ui.tableWidget_for_total_studied.setHorizontalHeaderLabels(["Total studied time"])
        self.ui.tableWidget_for_last_studied.horizontalHeader().setSectionResizeMode(1)
        self.ui.tableWidget_for_last_studied.setHorizontalHeaderLabels(["Last studied time"])
        self.ui.tableWidget_for_records.horizontalHeader().setSectionResizeMode(1)
        self.ui.tableWidget_for_records.setHorizontalHeaderLabels(["Deck name","Studied time"])
        self.update_deck_list()
        self.ui.label_4.setOpenExternalLinks(True)
        self.ui.label_6.setOpenExternalLinks(True)
        self.stopwatch_for_study()
        self.setting_current_time_to_datetime_edit()
        self.ui.label_3.setHidden(1)

        "__________SIGNALS__________"
        """This section includes signals that program will use."""
        self.ui.btnCreateDeck.clicked.connect(self.create_new_deck)
        self.ui.btnRenameDeck.clicked.connect(self.rename_deck)
        self.ui.btnDeleteDeck.clicked.connect(self.delete_deck)
        self.ui.btnSortDecks.clicked.connect(self.sort_deck_names)
        self.ui.btnDeleteCard.clicked.connect(self.delete_card_from_list_and_database)
        self.ui.btnCreateCard.clicked.connect(self.changing_page_to_card_creation)
        self.ui.btn_creation_clear.clicked.connect(self.clear_text_edits)
        self.ui.btn_add_the_card_below.clicked.connect(self.add_the_card_below)
        self.ui.btn_creation_remove_card.clicked.connect(self.remove_selected_card_from_list)
        self.ui.btn_creation_cancel.clicked.connect(self.cancel_without_saving_card_list)
        self.ui.btn_creation_add_all_to_the_deck.clicked.connect(self.add_cards_to_database)
        self.ui.btn_start_study.clicked.connect(self.show_card_for_study)
        self.ui.btnRed.clicked.connect(self.red_clicked)
        self.ui.btnOrange.clicked.connect(self.orange_clicked)
        self.ui.btnYellow.clicked.connect(self.yellow_clicked)
        self.ui.btnGreen.clicked.connect(self.green_clicked)
        self.ui.btnBlue.clicked.connect(self.blue_clicked)
        self.ui.btnShow.clicked.connect(self.show_back)
        self.ui.btn_homepage_deckcars.clicked.connect(self.tool_bar_deckandcard)
        self.ui.btn_homepage_study.clicked.connect(self.tool_bar_study)
        self.ui.btn_stop_studying.clicked.connect(self.stop_button_worked)
        self.ui.btn_start_study.clicked.connect(self.start_button_worked)
        self.ui.btnSortDecks_2.clicked.connect(self.sorting_combobox_for_statistics)
        self.ui.btn_clear_day.clicked.connect(self.clearday_worked_for_logs)
        self.ui.btn_log_record.clicked.connect(self.remove_log_worked_for_logs)
        self.ui.comboBox_for_statistic.currentIndexChanged.connect(self.when_user_select_a_deck_from_combobox_statistic)
        self.ui.comboBox_deck_select.currentTextChanged.connect(self.clear_labels_when_deckname_change)
        self.ui.listDeck.clicked.connect(self.update_card_table)
        self.ui.tableCards.itemDoubleClicked.connect(self.edit_card_by_list_tool)
        self.ui.tableCards.itemChanged.connect(self.edit_card_by_list)
        self.ui.tableWidget_creation_card_list.itemDoubleClicked.connect(self.space_character_blocker_tool)
        self.ui.tableWidget_creation_card_list.itemChanged.connect(self.space_character_blocker)
        self.ui.dateTimeEdit_for_statistics.dateChanged.connect(self.datetime_input_catches)
        self.ui.tableWidget_for_records.clicked.connect(self.selecting_log_from_tablewidget)

        "__________TOOLBAR_AND_ACTIONS__________"
        """This section includes commands that work with toolbar."""
        self.ui.actionHomePage.triggered.connect(self.tool_bar_homepage)
        self.ui.actionDeckandCard.triggered.connect(self.tool_bar_deckandcard)
        self.ui.actionStudy.triggered.connect(self.tool_bar_study)
        self.ui.actionStatistics.triggered.connect(self.tool_bar_statistics)
        


    ############################################################################################################################################
    # This method includes commands that must run before the program closes.
    # Asks the users if they really wants to close application.
    # If user's answer is 'Yes' it stops studying and database connections.
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'LearnQuick', 'Are you sure you want to close LearnQuick?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes: 
            self.stop_button_worked()
            DATABASE_DISCONNECT()
            DATABASE_DISCONNECT_for_logs()
            event.accept()
        else: 
            event.ignore()
    ############################################################################################################################################



    "_______________________________________________________________HOME PAGE__________________________________________________________________"
    """This section includes commands to use on Homepage"""

    ############################################################################################################################################
    # This method catches a signal if user click 'Home' section from toolbar.
    # The main goal of this method is that, changing current page to 'Homepage'.
    def tool_bar_homepage(self): 
        self.stop_button_worked()
        self.ui.stackedWidget_MainApp.setCurrentIndex(0)
    ############################################################################################################################################



    "__________________________________________________________DECK AND CARDS PAGE_____________________________________________________________"
    """This section includes commands to use on Deck and Cards"""

    ############################################################################################################################################
    # This method catches a signal if user click 'Deck and Cards' section from toolbar.
    # The main goal of this method is that, changing current page to 'Deck and Cards'.
    def tool_bar_deckandcard(self): 
        self.stop_button_worked()
        self.ui.stackedWidget_MainApp.setCurrentIndex(1)
        self.ui.label_shows_card_back.clear()
        self.ui.label_shows_card_front.clear()
    ############################################################################################################################################


    ############################################################################################################################################
    # This method catches a signal if user click 'Create Deck' button.
    # The main goal of this method is that, creating new deck with a deckname input from user.
    def create_new_deck(self):
        if(re.compile('[@_!#$%^&*()<>?/\|}{~:]').search(self.ui.typeDeckName.text()) == None):
            if self.ui.typeDeckName.text() == "" or self.ui.typeDeckName.text().startswith(" "):
                QMessageBox.warning(self, "Invalid Deck Name", "Deck name can't be empty and can't start with space character.", QMessageBox.Ok)
            elif self.ui.typeDeckName.text() in table_list:
                label = "{} is already exists.".format(self.ui.typeDeckName.text())
                QMessageBox.warning(self, "Invalid Deck Name", label, QMessageBox.Ok)
            elif self.ui.typeDeckName.text()[0].isdigit() == True:
                QMessageBox.warning(self, "Invalid Deck Name", "Deck name can't start with number", QMessageBox.Ok)
            else:
                DATABASE_create_deck(self.ui.typeDeckName.text())
                self.update_deck_list()           
        else:
            QMessageBox.warning(self, "Invalid Deck Name", "Deck name cannot contain special characters.", QMessageBox.Ok)
    ############################################################################################################################################
    # This method catches a signal if user click 'Rename Deck' button.
    # The main goal of this method is that, changing deck's name with a deckname input from user.
    def rename_deck(self): 
        if self.ui.typeDeckName.text() == "":
            QMessageBox.warning(self, "Invalid Value", "Please select or type the name of the deck.", QMessageBox.Ok)
        elif self.ui.typeDeckName.text() not in table_list:
            label = "There is no deck named {}".format(self.ui.typeDeckName.text())
            QMessageBox.warning(self, "Invalid Deck Name", label, QMessageBox.Ok)
        else:
            new_deckname, ok = QInputDialog.getText(self, "Edit Deck", "New Deck Name")
            if new_deckname in table_list:
                label = "{} is already exists.".format(new_deckname)
                QMessageBox.warning(self, "Invalid Deck Name", label, QMessageBox.Ok)
            elif new_deckname.startswith(" ") or new_deckname == "":
                QMessageBox.warning(self, "Invalid Deck Name", "New deck name can't be empty and can't start with space character.", QMessageBox.Ok)
            elif (re.compile('[@_!#$%^&*()<>?/\|}{~:]').search(new_deckname) != None):
                QMessageBox.warning(self, "Invalid Deck Name", "New deck name cannot contain special characters.", QMessageBox.Ok)
            elif new_deckname[0].isdigit() == True:
                QMessageBox.warning(self, "Invalid Deck Name", "New deck name can't start with number", QMessageBox.Ok)
            else:
                if self.ui.typeDeckName.text() == "German Top200 Words (Default Deck)":
                    DATABASE_user_deleted_default()
                DATABASE_rename_deck(self.ui.typeDeckName.text(), new_deckname)
                DATABASE_change_decknames_from_db(self.ui.typeDeckName.text(), new_deckname)
                self.datetime_input_catches()
                self.update_deck_list()
    ############################################################################################################################################
    # This method catches a signal if user click 'Delete Deck' button.
    # The main goal of this method is that, deleting deck.
    def delete_deck(self):
        if self.ui.typeDeckName.text() == "":
            QMessageBox.warning(self, "Invalid Value", "Please select or type the name of the deck.", QMessageBox.Ok)
        elif self.ui.typeDeckName.text() not in table_list:
            label = "There is no deck named {}".format(self.ui.typeDeckName.text())
            QMessageBox.warning(self, "Invalid Deck Name", label, QMessageBox.Ok)
        else:
            label = "Do you really want to delete {}".format(self.ui.typeDeckName.text())
            question = QMessageBox.question(self,"Delete Deck", label, QMessageBox.Yes | QMessageBox.No)
            if question == QMessageBox.Yes:
                if self.ui.typeDeckName.text() == "German Top200 Words (Default Deck)":
                    DATABASE_user_deleted_default()
                DATABASE_delete_deck(self.ui.typeDeckName.text())
                DATABASE_delete_logs_when_a_deck_deleted(self.ui.typeDeckName.text())
                self.ui.tableCards.clear()
                self.ui.tableCards.setHorizontalHeaderLabels(["Front","Back"])
                self.ui.typeDeckName.clear()
                self.ui.tableCards.setRowCount(0)
                self.datetime_input_catches()
                self.update_deck_list()
    ############################################################################################################################################
    # This method catches a signal if user click 'Sort Decks' button.
    # The main goal of this method is that, sorting decks (items) in QListWidget.
    def sort_deck_names(self):
        self.ui.listDeck.sortItems()
    ############################################################################################################################################
    

    ############################################################################################################################################
    # This method works with other methods.
    # The main goal of this method is that, inserting decknames into QListWidget.
    def update_deck_list(self):
        table_list.clear()
        self.ui.listDeck.clear()
        DATABASE_get_decks()
        for table in table_list:
            if table != "sqlite_sequence":
                self.ui.listDeck.addItem(table)
    ############################################################################################################################################
    # This method catches a signal if user click a deck (item) from QListWidget.
    # The main goal of this method is that, inserting all cards into QTableWidget.
    def update_card_table(self):
        currently_selected_deck_name = self.ui.typeDeckName.text()
        card_list.clear()
        self.ui.tableCards.clear()
        DATABASE_get_cards(currently_selected_deck_name)
        tablerow = 0
        self.ui.tableCards.setRowCount(len(card_list))
        for i in card_list:
            self.ui.tableCards.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(i[1]))
            self.ui.tableCards.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(i[2]))
            tablerow += 1
        self.ui.tableCards.setHorizontalHeaderLabels(["Front","Back"])
    ############################################################################################################################################
    
    
    ############################################################################################################################################
    # This method catches a signal if user click 'Delete Card' button.
    # The main goal of this method is that, deleting selected card from list and database.
    def delete_card_from_list_and_database(self): 
        selected_deckname = self.ui.typeDeckName.text()
        current_row = self.ui.tableCards.currentRow()
        if selected_deckname == "":
            QMessageBox.warning(self, "Card Error", "Please select a deck from deck list.", QMessageBox.Ok)
        elif current_row == -1 and self.ui.tableCards.rowCount() != 0:
            QMessageBox.warning(self, "Card Error", "Please select a card from card list.", QMessageBox.Ok)
        elif current_row == -1 and self.ui.tableCards.rowCount() == 0:
            QMessageBox.warning(self, "Card Error", "There are no cards in the deck that can be deleted.", QMessageBox.Ok)
        else:
            selected_front =  (self.ui.tableCards.item(current_row, 0).text())
            selected_back = (self.ui.tableCards.item(current_row, 1).text())
            DATABASE_delete_card(selected_deckname, selected_front, selected_back)
            self.update_card_table()
    ############################################################################################################################################
    # This method catches a signal if user doubleclick a card (item) in QTableWidget.
    # The main goal of this method is that, saving old front and back sides of card before editing.
    def edit_card_by_list_tool(self):
        try:   
            global current_front
            global current_back
            current_front = (self.ui.tableCards.item(self.ui.tableCards.currentRow(), 0).text())
            current_back = (self.ui.tableCards.item(self.ui.tableCards.currentRow(), 1).text())
        except:
            pass
    ############################################################################################################################################
    # This method catches a signal if user change a card (item) from QTableWidget.
    # The main goal of this method is that, ensuring the changes made by the user are applied to QTableWidget and database.
    def edit_card_by_list(self):
        try:
            deckname = self.ui.typeDeckName.text()
            new_front = (self.ui.tableCards.item(self.ui.tableCards.currentRow(), 0).text()).strip() # değişenin front'i
            new_back = (self.ui.tableCards.item(self.ui.tableCards.currentRow(), 1).text()).strip() # değişenin back'i
            DATABASE_get_fronts_and_backs(deckname)
            x=0
            for front, back in zip(fronts_list, backs_list):
                if front == new_front and back == new_back:
                    label = "Front: {}\nBack: {}\nis already exists.".format(new_front, new_back)
                    QMessageBox.warning(self, "Invalid Card", label, QMessageBox.Ok)
                    self.update_card_table()
                    x=1
                    break
            if x==0:
                if new_front == "":
                    self.update_card_table()
                elif new_back == "":
                    self.update_card_table()
                else:
                    DATABASE_update_card(deckname, current_front, current_back, new_front, new_back)
                    self.update_card_table()
        except:
            pass
    ############################################################################################################################################



    "___________________________________________________________CARD CREATION PAGE_____________________________________________________________"
    """This section includes commands to use on Card Creation Page"""

    ############################################################################################################################################
    # This method catches a signal if user click 'Create Card' button.
    # The main goal of this method is that, changing current page to 'Card Creation Page'.
    def changing_page_to_card_creation(self):
        if self.ui.typeDeckName.text() == "":
            QMessageBox.warning(self, "Invalid Deck Name", "Please select or type the name of the deck.", QMessageBox.Ok)
        elif self.ui.typeDeckName.text() not in table_list:
            label = "There is no deck named {}".format(self.ui.typeDeckName.text())
            QMessageBox.warning(self, "Invalid Deck Name", label, QMessageBox.Ok)
        else:
            label = "{}".format(self.ui.typeDeckName.text())
            self.ui.lbl_title_creation_cardname.setText(label)
            self.ui.tableWidget_creation_card_list.setHorizontalHeaderLabels(["Front","Back"])
            self.ui.stackedWidget_MainApp.setCurrentIndex(3)
    ############################################################################################################################################


    ############################################################################################################################################
    # This method catches a signal if user click 'Clear' button.
    # The main goal of this method is that, clearing labels in card creation page.
    def clear_text_edits(self):
        self.ui.textEdit_creation_back.clear()
        self.ui.textEdit_creation_front.clear()
    ############################################################################################################################################
    # This method catches a signal if user click 'Add the card below' button.
    # The main goal of this method is that, inserting card into QTableWidget as an item.
    def add_the_card_below(self):
        front = self.ui.textEdit_creation_front.toPlainText().strip()
        back = self.ui.textEdit_creation_back.toPlainText().strip()
        value = self.ui.tableWidget_creation_card_list.rowCount()
        self.clear_text_edits()
        if front == "":
            QMessageBox.warning(self, "Invalid Value", "Front can't be empty.", QMessageBox.Ok)
        elif back == "":
            QMessageBox.warning(self, "Invalid Value", "Back can't be empty.", QMessageBox.Ok)
        elif front == "" and back == "":
            QMessageBox.warning(self, "Invalid Value", "Front and Back can't be empty.", QMessageBox.Ok)
        else:
            self.ui.tableWidget_creation_card_list.insertRow(value)
            self.ui.tableWidget_creation_card_list.setItem(value, 0, QtWidgets.QTableWidgetItem(front))
            self.ui.tableWidget_creation_card_list.setItem(value, 1, QtWidgets.QTableWidgetItem(back))
            self.ui.tableWidget_creation_card_list.setHorizontalHeaderLabels(["Front","Back"])
            self.ui.textEdit_creation_front.setFocus()
    ############################################################################################################################################


    ############################################################################################################################################
    # This method catches a signal if user click 'Remove Card' button.
    # The main goal of this method is that, removing selected card (item) from QTableWidget.
    def remove_selected_card_from_list(self):
        current_row = self.ui.tableWidget_creation_card_list.currentRow()
        self.ui.tableWidget_creation_card_list.removeRow(current_row)
    ############################################################################################################################################
    # This method catches a signal if user click 'Cancel' button.
    # The main goal of this method is that, discarding all progress while creating card and turning back to 'Deck and Cards' page.
    def cancel_without_saving_card_list(self):
        if self.ui.tableWidget_creation_card_list.rowCount() > 0:
            question = QMessageBox.question(self,"Delete Deck", "Do you really want to discard all cards that you want to create?", QMessageBox.Yes | QMessageBox.No)
            if question == QMessageBox.Yes:
                self.ui.tableWidget_creation_card_list.clear()
                self.ui.tableWidget_creation_card_list.setHorizontalHeaderLabels(["Front","Back"])
                self.ui.tableWidget_creation_card_list.setRowCount(0)
                self.clear_text_edits()
                self.ui.stackedWidget_MainApp.setCurrentIndex(1)
        else:
            self.clear_text_edits()
            self.ui.stackedWidget_MainApp.setCurrentIndex(1)
    ############################################################################################################################################


    ############################################################################################################################################
    # This method catches a signal if user click 'Add all to the deck' button.
    # The main goal of this method is that, inserting all cards(items in QTableWidget) into database and turning back to 'Deck and Cards' page.
    def add_cards_to_database(self):
        global creation_fronts_list
        global creation_backs_list
        creation_fronts_list = []
        creation_backs_list = []
        DATABASE_get_fronts_and_backs(self.ui.typeDeckName.text())
        for index in range(self.ui.tableWidget_creation_card_list.rowCount()):
            global creation_front
            global creation_back
            creation_front = self.ui.tableWidget_creation_card_list.item(index, 0).text()
            creation_back = self.ui.tableWidget_creation_card_list.item(index, 1).text()
            if self.is_there_same_one_on_the_list() == True:
                label = "You tried to add same card more than one. For this reason program added the card once.\n{} (FRONT)\n{} (BACK)".format(creation_front, creation_back)
                QMessageBox.information(self, "Card Error", label , QMessageBox.Ok)
            elif self.is_there_same_one_in_the_database() == True:
                label = "Same card is already in the deck.\n{} (Front)\n{} (Back)".format(creation_front, creation_back)
                QMessageBox.information(self, "Card Error", label, QMessageBox.Ok)
            else:
                creation_fronts_list.append(creation_front)
                creation_backs_list.append(creation_back)
                DATABASE_create_card(self.ui.typeDeckName.text(),creation_front,creation_back)
        self.ui.tableWidget_creation_card_list.clear()
        self.ui.tableWidget_creation_card_list.setRowCount(0)
        self.ui.tableWidget_creation_card_list.setHorizontalHeaderLabels(["Front","Back"])
        self.ui.textEdit_creation_back.clear()
        self.ui.textEdit_creation_front.clear()
        self.update_card_table()
        self.ui.stackedWidget_MainApp.setCurrentIndex(1)
    ############################################################################################################################################
    # This method works with other methods.
    # The main goal of this method is that, trying to find same card in QTableWidget before inserting.
    def is_there_same_one_on_the_list(self):
        for listed_front, listed_back in zip(creation_fronts_list, creation_backs_list):
            if listed_front == creation_front and listed_back == creation_back:
                return True
    ############################################################################################################################################
    # This method works with other methods.
    # The main goal of this method is that, trying to find same card in database before inserting.
    def is_there_same_one_in_the_database(self): 
        for db_listed_front, db_listed_back in zip(fronts_list, backs_list):
            if db_listed_front == creation_front and db_listed_back == creation_back:
                return True
    ############################################################################################################################################
 
 
    ############################################################################################################################################
    # This method catches a signal if user doubleclick to QTableWidget.
    # The main goal of this method is that, saving current front and back sides of card before space_character_blocker method.
    def space_character_blocker_tool(self):
        global current_front_2
        global current_back_2
        current_front_2 = (self.ui.tableWidget_creation_card_list.item(self.ui.tableWidget_creation_card_list.currentRow(), 0).text())
        current_back_2 = (self.ui.tableWidget_creation_card_list.item(self.ui.tableWidget_creation_card_list.currentRow(), 1).text())
    ############################################################################################################################################    
    # This method catches a signal if user change a card(item) in QTableWidget.
    # The main goal of this method is that, making sure user's input is not empty and has not useless space characters.
    def space_character_blocker(self):
        try:
            new_front_2 = self.ui.tableWidget_creation_card_list.item(self.ui.tableWidget_creation_card_list.currentRow(), 0).text().strip()
            new_back_2 = self.ui.tableWidget_creation_card_list.item(self.ui.tableWidget_creation_card_list.currentRow(), 1).text().strip()
            if new_front_2 == "":
                self.ui.tableWidget_creation_card_list.item(self.ui.tableWidget_creation_card_list.currentRow(), 0).setText(current_front_2)
            elif new_back_2 == "":
                self.ui.tableWidget_creation_card_list.item(self.ui.tableWidget_creation_card_list.currentRow(), 1).setText(current_back_2)
            else:
                self.ui.tableWidget_creation_card_list.item(self.ui.tableWidget_creation_card_list.currentRow(), 0).setText(new_front_2)
                self.ui.tableWidget_creation_card_list.item(self.ui.tableWidget_creation_card_list.currentRow(), 1).setText(new_back_2)
        except:
            pass
    ############################################################################################################################################



    "_______________________________________________________________STUDY PAGE_________________________________________________________________"
    """This section includes commands to use on Study Page"""

    ############################################################################################################################################
    # This method catches a signal if user click 'Study' section from toolbar.
    # The main goal of this method is that, changing current page to 'Study Page'.
    def tool_bar_study(self):
        if len(table_list) <= 1:
            QMessageBox.information(self, "Deck Error", "Please create a deck first and add cards in it.", QMessageBox.Ok)
        else:
            self.get_decks_to_study_combobox()
            self.clear_lcd_numbers()
            self.ui.stackedWidget_MainApp.setCurrentIndex(2)
    ############################################################################################################################################


    ############################################################################################################################################
    # This method works with other methods.
    # The main goal of this method is that, inserting all decks into QComboBox.
    def get_decks_to_study_combobox(self):
        self.ui.comboBox_deck_select.clear()
        for deck in table_list:
            if deck != "sqlite_sequence":
                self.ui.comboBox_deck_select.addItem(deck)
    ############################################################################################################################################
    # This method works with other methods and cathes a signal if user click 'Start' button.
    # The main goal of this method is that, while considering chance showing cards to user with label texts.
    def show_card_for_study(self):
        self.ui.comboBox_deck_select.setDisabled(1)
        if self.is_deck_empty_in_study_page()== False:
            deckname = self.ui.comboBox_deck_select.currentText()
            DATABASE_get_all_reds_into_list(deckname)
            DATABASE_get_all_oranges_into_list(deckname)
            DATABASE_get_all_yellows_into_list(deckname)
            DATABASE_get_all_greens_into_list(deckname)
            DATABASE_get_all_blues_into_list(deckname)
            self.lcd_numbers()
            
            self.ui.progressBar.setEnabled(1)
            self.progress_bar_for_studying()
            while True:
                rand = random.randrange(1,101)
                global selected
                if rand >= 1 and rand <= 35 and len(red_list) != 0:
                    selected = random.choice(red_list)
                    self.ui.label_shows_card_front.setText(selected[1])
                    break
                elif rand >= 36 and rand <= 60 and len(orange_list) != 0:
                    selected = random.choice(orange_list)
                    self.ui.label_shows_card_front.setText(selected[1])
                    break
                elif rand >= 61 and rand <= 80 and len(yellow_list) != 0:
                    selected = random.choice(yellow_list)
                    self.ui.label_shows_card_front.setText(selected[1])
                    break
                elif rand >= 81 and rand <= 95 and len(green_list) != 0:
                    selected = random.choice(green_list)
                    self.ui.label_shows_card_front.setText(selected[1])
                    break
                elif rand >= 96 and rand <= 100 and len(blue_list) != 0:
                    selected = random.choice(blue_list)
                    self.ui.label_shows_card_front.setText(selected[1])
                    break
        else:
            self.ui.comboBox_deck_select.setEnabled(1)
            label = "There are no cards in {}".format(self.ui.comboBox_deck_select.currentText())
            QMessageBox.information(self, "Deck Error", label, QMessageBox.Ok)
    ############################################################################################################################################


    ############################################################################################################################################
    # This method catches a signal if user click 'Red' button.
    # The main goal of this method is that, changing card's property to red.
    def red_clicked(self):
        if self.ui.label_shows_card_front.text() != "":
            DATABASE_reset_colors_for_card(self.ui.comboBox_deck_select.currentText(), selected[1], selected[2])
            DATABASE_setting_red(self.ui.comboBox_deck_select.currentText(), selected[1], selected[2])
            self.show_card_for_study()
            self.ui.label_shows_card_back.clear()
    ############################################################################################################################################
    # This method catches a signal if user click 'Orange' button.
    # The main goal of this method is that, changing card's property to orange.
    def orange_clicked(self): 
        if self.ui.label_shows_card_front.text() != "":
            DATABASE_reset_colors_for_card(self.ui.comboBox_deck_select.currentText(), selected[1], selected[2])
            DATABASE_setting_orange(self.ui.comboBox_deck_select.currentText(), selected[1], selected[2])
            self.show_card_for_study()
            self.ui.label_shows_card_back.clear()
    ############################################################################################################################################
    # This method catches a signal if user click 'Yellow' button.
    # The main goal of this method is that, changing card's property to yellow.
    def yellow_clicked(self):
        if self.ui.label_shows_card_front.text() != "":
            DATABASE_reset_colors_for_card(self.ui.comboBox_deck_select.currentText(), selected[1], selected[2])
            DATABASE_setting_yellow(self.ui.comboBox_deck_select.currentText(), selected[1], selected[2])
            self.show_card_for_study()
            self.ui.label_shows_card_back.clear()
    ############################################################################################################################################
    # This method catches a signal if user click 'Green' button.
    # The main goal of this method is that, changing card's property to green.
    def green_clicked(self):
        if self.ui.label_shows_card_front.text() != "":
            DATABASE_reset_colors_for_card(self.ui.comboBox_deck_select.currentText(), selected[1], selected[2])
            DATABASE_setting_green(self.ui.comboBox_deck_select.currentText(), selected[1], selected[2])
            self.show_card_for_study()
            self.ui.label_shows_card_back.clear()
    ############################################################################################################################################
    # This method catches a signal if user click 'Blue' button.
    # The main goal of this method is that, changing card's property to blue.
    def blue_clicked(self): 
        if self.ui.label_shows_card_front.text() != "":
            DATABASE_reset_colors_for_card(self.ui.comboBox_deck_select.currentText(), selected[1], selected[2])
            DATABASE_setting_blue(self.ui.comboBox_deck_select.currentText(), selected[1], selected[2])
            self.show_card_for_study()
            self.ui.label_shows_card_back.clear()
    ############################################################################################################################################
    # This method catches a signal if user click 'Show' button.
    # The main goal of this method is that, showing back side of the card to user.
    def show_back(self):
        if self.ui.label_shows_card_front.text() != "":
            self.ui.label_shows_card_back.setText(selected[2])
    ############################################################################################################################################
    # This method works with other methods.
    # The main goal of this method is that, checking the deck's inside empty or not.
    def is_deck_empty_in_study_page(self):
        try:
            DATABASE_get_cards(self.ui.comboBox_deck_select.currentText())

            if len(card_list) == 0:
                return True
            else:
                return False
        except sqlite3.OperationalError:
            pass
    ############################################################################################################################################
    # This method catches a signal if user change current in QComboBox.
    # The main goal of this method is that, clearing labels and setting color buttons disable while conmsidering deck's inside.
    def clear_labels_when_deckname_change(self):
        self.ui.label_shows_card_front.clear()
        self.ui.label_shows_card_back.clear()
        if self.is_deck_empty_in_study_page()== True:
            self.ui.btnRed.setDisabled(1)
            self.ui.btnOrange.setDisabled(1)
            self.ui.btnYellow.setDisabled(1)
            self.ui.btnGreen.setDisabled(1)
            self.ui.btnBlue.setDisabled(1)
            self.ui.btnShow.setDisabled(1)
        elif self.is_deck_empty_in_study_page()== False:
            self.ui.btnRed.setEnabled(1)
            self.ui.btnOrange.setEnabled(1)
            self.ui.btnYellow.setEnabled(1)
            self.ui.btnGreen.setEnabled(1)
            self.ui.btnBlue.setEnabled(1)
            self.ui.btnShow.setEnabled(1)
    ############################################################################################################################################


    ############################################################################################################################################
    # This method works with other methods.
    # The main goal of this method is that, setting card count into QLCDNumber of corresponding color.
    def lcd_numbers(self):
        self.ui.lcdNumber_Red.display(len(red_list))
        self.ui.lcdNumber_Orange.display(len(orange_list))
        self.ui.lcdNumber_Yellow.display(len(yellow_list))
        self.ui.lcdNumber_Green.display(len(green_list))
        self.ui.lcdNumber_Blue.display(len(blue_list))
    ############################################################################################################################################
    # This method works with other methods.
    # The main goal of this method is that, setting all QLCDNumbers to zero.
    def clear_lcd_numbers(self):
        self.ui.lcdNumber_Red.display(0)
        self.ui.lcdNumber_Orange.display(0)
        self.ui.lcdNumber_Yellow.display(0)
        self.ui.lcdNumber_Green.display(0)
        self.ui.lcdNumber_Blue.display(0)
    ############################################################################################################################################


    ############################################################################################################################################
    # This method catches a signal if user click 'Start' button.
    # The main goal of this method is that, starting the time for user's studytime statistics and saving current date.
    def start_button_worked(self):
        self.flag = True
        self.current_deck_name_for_timing = self.ui.comboBox_deck_select.currentText()
        self.study_starting_time = datetime.strftime(datetime.now(), "%d %B %Y") 
    ############################################################################################################################################    
    # This method catches a signal if user click 'Stop' button.
    # The main goal of this method is that, stoping the time for user's studytime statistics and clearing labels.
    def stop_button_worked(self):
        self.ui.progressBar.setDisabled(1)
        self.ui.progressBar.setValue(0)
        self.ui.label_shows_card_front.clear()
        self.ui.label_shows_card_back.clear()
        self.clear_lcd_numbers()
        if 0 <= float(self.ui.label_3.text()) < 1:
            self.flag = False
            self.count = 0
            self.ui.label_3.setText(str(self.count))
        else:
            self.flag = False
            self.sending_logs_to_db()
            self.count = 0
            self.ui.label_3.setText(str(self.count))
        self.ui.comboBox_deck_select.setEnabled(1)
    ############################################################################################################################################
    # This method works with other methods.
    # The main goal of this method is that, to act as a stopwatch.
    def stopwatch_for_study(self):
        self.count = 0
        self.flag = False
        self.ui.label_3.setText(str(self.count))
        timer = QTimer(self)
        timer.timeout.connect(self.stopwatch_for_study_tool)
        timer.start(100)
    ############################################################################################################################################
    # This method works with other methods.
    # The main goal of this method is that, to act as a stopwatch.
    def stopwatch_for_study_tool(self): 
        if self.flag:
            self.count+= 1
            text = str(self.count / 10)
            self.ui.label_3.setText(text)
    ############################################################################################################################################
    # This method works with other methods.
    # The main goal of this method is that, showing a progress bar according to blue card count. 
    def progress_bar_for_studying(self): 
        card_count = len(red_list) + len(orange_list) + len(yellow_list) + len(green_list) + len(blue_list)
        try:
            value= (len(blue_list)/card_count) * 100
            self.ui.progressBar.setValue(int(value))
        except ZeroDivisionError:
            self.ui.progressBar.setValue(0)
    ############################################################################################################################################



    "_______________________________________________________________STATISTICS_________________________________________________________________"
    """This section includes commands to use on Statistics"""

    ############################################################################################################################################
    # This method catches a signal if user click 'Statistics' section from toolbar.
    # The main goal of this method is that, changing current page to 'Statistics'.
    def tool_bar_statistics(self):
        self.stop_button_worked()
        self.get_decks_to_combobox_for_statistics()
        self.reset_card_count_labels()
        self.ui.stackedWidget_MainApp.setCurrentIndex(4)
        self.datetime_input_catches()
        self.database_index_no = ""
    ############################################################################################################################################

   
    ############################################################################################################################################
    # This method works with other methods.
    # The main goal of this method is that, inserting all decknames into QComboBox.
    def get_decks_to_combobox_for_statistics(self):
        self.ui.comboBox_for_statistic.clear()
        for deck in table_list:
            if deck != "sqlite_sequence":
                self.ui.comboBox_for_statistic.addItem(deck)
        self.ui.comboBox_for_statistic.setCurrentIndex(-1)
    ############################################################################################################################################
    # This method catches a signal if user click 'Sort' button.
    # The main goal of this method is that, sorting decks(items) in QComboBox.
    def sorting_combobox_for_statistics(self):
        table_list.sort(key = lambda x : x.lower())
        self.get_decks_to_combobox_for_statistics()
        self.reset_card_count_labels()
    ############################################################################################################################################
    # This method catches a signal if user change current index in QComboBox.
    # The main goal of this method is that, showing all stats to the user according to deckname that user has selected.
    def when_user_select_a_deck_from_combobox_statistic(self):
        try:
            DATABASE_get_all_reds_into_list(self.ui.comboBox_for_statistic.currentText())
            DATABASE_get_all_oranges_into_list(self.ui.comboBox_for_statistic.currentText())
            DATABASE_get_all_yellows_into_list(self.ui.comboBox_for_statistic.currentText())
            DATABASE_get_all_greens_into_list(self.ui.comboBox_for_statistic.currentText())
            DATABASE_get_all_blues_into_list(self.ui.comboBox_for_statistic.currentText())
        except:
            pass
        total_card_count = len(red_list) + len(orange_list) + len(yellow_list) + len(green_list) + len(blue_list)
        self.ui.lbl_red_count.setText(str(len(red_list)))
        self.ui.lbl_orange_count.setText(str(len(orange_list)))
        self.ui.lbl_yellow_count.setText(str(len(yellow_list)))
        self.ui.lbl_green_count.setText(str(len(green_list)))
        self.ui.lbl_blue_count.setText(str(len(blue_list)))
        self.ui.lbl_total_count.setText(f"Total\n{str(total_card_count)}")

        gl_one = DATABASE_getting_last_studied_time(self.ui.comboBox_for_statistic.currentText())
        if gl_one == None:
            self.ui.tableWidget_for_last_studied.clear()
            self.ui.tableWidget_for_last_studied.setRowCount(1)
            self.ui.tableWidget_for_last_studied.setItem(0,0, QtWidgets.QTableWidgetItem(""))
            self.ui.tableWidget_for_last_studied.item(0, 0).setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.tableWidget_for_last_studied.setHorizontalHeaderLabels(["Last studied time"])
        else:
            dt = datetime.strptime(gl_one, '%d/%m/%Y')
            dt = datetime.strftime(dt, "%d %B %Y")
            self.ui.tableWidget_for_last_studied.clear()
            self.ui.tableWidget_for_last_studied.setRowCount(1)
            self.ui.tableWidget_for_last_studied.setItem(0,0, QtWidgets.QTableWidgetItem(dt))
            self.ui.tableWidget_for_last_studied.item(0, 0).setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.tableWidget_for_last_studied.setHorizontalHeaderLabels(["Last studied time"])

        i = DATABASE_getting_total_studied_time(self.ui.comboBox_for_statistic.currentText())
        if i == 0:
            self.ui.tableWidget_for_total_studied.clear()
            self.ui.tableWidget_for_total_studied.setRowCount(1)
            self.ui.tableWidget_for_total_studied.setItem(0,0, QtWidgets.QTableWidgetItem(""))
            self.ui.tableWidget_for_total_studied.item(0, 0).setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.tableWidget_for_total_studied.setHorizontalHeaderLabels(["Total studied time"])
        else:
            seconds = int(i)
            hours = divmod(seconds,3600)[0]
            minutes = divmod(seconds-(hours*3600),60)[0]
            kalan_seconds = seconds-((hours*3600)+(minutes*60))
            if kalan_seconds == 0 and hours == 0 and minutes == 0:
                time_label_one = ""
            elif hours > 1: 
                time_label_one = f"{hours} Hours {minutes} Minutes {kalan_seconds} Seconds"
            elif hours == 1:
                time_label_one = f"{hours} Hour {minutes} Minutes {kalan_seconds} Seconds"
            elif hours == 0 and minutes > 1:
                time_label_one = f"{minutes} Minutes {kalan_seconds} Seconds"
            elif hours == 0 and minutes == 1:
                time_label_one = f"{minutes} Minute {kalan_seconds} Seconds"
            elif hours == 0 and minutes == 0:
                time_label_one = f"{kalan_seconds} Seconds"
            self.ui.tableWidget_for_total_studied.clear()
            self.ui.tableWidget_for_total_studied.setRowCount(1)
            self.ui.tableWidget_for_total_studied.setItem(0,0, QtWidgets.QTableWidgetItem(time_label_one))
            self.ui.tableWidget_for_total_studied.item(0, 0).setTextAlignment(QtCore.Qt.AlignCenter)
            self.ui.tableWidget_for_total_studied.setHorizontalHeaderLabels(["Total studied time"])  
    ############################################################################################################################################
    # This method works with other methods.
    # The main goal of this method is that, clearing color card counts from labels.
    def reset_card_count_labels(self):
        self.ui.lbl_red_count.setText("")
        self.ui.lbl_orange_count.setText("")
        self.ui.lbl_yellow_count.setText("")
        self.ui.lbl_green_count.setText("")
        self.ui.lbl_blue_count.setText("")
        self.ui.lbl_total_count.setText("")
    ############################################################################################################################################


    ############################################################################################################################################
    # This method works when the application open.
    # The main goal of this method is that, setting today's date to QDateTimeEdit.
    def setting_current_time_to_datetime_edit(self):
        current_time = str(datetime.now()).split(" ")[0].split("-")
        date = QDate(int(current_time[0]), int(current_time[1]), int(current_time[2]))
        self.ui.dateTimeEdit_for_statistics.setDate(date)
    ############################################################################################################################################
    # This method catches a signal if user change date from QDateTimeEdit.
    # The main goal of this method is that, showing all logs to the user according to date that user has selected.
    def datetime_input_catches(self):
        input_datetime_for_logs = self.ui.dateTimeEdit_for_statistics.text()
        logs = DATABASE_get_logs_from_db(input_datetime_for_logs)
        if logs == None:
            self.ui.tableWidget_for_records.clear()
            self.ui.tableWidget_for_records.setRowCount(0)
        else:
            self.ui.tableWidget_for_records.clear()
            tablerow = 0
            self.ui.tableWidget_for_records.setRowCount(len(logs))
            for i in logs:
                self.ui.tableWidget_for_records.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(i[1]))
                self.ui.tableWidget_for_records.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(i[2]))
                self.ui.tableWidget_for_records.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(i[0])))
                tablerow += 1
        self.ui.tableWidget_for_records.hideColumn(2)
        self.ui.tableWidget_for_records.setHorizontalHeaderLabels(["Deck name","Study time","id"])
    ############################################################################################################################################
    # This method works with other methods.
    # The main goal of this method is that, sending time value to the database after user's click to stop button when studying.
    def sending_logs_to_db(self):
        starting_time_for_logs = datetime.strptime(self.study_starting_time, '%d %B %Y')
        starting_time_for_logs = datetime.strftime(starting_time_for_logs, "%d/%m/%Y")
        current_deckname_for_logs = self.ui.comboBox_deck_select.currentText()
        seconds = float(self.ui.label_3.text())
        seconds = int(str(seconds).split(".")[0])
        hours = divmod(seconds,3600)[0]
        minutes = divmod(seconds-(hours*3600),60)[0]
        kalan_seconds = seconds-((hours*3600)+(minutes*60))
        if kalan_seconds == 0 and hours == 0 and minutes == 0:
            time_label_two = "No info"
        elif hours > 1: 
            time_label_two = f"{hours} Hours {minutes} Minutes {kalan_seconds} Seconds"
        elif hours == 1:
            time_label_two = f"{hours} Hour {minutes} Minutes {kalan_seconds} Seconds"
        elif hours == 0 and minutes > 1:
            time_label_two = f"{minutes} Minutes {kalan_seconds} Seconds"
        elif hours == 0 and minutes == 1:
            time_label_two = f"{minutes} Minute {kalan_seconds} Seconds"
        elif hours == 0 and minutes == 0:
            time_label_two = f"{kalan_seconds} Seconds"
        DATABASE_creating_table_for_day(starting_time_for_logs)
        DATABASE_insert_log_inside_table(starting_time_for_logs, current_deckname_for_logs, time_label_two)
    ############################################################################################################################################
    # This method catches a signal if user click 'Clear day' button.
    # The main goal of this method is that, removing all logs in that selected day.
    def clearday_worked_for_logs(self):
        if self.ui.tableWidget_for_records.rowCount() == 0:
            QMessageBox.warning(self, "Clear Day", f"There is no log for {self.ui.dateTimeEdit_for_statistics.text()}.", QMessageBox.Ok)
        else:
            label = f"Do you really want to clear {self.ui.dateTimeEdit_for_statistics.text()}?"
            question = QMessageBox.question(self,"Clear Day", label, QMessageBox.Yes | QMessageBox.No)
            if question == QMessageBox.Yes:
                DATABASE_clear_day_log(self.ui.dateTimeEdit_for_statistics.text())
                self.datetime_input_catches()
                self.when_user_select_a_deck_from_combobox_statistic()
    ############################################################################################################################################
    # This method catches a signal if user click a log(item) in QTableWidget.
    # The main goal of this method is that, saving current row's data before removing.
    def selecting_log_from_tablewidget(self):
        current_row_for_logs = self.ui.tableWidget_for_records.currentRow()
        self.database_index_no =  (self.ui.tableWidget_for_records.item(current_row_for_logs, 2).text())
    ############################################################################################################################################
    # This method catches a signal if user click 'Remove log' button.
    # The main goal of this method is that, removing selected log from QTableWidget and database.
    def remove_log_worked_for_logs(self):
        if self.database_index_no != "":
            question = QMessageBox.question(self,"Remove Log", "Do you really want to remove selected log?", QMessageBox.Yes | QMessageBox.No)
            if question == QMessageBox.Yes:
                DATABASE_remove_record_from_db(self.ui.dateTimeEdit_for_statistics.text(), self.database_index_no)
                self.datetime_input_catches()
                self.when_user_select_a_deck_from_combobox_statistic()
        else:
            QMessageBox.warning(self, "Remove Log", "Please select a log from list.", QMessageBox.Ok)
        self.database_index_no = ""
    ############################################################################################################################################


    

if __name__ == '__main__': 
    app = QtWidgets.QApplication(sys.argv)     
    win = myApp()                              
    win.show()                                 
    sys.exit(app.exec_())                                                              