def get_instr_info_at_umn(probe='a'):
    remote_root = 'https://rbsp.space.umn.edu/rbsp_efw'

def get_instr_info_at_cdaweb(probe='a'):

    remote_root = 'https://cdaweb.gsfc.nasa.gov/pub/data/rbsp'
    rbspx = 'rbsp'+probe
    prefix = rbspx+'_'
    version = '%v'

    valid_date = {
        'a':['2012-09-05','2019-10-15'],
        'b':['2012-09-05','2019-07-17'],
        }

    instr_info = {
        'valid_date': valid_date[probe],
    }

    # Spice product.
    instr_info['ephemeris'] = {
        'base_name': prefix+'spice_products_%Y%m%d_'+version+'cdf',
        'local_path': [rbspx,'ephemeris','efw-ephem','%Y'],
        'remote_path': [rbspx,'ephemeris','efw-ephem','%Y'],
    }

    # Level 1 data.
    l1_info = dict()
    for key in ['esvy','vsvy','vb1','mscb1','vb2','mscb2']:
        l1_info[key] = {
            'base_name': prefix+'l1_'+key+'_%Y%m%d_'+version+'.cdf',
            'local_path': [rbspx,'efw','l1',key,'%Y'],
            'remote_path': [rbspx,'l1','efw',key,'%Y'],
        }
    for key in ['vb1-split','mscb1-split']:
        l1_info[key] = {
            'base_name': prefix+'efw_l1_'+key+'_%Y%m%dt%H%M%S_'+version+'.cdf',
            'local_path': [rbspx,'efw','l1',key,'%Y'],
            'remote_path': [rbspx,'l1','efw',key,'%Y'],
            'cadence': 15*60, 
        }
    instr_info['l1'] = l1_info

    # Level 2 data.
    l2_info = dict()
    l2_info['uvw'] = {
        'base_name': prefix+'efw-l2_e-hires-uvw_%Y%m%d_'+version+'.cdf',
        'local_path': [rbspx,'efw','l2','e-highres-uvw','%Y'],
        'remote_path': [rbspx,'l2','efw','e-highres-uvw','%Y'],
    }
    l2_info['vsvy-hires'] = {
        'base_name': prefix+'efw-l2_vsvy-hires_%Y%m%d_'+version+'.cdf',
        'local_path': [rbspx,'efw','l2','vsvy-highres','%Y'],
        'remote_path': [rbspx,'l2','efw','vsvy-highres','%Y'],
    }
    l2_info['spinfit'] = {
        'base_name': rbspx+'_efw-l2_e-spinfit-mgse_%Y%m%d_'+version+'.cdf',
        'local_path': [rbspx,'efw','l2','e-spinfit-mgse','%Y'],
        'remote_path': [rbspx,'l2','efw','e-spinfit-mgse','%Y'],
    }
    instr_info['l2'] = l2_info

    # Level 3 data.
    valid_date = {
        'a':['2012-09-18','2019-10-15'],
        'b':['2012-09-18','2019-07-17'],
    }
    l3_info = {
        'valid_date': valid_date[probe]
    }
    l3_info['spinfit'] = {
        'base_name': prefix+'efw-l3_%Y%m%d_'+version+'.cdf',
        'local_path': [rbspx,'efw','l3','%Y'],
        'remote_path': [rbspx,'l3','efw','%Y'],
    }
    instr_info['l3'] = l3_info

    # Fill in cadence and valid range using default values.
    instr_info['remote_root'] = remote_root
    instr_info['cadence'] = 'day'
    
    return instr_info

remote_info = {
    'cdaweb': get_instr_info_at_cdaweb,
    'umn': get_instr_info_at_umn,
}
avail_remote_servers = remote_info.keys()

class EFW:


    def __init__(self, probe) -> None:
        self.probe = probe

    
    def read(self, id, time_range, remote_server='cdaweb'):
        the_remote_info = remote_info[remote_server]



    def read_q_uvw2gse(self, time_range=None, probe='a'):

        for remote_server, get_instr_info in EFW.remote_root.items():
            try:
                instr_info = get_instr_info(probe)
                file_id = [remote_server,'ephemeris']
                # dl = DataLoader(time_range)
                # _ = dl.load_file(id=file_id)



            except:
                continue
        else:
            raise ValueError('No remote server is available')



    def read_efield_spinfit(self, time_range=None, probe='a'):
        pass

    def read_sc_pot(self):
        pass

    def read_density(self):
        pass