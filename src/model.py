import os
import yaml
from missions import supported_missions


from os.path import expanduser
def homedir():
    return expanduser('~')

def join_path(*args):
    return os.path.join(*args)


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


default_project_id = 'slib'
default_project_dir = join_path(homedir(),'projects')
default_event_id = 'generic'
default_event_dir = join_path(default_project_dir,default_project_id)

class Event:

    def __init__(self, id=default_event_id, time_range=[],
        dir=default_event_dir, 
        plot_dir=None,
        data_dir=None,
        ) -> None:
        self.id = id
        self.dir = dir
        self.time_range = time_range

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
            the_mission = (supported_missions[mission])(**settings)
            the_func = getattr(the_mission,phys_quant)
            time_range = data_request.time_range

            print(f'Processing data_request: {data_request.id}')
            return the_func(time_range, **settings)

    def read_data(self, data_requests=None):
        if data_requests is None:
            data_requests = self.data_requests
        for data_request in data_requests:
            self.process_data_request(data_request)
    
    def read(self, mission, phys_quant, time_range=None, settings={}, **kwargs):
        # Sheng: does order of kwargs and settings matter? 2024_0426.
        data_request = self.add_data_request(mission, phys_quant, time_range, {**kwargs,**settings})
        return self.process_data_request(data_request)


class Project:
    def __init__(self, id=default_project_id, dir=default_project_dir) -> None:
        self.id = id
        self.dir = dir
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




# # Function to load configuration from a YAML file
# def load_config(file_path):
#     with open(file_path, "r") as file:
#         config = yaml.safe_load(file)
#     return config
# 
# # Example Usage:
# config_path = "config.yml"
# config = load_config(config_path)
# 
# # Specify the project id and event id when creating the Project and Event instances
# project_id = "project_1"
# id = "1"
# 
# # Creating a Project instance using the loaded configuration and the specified id
# project_config = next((p for p in config.get("projects", []) if p["id"] == project_id), {})
# 
# if project_config:
#     local_project_root = join_path(config["default_local_root"], project_id)
# 
#     project = Project(id=project_id, dir=local_project_root,)
# 
#     # Creating an Event instance with the specified event id
#     event = Event(id=id, time_range=["2023-01-01T00:00:00", "2023-01-02T00:00:00"], data_requests=[])
# 
#     # Adding an event to the project
#     project.add_event(event)
# 
#     # Accessing the event dir directly
#     print(f"Event dir: {event.dir}")
# 
#     # Checking equality based on identity
#     print(f"Are project and event equal? {project == event}")
# else:
#     print(f"Project with id '{project_id}' not found in the configuration.")

