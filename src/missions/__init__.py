
avail_missions = dict()
def register_mission(mission):
    avail_missions[mission.id] = mission
    return mission

import missions.rbsp.rbsp as rbsp
import missions.themis.themis as themis