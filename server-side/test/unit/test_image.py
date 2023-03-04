# test structure adapted from: https://www.youtube.com/watch?v=OcD52lXq0e8

from app import Image

def test_new_image():
    """
    GIVEN an Image model
    WHEN a new Image is uploaded to the system
    THEN check if the image has the correct defined and default data
    """
    image = Image(0, 'src/assets/user_images/sage.jpg', 0, 0, 'test_dataset')

    assert image.image_id == 0
    assert image.path == 'src/assets/user_images/sage.jpg'
    assert image.uploader_id == 0
    assert image.upload_id == 0
    assert image.dataset_name == 'test_dataset'
    assert image.verifier_id == None
    assert image.label == None
    assert image.location == None
    assert image.access == 0