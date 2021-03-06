# Light-OCR-Data

## 1. AIHUB 데이터셋

* AIHUB에서 공개한 [한국어 글자체 이미지 데이터셋](https://aihub.or.kr/aidata/133) 중 Text in the Wild의 이미지/annotation을 사용했습니다. 각 도로교통표지판, 상품, 간판과 기타 카테고리로 분류됩니다.
* 약 100,000개의 이미지/annotation 중에서 각 카테고리 별로 10% 씩 선별하여, 약 9,900개를 [모델 평가](https://github.com/jentiai/Korean-Light-OCR-API)에 사용하였습니다. 선별한 테스트 데이터 리스트는 dataset/aihub_test_image_list.txt에서 확인하실 수 있습니다.

## 2. AIHUB 테스트 이미지 분리

* **코드 실행 전, AIHUB 데이터셋의 압축을 해제해야합니다.** 압축 해제 후 데이터 디렉토리 구조는 다음과 같습니다.
  ```
  AIHUB
    |---book
    |     |---000334C2A3FCD51B5C2F5AE7DE872A7C.jpg
    |     |---0008D5F549FE35B36BF92091E2D01646.jpg
    |                        .
    |                        .
    |---Goods
    |     |---00024467863E82F72B18598125DAE6B5.jpg
    |     |---000B7167D8521139AE0DF9B387C034D5.jpg
    |                        .
    |                        .
    |---Singboard
    |     |---0003053D121A0074B66CA75DCD51C8F3.jpg
    |     |---000AD252F19F62A9055C2CB8864B07E8.jpg
    |                        .
    |                        .
    |---Traffic_Sign
    |     |---000D6985A1C98F0549F53FEE4FA556B8.jpg
    |     |---001353D4CEF660E0C1F54B40FB4469B3.jpg
    |                        .
    |                        .
    |
    |---textinthewild_data_info.json
  ```

* 다음을 실행하여 선별한 테스트 이미지를 분리할 수 있습니다. 이때, ``--output``으로 설정할 디렉토리는 ``--aihub`` 디렉토리와 다른 곳으로 지정해야합니다.
  ```
  python make_dataset.py --aihub [path/to/image] --list_path [path/to/list/txt] --output [path/to/output]
  ```
* `--aihub`: 앞서 압축을 모두 푼 AIHUB dataset의 디렉토리.
* `--list_path`: AIHUB 테스트 이미지를 정리한 리스트 파일 경로.
* `--output`: AIHUB 테스트 이미지 및 GT를 저장될 디렉토리 경로.


## 3. API
* KaKao OCR API 및 Naver OCR API 사용법 입니다. 앞서 분리한 테스트 이미지 전체에 대한 각 API의 결과를 json 파일로 생성합니다. (Kakao OCR API의 경우 일일 사용 5000개 제한으로 초과 시 json 파일에 error가 작성됩니다.)

  

  ```
  python kakao.py [path/to/image] [appkey]
  ```
  ```
  python naver.py [path/to/image] [api_url] [api_key]
  ```
  ```
  python jenti.py [path/to/image]
  ```

* 코드를 실행한 위치에 ``{kakao, naver, jenti}.json``가 생성됩니다. 저희 [평가 코드](https://github.com/jentiai/Korean-Light-OCR-API.git)를 통해 각 OCR API의 성능을 확인할 수 있습니다.

## 4. 지원
본 연구개발은 2021년도 정부(과학기술정보통신부)의 재원으로 정보통신기획평가원의 지원을 받아 수행한 연구 성과물의 일부입니다. 해당 연구과제에 대한 정보는 아래와 같습니다.

* 과제번호: 2021-0-00023
* 연구사업명: 인공지능산업원천기술개발
* 연구과제명: 복합재난 상황에서의 문제해결을 위한 경량화 한글 탐지/인식 기술 개발
* 주관연구기관: [주식회사 젠티](http://jenti.ai/)
