# cdf_handler.py
from spacepy import pycdf
import os
import numpy as np
from iohandler import IOHandler

class CDFHandler(IOHandler):
    def __init__(self, file):
        # Call the constructor of the parent class
        super().__init__(file)

    # Variable operations
    def get_var_name(self):
        with pycdf.CDF(self.file[0]) as cdf_file:
            # Get available variable names
            return list(cdf_file.keys())

    def get_var(self, var_name, ranges=None):
        if not self.has_var(var_name):
            raise KeyError(f"Dataset '{var_name}' not found.")

        nfile = len(self.file)
        if ranges is None:
            ranges = [None]*nfile
        if len(ranges) != nfile:
            ranges = [None]*nfile

        data = None
        for file,range in zip(self.file,ranges):
            with pycdf.CDF(file) as cdf_file:
                # Get the value of the variable
                the_data = cdf_file[var_name][...]
                if range is not None:
                    the_data = the_data[range[0]:range[1]]
                if data is None:
                    data = the_data
                else:
                    data = np.concatenate((data,the_data), axis=0)
        return data
    
    def set_var(self, var_name, value, setting=None):
        if self.has_var(var_name):
            self.delete_var(var_name)

        for file in self.file:
            if not os.path.exists(file):
                _ = pycdf.CDF(file, create=True)

            with pycdf.CDF(file, readonly=False) as cdf_file:
                # Set the value of one variable
                cdf_file[var_name] = value

                # Save settings if provided
                if setting is not None:
                    self.set_var_setting(var_name, setting)

    def set_var_setting(self, var_name, setting):
        if not self.has_var(var_name):
            raise KeyError(f"Dataset '{var_name}' not found.")
        
        if not isinstance(setting, dict):
            raise ValueError('setting should be a dict.')

        for file in self.file:
            with pycdf.CDF(file, readonly=False) as cdf_file:
                # Set the variable's setting.
                variable = cdf_file[var_name]
                for setting_name,val in setting.items():
                    variable.attrs[setting_name] = val


    def rename_var(self, old_name, new_name):
        if not self.has_var(old_name):
            raise KeyError(f"Dataset '{old_name}' not found.")

        for file in self.file:
            with pycdf.CDF(file, readonly=False) as cdf_file:
                # Rename a variable in the CDF file
                cdf_file.rename(old_name, new_name)

    def has_var(self, var_name):
        with pycdf.CDF(self.file[0]) as cdf_file:
            # Check if the variable exists
            return var_name in cdf_file

    def delete_var(self, var_name):
        if not self.has_var(var_name):
            raise KeyError(f"Dataset '{var_name}' not found.")

        for file in self.file:
            with pycdf.CDF(file, readonly=False) as cdf_file:
                # Delete a variable from the CDF file
                del cdf_file[var_name]

    # Settings
    def get_setting_name(self):
        with pycdf.CDF(self.file[0]) as cdf_file:
            # Get available global attribute names (settings)
            return list(cdf_file.attrs.keys())

    def get_setting(self, setting_name=None):
        def get_setting_val(v):
            val = list()
            for i in range(v.max_idx()+1):
                val.append(v._get_entry(i))
            return val

        with pycdf.CDF(self.file[0], readonly=True) as cdf_file:
            # Get the value of the global attribute (setting)
            g_attrs = cdf_file.attrs
            if setting_name is None:
                attrs = dict()  # necessary b/c g_attrs.values() are not 'real' values yet.
                for k in g_attrs.keys():
                    v = g_attrs[k]
                    attrs[k] = get_setting_val(v)
                return attrs
            else:
                if not self.has_setting(setting_name):
                    raise KeyError(f"Global attribute '{setting_name}' not found.")
                v = g_attrs[setting_name]
                return get_setting_val(v)

    def set_setting(self, setting):
        if not isinstance(setting, dict):
            raise ValueError('setting should be a dict.')

        for file in self.file:
            if not os.path.exists(file):
                _ = pycdf.CDF(file, create=True)

            with pycdf.CDF(file, readonly=False) as cdf_file:
                # Set the value of the global attribute (setting)
                for setting_name,val in setting.items():
                    cdf_file.attrs[setting_name] = val

    def rename_setting(self, old_name, new_name):
        if not self.has_setting(old_name):
            raise KeyError(f"Global attribute '{old_name}' not found.")

        for file in self.file:
            with pycdf.CDF(file, readonly=False) as cdf_file:
                # Rename a global attribute (setting) in the CDF file
                cdf_file.attrs[new_name] = cdf_file.attrs[old_name]
                del cdf_file.attrs[old_name]


    def has_setting(self, setting_name):
        with pycdf.CDF(self.file[0]) as cdf_file:
            # Check if the global attribute (setting) exists
            return setting_name in cdf_file.attrs

    def delete_setting(self, setting_name):
        if not self.has_setting(setting_name):
            raise KeyError(f"Global attribute '{setting_name}' not found.")

        for file in self.file:
            with pycdf.CDF(file, readonly=False) as cdf_file:
                # Delete a global attribute (setting) from the CDF file
                del cdf_file.attrs[setting_name]

    # Variable settings
    def get_var_setting_name(self, var_name):
        if not self.has_var(var_name):
            raise KeyError(f"Dataset '{var_name}' not found.")

        with pycdf.CDF(self.file[0]) as cdf_file:
            # Get available variable attribute (var_setting) names for the given variable
            return list(cdf_file[var_name].attrs.keys())


    def get_var_setting(self, var_name, setting_name=None):
        # Get the value of the variable attribute (var_setting) for the given variable

        def get_setting_val(v):
            return v

        with pycdf.CDF(self.file[0], readonly=True) as cdf_file:
            # Get the value of the variable attribute (setting)
            v_attrs = cdf_file[var_name].attrs
            if setting_name is None:
                attrs = dict()  # necessary b/c v_attrs.values() are not 'real' values yet.
                for k in v_attrs.keys():
                    v = v_attrs[k]
                    attrs[k] = get_setting_val(v)
                return attrs
            else:
                if self.has_setting(setting_name):
                    raise KeyError(f"Variable attribute '{setting_name}' not found.")
                v = v_attrs[setting_name]
                return get_setting_val(v)


    def rename_var_setting(self, var_name, setting_name, new_key):
        if not self.has_var_setting(var_name, setting_name):
            raise KeyError(f"Variable attribute '{setting_name}' not found for variable '{var_name}'.")

        for file in self.file:
            with pycdf.CDF(file, readonly=False) as cdf_file:
                # Rename a variable attribute (var_setting) for the given variable
                var_attrs = cdf_file[var_name].attrs
                var_attrs[new_key] = var_attrs.pop(setting_name)


    def has_var_setting(self, var_name, setting_name):
        if not self.has_var(var_name):
            raise KeyError(f"Dataset '{var_name}' not found.")

        with pycdf.CDF(self.file[0]) as cdf_file:
            # Check if the variable attribute (var_setting) exists for the given variable
            return setting_name in cdf_file[var_name].attrs


    def delete_var_setting(self, var_name, setting_name):
        if not self.has_var_setting(var_name, setting_name):
            raise KeyError(f"Variable attribute '{setting_name}' not found for variable '{var_name}'.")

        for file in self.file:
            with pycdf.CDF(file, readonly=False) as cdf_file:
                # Delete a variable attribute (var_setting) from the given variable
                var_attrs = cdf_file[var_name].attrs
                del var_attrs[setting_name]



def read_var(var_name, files, ranges=None, steps=None):

    if type(files) is not list:
        files = [files]
    nfile = len(files)

    if ranges is None:
        ranges = [None]*nfile
    if len(ranges) != nfile:
        ranges = [None]*nfile

    if steps is None:
        steps = [1]*nfile
    if len(steps) != nfile:
        steps = [1]*nfile

    cdf = CDFHandler(files[0])
    if not cdf.has_var(var_name):
        raise KeyError(f"Dataset '{var_name}' not found.")
    
    data = None
    for file,range,step in zip(files,ranges,steps):
        cdf = CDFHandler(file)
        the_data = cdf.get_var(var_name)
        if range is None:
            range = [0,the_data.shape[0]]
        the_data = the_data[range[0]:range[1]:step]
        if data is None:
            data = the_data
        else:
            data = np.concatenate((data,the_data), axis=0)

    return data


valid_cdf_type = {
    1:  'CDF_INT1',
    2:  'CDF_INT2',
    4:  'CDF_INT4',
    8:  'CDF_INT8',
    11: 'CDF_UINT1',
    12: 'CDF_UINT2',
    14: 'CDF_UINT4',
    21: 'CDF_REAL4',
    22: 'CDF_REAL8',
    31: 'CDF_EPOCH',
    32: 'CDF_EPOCH16',
    33: 'CDF_TIME_TT2000',
    41: 'CDF_BYTE',
    44: 'CDF_FLOAT',
    45: 'CDF_DOUBLE',
    51: 'CDF_CHAR',
    52: 'CDF_UCHAR',
}