# hdf5_handler.py
import h5py
from iohandler import IOHandler

class HDF5Handler(IOHandler):
    def __init__(self, file):
        # Call the constructor of the parent class
        super().__init__(file)

    # Variable operations
    def get_var_name(self):
        with h5py.File(self.file[0], 'r') as hf:
            return list(hf.keys())

    def get_var(self, var_name):
        with h5py.File(self.file[0], 'r') as hdf5_file:
            # Get the value of the variable
            if var_name in hdf5_file:
                return hdf5_file[var_name][...]
            else:
                raise KeyError(f"Dataset '{var_name}' not found in the HDF5 file.")

    def set_var(self, var_name, value, setting=None):
        for file in self.file:
            if self.has_var(var_name):
                self.delete_var(var_name)
            with h5py.File(file, 'a') as hdf5_file:
                # Set the value of the variable
                hdf5_file[var_name] = value

                # Save settings if provided
                if setting is not None:
                    self.set_var_setting(var_name, setting)

    def set_var_setting(self, var_name, setting):
        for file in self.file:
            with h5py.File(file, 'a') as hdf5_file:
                # Set the value of the variable attribute (var_setting)
                if var_name in hdf5_file:
                    variable = hdf5_file[var_name]
                    for setting_name in setting.keys():
                        variable.attrs[setting_name] = setting[setting_name]
                    print(f'Setting {setting_name} added to {var_name} in {file}')
                else:
                    print(f'Variable {var_name} does not exist in {file}. Cannot add attribute.')

    def rename_var(self, old_name, new_name):
        for file in self.file:
            with h5py.File(file, 'a') as hdf5_file:
                # Rename a variable in the HDF5 file
                if old_name in hdf5_file:
                    hdf5_file[new_name] = hdf5_file.pop(old_name)
                else:
                    raise KeyError(f"Dataset '{old_name}' not found in the HDF5 file.")

    def has_var(self, var_name):
        with h5py.File(self.file[0], 'r') as hdf5_file:
            # Check if the variable exists
            return var_name in hdf5_file

    def delete_var(self, var_name):
        for file in self.file:
            with h5py.File(file, 'a') as hdf5_file:
                # Delete a variable from the HDF5 file
                if var_name in hdf5_file:
                    del hdf5_file[var_name]
                else:
                    raise KeyError(f"Dataset '{var_name}' not found in the HDF5 file.")

    # Settings
    def get_setting_name(self):
        with h5py.File(self.file[0], 'r') as hdf5_file:
            # Get available global attribute names (settings)
            return list(hdf5_file.attrs.keys())

    def get_setting(self, setting_name=None):
        with h5py.File(self.file[0], 'r') as hdf5_file:
            # Get the value of the global attribute (setting)
            if setting_name is None:
                return hdf5_file.attrs
            if setting_name in hdf5_file.attrs:
                return hdf5_file.attrs[setting_name]
            else:
                raise KeyError(f"Global attribute '{setting_name}' not found in the HDF5 file.")

    def set_setting(self, setting):
        for file in self.file:
            with h5py.File(file, 'a') as hdf5_file:
                # Set the value of the global attribute (setting)
                for setting_name in setting.keys():
                    hdf5_file.attrs[setting_name] = setting[setting_name]

    def rename_setting(self, old_name, new_name):
        for file in self.file:
            with h5py.File(file, 'a') as hdf5_file:
                # Rename a global attribute (setting) in the HDF5 file
                if old_name in hdf5_file.attrs:
                    hdf5_file.attrs[new_name] = hdf5_file.attrs.pop(old_name)
                else:
                    raise KeyError(f"Global attribute '{old_name}' not found in the HDF5 file.")

    def has_setting(self, setting_name):
        with h5py.File(self.file[0], 'r') as hdf5_file:
            # Check if the global attribute (setting) exists
            return setting_name in hdf5_file.attrs

    def delete_setting(self, setting_name):
        for file in self.file:
            with h5py.File(file, 'a') as hdf5_file:
                # Delete a global attribute (setting) from the HDF5 file
                if setting_name in hdf5_file.attrs:
                    del hdf5_file.attrs[setting_name]
                else:
                    raise KeyError(f"Global attribute '{setting_name}' not found in the HDF5 file.")

    # Variable settings
    def get_var_setting_name(self, var_name):
        with h5py.File(self.file[0], 'r') as hdf5_file:
            # Get available variable attribute names (var_setting) for the given variable
            if var_name in hdf5_file:
                return list(hdf5_file[var_name].attrs.keys())
            else:
                raise KeyError(f"Variable '{var_name}' not found in the HDF5 file.")

    def get_var_setting(self, var_name, setting_name=None):
        with h5py.File(self.file[0], 'r') as hdf5_file:
            # Get the value of the variable attribute (var_setting) for the given variable
            if var_name in hdf5_file:
                var_attrs = hdf5_file[var_name].attrs
                if setting_name is None:
                    return var_attrs
                if setting_name in var_attrs:
                    return var_attrs[setting_name]
                else:
                    raise KeyError(f"Variable attribute '{setting_name}' not found for variable '{var_name}'.")
            else:
                raise KeyError(f"Variable '{var_name}' not found in the HDF5 file.")

    def rename_var_setting(self, var_name, setting_name, new_name):
        for file in self.file:
            with h5py.File(file, 'a') as hdf5_file:
                # Rename a variable attribute (var_setting) for the given variable
                if var_name in hdf5_file:
                    var_attrs = hdf5_file[var_name].attrs
                    if setting_name in var_attrs:
                        # Rename by creating a new key and deleting the old one
                        var_attrs[new_name] = var_attrs.pop(setting_name)
                    else:
                        raise KeyError(f"Variable attribute '{setting_name}' not found for variable '{var_name}'.")
                else:
                    raise KeyError(f"Variable '{var_name}' not found in the HDF5 file.")

    def has_var_setting(self, var_name, setting_name):
        with h5py.File(self.file[0], 'r') as hdf5_file:
            # Check if the variable attribute (var_setting) exists for the given variable
            if var_name in hdf5_file:
                var_attrs = hdf5_file[var_name].attrs
                return setting_name in var_attrs
            else:
                raise KeyError(f"Variable '{var_name}' not found in the HDF5 file.")

    def delete_var_setting(self, var_name, setting_name):
        for file in self.file:
            with h5py.File(file, 'a') as hdf5_file:
                # Delete a variable attribute (var_setting) for the given variable
                if var_name in hdf5_file:
                    var_attrs = hdf5_file[var_name].attrs
                    if setting_name in var_attrs:
                        del var_attrs[setting_name]
                    else:
                        raise KeyError(f"Variable attribute '{setting_name}' not found for variable '{var_name}'.")
                else:
                    raise KeyError(f"Variable '{var_name}' not found in the HDF5 file.")