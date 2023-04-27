# test structure adapted from: https://www.youtube.com/watch?v=OcD52lXq0e8

from app import Dataset

def test_new_dataset():
    """
    GIVEN a Dataset model
    WHEN a new Dataset is created during image upload
    THEN check if the dataset has the proper data
    """
    dataset = Dataset("Nevada Wildfire Research", "Understanding wildfires")

    assert dataset.name == "Nevada Wildfire Research"
    assert dataset.description == "Understanding wildfires"
    assert dataset.project_id == None