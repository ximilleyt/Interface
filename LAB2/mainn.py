import sys

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QFrame, QLabel, QPushButton,
    QHBoxLayout, QVBoxLayout, QStackedWidget,
    QFormLayout, QComboBox, QMessageBox,
    QLineEdit, QTextEdit, QSplitter
)
from PyQt5.QtCore import (
    Qt, QSize, QPoint, QEasingCurve,
    QPropertyAnimation, QParallelAnimationGroup
)
from PyQt5.QtGui import QIcon, QFontDatabase, QFont, QPixmap


DARK_BG = "#2B2B2B"
CARD_BG = "#3C3C3C"
BORDER = "#505050"
TEXT_LIGHT = "#FFFFFF"

class AnimatedStackedWidget(QStackedWidget):
    def __init__(self):
        super().__init__()

    def setCurrentIndex(self, index):
        self.slideInIndex(index)

    def slideInIndex(self, index):
        count = self.count()
        if index < 0:
            index = 0
        elif index >= count:
            index = count - 1

        current = self.currentWidget()
        next_widget = self.widget(index)
        offset = self.width()

        next_widget.setGeometry(self.rect())
        next_widget.move(offset, 0)
        next_widget.show()
        next_widget.raise_()

        anim_group = QParallelAnimationGroup(self)
        anim1 = QPropertyAnimation(current, b"pos", self)
        anim1.setDuration(250)
        anim1.setStartValue(QPoint(0, 0))
        anim1.setEndValue(QPoint(-offset, 0))
        anim1.setEasingCurve(QEasingCurve.OutSine)
        anim_group.addAnimation(anim1)

        anim2 = QPropertyAnimation(next_widget, b"pos", self)
        anim2.setDuration(250)
        anim2.setStartValue(QPoint(offset, 0))
        anim2.setEndValue(QPoint(0, 0))
        anim2.setEasingCurve(QEasingCurve.OutSine)
        anim_group.addAnimation(anim2)

        anim_group.finished.connect(lambda idx=index: QStackedWidget.setCurrentIndex(self, idx))
        anim_group.start()

class SideBarButton(QPushButton):
    def __init__(self, icon_path, tooltip):
        super().__init__()
        self.setFixedSize(60, 60)
        self.setIcon(QIcon(icon_path))
        self.setIconSize(QSize(28, 28))
        self.setToolTip(tooltip)
        self.setCursor(Qt.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                border: none;
            }}
            QPushButton:hover {{
                background: {BORDER};
            }}
        """)

class TitleBar(QFrame):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(60)
        self.setStyleSheet(f"background: {CARD_BG}; border-bottom: 1px solid {BORDER};")
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 0, 20, 0)
        self.title = QLabel("Home")
        self.title.setStyleSheet(f"font-size: 20px; color: {TEXT_LIGHT}; font-weight: 300;")
        layout.addWidget(self.title)
        layout.addStretch()

class ContentFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"background: {CARD_BG}; border-radius: 8px;")
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

    def addWidget(self, widget):
        self.layout.addWidget(widget)

    def addLayout(self, layout):
        self.layout.addLayout(layout)

class HomeScreen(ContentFrame):
    def __init__(self):
        super().__init__()
        image_container = QLabel()
        pixmap = QPixmap("icons/logo.png")
        pixmap = pixmap.scaled(256, 256, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_container.setPixmap(pixmap)
        image_container.setAlignment(Qt.AlignCenter)

        lbl = QLabel("Добро пожаловать в Veil")
        lbl.setStyleSheet(f"font-size: 24px; color: {TEXT_LIGHT}; font-weight: 500;")
        lbl.setAlignment(Qt.AlignCenter)

        instructions = QLabel("Выберите режим работы из панели слева")
        instructions.setStyleSheet(f"font-size: 16px; color: {TEXT_LIGHT}; font-weight: 200;")
        instructions.setAlignment(Qt.AlignCenter)

        self.layout.addStretch(1)
        self.addWidget(image_container)
        self.layout.addSpacing(10)
        self.addWidget(lbl)
        self.layout.addSpacing(10)
        self.addWidget(instructions)
        self.layout.addStretch(2)
        self.layout.setAlignment(Qt.AlignCenter)

class BasicScreen(ContentFrame):
    def __init__(self):
        super().__init__()
        lbl = QLabel("Обычный режим")
        lbl.setStyleSheet(f"font-size: 20px; color: {TEXT_LIGHT}; font-weight: 300;")
        self.addWidget(lbl)

        enc_frame = QFrame()
        enc_layout = QVBoxLayout(enc_frame)
        lbl1 = QLabel("Введите текст:")
        lbl1.setStyleSheet(f"color: {TEXT_LIGHT};")
        enc_layout.addWidget(lbl1)
        self.basic_text = QTextEdit()
        self.basic_text.setStyleSheet(f"background: {DARK_BG}; color: {TEXT_LIGHT}; border: 1px solid {BORDER};")
        enc_layout.addWidget(self.basic_text)
        btn_enc = QPushButton("Зашифровать")
        btn_enc.setStyleSheet(f"background: {BORDER}; color: {TEXT_LIGHT}; border: none; padding: 6px;")
        btn_enc.clicked.connect(self.basic_encrypt)
        enc_layout.addWidget(btn_enc)

        dec_frame = QFrame()
        dec_layout = QVBoxLayout(dec_frame)
        lbl2 = QLabel("Введите зашифрованный текст:")
        lbl2.setStyleSheet(f"color: {TEXT_LIGHT};")
        dec_layout.addWidget(lbl2)
        self.basic_decrypt_text = QTextEdit()
        self.basic_decrypt_text.setStyleSheet(f"background: {DARK_BG}; color: {TEXT_LIGHT}; border: 1px solid {BORDER};")
        dec_layout.addWidget(self.basic_decrypt_text)
        self.basic_key = QLineEdit()
        self.basic_key.setPlaceholderText("Введите ключ")
        self.basic_key.setStyleSheet(f"background: {DARK_BG}; color: {TEXT_LIGHT}; border: 1px solid {BORDER};")
        dec_layout.addWidget(self.basic_key)
        btn_dec = QPushButton("Дешифровать")
        btn_dec.setStyleSheet(f"background: {BORDER}; color: {TEXT_LIGHT}; border: none; padding: 6px;")
        btn_dec.clicked.connect(self.basic_decrypt)
        dec_layout.addWidget(btn_dec)

        splitter = QSplitter()
        splitter.addWidget(enc_frame)
        splitter.addWidget(dec_frame)
        self.addWidget(splitter)

        self.result = QTextEdit()
        self.result.setReadOnly(True)
        self.result.setStyleSheet(f"background: {DARK_BG}; color: {TEXT_LIGHT}; border: 1px solid {BORDER};")
        self.addWidget(self.result)

    def basic_encrypt(self):
        text = self.basic_text.toPlainText()
        encrypted = text[::-1]
        dummy_key = "key_123"
        self.result.setText(f"Зашифровано: {encrypted}\nКлюч: {dummy_key}")

    def basic_decrypt(self):
        encrypted_text = self.basic_decrypt_text.toPlainText()
        key = self.basic_key.text()
        decrypted = encrypted_text[::-1]
        self.result.setText(f"Дешифровано. Ключ: {key}\nЗашифрованный текст: {encrypted_text}\nРезультат: {decrypted}")

class AdvancedScreen(ContentFrame):
    def __init__(self):
        super().__init__()
        lbl = QLabel("Продвинутый режим")
        lbl.setStyleSheet(f"font-size: 20px; color: {TEXT_LIGHT}; font-weight: 300;")
        self.addWidget(lbl)

        enc_frame = QFrame()
        enc_layout = QVBoxLayout(enc_frame)
        lbl1 = QLabel("Текст для шифрования:")
        lbl1.setStyleSheet(f"color: {TEXT_LIGHT};")
        enc_layout.addWidget(lbl1)
        self.advanced_encrypt_text = QTextEdit()
        self.advanced_encrypt_text.setStyleSheet(f"background: {DARK_BG}; color: {TEXT_LIGHT}; border: 1px solid {BORDER};")
        enc_layout.addWidget(self.advanced_encrypt_text)
        self.advanced_algo = QComboBox()
        self.advanced_algo.addItems(["Caesar", "AES", "RSA"])
        self.advanced_algo.setStyleSheet(f"background: {DARK_BG}; color: {TEXT_LIGHT}; border: 1px solid {BORDER};")
        enc_layout.addWidget(self.advanced_algo)
        btn_enc2 = QPushButton("Зашифровать")
        btn_enc2.setStyleSheet(f"background: {BORDER}; color: {TEXT_LIGHT}; border: none; padding: 6px;")
        btn_enc2.clicked.connect(self.advanced_encrypt)
        enc_layout.addWidget(btn_enc2)

        dec_frame = QFrame()
        dec_layout = QVBoxLayout(dec_frame)
        lbl2 = QLabel("Зашифрованный текст:")
        lbl2.setStyleSheet(f"color: {TEXT_LIGHT};")
        dec_layout.addWidget(lbl2)
        self.advanced_decrypt_text = QTextEdit()
        self.advanced_decrypt_text.setStyleSheet(f"background: {DARK_BG}; color: {TEXT_LIGHT}; border: 1px solid {BORDER};")
        dec_layout.addWidget(self.advanced_decrypt_text)
        self.advanced_algo_dec = QComboBox()
        self.advanced_algo_dec.addItems(["Caesar", "AES", "RSA"])
        self.advanced_algo_dec.setStyleSheet(f"background: {DARK_BG}; color: {TEXT_LIGHT}; border: 1px solid {BORDER};")
        dec_layout.addWidget(self.advanced_algo_dec)
        self.advanced_key = QLineEdit()
        self.advanced_key.setPlaceholderText("Введите ключ")
        self.advanced_key.setStyleSheet(f"background: {DARK_BG}; color: {TEXT_LIGHT}; border: 1px solid {BORDER};")
        dec_layout.addWidget(self.advanced_key)
        btn_dec2 = QPushButton("Дешифровать")
        btn_dec2.setStyleSheet(f"background: {BORDER}; color: {TEXT_LIGHT}; border: none; padding: 6px;")
        btn_dec2.clicked.connect(self.advanced_decrypt)
        dec_layout.addWidget(btn_dec2)

        splitter = QSplitter()
        splitter.addWidget(enc_frame)
        splitter.addWidget(dec_frame)
        self.addWidget(splitter)

        self.adv_result = QTextEdit()
        self.adv_result.setReadOnly(True)
        self.adv_result.setStyleSheet(f"background: {DARK_BG}; color: {TEXT_LIGHT}; border: 1px solid {BORDER};")
        self.addWidget(self.adv_result)

    def advanced_encrypt(self):
        text = self.advanced_encrypt_text.toPlainText()
        algo = self.advanced_algo.currentText()
        dummy_key = "key_456"
        encrypted = text[::-1]
        self.adv_result.setText(f"Зашифровано с помощью {algo}\nКлюч: {dummy_key}\nРезультат: {encrypted}")

    def advanced_decrypt(self):
        encrypted_text = self.advanced_decrypt_text.toPlainText()
        algo = self.advanced_algo_dec.currentText()
        key = self.advanced_key.text()
        decrypted = encrypted_text[::-1]
        self.adv_result.setText(f"Дешифровано {algo} с ключом '{key}'\nЗашифрованный текст: {encrypted_text}\nРезультат: {decrypted}")

class SettingsScreen(ContentFrame):
    def __init__(self):
        super().__init__()
        self.layout.setAlignment(Qt.AlignCenter)
        self.layout.setContentsMargins(20, 20, 20, 20)
        self.layout.setSpacing(10)
        self.layout.insertSpacing(0, -200)

        lbl = QLabel("Настройки")
        lbl.setStyleSheet("""
            font-size: 28px;
            color: %s;
            font-weight: 400;
        """ % TEXT_LIGHT)
        lbl.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(lbl)
        self.layout.addSpacing(15)

        form = QFormLayout()
        form.setContentsMargins(0, 0, 0, 0)
        form.setVerticalSpacing(12)
        form.setFormAlignment(Qt.AlignHCenter)

        theme_label = QLabel("Тема:")
        theme_label.setStyleSheet(f"font-size: 18px; color: {TEXT_LIGHT};")
        form.addRow(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.theme_combo.setFixedHeight(40)
        self.theme_combo.setStyleSheet(f"""
            background: {DARK_BG};
            color: {TEXT_LIGHT};
            border: 1px solid {BORDER};
            font-size: 18px;
            padding: 4px 8px;
        """)
        form.addRow(self.theme_combo)

        save_btn = QPushButton("Сохранить")
        save_btn.setFixedSize(140, 40)
        save_btn.setStyleSheet(f"""
            background: {BORDER};
            color: {TEXT_LIGHT};
            border: none;
            font-size: 18px;
            border-radius: 6px;
            padding: 6px;
        """)
        save_btn.clicked.connect(self.save_settings)

        btn_wrapper = QHBoxLayout()
        btn_wrapper.setAlignment(Qt.AlignCenter)
        btn_wrapper.addWidget(save_btn)
        form.addRow(btn_wrapper)

        self.layout.addLayout(form)

    def save_settings(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Успех")
        msg.setText("Настройки сохранены!")
        msg.setStyleSheet(f"""
            QMessageBox {{
                background: {CARD_BG};
                color: {TEXT_LIGHT};
            }}
            QLabel {{
                color: {TEXT_LIGHT};
                font-size: 14px;
            }}
            QPushButton {{
                background: {BORDER};
                color: {TEXT_LIGHT};
                border: none;
                padding: 6px;
                min-width: 80px;
            }}
        """)
        msg.exec_()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Veil")
        self.setGeometry(100, 100, 1200, 800)
        self.setStyleSheet(f"QMainWindow {{ background: {DARK_BG}; color: {TEXT_LIGHT}; }}")

        QFontDatabase.addApplicationFont("Roboto-Regular.ttf")
        self.setFont(QFont("Roboto", 10))

        main = QWidget()
        self.setCentralWidget(main)
        hbox = QHBoxLayout(main)
        hbox.setContentsMargins(0, 0, 0, 0)

        sidebar = QFrame()
        sidebar.setFixedWidth(80)
        sidebar.setStyleSheet(f"background: {CARD_BG}; border-right: 1px solid {BORDER};")
        vbar = QVBoxLayout(sidebar)
        vbar.setAlignment(Qt.AlignTop)

        icons = [
            ("icons/home.svg", "Home"),
            ("icons/user.svg", "Basic Mode"),
            ("icons/advanced.svg", "Advanced Mode"),
            ("icons/settings.svg", "Settings"),
        ]
        for idx, (icon, tip) in enumerate(icons):
            btn = SideBarButton(icon, tip)
            btn.clicked.connect(lambda _, i=idx: self.switch_page(i))
            vbar.addWidget(btn)

        hbox.addWidget(sidebar)

        wrapper = QWidget()
        vbox = QVBoxLayout(wrapper)
        vbox.setContentsMargins(20, 20, 20, 20)

        self.title_bar = TitleBar()
        vbox.addWidget(self.title_bar)

        self.stack = AnimatedStackedWidget()
        self.stack.addWidget(HomeScreen())
        self.stack.addWidget(BasicScreen())
        self.stack.addWidget(AdvancedScreen())
        self.stack.addWidget(SettingsScreen())
        vbox.addWidget(self.stack)

        hbox.addWidget(wrapper)

    def switch_page(self, idx):
        pages = ["Home", "Basic", "Advanced", "Settings"]
        self.title_bar.title.setText(pages[idx])
        self.stack.setCurrentIndex(idx)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
