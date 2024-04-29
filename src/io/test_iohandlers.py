# Importing the CDFHandler and HDF5Handler classes
from cdf import CDFHandler
from hdf5 import HDF5Handler
import numpy as np
import sys, os

def test_iohandlers():
    # Creating instances of the handlers with sample file paths

    my_path = os.path.dirname(os.path.realpath(__file__))
    print(my_path)

    cdf_file_path = os.path.join(my_path,"path_to_file.cdf")
    hdf5_file_path = os.path.join(my_path,"path_to_file.h5")

    handlers = []
    handlers.append(CDFHandler(cdf_file_path))
    handlers.append(HDF5Handler(hdf5_file_path))

    for handler in handlers:
        handler.set_setting({"global_attr":"value"})
        print("Global attribute value:", handler.get_setting("global_attr"))

        # Check if a global attribute exists
        print("Global attribute exists:", handler.has_setting("global_attr"))

        # Rename a global attribute
        handler.rename_setting("global_attr", "new_global_attr")
        print("Renamed global attribute:", handler.get_setting("new_global_attr"))

        # Delete a global attribute
        handler.delete_setting("new_global_attr")
        print("Global attribute deleted:", not handler.has_setting("new_global_attr"))

        # Set variable data.
        variable_name = 'variable'
        variable_value = np.array([1, 2, 3])
        handler.set_var(variable_name, variable_value)
        print("Variable value set:", handler.get_var(variable_name))

        # Set and retrieve variable attributes
        handler.set_var_setting("variable", {"var_attr":"var_value"})
        print("Variable attribute value:", handler.get_var_setting("variable", "var_attr"))

        # Check if a variable attribute exists
        print("Variable attribute exists:", handler.has_var_setting("variable", "var_attr"))

        # Rename a variable attribute
        handler.rename_var_setting("variable", "var_attr", "new_var_attr")
        print("Renamed variable attribute:", handler.get_var_setting("variable", "new_var_attr"))

        # Delete a variable attribute
        handler.delete_var_setting("variable", "new_var_attr")
        print("Variable attribute deleted:", not handler.has_var_setting("variable", "new_var_attr"))


if __name__ == '__main__':
    test_iohandlers()