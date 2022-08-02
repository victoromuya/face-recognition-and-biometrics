# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'lbp_img.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication,QWidget, QVBoxLayout, QPushButton, QFileDialog , QLabel, QTextEdit, QMessageBox
from imutils import paths
import numpy as np
import imutils
import cv2
import os

class Ui_load_img(object):
    
    global subjects 
    subjects = ["", "George_Clooney","Matt_Damon","Nicolas_Cage","Tom_Cruise"]
    
    def detect_face(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2,minNeighbors=5);
        if (len(faces) == 0):
            return None, None
        (x, y, w, h) = faces[0]
        return gray[y:y+w, x:x+h], faces[0]
    
    def prepare_training_data(self, data_folder_path):
        dirs = os.listdir(data_folder_path)

        faces = []
    #list to hold labels for all subjects
        labels = []
    #let's go through each directory and read images within it
        for dir_name in dirs:     
        #our subject directories start with letter 's' so
        #ignore any non-relevant directories if any
            if not dir_name.startswith("s"):
                continue;
#------STEP-2--------
#extract label number of subject from dir_name
#format of dir name = slabel
#, so removing letter 's' from dir_name will give us label
            label = int(dir_name.replace("s", ""))
            subject_dir_path = data_folder_path + "/" + dir_name
            subject_images_names = os.listdir(subject_dir_path)
            for image_name in subject_images_names:    
            #ignore system files like .DS_Store
                if image_name.startswith("."):
                    continue;
            #build image path
            #sample image path = training-data/s1/1.pgm
                image_path = subject_dir_path + "/" + image_name
            #read image
                image = cv2.imread(image_path)
            #display an image window to show the image
            #cv2.imshow("Training on image...", image)
                cv2.waitKey(100)
            #detect face
                face, rect = self.detect_face(image)

                if face is not None:
                    faces.append(face)
                    labels.append(label)
                cv2.destroyAllWindows()
                cv2.waitKey(1)
        
        cv2.destroyAllWindows()
        return faces, labels
    
    def draw_rectangle(self, img, rect):
        (x, y, w, h) = rect
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
    def draw_text(self, img, text, x, y):
        cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)
    
    
    def predict(self, test_img):
        print("Preparing data...")
        faces, labels = self.prepare_training_data("C:/Users/HP/Documents/vics/spyders/face_detection_gabor/train")
        print("Data prepared")
        
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        face_recognizer.train(faces, np.array(labels))
        
        img = test_img.copy()
        face, rect = self.detect_face(img)
        label = face_recognizer.predict(face)
        label_text = subjects[label[0]]
        self.draw_rectangle(img, rect)
        self.draw_text(img, label_text, rect[0], rect[1]-5)
        return img
    
    def browse(self):
        fname = QFileDialog.getOpenFileName()
        self.imagePath = fname[0]
        
        pixmap = QPixmap(self.imagePath)
        self.lbl_img.setPixmap(QPixmap(pixmap))
        self.lbl_img.setScaledContents(True)

        """
        dir_name = self.imagePath.split("/")
        self.name = dir_name[-1]
        print(self.name[:-4])
        """
    
    def recog(self):
        f = open("imgpath.txt", 'r')
        thepath = f.read()
        realname = thepath.split("/")
        therealname = realname[-1]

        """
        dir_n = "C:/Users/HP/Documents/vics/spyders/face_detection_gabor/data/input/image.jpg"
        dir_name = dir_n.split("/")
        self.name = dir_name[-1]
        """
        
        test_img1 = cv2.imread(self.imagePath)
        # perform a prediction
        predicted_img1 = self.predict(test_img1)
        cv2.imshow(therealname[:-4], predicted_img1)
    
    def setupUi(self, load_img):
        load_img.setObjectName("load_img")
        load_img.resize(400, 202)
        self.lbl_back = QtWidgets.QLabel(load_img)
        self.lbl_back.setGeometry(QtCore.QRect(0, 0, 401, 201))
        self.lbl_back.setObjectName("lbl_back")
        self.lbl_img = QtWidgets.QLabel(load_img)
        self.lbl_img.setGeometry(QtCore.QRect(10, 10, 181, 151))
        self.lbl_img.setObjectName("lbl_img")

        """
        pixmap = QPixmap("C:/Users/HP/Documents/vics/spyders/face_detection_gabor/data/input/image.jpg")
        self.lbl_img.setPixmap(QPixmap(pixmap))
        self.lbl_img.setScaledContents(True)
          """  
      
        self.btn_browse = QtWidgets.QPushButton(load_img)
        self.btn_browse.setGeometry(QtCore.QRect(10, 170, 171, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.btn_browse.setFont(font)
        self.btn_browse.setObjectName("btn_browse")
        self.btn_browse.clicked.connect(self.browse)
     
        
        self.pushButton = QtWidgets.QPushButton(load_img)
        self.pushButton.setGeometry(QtCore.QRect(230, 50, 141, 91))
        font = QtGui.QFont()
        font.setFamily("Cambria")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.recog)

        self.retranslateUi(load_img)
        QtCore.QMetaObject.connectSlotsByName(load_img)

    def retranslateUi(self, load_img):
        _translate = QtCore.QCoreApplication.translate
        load_img.setWindowTitle(_translate("load_img", "face"))
        self.lbl_back.setText(_translate("load_img", ""))
        self.lbl_img.setText(_translate("load_img", ""))
        self.btn_browse.setText(_translate("load_img", "BROWSE"))
        self.pushButton.setText(_translate("load_img", "RECOGNIZE"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    load_img = QtWidgets.QDialog()
    ui = Ui_load_img()
    ui.setupUi(load_img)
    load_img.show()
    sys.exit(app.exec_())