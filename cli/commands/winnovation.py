from time import sleep

import click
import cv2
import os

from core.face_recognition import get_face_embeddings, use_cuda, init
from core.search import retrieve_knn_search_data


@click.command("winnovation", hidden=True)
@click.option('--debug/--no-debug', default=False)
def winnovation(debug: bool) -> None:
    """
    This command takes a photo using opencv once a face has been detected and then searches for similar faces in the database.
    """
    root_dir = os.path.abspath(os.path.join(
        os.path.dirname(__file__), "..", ".."))
    cv2_cascade = os.path.join(
        root_dir, "core", "data", "haarcascade_frontalface_default.xml")

    cuda = use_cuda(True)
    init(cuda)

    # define a video capture object
    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(cv2_cascade)

    cv2.namedWindow("frame", cv2.WINDOW_NORMAL)

    while (True):
        cv2.setWindowTitle("frame", "AG-Systeem demo Winnovation")

        # Capture the video frame by frame
        ret, frame = cam.read()
        frame = cv2.flip(frame, 1)

        frame_copy = frame.copy()
        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame_copy, cv2.COLOR_BGR2GRAY)

        # Detect the faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw the rectangle around each face
        for (x, y, w, h) in faces:
            cv2.rectangle(
                frame_copy, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Display the resulting frame
        cv2.imshow('frame', frame_copy)

        keyPressed = cv2.waitKey(5)

        # Quit the program if the user presses 'q'
        if keyPressed:
            if keyPressed == ord('q'):
                print("Quitting...")
                break
            if keyPressed == 32:
                print("Processing photo...")

                # If there is a face detected, lookup the best match in the Elasticsearch database
                if len(faces) > 0:
                    try:
                        face_embeddings = get_face_embeddings(frame, cuda)

                        for face_emb in face_embeddings:
                            face_data = retrieve_knn_search_data(
                                face_emb['face_embedding'])
                            if face_data['hits']['total']['value'] > 0:
                                print(
                                    f"Found a match for {face_data['hits']['hits'][0]['_source']['file_name']}")

                                # Show frame and match next to each other
                                try:
                                    image_path = os.path.join(
                                        root_dir,
                                        face_data['hits']['hits'][0]['_source']['dataset'],
                                        face_data['hits']['hits'][0]['_source']['file_name']
                                    )

                                    print(f"Loading image from {image_path}")
                                    match = cv2.imread(image_path)

                                    # Draw the rectangle around each face
                                    for (x, y, w, h) in faces:
                                        cv2.rectangle(
                                            frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

                                    match_output = vconcat_resize_min(
                                        [frame, match])
                                    cv2.setWindowTitle(
                                        "frame", f"Match: {face_data['hits']['hits'][0]['_score'] * 100:.2f}%")
                                    cv2.imshow("frame", match_output)
                                    cv2.waitKey(0)
                                except Exception as e:
                                    print(f"Error loading image: {e}")
                                    pass

                            break
                    except Exception as e:
                        print(f"Error retrieving face embeddings: {e}")
                        pass

    # After the loop release the cap object
    cam.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


def vconcat_resize_min(im_list, interpolation=cv2.INTER_CUBIC):
    w_min = min(im.shape[1] for im in im_list)
    im_list_resize = [cv2.resize(im, (w_min, int(
        im.shape[0] * w_min / im.shape[1])), interpolation=interpolation) for im in im_list]
    return cv2.vconcat(im_list_resize)
