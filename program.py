import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QSlider, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2
import numpy as np

class ImageProcessor(QWidget):
    def __init__(self):
        super().__init__()

        # 이미지와 변환된 이미지를 저장할 변수
        self.image = None
        self.processed_image = None
        self.previous_image = None
        self.current_button = None  # 현재 선택된 버튼을 저장하는 변수
        self.mode = None  # 현재 모드를 저장하는 변수
        
        # UI 초기화
        self.init_ui()

    def init_ui(self):
        # 이미지 표시 레이블
        self.image_label = QLabel(self)

        # 버튼 초기화
        self.btn_load = QPushButton('이미지 등록', self)
        self.btn_process = QPushButton('프로그램 실행', self)
        self.btn_brightness = QPushButton('밝기 조절', self)
        self.btn_contrast = QPushButton('대비 조절', self)
        self.btn_edge = QPushButton('에지 강조', self)
        self.btn_morphology = QPushButton('모폴로지', self)
        self.btn_binarization = QPushButton('이진화', self)
        self.btn_save = QPushButton('이미지 파일 저장', self)
        self.btn_cancel = QPushButton('초기화', self)
        self.btn_exit = QPushButton('종료', self)

        # 전처리 조절 버튼 초기화
        self.btn_brightness.clicked.connect(self.slider_brightness_changed)
        self.btn_contrast.clicked.connect(self.slider_contrast_changed)
        self.btn_morphology.clicked.connect(self.slider_morphology_changed)
        self.btn_binarization.clicked.connect(self.slider_binarization_changed)
        self.btn_edge.clicked.connect(self.slider_edge_changed)
        
        # '완료' 버튼 초기화
        self.btn_complete = QPushButton('완료', self)
        self.btn_complete.setEnabled(False)  # 초기에는 비활성화 상태
        
        
        # 트랙바 초기화
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.slider_value_changed)
        # 트랙바 값을 표시할 QLabel 초기화
        self.label_slider_value = QLabel('여기에 전처리 threshold 파라미터가 표시됩니다', self)

        # 버튼 비활성화
        self.disable_buttons()

        # 버튼에 함수 연결
        self.btn_load.clicked.connect(self.load_image)
        self.btn_process.clicked.connect(self.process_image)
        self.btn_save.clicked.connect(self.save_image)
        self.btn_cancel.clicked.connect(self.cancel_process)
        self.btn_exit.clicked.connect(self.close)
        self.btn_complete.clicked.connect(self.complete_process)

        # 레이아웃 초기화
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.btn_load)
        vbox.addWidget(self.btn_process)
        vbox.addWidget(self.btn_brightness)
        vbox.addWidget(self.btn_contrast)
        vbox.addWidget(self.btn_edge)
        vbox.addWidget(self.btn_binarization)
        vbox.addWidget(self.btn_morphology)
        vbox.addWidget(self.slider)
        vbox.addWidget(self.btn_complete) 
        vbox.addWidget(self.btn_cancel)
        vbox.addWidget(self.btn_save)
        vbox.addWidget(self.btn_exit)
        # 레이아웃에 QLabel 추가
        vbox.addWidget(self.label_slider_value)
        

        self.setLayout(vbox)
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('이미지 전처리 프로그램')
        self.show()

    def load_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "이미지 열기", "", "Images (*.png *.jpg *.bmp *.jpeg);;All Files (*)", options=options)

        if file_name:
            self.image = cv2.imread(file_name)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.processed_image = np.copy(self.image)
            self.result_image = np.copy(self.image)
            print('process image shape:', self.processed_image.shape)
            self.display_image()

    def display_image(self):
        if self.processed_image is not None:
            # 이미지 크기를 512x512로 리사이즈
            displayed_image = cv2.resize(self.processed_image, (512, 512))
            
            # 이미지를 그레이스케일로 변환
            displayed_image_gray = cv2.cvtColor(displayed_image, cv2.COLOR_BGR2GRAY)
            
            bytes_per_line = 1 * displayed_image_gray.shape[1]  # gray 채널이므로 1채널

            q_image = QImage(displayed_image_gray.data, displayed_image_gray.shape[1], displayed_image_gray.shape[0], bytes_per_line, QImage.Format_Grayscale8)
            pixmap = QPixmap.fromImage(q_image)

            # QLabel에 전체 이미지를 표시
            self.image_label.setPixmap(pixmap)
            self.image_label.setAlignment(Qt.AlignCenter)
        else:
            # 이미지가 없을 때는 빈 QLabel로 설정
            self.image_label.clear()

    def process_image(self):
        # 이미지 처리 로직 추가
        # self.processed_image = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
        # 실시간 업데이트
        self.processed_image = np.copy(self.image)
        self.display_image()
        
        # 버튼 활성화
        self.enable_buttons()
        
        
    def btn_clicked(self):
        # 각 버튼이 클릭되었을 때 호출되는 메서드
        self.current_button = self.sender()
        
    def complete_process(self):
        # '완료' 버튼을 눌렀을 때의 동작 구현
        # 선택한 버튼만 활성화
        if self.current_button is not None:
            button_text = self.current_button.text()
            self.disconnect_previous_signal()

        self.enable_buttons()  # 다른 버튼들 활성화
        print('처리가 완료되었습니다. 다른 기능을 실행하세요.')
        
    def disconnect_previous_signal(self):
        # 이전에 선택된 버튼에 대한 이전 시그널을 제거
        button_text = self.current_button.text()
        if button_text == '밝기 조절':
            self.btn_brightness.clicked.disconnect(self.slider_brightness_changed)
        elif button_text == '대비 조절':
            self.btn_contrast.clicked.disconnect(self.slider_contrast_changed)
        elif button_text == '모폴로지':
            self.btn_morphology.clicked.disconnect(self.slider_morphology_changed)
        elif button_text == '이진화':
            self.btn_binarization.clicked.disconnect(self.slider_binarization_changed)
        elif button_text == '에지 강조':
            self.btn_edge.clicked.disconnect(self.slider_edge_changed)
            
            
########################## 트랙바 조절 #######################################



    def slider_brightness_changed(self):
        self.btn_clicked()
        print('밝기 조정을 시작합니다.')
    
        # 나머지 버튼은 비활성화
        self.btn_contrast.setEnabled(False)
        self.btn_edge.setEnabled(False)
        self.btn_morphology.setEnabled(False)
        self.btn_binarization.setEnabled(False)  
        
        self.previous_image = self.processed_image
        
        self.slider.setValue(0)
        self.slider.setMinimum(-50)
        self.slider.setMaximum(50)
        self.slider.setSingleStep(1)
        
        self.mode = 1
        self.display_image()
        
    def slider_contrast_changed(self):
        self.btn_clicked()
        print('대비 조정을 시작합니다.')
        
        # 나머지 버튼은 비활성화
        self.btn_brightness.setEnabled(False)
        self.btn_edge.setEnabled(False)
        self.btn_morphology.setEnabled(False)
        self.btn_binarization.setEnabled(False)  
        
        self.previous_image = self.processed_image
        
        self.slider.setValue(5) 
        self.slider.setMinimum(-5)
        self.slider.setMaximum(15)
        self.slider.setSingleStep(1) 
        
        self.mode = 2
        self.display_image()
    
    def slider_edge_changed(self):
        self.btn_clicked()
        print('에지 강조 조정을 시작합니다.')
        
        # 나머지 버튼은 비활성화
        self.btn_brightness.setEnabled(False)
        self.btn_contrast.setEnabled(False)
        self.btn_morphology.setEnabled(False)
        self.btn_binarization.setEnabled(False)  
        
        self.previous_image = self.processed_image
        
        self.slider.setValue(0) 
        self.slider.setMinimum(100)
        self.slider.setMaximum(225)
        self.slider.setSingleStep(1) 
        
        self.mode = 5
        self.display_image()
    
        
    def slider_morphology_changed(self):
        self.btn_clicked()
        print('모폴로지 조정을 시작합니다.')
        # 나머지 버튼은 비활성화
        self.btn_contrast.setEnabled(False)
        self.btn_edge.setEnabled(False)
        self.btn_brightness.setEnabled(False)
        self.btn_binarization.setEnabled(False)  
        
        self.previous_image = self.processed_image
        
        self.slider.setValue(5)
        self.slider.setMinimum(2)
        self.slider.setMaximum(10)
        self.slider.setSingleStep(1)
        
        self.mode = 3
        self.display_image()
        
    def slider_binarization_changed(self):
        self.btn_clicked()
        print('이진화 조정을 시작합니다.')
        # 나머지 버튼은 비활성화
        self.btn_contrast.setEnabled(False)
        self.btn_edge.setEnabled(False)
        self.btn_morphology.setEnabled(False)
        self.btn_brightness.setEnabled(False)  
        
        self.previous_image = self.processed_image
        
        self.slider.setValue(100) 
        self.slider.setMinimum(0)
        self.slider.setMaximum(255)
        self.slider.setSingleStep(1)
        
        self.mode = 4
        self.display_image()
        
        
        
    
    def slider_value_changed(self): 
        self.display_image()
        
        # 트랙바 값에 따라 전처리 함수를 호출
        if self.mode == 1:
            self.processed_image = self.adjust_brightness(self.previous_image)
        elif self.mode == 2:
            self.processed_image = self.adjust_contrast(self.previous_image)
        elif self.mode == 3:
            self.processed_image = self.apply_morphology(self.previous_image)
        elif self.mode == 4:
            self.processed_image = self.apply_binarization(self.previous_image)
        elif self.mode == 5:
            self.processed_image = self.apply_edge(self.previous_image)
            
        # QLabel에 트랙바 값 표시
        self.label_slider_value.setText(str(self.slider.value()))
        self.display_image()
        
        
        
    ############################ 전처리 버튼 ###############################################
    
    
    def adjust_brightness(self, image):
        factor = self.slider.value()  # -50 ~ +50 까지 1씩 변화
        print('현재 밝기 조정중', factor)
        # 밝기 조절 로직
        return cv2.convertScaleAbs(image, alpha=1, beta=factor)


    def adjust_contrast(self, image):
        factor = self.slider.value() / 5 # -2 ~ +2 까지 0.2씩 변화
        print('현재 대비 조정중', factor)
        # 대비 조절 로직
        return cv2.convertScaleAbs(image, alpha=factor)


    def apply_morphology(self, image): 
        factor = self.slider.value() / 10 # factor은 diameter_threshold_mm
        print('현재 모폴로지 조정중', factor)
        # 모폴로지 로직
        # 모폴로지 연산을 위한 구조 요소 생성 (원형)
        kernel_size = int((factor / 2) * 10)  # 직경이 1mm 미만인 경우를 고려하여 크기 조정
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kernel_size, kernel_size))
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

        
    def apply_binarization(self, image):
        factor = self.slider.value() # factor은 binary threshold
        print('현재 이진화 조정중', factor)
        # 이진화 로직
        _, binarized_image = cv2.threshold(image, factor, 255, cv2.THRESH_BINARY)
        return binarized_image


    def apply_edge(self, image):
        factor = self.slider.value()
        print('현재 에지 강조 조정중', factor) # 100~255까지 1씩 증가
        #에지 강조 로직
        edges = cv2.Canny(image, factor, 225)
        # 에지의 윤곽을 찾음
        contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # 에지 안쪽을 색칠하기 위한 빈 이미지 생성
        filled_image = np.zeros_like(image)
        # 에지 윤곽을 그림
        cv2.drawContours(filled_image, contours, -1, (255, 255, 255), thickness=cv2.FILLED)
        # 색칠된 이미지와 원본 이미지를 합침
        result_image = cv2.addWeighted(image, 1, filled_image, 0.5, 0)
        
        return result_image


    ############################# 저장 및 종료 ########################################


    def save_image(self):
        # 이미지를 그레이스케일로 변환
        gray_image = cv2.cvtColor(self.processed_image, cv2.COLOR_BGR2GRAY)
        cv2.imwrite("saved_image.png", gray_image)
        QMessageBox.information(self, '알림', '이미지가 저장되었습니다.')

    def cancel_process(self):
        self.processed_image = np.copy(self.image) # 초기화
        self.display_image()
        self.disable_buttons()
        self.enable_buttons()

    def enable_buttons(self):
        # 버튼 활성화
        self.btn_brightness.setEnabled(True)
        self.btn_contrast.setEnabled(True)
        self.btn_edge.setEnabled(True)
        self.btn_morphology.setEnabled(True)
        self.btn_binarization.setEnabled(True)
        self.btn_save.setEnabled(True)
        self.btn_cancel.setEnabled(True)
        self.btn_complete.setEnabled(True) 

    def disable_buttons(self):
        # 버튼 비활성화
        self.btn_brightness.setEnabled(False)
        self.btn_contrast.setEnabled(False)
        self.btn_edge.setEnabled(False)
        self.btn_morphology.setEnabled(False)
        self.btn_binarization.setEnabled(False)
        self.btn_save.setEnabled(False)
        self.btn_cancel.setEnabled(False)
        self.btn_complete.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageProcessor()
    sys.exit(app.exec_())
