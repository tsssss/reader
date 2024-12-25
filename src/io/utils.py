import os, sys
from os.path import expanduser

def get_home_dir():
    return expanduser('~')

def join_path(*args):
    return os.path.join(*args)

def file_exists(file):
    if isinstance(file,str):
        return os.path.exists(file)
    else:
        return False

def get_os():
    
    platform = sys.platform

    known_os = {
        'win': ['win32'],
        'unix': ['linux2','cygwin','os2','os2emx','riscos','atheos'],
        'mac': ['darwin'],
    }

    found_os = False
    for os in known_os:
        if platform in known_os[os]:
            found_os = True
            return os
    
    if not found_os:
        raise ValueError(f"Unknown os {platform}.") 


def get_disk_dir(disk_name):

    if type(disk_name) is not str:
        raise ValueError('disk_name should be a string.')

    os = get_os()
    if os == 'mac':
        disk_dir = '/'.join(['','Volumes',disk_name])
    elif os == 'unix':
        disk_dir = '/'.join(['','media',disk_name])
    elif os == 'win':
        import wmi
        c = wmi.WMI()
        for drive in c.Win32_LogicalDisk():
            if drive.VolumeName == disk_name:
                disk_dir = drive.Caption+'/'
                break
        else:
            disk_dir = None
    else:
        disk_dir = None
    
    if disk_dir is None:
        raise ValueError(f"Disk dir {disk_dir} not found for disk name: {disk_name}.")

    return disk_dir
    


def get_google_dir():

    google_name = 'My Drive'
    my_os = get_os()
    if my_os == 'win':
        google_root = os.path.join(get_disk_dir('Google Drive'))
        sub_items = os.listdir(google_root)
        for sub_item in sub_items:
            if google_name in sub_item:
                break
        else:
            raise ValueError(f'Google name {google_name} not found.')
        if google_name == sub_item:
            google_dir = os.path.join(google_root,google_name)
        else:
            # To follow the link.
            if 'lnk' in sub_item:
                from win32com.client import Dispatch
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(os.path.join(google_root,sub_item))
                target_path = shortcut.TargetPath
                google_dir = os.path.abspath(target_path)
            else:
                google_dir = ''

    elif my_os in ['mac','unix']:
        google_dir = os.path.join(get_home_dir(),google_name)
    else:
        raise ValueError(f'Unknown os: {my_os}.')

    if not os.path.exists(google_dir):
        raise ValueError(f"Google Drive path {google_dir} does not exist.")
    return google_dir