from missions import register_mission
from cotrans import regiser_coord

@register_mission
class THEMIS:
    id = 'themis'


@regiser_coord
def themis_dsl2gse():
    pass

@regiser_coord
def gse2themis_dsl():
    pass