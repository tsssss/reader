from missions import register_mission
from cotrans import regiser_coord
from missions.rbsp.efw import EFW


@register_mission
class RBSP:

    probes = ['a','b']
    id = 'rbsp'
    efw = EFW()


    def __init__(self, probe=None, **kwargs):
        if probe not in RBSP.probes:
            raise ValueError(f'Invalid probe {probe}')
        self.probe = probe
        self.prefix = 'rbsp'+probe+'_'
        self.prefix2 = 'rbsp'+'_'+probe+'_'
    
    def efield(self, time_range, coord='rbsp_mgse', spin_axis='e0', **kwargs):
        probe = self.probe
        pass

    avail_phys_quants = [efield]
    avail_instruments = [EFW]


@regiser_coord
def rbsp_uvw2gse():
    pass

@regiser_coord
def gse2rbsp_uvw():
    pass

@regiser_coord
def gse2rbsp_mgse():
    pass


@regiser_coord
def rbsp_mgse2gse():
    pass