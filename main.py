#!/usr/bin/env python3

import datetime
import sys
import holidays
from qtpy import QtWidgets

from ui.mainwindow import Ui_MainWindow

app = QtWidgets.QApplication(sys.argv)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("nethr")




        #init urlaub_array
        global urlaub_array
        urlaub_array = [
        [self.ui.label_urlaub_von_1,
        self.ui.label_urlaub_bis_1,
        self.ui.date_urlaub_von_1,
        self.ui.date_urlaub_bis_1],

        [self.ui.label_urlaub_von_2,
        self.ui.label_urlaub_bis_2,
        self.ui.date_urlaub_von_2,
        self.ui.date_urlaub_bis_2],

        [self.ui.label_urlaub_von_3,
        self.ui.label_urlaub_bis_3,
        self.ui.date_urlaub_von_3,
        self.ui.date_urlaub_bis_3],

        [self.ui.label_urlaub_von_4,
        self.ui.label_urlaub_bis_4,
        self.ui.date_urlaub_von_4,
        self.ui.date_urlaub_bis_4],

        [self.ui.label_urlaub_von_5,
        self.ui.label_urlaub_bis_5,
        self.ui.date_urlaub_von_5,
        self.ui.date_urlaub_bis_5],

        [self.ui.label_urlaub_von_6,
        self.ui.label_urlaub_bis_6,
        self.ui.date_urlaub_von_6,
        self.ui.date_urlaub_bis_6],

        [self.ui.label_urlaub_von_7,
        self.ui.label_urlaub_bis_7,
        self.ui.date_urlaub_von_7,
        self.ui.date_urlaub_bis_7],

        [self.ui.label_urlaub_von_8,
        self.ui.label_urlaub_bis_8,
        self.ui.date_urlaub_von_8,
        self.ui.date_urlaub_bis_8],

        [self.ui.label_urlaub_von_9,
        self.ui.label_urlaub_bis_9,
        self.ui.date_urlaub_von_9,
        self.ui.date_urlaub_bis_9]
        ]

        #hide labels urlaub 2-9
        self.init_hide_urlaub()


        #help button functionality
        self.ui.button_help.clicked.connect(self.set_help_text)

        #about button functionality
        self.ui.button_about.clicked.connect(self.set_about_text)

        #was_ist_sonderzeit button functionality
        self.ui.button_was_ist_sonderzeit.clicked.connect(self.set_sonderzeit_text)

        #show urlaub and hide urlaub buttons functionality
        self.ui.button_urlaub_hinzufuegen.clicked.connect(self.show_urlaub)
        self.ui.button_urlaub_entfernen.clicked.connect(self.hide_urlaub)

        #nettostunden berechnen button functionality
        self.ui.button_nettostunden_berechnen.clicked.connect(self.calculate_nettohours)


    def set_help_text(self):
        self.ui.text_dialog.setText("{}\n{}\n{}\n".format("Kontakt via About-Button",
                                                          "Feiertage sind nicht zu beachten, da sie automatisiert eingerechnet werden.",
                                                          "Datumsangaben sind immer inklusiv. Wenn also der 01.01.2001 der letzte Tag ist, an dem man Urlaub hat, muss dieser eingetragen werden."))

    def set_about_text(self):
        self.ui.text_dialog.setText("{}\n{}\n{}\n".format("Kontaktemail: nine.github@gmail.com",
                                                          "Kontaktwebsite: https://github.com/strahlii",
                                                          "Sourcecode: https://github.com/strahlii/nethrpy"))

    def set_sonderzeit_text(self):
        self.ui.text_dialog.setText("{}\n{}\n".format("Sonderzeiten = alles, was von der Netto-Arbeitszeit abgezogen werden muss (Meeting etc).",
                                                      "Falls nötig kann hier auch die Krankheitszeit in Stunden angegeben werden, wenn bei Urlaub kein Platz mehr dafür ist."))

    def set_nettoh_text(self, nettoh):
        self.ui.text_dialog.setText("{} {} {}".format("Ergebnis:", nettoh, "Stunden Netto"))

    #asks which_urlaub_to_show(), then shows the 4 urlaub-widgets via the array urlaub_array
    def show_urlaub(self):
        i = self.which_urlaub_to_show()
        if i is not None:
            global urlaub_array
            for e in urlaub_array[i]:
                e.show()

    #see show_urlaub()
    def hide_urlaub(self):
        i = self.which_urlaub_to_hide()
        if i is not None:
            global urlaub_array
            for e in urlaub_array[i]:
                e.hide()

    #from 0 to 8 asks urlaub_array widget if its hidden, if yes, return the first one (lowest index)
    def which_urlaub_to_show(self):
        global urlaub_array
        for i in range(9):
            if urlaub_array[i][0].isHidden():
                return i
        return None

    #from 8 to 0 asks urlaub_array widget if its shown, if yes, return the last one (highest index)
    def which_urlaub_to_hide(self):
        global urlaub_array
        for i in reversed(range(9)):
            if urlaub_array[i][0].isHidden() == False:
                return i
        return None

    #hides every widget in urlaub_array
    def init_hide_urlaub(self):
        global urlaub_array
        for i in urlaub_array:
            if i is urlaub_array[0]:
                continue
            for e in i:
                e.hide()

    #starts nethr__init__
    def calculate_nettohours(self):
        nettoh = self.nethr__init__()
        self.set_nettoh_text(nettoh)

    #gets all values to calculate the netto hours
    def nethr__init__(self):
        global urlaub_array
        urlaub_list = []
        QDateEdit = type(self.ui.date_urlaub_von_1)
        for i in urlaub_array:
            for e in i:
                obj_type = type(e)
                if obj_type is QDateEdit and e.isVisible():
                    urlaub_list.append(e.date().toPyDate())
        offh = self.ui.spin_sonderzeit.value()
        hperday_array = [self.ui.spin_montag.value(), self.ui.spin_dienstag.value(), self.ui.spin_mittwoch.value(), self.ui.spin_donnerstag.value(), self.ui.spin_freitag.value(), self.ui.spin_samstag.value(), self.ui.spin_sonntag.value()]
        start = self.ui.date_zeitraum_von.date().toPyDate()
        end = self.ui.date_zeitraum_bis.date().toPyDate()
        urlaub_list_every_date = self.get_every_urlaub(urlaub_list)
        ger_holidays = self.get_holidays_state()

        return self.calculate(start, end, hperday_array, urlaub_list_every_date, offh, ger_holidays)

    def get_holidays_state(self):
        state = self.ui.combo_box_state.currentText()
        if state == "Baden-Wuerttemberg":
            return holidays.CountryHoliday('DE', prov='BW')
        elif state == "Bayern":
            return holidays.CountryHoliday('DE', prov='BY')
        elif state == "Berlin":
            return holidays.CountryHoliday('DE', prov='BE')
        elif state == "Brandenburg":
            return holidays.CountryHoliday('DE', prov='BB')
        elif state == "Bremen":
            return holidays.CountryHoliday('DE', prov='HB')
        elif state == "Hamburg":
            return holidays.CountryHoliday('DE', prov='HH')
        elif state == "Hessen":
            return holidays.CountryHoliday('DE', prov='HE')
        elif state == "Mecklenburg-Vorpommern":
            return holidays.CountryHoliday('DE', prov='MV')
        elif state == "Niedersachsen":
            return holidays.CountryHoliday('DE', prov='NI')
        elif state == "Nordrhein-Westfalen":
            return holidays.CountryHoliday('DE', prov='NW')
        elif state == "Rheinland-Pfalz":
            return holidays.CountryHoliday('DE', prov='RP')
        elif state == "Saarland":
            return holidays.CountryHoliday('DE', prov='SL')
        elif state == "Sachsen":
            return holidays.CountryHoliday('DE', prov='SN')
        elif state == "Sachsen-Anhalt":
            return holidays.CountryHoliday('DE', prov='ST')
        elif state == "Schleswig-Holstein":
            return holidays.CountryHoliday('DE', prov='SH')
        elif state == "Thueringen":
            return holidays.CountryHoliday('DE', prov='TH')



    def get_every_urlaub(self, urlaub_list):
        urlaub_list_every_date = []
        td = datetime.timedelta(days=1)
        i=0
        while i+1 < len(urlaub_list):
            currday = urlaub_list[i]
            end = urlaub_list[i+1]
            while currday <= end:
                urlaub_list_every_date.append(currday)
                currday = currday + td
            i = i + 2
        return urlaub_list_every_date


    def calculate(self, start, end, hperday_array, urlaub_list_every_date, offh, ger_holidays):
        nettoh = 0
        currday = start
        td = datetime.timedelta(days=1)
        while currday <= end:
            if currday not in ger_holidays and currday not in urlaub_list_every_date:
                nettoh = nettoh + hperday_array[currday.weekday()]
            currday = currday + td
        nettoh = nettoh - offh
        return nettoh


    ######discontinued######
    #crops urlaub_list so that entries align with start/end of zeitraum if they started before zeitraum or ended after zeitraum. if they began after zeitraum ends or ended before zeitraum starts, they get deleted from the urlaub_list
    def crop_urlaub(self, start, end, urlaub_list):
        i=0
        while i+1 < len(urlaub_list):
            if urlaub_list[i] > end or urlaub_list[i+1] < start:
                del urlaub_list[i]
                del urlaub_list[i]
            else:
                if urlaub_list[i] < start:
                    urlaub_list[i] = start
                if urlaub_list[i+1] > end:
                    urlaub_list[i+1] = end
            i=i+2



window = MainWindow()

window.show()



sys.exit(app.exec_())
