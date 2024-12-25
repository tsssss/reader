from missions import register_mission
from cotrans import regiser_coord

# Need to import each instrument here.
from missions.rbsp.efw import EFW


@register_mission
class RBSP:

    probes = ['a','b']
    id = 'rbsp'

    def __init__(self, probe=None, **kwargs):
        if probe not in RBSP.probes:
            raise ValueError(f'Invalid probe {probe}')
        self.probe = probe
        self.prefix = 'rbsp'+probe+'_'
        self.prefix2 = 'rbsp'+'_'+probe+'_'
    

        # Instantiate and register each instrument.
        self.avail_instruments = []
        self.efw = EFW(probe)
        self.avail_instruments.append(self.efw)


    

    # Functions that read physical quantities.
    def efield(self, time_range, coord='rbsp_mgse', spin_axis='e0', **kwargs):
        var = self.efw.read('l3', time_range, **kwargs)
        pass

    # Need to register each function that reads physical quantities.
    avail_phys_quants = [efield]


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