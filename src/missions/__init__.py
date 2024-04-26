
supported_missions = dict()
def register_mission(the_mission):
    supported_missions[the_mission.name] = the_mission
    return the_mission

import missions.rbsp.rbsp
import missions.themis.themis