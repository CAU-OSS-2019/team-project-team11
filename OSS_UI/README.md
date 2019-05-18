# Open-Source S/W project - Minimum UI

1. need to run
* PyQT5
* Python 3. over
2. Code preview
```python
layout = QtWidgets.QVBoxLayout()

        layout.addWidget(self.face_detection_widget)
        self.run_button = QtWidgets.QPushButton('Start')
        layout.addWidget(self.run_button)
        self.btn = QPushButton("NSFW")
        layout.addWidget(self.btn)
        self.le = QLabel("")
        
        layout.addWidget(self.le)
        self.btn.clicked.connect(self.getfile)
        self.run_button.clicked.connect(self.record_video.start_recording)
        self.setLayout(layout)
```
* start button for start webcam and face detector
* NSFW button for open file and show in window
