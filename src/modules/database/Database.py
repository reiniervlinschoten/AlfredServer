import sqlite3

from src.modules.logging.logger import setup_logger


class Database:
    def __init__(self, path):
        self.path = path
        self.logger = setup_logger(__name__)
        self.setup_database()

    def query(self, command, placeholder=(), return_val="fetchall"):
        """Queries the database and returns:
           - a tuple of tuples containing the selection
           - a tuple of tuples containing the description of the selection
           - False when failing"""
        c = sqlite3.connect(self.path)
        if return_val == "fetchall":
            self.logger.info(
                "Command: {0}, placeholder {1}, return value: {2}".format(command, placeholder, return_val))
            result = c.execute(command, placeholder).fetchall()
        elif return_val == "description":
            self.logger.info(
                "Command: {0}, placeholder {1}, return value: {2}".format(command, placeholder, return_val))
            result = c.execute(command, placeholder).description
        else:
            self.logger.debug("Given return value {0} not understood".format(return_val))
            result = False
        c.commit()
        c.close()
        return result

    def setup_database(self):
        """Sets up the database with the devices table"""
        creation_string_devices = "CREATE TABLE IF NOT EXISTS devices " \
                                  "(id          INTEGER NOT NULL    PRIMARY KEY," \
                                  "name         TEXT    NOT NULL    UNIQUE," \
                                  "device_type  TEXT    NOT NULL," \
                                  "location     TEXT    NOT NULL," \
                                  "ip           TEXT    NOT NULL    UNIQUE," \
                                  "brand        TEXT    NOT NULL)"
        self.logger.info("Setting up database")
        self.query(creation_string_devices)

    def add_device(self, device_object):
        """Enters the given device in the database.
           Returns True when the device is registered.
           Returns False when the device could not be registered"""
        try:
            self.query("INSERT INTO devices (name, device_type, location, ip, brand) VALUES (?,?,?,?,?)",
                       placeholder=(device_object.name,
                                    device_object.device_type,
                                    device_object.location,
                                    device_object.ip,
                                    device_object.brand))
            self.logger.info("Inserted device: {0} {1} {2} {3} {4}".format(device_object.name,
                                                                           device_object.device_type,
                                                                           device_object.location,
                                                                           device_object.ip,
                                                                           device_object.brand))
        except sqlite3.IntegrityError as e:
            self.logger.debug(str(e))

    def get_devices(self):
        """Returns a list of tuples of all devices."""
        self.logger.info("Returning all devices from database")
        return self.query("SELECT name, device_type, location, ip, brand FROM 'devices'")
