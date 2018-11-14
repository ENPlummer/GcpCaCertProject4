import io

from google.cloud import storage
from google.cloud import vision
from google.cloud.vision import types

def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))

    return destination_file_name

def detect_labels(destination_file_name):

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # The name of the image file to annotate
    file_name = destination_file_name

    # Loads the image into memory
    with io.open(file_name, 'rb') as image_file:
        content = image_file.read()

    image = types.Image(content=content)

    # Performs label detection on the image file
    response = client.label_detection(image=image)
    labels = response.label_annotations

    print('Labels:')
    for label in labels:
        print(label.description)


def analyze_image(event, context):
    """Triggered by a change to a Cloud Storage bucket.
    Args:
         event (dict): Event payload.
         context (google.cloud.functions.Context): Metadata for the event.
    """
    print(event)
    bucket_name = event['bucket']
    source_blob_name = event['name']
    destination_file_name = '/tmp/file.jpg'
    detect_labels(download_blob(bucket_name, source_blob_name, destination_file_name))
