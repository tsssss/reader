from model import Project, Event, DataRequest


def test_create_project_event_request():
    project = Project('2024_low_lshell_outflow')
    print(f'project.id: {project.id}')
    print(f'project.root_dir: {project.root_dir}')
    print(f'project.plot_dir: {project.plot_dir}')
    event_id = '2024_0404_01'
    event = project.add_event(event_id, time_range=['2014-04-01','2014-04-02'])
    print(f'event.id: {event_id}')
    print(f'event.plot_dir: {event.plot_dir}')
    print(f'event.data_dir: {event.data_dir}')

    event2 = project.add_event(time_range=['2014_0401','2014_0402'])

    assert project.has_event(event_id)
    assert project.has_event(event2)

    project.del_event(event_id)
    assert project.has_event(event_id) is False
    project.del_event(event2)
    assert project.has_event(event2) is False

    
    data_request = event.add_data_request('rbsp','efield',settings={'probe':'a','spin_axis':'edot0'})
    print(f'data_request.mission: {data_request.mission}')
    print(f'data_request.phys_quant: {data_request.phys_quant}')
    print(f'data_request.id: {data_request.id}')
    assert event.has_data_request(data_request)
    var = event.read_data()
    var = event.read('rbsp','efield',settings={'probe':'b','spin_axis':'e0'})
    var = event.read('rbsp','efield',probe='a')
    var = event.read('rbsp','bfield',probe='a')




if __name__ == '__main__':
    test_create_project_event_request()