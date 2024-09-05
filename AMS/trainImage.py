import os, cv2
import numpy as np
from PIL import Image

def TrainImage(haarcasecade_path, trainimage_path, trainimagelabel_path, message, text_to_speech):
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(haarcasecade_path)
    faces, Ids = getImagesAndLabels(trainimage_path, detector)
    
    recognizer.train(faces, np.array(Ids))
    recognizer.save(trainimagelabel_path)
    
    # Save each trained image (Optional)
    save_trained_images(trainimage_path, faces, Ids)
    
    res = "Image Trained successfully"
    message.configure(text=res)
    text_to_speech(res)

def getImagesAndLabels(path, detector):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    Ids = []

    for imagePath in imagePaths:
        if os.path.isfile(imagePath):
            try:
                pilImage = Image.open(imagePath).convert("L")
                imageNp = np.array(pilImage, "uint8")
                Id = int(os.path.split(imagePath)[-1].split("_")[1])

                facesDetected = detector.detectMultiScale(imageNp)
                for (x, y, w, h) in facesDetected:
                    faces.append(imageNp[y:y + h, x:x + w])
                    Ids.append(Id)

            except Exception as e:
                print(f"Error processing file {imagePath}: {e}")

    return faces, Ids

# Function to save each face after training
def save_trained_images(directory, faces, Ids):
    save_path = os.path.join(directory, "TrainedFaces")
    
    # Create directory if it doesn't exist
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    
    for i, face in enumerate(faces):
        file_name = os.path.join(save_path, f"Face_{Ids[i]}.jpg")
        cv2.imwrite(file_name, face)
        print(f"Saved: {file_name}")
