from app import Project

test_data = {'project-name': "Wildfire Research",
             'user-id': 1}

def test_new_project():
    """
    GIVEN a Project model
    WHEN a new Project is created from Collections
    THEN check if the Project entry has the proper data
    """
    project_name = test_data["project-name"]
    owner_id = test_data["user-id"]
    project = Project(project_name, owner_id)

    assert project.name == test_data["project-name"]
    assert project.owner_id == test_data["user-id"]