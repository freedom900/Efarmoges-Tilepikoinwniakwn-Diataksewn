import sys
from math import floor, ceil
import serial
from PyQt5.QtGui import QPixmap, QIcon, QColor, QPalette, QPainter
from PyQt5.QtCore import Qt, QSize, QPoint, QTimer, QObject, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel, QScrollArea, \
    QTabWidget


class SquircleButton(QPushButton):
    def __init__(self, text1, text2, icon_path, color):
        super().__init__(text1)
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(60, 10, 0, 0)

        # First line label
        self.label1 = QLabel(text1)
        self.label1.setStyleSheet("font-size: 20px; color: white;")
        self.layout.addWidget(self.label1)

        # Second line label
        self.label2 = QLabel(text2)
        self.label2.setStyleSheet("font-size: 13px; color: black;")
        self.label2.setWordWrap(1)
        self.layout.addWidget(self.label2)

        self.layout.addStretch(1)

        # for icons and buttons style
        self.setStyleSheet(f"QPushButton {{ background-color: {color}; border-radius: 20px; color: {color}; \
        font-size: 20px; border: 2px solid black; text-align: left; padding-left: 5px; }}")
        self.setFixedSize(350, 80)  # Set fixed size for squircle button
        self.setIcon(QIcon(icon_path))  # Set icon for the button
        self.setIconSize(QSize(50, 50))  # Set the size of the icon
        self.setLayout(self.layout)


class SquareButton(QPushButton):
    def __init__(self, text, color, text_color):
        super().__init__(text)
        self.setStyleSheet("QPushButton { background-color: %s; color: %s; font-size: 15px; text-align: \
        left; border: 2px solid black; }" % (color, text_color))
        self.setFixedSize(300, 70)  # Set fixed size for square button


class BaseWindow(QMainWindow):
    def __init__(self, title, background_color, logo_path):
        super().__init__()
        self.setWindowTitle(title)
        self.setWindowIcon(QIcon("./photos/oasth.png"))
        self.background_color(background_color)

        # Create main widget and layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Set the logo
        self.logo_path = logo_path
        self.set_logo(logo_path)

        # Create back button
        self.back_button = QPushButton("Back")
        self.back_button.clicked.connect(self.switch_window)
        self.layout.addWidget(self.back_button, alignment=Qt.AlignTop | Qt.AlignLeft)

    def set_logo(self, logo_path):
        # Create and set QLabel with scaled pixmap
        pixmap = QPixmap(logo_path)
        scaled_pixmap = pixmap.scaledToWidth(350)  # Adjust the width as needed
        image_label = QLabel()
        image_label.setPixmap(scaled_pixmap)
        self.layout.addWidget(image_label)

    def background_color(self, color):
        palette = self.palette()
        palette.setColor(QPalette.Background, QColor(color))
        self.setAutoFillBackground(True)
        self.setPalette(palette)

    def switch_window(self):
        self.close()
        self.main_window = MainWindow()
        self.main_window.show()

    def switch_window_tabs(self, text):
        sender = self.sender()
        if sender:
            self.close()
            self.tabs_window = Tabs(text)
            self.tabs_window.show()

    def create_buses_window(self, buttons_info):
        self.setFixedSize(QSize(375, 600))
        # Create a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow the widget inside the scroll area to resize

        # Create a widget to contain the buttons
        buttons_widget = QWidget()

        # Create a layout for the buttons widget
        buttons_layout = QVBoxLayout(buttons_widget)

        # Add buttons to the layout
        for bus_number in buttons_info:
            button = SquareButton(bus_number, "#605d5d", "#b2b2e0")
            button.clicked.connect(lambda checked, text=bus_number: self.switch_window_tabs(text))
            buttons_layout.addWidget(button)

        # Set spacing between buttons
        buttons_layout.setSpacing(0)
        buttons_widget.setLayout(buttons_layout)
        scroll_area.setWidget(buttons_widget)

        # Set the central widget of the window
        self.central_widget.setLayout(QVBoxLayout())
        self.layout.addWidget(scroll_area)


class MainWindow(BaseWindow):
    def __init__(self):
        super().__init__("oasth2.0", "#A0A4AD", "./photos/logo.png")

        # Counter for people inside the building
        self.people_count = 0

        buttons_info = [
            ("Nearby Stops", "Using device's location feature", "./photos/nearbystops.png"),
            ("Bus Locations", "Real-time bus locations", "./photos/buslocations.png"),
            ("Arrivals", "Display information including bus arrivals and route info",
             "./arrivals.png"),
            ("Travel Directions", "Provision of the most optimal route using the public transport means",
             "./photos/traveldirections.png"),
            ("Routes", "Timetables, stops, routes etc.", "./photos/routes.png"),
            ("News", "News, announcements etc.", "./photos/news.png")
        ]
        for button_text, explanation, icon_path in buttons_info:
            button = SquircleButton(button_text, explanation, icon_path, "#605d5d")
            button.clicked.connect(self.switch_window)
            self.layout.addWidget(button)

        self.back_button.hide()

    def switch_window(self):
        sender = self.sender()
        if sender:
            self.hide()
            window_name = sender.text()
            window_class = globals()[window_name.replace(" ", "")]
            self.another_window = window_class()
            self.another_window.show()


class NearbyStops(BaseWindow):
    def __init__(self):
        super().__init__("Nearby Stops", "#A0A4AD", "./photos/nearbylogo.png")
        buttons_info = [
            " FITITIKI LESHI\n 200m.\n To: KTEL ",
            " AHEPA\n 350m.\n To: KTEL ",
            " UNIVERSITY OF MACEDONIA\n 270m.\n To: KTEL ",
            " SINTRIVANI\n 800m.\n To: KTEL ",
            " AGIA FOTINI\n 350m.\n To: IKEA ",
            " 424 STRATIOTIKO NOSOKOMEIO\n 500m.\n To: IKEA ",
            " AHEPA (AGIOU DIMITRIOU)\n 400m.\n To: N.S. STATHMOS ",
            " KAMARA\n 1250m.\n To: KTEL",
        ]
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)  # Allow the widget inside the scroll area to resize

        # Create a widget to contain the buttons
        buttons_widget = QWidget()

        # Create a layout for the buttons widget
        buttons_layout = QVBoxLayout(buttons_widget)

        for bus_number in buttons_info:
            button = SquareButton(bus_number, "#605d5d", "#b2b2e0")
            buttons_layout.addWidget(button)

        buttons_layout.setSpacing(0)
        buttons_widget.setLayout(buttons_layout)
        scroll_area.setWidget(buttons_widget)

        # Set the central widget of the window
        self.central_widget.setLayout(QVBoxLayout())
        self.layout.addWidget(scroll_area)


class BusLocations(BaseWindow):
    def __init__(self):
        super().__init__("Bus Locations", "#A0A4AD", "./photos/locationslogo.png")
        buttons_info = [
            "01N\n AIRPORT - KTEL MAKEDONIA Night",
            "01X\n AIRPORT - KTEL MAKEDONIA",
            "02K\n AS IKEA - KTEL MAKEDONIA",
            "03K\n AS IKEA - NS STATHMOS",
            "06\n KALAMARIA - VENIZELOU",
            "12\n KTEL - KATO TOUMPA",
            "24\n PL. ELEFTHERIAS - CHILIA DENDRA",
            "45\n KTEL MAKEDONIAS - KOSMOS",
            "69\n AS IKEA - EPANOMI",
        ]
        self.create_buses_window(buttons_info)


class Arrivals(BaseWindow):
    def __init__(self):
        super().__init__("Arrivals", "#A0A4AD", "./photos/arrivalslogo.png")
        buttons_info = [
            "01N\n AIRPORT - KTEL MAKEDONIA Night",
            "01X\n AIRPORT - KTEL MAKEDONIA",
            "02K\n AS IKEA - KTEL MAKEDONIA",
            "03K\n AS IKEA - NS STATHMOS",
            "06\n KALAMARIA - VENIZELOU",
            "12\n KTEL - KATO TOUMPA",
            "24\n PL. ELEFTHERIAS - CHILIA DENDRA",
            "45\n KTEL MAKEDONIAS - KOSMOS",
            "69\n AS IKEA - EPANOMI",
        ]
        self.create_buses_window(buttons_info)


class TravelDirections(BaseWindow):
    def __init__(self):
        super().__init__("Travel Directions", "#A0A4AD", "./photos/traveldirectionslogo.png")
        self.label = QLabel("Coming Soon!")
        self.label.setStyleSheet("QLabel { color: black; font-size: 25px; }")
        self.layout.addWidget(self.label, alignment=Qt.AlignCenter)

        pixmap = QPixmap("./photos/hamster.png")
        scaled_pixmap = pixmap.scaledToWidth(350)  # Adjust the width as needed
        image_label = QLabel()
        image_label.setPixmap(scaled_pixmap)
        self.layout.addWidget(image_label)
        self.label2 = QLabel("Where it all started")
        self.label2.setStyleSheet("QLabel { color: black; font-size: 15px; }")
        self.layout.addWidget(self.label2)

class Routes(BaseWindow):
    def __init__(self):
        super().__init__("Routes", "#A0A4AD", "./photos/routeslogo.png")
        buttons_info = [
            "01N\n AIRPORT - KTEL MAKEDONIA Night",
            "01X\n AIRPORT - KTEL MAKEDONIA",
            "02K\n AS IKEA - KTEL MAKEDONIA",
            "03K\n AS IKEA - NS STATHMOS",
            "06\n KALAMARIA - VENIZELOU",
            "12\n KTEL - KATO TOUMPA",
            "24\n PL. ELEFTHERIAS - CHILIA DENDRA",
            "45\n KTEL MAKEDONIAS - KOSMOS",
            "69\n AS IKEA - EPANOMI",
        ]
        self.create_buses_window(buttons_info)


class News(BaseWindow):
    def __init__(self):
        super().__init__("News", "#A0A4AD", "./photos/newslogo.png")

        # Create label to display the title of the news about our new app
        self.label = QLabel("New upgraded OASTH!")
        self.label.setStyleSheet("QLabel { color: white; font-size: 28px; }")
        self.layout.addWidget(self.label)

        # Make a second label to add info about our app

        self.label2 = QLabel(
            '<font color="black">We would like to present you our new addition to our buses! <br>We have '
            'created a sensor that can count how many people got on and off the bus and updates our buses '
            'on the app! The buses are colorized according to how full are in real time. </font><font '
            'color="green"> <br>Green </font><font color="black">means they are up to 25% full, </font><font '
            'color="yellow">yellow </font><font color="black">means they are up to 50% full, </font><font '
            'color="orange">orange </font><font color="black">means that they are up to 75% full, '
            '</font><font color="red">red </font><font color="black">means that they are up to 99% full '
            'and finally </font><font color="purple">purple </font><font color="black"> means that they '
            'are 100% (or more!) full. This way you can plan in advance which bus you would like to take '
            'without waiting for it only to show up full and miss it.<br><br>Hope you enjoy the new '
            'update!</font>')

        self.label2.setWordWrap(True)  # wraps at \n
        self.layout.addWidget(self.label2)


class StopsList(QPushButton):
    def __init__(self, text, color, text_color):
        super().__init__(text)
        self.setStyleSheet("QPushButton { background-color: %s; color: %s; font-size: 15px; text-align: \
        left; border: 2px solid black; }" % (color, text_color))
        self.setFixedSize(330, 30)  # Set fixed size for square button


class Tabs(BaseWindow):
    def __init__(self, text):
        super().__init__("Tabs", "#A0A4AD", "./photos/locationslogo.png")
        tab_widget = QTabWidget()
        self.bus_number = text.split("\n")[0]
        self.setFixedSize(QSize(375, 600))

        # Create a QLabel to display the text above the tabs
        self.text_label = QLabel(text)
        self.text_label.setStyleSheet("font-size: 20px; color: white;")
        self.layout.addWidget(self.text_label)

        self.bus_line = self.bus_number + ".png"
        bus_time = "T" + self.bus_line

        # Create three tabs
        tab1 = QWidget()
        tab2 = QWidget()
        tab3 = QWidget()

        # Create layouts for each tab
        layout1 = QVBoxLayout(tab1)
        layout2 = QVBoxLayout(tab2)
        layout3 = QVBoxLayout(tab3)

        # Add the timetables for each bus
        pixmap = QPixmap(f"./photos/{bus_time}")
        scaled_pixmap = pixmap.scaledToWidth(300)  # Adjust the width as needed
        image_label = QLabel()
        image_label.setPixmap(scaled_pixmap)
        layout1.addWidget(image_label)

        # Create the stops for each bus
        if self.bus_number == "01N":
            enani = ["TS KTEL", "OMOSPONDIA", "ORIZOMILI", "MHXANOURGIO OSE", "VOSPOROS", "BALTA", "KOLETI",
                     "STROFI EPTALOFOU", "AGION PANTON", "NEOS SIRODROMIKOS STATHMOS", "ZOGRAFOU",
                     "PLATIA DIMOKRATIAS", "KOLOMVOU", "ANTIGONIDON", "PLATIA ARISTOTELOUS", "MITROPOLITOU GENNADOU",
                     "AGIAS SOFIAS", "IASONIDOU", "KAMARA"]
            for stops in enani:
                stopbutton = StopsList(stops, "#605d5d", "#b2b2e0")
                layout2.addWidget(stopbutton)
        elif self.bus_number == "01X":
            enaxi = ["TS KTEL", "ORIZOMILI", "STROFI EPTALOFOU", "NEOS SIDIRODROMIKOS STATHMOS", "KOLOMVOU",
                     "PLATIA ARISTOTELOUS", "KAMARA", "AGIA FOTINI-UNIVERSITY OF MACEDONIA", "DIMARHIAKO MEGARO",
                     "FALIRO", "SHOLI TIFLON", "LAOGRAFIKO MOUSEIO", "MEGARO MOUSIKIS-25 MARTIOU",
                     "PERIFERIAKI ENOTITA THESSALONIKIS", "KRIKELA", "AGORA", "EMPORIKO KENTRO", "GEORGIKI SHOLI",
                     "ASTINOMIA", "MACEDONIA AIRPORT-DEPARTURES", "MACEDONIA AIRPORT-ARRIVALS"]
            for stops in enaxi:
                button = StopsList(stops, "#605d5d", "#b2b2e0")
                layout2.addWidget(button)
        elif self.bus_number == "02K":
            dyokappa = ["ANATOLIKOS STATHMOS IKEA", "IKEA", "NAFPIGIA", "VIAMIL", "KALAMARI",
                        "KLISTO GIPEDO MPASKET PILEAS", "PRONIA", "AGORA", "AMAXOSTASIO", "NOSOKOMEIO AGIOS PAVLOS",
                        "STRATOPEDO", "AGIOS PANTELEIMON", "PERIPTERO", "KRIKELA", "VIZANTIO",
                        "PERIFERIAKI ENOTITA THESSALONIKIS", "AGIOS ELEFTHERIOS", "VOULGARI", "GIMNASIO", "IPPOKRATIO",
                        "THEAGENIO", "PAPAFIO", "424 STRATIOTIKO NOSOKOMEIO", "SHOLI AXIOMATIOKON",
                        "UNIVERSITY OF MACEDONIA", "AHEPA", "SINTRIVANI", "KAMARA", "IASONIDOU",
                        "AGIAS SOFIAS", "PLATIA ARISTOTELOUS", "ALKAZAR", "ANTIGONIDON", "KOLOMVOU",
                        "PLATIA DIMOKRATIAS", "NEOS SIDIRODROMIKOS STATHMOS", "AGION PANTON", "STROFI EPTALOFOU",
                        "BALTA", "VOSPOROS", "MIHANOURGIO OSE", "OMOSPONDIA", "GEFIRA", "TS KTEL"]
            for stops in dyokappa:
                button = StopsList(stops, "#605d5d", "#b2b2e0")
                layout2.addWidget(button)
        elif self.bus_number == "03K":
            triakappa = ["ANATOLIKOS STATHMOS IKEA", "IKEA", "NAFPIGIA", "VIAMIL", "KALAMARI",
                         "KLISTO GIPEDO MPASKET PILEAS", "PRONIA", "AGORA", "AMAXOSTASIO", "NOSOKOMEIO AGIOS PAVLOS",
                         "STRATOPEDO", "AGIOS PANTELEIMON", "PERIPTERO", "KRIKELA", "VIZANTIO",
                         "PERIFERIAKI ENOTITA THESSALONIKIS", "CASA BIANCA", "25 MARTIOU", "GEORGIOU", "ANALIPSI",
                         "BOTSARI", "LAOGRAFIKO MOUSEIO", "SHOLI TIFLON", "FALIRO", "EVZONON", "DIMARHIAKO MEGARO",
                         "H.A.N.TH", "KENTRO ISTORIAS THESSALONIKIS", "DIAGONIOS", "AGIAS SOFIAS",
                         "PLATIA ARISTOTELOUS", "PLATIA EMPORIOU", "DIIKITIKA DIKASTIRIA", "IKA", "ANAGENISEOS",
                         "NEOS SIDIRODROMIKOS STATHMOS"]
            for stops in triakappa:
                button = StopsList(stops, "#605d5d", "#b2b2e0")
                layout2.addWidget(button)
        elif self.bus_number == "06":
            eksi = ["TS KRINIS", "STROFI ETHNIKIS SHOLIS DIKASTON", "GIPEDO FINIKA", "STRATIGOU STEFANOU SARAFI",
                    "PAPAZOGLOU", "ANDREA PAPANDREOU", "VRIOULON", "PALIO TERMA", "ERGATIKES KATIKIES", "KAPNAPOTHIKES",
                    "SHOLIO", "PLATANOS", "IDRIMA", "PLATIA SKRA", "TAHIDROMIO", "PALIO DIMARHIO", "PONTOU",
                    "PALIO TAHIDROMIO", "DIOROFA", "GAVRIILIDI", "ELLINIKO KOLLEGIO",
                    "PERIFERIAKI ENOTITA THESSSALONIKIS", "CASA BIANCA", "25 MARTIOU", "GEORGIOU", "ANALIPSI",
                    "BOTSARI", "LAOGRAFIKO MOUSEIO", "SHOLI TIFLON", "FALIRO", "EVZONON", "DIMARHIAKO MEGARO",
                    "H.A.N.TH.", "KENTRO ISTORIAS THESSALONIKIS", "DIAGONIOS", "AGIAS SOFIAS", "PLATIA ARISTOTELOUS",
                    "TS PLATIA ELEFTHERIAS"]
            for stops in eksi:
                button = StopsList(stops, "#605d5d", "#b2b2e0")
                layout2.addWidget(button)
        elif self.bus_number == "12":
            dwdeka = ["TS KTEL", "OMOSPONDIA", "ORIZOMILI", "MIHANOURGIO OSE", "VOSPOROS", "BALTA", "OPAP", "TSORLINI",
                      "PALIOS SIDIRODROMIKOS STATHMOS", "NEA DIKASTIRIA", "KOLOMVOU", "ANTIGONIDON", "AGIOS MINAS",
                      "VENIZELOU", "PLATIA ARISTOTELOUS", "MITROPOLI", "DIAGONIOS", "ETERIA MAKEDONIKON SPOUDON",
                      "MOUSIA", "STRATIGIO-MOUSIO VYZ.POLITISMOU", "STRATODIKIO", "POLEMIKO MOUSIO",
                      "424 STRATIOTIKO MOUSIO", "PAPAFIO", "IFANET", "AGIOS FANOURIOS", "KLEANTHOUS", "GIPEDO PAOK",
                      "GEFIRA", "VOSPOROU", "KLIMATARIA", "PILEAS 1", "PILEAS 2", "TS KATO TOYMPAS"]
            for stops in dwdeka:
                button = StopsList(stops, "#605d5d", "#b2b2e0")
                layout2.addWidget(button)
        elif self.bus_number == "24":
            eikostesera = ["TS VENIZELOU", "AGORA", "PLATIA ARISTOTELOUS", "MITROPOLITOU GENNADIOU", "AGIAS SOFIAS",
                           "IASONIDOU", "KAMARA", "SINTRIVANI", "FITITIKI LESHI", "AHEPA", "TELLOGLIO", "EVAGGELISTRIA",
                           "NOSOKOMIO", "AGIOS PAVLOS", "SHOLIO", "PLATIA HILION DENDRON", "TS HILION DENDRON"]
            for stops in eikostesera:
                button = StopsList(stops, "#605d5d", "#b2b2e0")
                layout2.addWidget(button)
        elif self.bus_number == "45":
            sarantapente = ["TS KTEL", "ORIZOMILI", "NEOS SIDIRODROMIKOS STATHMOS", "KOLOVMOU", "ANTIGONIDON",
                            "PLATIA ARISTOTELOUS", "KAMARA", "AHEPA", "IPPOKRATIO", "25 MARTIOU", "KTEL HALKIDIKIS",
                            "MEDITERRANEAN COSMOS"]
            for stops in sarantapente:
                button = StopsList(stops, "#605d5d", "#b2b2e0")
                layout2.addWidget(button)
        elif self.bus_number == "69":
            nice = ["ANATOLIKOS STATHMOS IKEA", "POLIFOTA", "GEORGIKI SHOLI", "AERODROMIO", "FLOREX", "IEK",
                    "THESSALONIKIA", "NERAIDA", "KOSMODROMIO", "DIASTAVROSI", "STROFI EPANOMIS", "XENODOHIO", "ILIOS",
                    "1 PLAGIARIOU", "2 PLAGIARIOU", "STATHI", "STROFI", "KINOTITA", "VENZINADIKO-EXODOS PLAGIARIOU",
                    "PTINOTROFIO", "VILES", "EKKLISAKI", "ARAMPATZI", "KATIKIES", "ERGOSTASIO", "AMPELAKIA",
                    "IKONOMIDI", "GEFIRA", "SINERGIO", "MILOS", "MITADIKA", "EKKLISIA", "28 OKTOVRIOU",
                    "AGIOS SPIRIDON" "EPANOMI-EKKLISAKI", "SHOLIO", "KTIMA KONSTA", "APOTHIKI SITIRON", "FARMAKIDI",
                    "THERMOKIPIA", "KOLLIOU", "KTIMA SARAFI", "IKODOMI PAPA", "AGIA MARINA", "PARALIA"]
            for stops in nice:
                button = StopsList(stops, "#605d5d", "#b2b2e0")
                layout2.addWidget(button)
        layout2.setSpacing(0)
        layout2.setContentsMargins(0, 0, 0, 0)

        self.capacity = 20
        self.num_people = 0
        self.initial_pos = True

        # Start reading data from Arduino
        self.start_reading_serial()

        self.image_label = QLabel()  # Make it a member variable
        layout3.addWidget(self.image_label)

        # Create a label to display the number of people
        self.people_label = QLabel()
        layout3.addWidget(self.people_label, alignment=Qt.AlignCenter)

        # Create a scroll area for the first and second tab
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(tab2)

        scroll_area2 = QScrollArea()
        scroll_area2.setWidgetResizable(True)
        scroll_area2.setWidget(tab1)

        # Add the tabs to the tab widget
        tab_widget.addTab(scroll_area2, "TIMETABLES")
        tab_widget.addTab(scroll_area, "STOPS")
        tab_widget.addTab(tab3, "BUS LOCATIONS")

        # Set layout for the central widget
        self.central_widget.setLayout(QVBoxLayout())

        # Add the tab widget to the central widget layout
        self.central_widget.layout().addWidget(tab_widget)
        tab_widget.setStyleSheet("""
                    QTabBar::tab {background-color: #605d5d; color: white; padding: 8px; border: 2px solid transparent;}
                    QTabBar::tab:selected { background-color: #FFFFFF; color: #605d5d; border-bottom-color: #007bff; }
                    QTabWidget::pane {background-color: #A0A4AD;} """)

    def start_reading_serial(self):
        self.arduino_Serial_Data = serial.Serial('COM13', 9600)
        QTimer.singleShot(1000, self.read_serial_data)

    def read_serial_data(self):
        if self.arduino_Serial_Data.inWaiting() > 0:
            my_data = str(self.arduino_Serial_Data.readline())
            self.res = "".join([char for char in my_data if char.isdigit()])
            if "102" in self.res:
                if len(self.res) == 6:
                    self.num_people = int(self.res) % 1021
                    self.people_label.setText(f"Number of People: {self.num_people}")
                    self.change_bus_color()
                else:
                    self.num_people = int(self.res) % 102
                    self.people_label.setText(f"Number of People: {self.num_people}")
                    self.change_bus_color()

        QTimer.singleShot(1000, self.read_serial_data)

    def change_bus_color(self):
        # Determine the bus color based on the number of people
        if self.num_people < self.capacity * 0.25:
            bus_color = "green"
        elif self.capacity * 0.25 <= self.num_people < self.capacity * 0.5:
            bus_color = "yellow"
        elif self.capacity * 0.5 <= self.num_people < self.capacity * 0.75:
            bus_color = "orange"
        elif self.capacity * 0.75 <= self.num_people < self.capacity * 0.99:
            bus_color = "red"
        else:
            bus_color = "purple"

        # Load the corresponding bus pixmap
        bus_pixmap = QPixmap(f"./photos/{bus_color}.png")
        bus_pixmap = bus_pixmap.scaled(45, 45, Qt.KeepAspectRatio)

        # Load the route pixmap
        route_pixmap = QPixmap(f"./photos/{self.bus_number}.png")

        # Draw the bus pixmap on top of the route pixmap
        painter = QPainter(route_pixmap)
        # painter.drawPixmap(QPoint(75, 80), bus_pixmap)
        if len(self.res) == 6:
            painter.drawPixmap(QPoint(105, 130), bus_pixmap)
            self.initial_pos = False
        else:  # len(self.res) == 4 or 5
            if self.initial_pos:
                painter.drawPixmap(QPoint(75, 85), bus_pixmap)
            else:
                painter.drawPixmap(QPoint(145, 175), bus_pixmap)

        painter.end()

        # Set the combined pixmap to the image_label
        self.image_label.setPixmap(route_pixmap)

    def closeEvent(self, event):
        self.arduino_Serial_Data.close()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app_icon = QIcon("./photos/oasth.png")
    app.setWindowIcon(app_icon)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
