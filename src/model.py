from missions import avail_missions
from io.utils import join_path, get_home_dir, file_exists
import io

cache = {}



default_local_root = join_path(get_home_dir(),'data')
default_project_id = 'slib'
default_project_dir = join_path(get_home_dir(),'projects')
default_event_id = 'generic'
default_event_dir = join_path(default_project_dir,default_project_id)


class DataRequest:

    def __init__(self, mission, phys_quant, time_range, settings=None) -> None:
        self.mission = mission
        self.phys_quant = phys_quant
        self.time_range = tuple(time_range)
        self.settings = settings
    
    def __key(self):
        the_key = [self.mission,self.phys_quant,self.time_range]
        if self.settings is not None:
            for key,val in self.settings.items():
                the_key.append((key,val))
        return tuple(the_key)

    def __hash__(self) -> int:
        return hash(self.__key())

    @property
    def id(self):
        return self.__key()


class Event:

    def __init__(self,
        id=default_event_id,
        time_range=[],
        dir=default_event_dir, 
        local_root=default_local_root,
        plot_dir=None,
        data_dir=None,
        data_file=None,     # Set to save data to this file. Otherwise just load data to memory.
        ) -> None:

        self.id = id
        self.dir = dir
        self.time_range = time_range
        self.local_root = local_root
        if data_file is None:
            self.data_file = None
        else:
            self.data_file = io.file(data_file)

        self.root_dir = join_path(dir,id)
        if data_dir is None:
            data_dir = join_path(self.root_dir,'data')
        self.data_dir = data_dir
        if plot_dir is None:
            plot_dir = join_path(self.root_dir,'plot')
        self.plot_dir = plot_dir
        self.data_requests = set()
    
    def __key(self):
        return (self.id)
    
    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other):
        # Check for equality based on identity (id)
        return isinstance(other, Event) and self.__key() == other.__key()

    def add_data_request(self, mission, phys_quant, time_range=None, settings=None):
        # Add validation or business logic if needed
        # self.data_requests.append(data_request)
        if time_range is None:
            time_range = self.time_range
        data_request = DataRequest(mission, phys_quant, time_range, settings)
        self.data_requests.add(data_request)
        return data_request
    
    def has_data_request(self, data_request_info):
        if isinstance(data_request_info, DataRequest):
            return data_request_info in self.data_requests
        else:
            for data_request in self.data_requests:
                if data_request_info == data_request.id:
                    return True
            else:
                return False
    
    def del_data_request(self, data_request_info):
        if isinstance(data_request_info, DataRequest):
            self.data_requests.remove(data_request_info)
        else:
            for data_request in self.data_requests:
                if data_request_info == data_request.id:
                    self.data_requests.remove(data_request)
                    break

    def process_data_request(self, data_request):
        if self.has_data_request(data_request) is False:
            print(f'data_request is not found')
            return None
        else:
            mission = data_request.mission
            phys_quant = data_request.phys_quant
            settings = data_request.settings
            the_mission = (avail_missions[mission])(**settings)
            # obj_func = getattr(the_mission,phys_quant)
            for class_func in the_mission.avail_phys_quants:
                if class_func.__name__ == phys_quant:
                    break
            else:
                print(f'{the_mission.id} does not implement reading function for {phys_quant} yet')
                return None
            
            time_range = data_request.time_range
            print(f'Processing data_request: {data_request.id}')
            # return obj_func(the_mission, time_range, **settings)
            return class_func(the_mission, time_range, **settings)

    def read_data(self, data_requests=None):
        if data_requests is None:
            data_requests = self.data_requests
        for data_request in data_requests:
            self.process_data_request(data_request)
    

    # This is where we do smart things.
    def read(self,
        mission,
        phys_quant,
        time_range=None,
        update=False,       # Set to update the actual data.
        get_name=False,     # This is to get the default var_info.
        var_info=None,      # This is rename vars.
        local_root=default_local_root,
        dep_vars=[],     # Set this to interpolate data to these depend_vars.
        **kwargs):


        # Sheng: does order of kwargs and settings matter? 2024_0426.
        the_settings = {**kwargs}
        data_request = self.add_data_request(mission, phys_quant, time_range, the_settings)

        # Get orig var_info.
        name_request = data_request.copy()
        name_request['get_name'] = True
        orig_var_info = self.process_data_request(name_request)
        if var_info is None: var_info = orig_var_info
        if get_name: return orig_var_info

        # Try to load from memory.
        if update:
            cache.del_var(var_info)
        if not cache.check_if_update(var_info, data_request.id):
            return var_info

        
        # Try to load from data file.
        if self.data_file is not None:
            if update:
                with open(self.data_file.name):
                    self.data_file.del_var(var_info)
            try:
                self.data_file.read_var(var_info, cache=cache)
            except:
                pass

        # Try to load from mission based routines.
        orig_var_info = self.process_data_request(data_request)
        for orig_var,var in enumerate(orig_var_info,var_info):
            cache.rename_var(orig_var,output=var)
        
        # Deal with dep_vars.
        cache.interp_var(var_info, dep_vars)
        
        # Save to file.
        if self.data_file is not None:
            with open(self.data_file.name):
                for var in var_info:
                    self.data_file.save_var(var)

        return var_info


class Project:

    def __init__(self,
        id=default_project_id,          # the id of the project.
        dir=default_project_dir,        # the path of the project.
        local_root=default_local_root,  # the path to save the mission-based data files.
        ) -> None:

        self.id = id
        self.dir = dir
        self.local_root = join_path(local_root)
        self.root_dir = join_path(dir,id)
        self.data_dir = join_path(self.root_dir,'data')
        self.plot_dir = join_path(self.root_dir,'plot')
        self.file = join_path(self.root_dir,self.id+'_project_info.dat')
        self.events = set()
    
    def __key(self):
        return self.id

    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other):
        # Check for equality based on identity (id)
        return isinstance(other, Project) and self.__key() == other.__key()
    

    def add_event(self, event_id=None, time_range=None, dir=None):
        # Add validation or business logic if needed
        if event_id is None:
            if time_range is None:
                event_id = default_event_id
            else:
                event_id = time_range[0]
        print(f'Adding Event {event_id} to Project {self.id}')
        if dir is None: dir = self.root_dir
        data_dir = join_path(self.data_dir,event_id)
        plot_dir = join_path(self.plot_dir,event_id)
        event = Event(event_id, time_range, dir, plot_dir=plot_dir, data_dir=data_dir)
        self.events.add(event)
        return event
    
    def get_event(self, event_id):
        for event in self.events:
            if event_id == event.id:
                return event
        else:
            return None
    
    def has_event(self, event_info):
        if isinstance(event_info, Event):
            return event_info in self.events
        else:
            for event in self.events:
                if event_info == event.id:
                    return True
            else:
                return False
    
    def del_event(self, event_info):
        if isinstance(event_info, Event):
            self.events.remove(event_info)
        else:
            for event in self.events:
                if event_info == event.id:
                    self.events.remove(event)
                    break