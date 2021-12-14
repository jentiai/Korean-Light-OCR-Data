# Light-OCR-Data

## 1. AIHUB 데이터셋
* 한국어 글자체 이미지 중 Text in the Wild 이미지를 사용했습니다.
  * https://aihub.or.kr/aidata/133

| 도로교통표지판 | 상품 | 간판 | 기타 |
| ------------- | --- | --- | --- |
|![txtwild_data01](https://user-images.githubusercontent.com/72335925/145942175-f00badb1-542e-4f02-a9bf-a57632ae495e.png)|![txtwild_data02](https://user-images.githubusercontent.com/72335925/145942196-14444228-fab0-47a9-95ae-30106213fbab.png)|![txtwild_data03](https://user-images.githubusercontent.com/72335925/145942238-1e2b29dc-d022-4b63-8489-2413237a4aae.png)|![txtwild_data04](https://user-images.githubusercontent.com/72335925/145942247-d426244b-3af7-4884-bc21-2cc79322807d.png)

* 10 만장의 이미지 파일 중 카테고리 별로 10%씩 테스트셋으로 뽑아 사용했습니다.

## 2. AIHUB 테스트 이미지 분리
* AIHUB 테스트 이미지 분리를 위해선 다음을 수행합니다.
* 코드 실행 전 AIHUB 이미지의 압축은 모두 풀려있어야 합니다.
* AIHUB 테스트 이미지 리스트는 dataset/aihub_test_image_list.txt에 있습니다.
* output 폴더는 aihub 디렉토리와 다른 곳으로 지정해야합니다.
```
python make_dataset.py --aihub [path/to/image] --list_path [path/to/list/txt] --output [path/to/output]
```
* `--aihub`: aihub 이미지 및 json 파일 디렉토리 (모든 카테고리의 상위 폴더, 모든 압축을 푼 상태)
* `--list_path`: aihub 테스트 이미지를 정리한 리스트 파일 경로
* `--output`: aihub 테스트 이미지 및 GT를 저장할 디렉토리 경로

output에 aihub_test_image, gt 로 테스트 이미지 및 gt 폴더가 생성됩니다.

## 3. API
* 카카오 및 네이버 API 사용법 입니다.
* AIHUB 테스트 이미지 전체의 결과를 하나의 json 파일로 생성합니다.
```
python kakao.py [path/to/image] [appkey]
```
```
python naver.py [path/to/image] [api_url] [api_key]
```

코드를 실행한 위치에 kakao.json 및 naver.json 파일이 생성됩니다.
