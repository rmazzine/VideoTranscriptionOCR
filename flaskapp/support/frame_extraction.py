import base64
import cv2


def frame_extraction(video_name):
    """Gets a filename, extracts a pic after each 10 seconds

    :param video_name: The video file path
    :return: (list) List with with the frames file paths
    """
    vidcap = cv2.VideoCapture(video_name)

    fr = vidcap.get(cv2.CAP_PROP_FPS)

    print(fr)

    success, image = vidcap.read()
    count = 0

    screenshot_file_names = []
    while success:
        if count % float(int(fr)*10) == 0:
            screenshot_fn = f'{video_name}_sc_{count}.jpg'
            # save frame as JPEG file
            cv2.imwrite(screenshot_fn, image)
            screenshot_file_names.append(screenshot_fn)

        success, image = vidcap.read()
        count += 1

    return screenshot_file_names
