from abc import ABC, abstractmethod

class IOHandler(ABC):
    def __init__(self, file=None):
        if type(file) is list:
            self.file = file
        else:
            self.file = [file]

    # Variable operations
    @abstractmethod
    def get_var_name(self):
        # Get available variable names.
        pass

    @abstractmethod
    def get_var(self, var_name):
        # Get the value of the variable.
        pass

    @abstractmethod
    def set_var(self, var_name, value):
        # Set the value of one variable.
        pass

    @abstractmethod
    def set_var_setting(self, var_name, setting):
        # Set settings of one variable.
        pass

    @abstractmethod
    def rename_var(self, old_name, new_name):
        pass

    @abstractmethod
    def has_var(self, var_name):
        pass

    @abstractmethod
    def delete_var(self, var_name):
        pass


    # Settings.
    @abstractmethod
    def get_setting_name(self):
        # Get available setting names.
        pass

    @abstractmethod
    def get_setting(self, setting_name):
        # Get the value of the setting.
        pass

    @abstractmethod
    def set_setting(self, setting):
        # Set the value of one setting.
        pass

    @abstractmethod
    def rename_setting(self, old_name, new_name):
        pass

    @abstractmethod
    def has_setting(self, setting_name):
        pass

    @abstractmethod
    def delete_setting(self, setting_name):
        pass


    # Variable settings.
    @abstractmethod
    def get_var_setting_name(self, var_name):
        # Get available setting names of one variable.
        pass

    @abstractmethod
    def get_var_setting(self, var_name, setting_name):
        # Set the value of one setting for the given variable.
        pass

    @abstractmethod
    def rename_var_setting(self, var_name, setting_name, new_key):
        pass

    @abstractmethod
    def has_var_setting(self, var_name, setting_name):
        pass

    @abstractmethod
    def delete_var_setting(self, var_name, setting_name):
        pass