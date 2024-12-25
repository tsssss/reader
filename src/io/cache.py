from collections import OrderedDict

class CacheManager():
    def __init__(self, cache=None):
        if cache is not None:
            self.cache = cache
        else:
            self.cache = OrderedDict()
        
    def check_if_update(self, var_name, var_id=None):

        if not self.has_var(var_name):
            return True
        
        if var_id is None:
            return False

        old_id = self.get_var_setting(var_name, 'var_id')
        if old_id is None:
            return True
        
        return (old_id != var_id)

    
    def get_var_name(self):
        return list(self.cache.keys())
    
    def get_var(self, var_name):
        if not self.has_var(var_name):
            raise KeyError(f"Dataset '{var_name}' not found.")

        # Get the variable
        return self.cache[var_name]
    
    def get_var_value(self, var_name):
        if not self.has_var(var_name):
            raise KeyError(f"Dataset '{var_name}' not found.")

        # Get the value of the variable
        return self.cache[var_name].values
    
    def get_var_setting(self, var_name, setting_name=None):
        if setting_name is None:
            if not self.has_var(var_name):
                raise KeyError(f"Dataset '{var_name}' not found.")
            return self.cache[var_name].attrs
        else:
            if not self.has_var_setting(var_name, setting_name):
                raise KeyError(f"Variable attribute '{setting_name}' not found for variable '{var_name}'.")
            return self.cache[var_name].attrs[setting_name]
    
    def set_var(self, var_name, value, setting=None):
        self.cache[var_name] = value

        if setting is not None:
            self.set_var_setting(var_name, setting)
    
    
    def set_var_setting(self, var_name, setting):
        if not self.has_var(var_name):
            raise KeyError(f"Dataset '{var_name}' not found.")

        if not isinstance(setting, dict):
            raise ValueError('setting should be a dict.') 

        # Set the variable's setting.
        if self.has_var(var_name):
            for setting_name,val in setting.items():
                self.cache[var_name].attrs[setting_name] = val


    def get_var_setting(self, var_name, setting_name=None):

        if setting_name is None:
            if not self.has_var(var_name):
                return None
            return self.cache[var_name].attrs
        else:
            if not self.has_var_setting(var_name, setting_name):
                return None
            return self.cache[var_name].attrs[setting_name]
    
    def has_var_setting(self, var_name, setting_name):
        if not self.has_var(var_name):
            return None
        return setting_name in self.cache[var_name].attrs
        

    def has_var(self, var_name):
        return var_name in self.cache

    def delete_var(self, var_name):
        if not self.has_var(var_name):
            del self.cache[var_name]


    
default_cache = CacheManager()