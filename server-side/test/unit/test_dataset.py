# test structure adapted from: https://www.youtube.com/watch?v=OcD52lXq0e8

from app import Dataset

def test_new_dataset():
    """
    GIVEN a Dataset model
    WHEN a new Dataset is created during image upload
    THEN check if the dataset has the proper data
    """
    dataset = Dataset("Site 1 Dataset", "Nevada Wildfire Research")

    assert dataset.dataset_name == "Site 1 Dataset"
    assert dataset.project_name == "Nevada Wildfire Research"