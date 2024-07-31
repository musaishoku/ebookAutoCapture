# ebookAutoCapture

![image](https://github.com/user-attachments/assets/89204895-e468-411e-8847-c34506cd1792)

### 프로그램 소개

e북을 이미지로 자동으로 캡쳐해서 저장해주는 간단한 프로그램입니다!
저장된 이미지 파일들을 묶어서 PDF파일로 만들던가 해서 쓰면 됩니다.

종이책을 사서 들고 다니기는 불편하고, e북은 원하는 필기 앱에 넣어서 쓸 수가 없는게 불편해서,
이런 불편함을 해결해보고자 직접 만들어봤습니다.


### 사용방법

이 프로그램은 윈도우11 yes24,알라딘 e북 리더 환경에서만 테스트 되었습니다. 

실행시 반드시 관리자 권한으로 실행해야 합니다! 그래야지만 pyautogui라이브러리가 제대로 동작하더라구요ㅠ

1. 먼저 캡처 영역부터 설정해야 합니다. 원하는 영역의 왼쪽 상단과 오른쪽 하단의 좌표를 기입하는 방식입니다. '좌표 설정'버튼을 누른 후 마우스 커서를 원하는 위치로 옮기고, 스페이스바를 눌러줍니다. 그러면 좌표가 기입됩니다! 왼쪽 오른쪽 둘 다 같은 방식으로 진행해 주시면 됩니다.
2. 몇 페이지를 캡쳐할 것인지 총 페이지 수를 기입해 줍니다. 기입된 수만큼 프로그램이 자동으로 페이지를 넘기면서 캡쳐합니다.
3. 파일 이름을 기입합니다.
4. 슬라이더를 움직여서 캡쳐 간격을 설정합니다. e북 리더의 페이지 로딩 속도에 맞춰서 알맞게 세팅해주시면 됩니다.
5. 페이지를 넘기는 방식을 선택해야 합니다. '키보드 방향키'방식은 프로그램이 자동으로 오른쪽 방향키를 눌러서 페이지를 넘깁니다. 이때 포커스가 e북 리더에 맞추어져 있어야 합니다. '마우스 클릭'방식은 커서가 놓여져 있는 위치에서 자동으로 좌클릭을 하며 페이지를 넘깁니다. 사용하시는 e북 리더에 맞춰서 세팅하시면 됩니다.
6. 이제 마지막으로 '저장 경로 설정'버튼을 눌러서 캡쳐한 이미지들을 저장할 경로를 설정해주면 됩니다.

'작업 시작'버튼을 누르면 2초 후부터 프로그램이 자동으로 캡쳐를 시작합니다!

https://www.youtube.com/watch?v=kQkLwIIvzFk

dist폴더의 exe파일을 다운로드 받아서 실행하시면 됩니다!

### 주의사항

캡쳐한 이미지들은 반드시 개인적인 목적으로만 사용해야 합니다!!!!

