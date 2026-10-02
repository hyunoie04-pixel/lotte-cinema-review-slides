# Cinema Intelligence — 영화 관람평 분석 전체 프로젝트

[라이브 HTML 슬라이드](https://hyunoie04-pixel.github.io/lotte-cinema-review-slides/) · [분석 보고서](https://hyunoie04-pixel.github.io/lotte-cinema-review-slides/lotte_report/report.html)

롯데시네마 예매순 상위 10편의 공개 관람평 541개를 Firecrawl로 수집하고 분석한 결과 및 18장 HTML 슬라이드 덱입니다. 수집 기준일: 2026년 10월 2일 KST.

## 저장된 결과

| 경로 | 내용 |
|---|---|
| index.html / style.css / deck.js | 배포된 18장 덱, 애니메이션, 인터랙티브 SVG 그래프 10개 |
| assets/ | GPT 이미지 생성 도구로 만든 WebP 에셋 3개와 정확한 생성 프롬프트 |
| image_assets/ | 선택한 이미지의 원본 PNG 3개 |
| data/ | 덱에서 사용한 집계 JSON, 영화 정보 CSV |
| lotte_raw/ | Firecrawl 목록·상세 페이지·추가 리뷰 수집 응답 원본 JSON |
| lotte_report/ | 검색 가능한 HTML 보고서, Markdown, 영화·리뷰 CSV 및 분석 JSON |
| deck_qa/ | Chrome 화면 검토 스크린샷과 최종 레이아웃 검사 결과 |
| build_lotte_report.py | 저장된 Firecrawl 원본에서 정제 데이터와 보고서 생성 |
| build_deck.py | 분석 결과에서 HTML 덱·집계 데이터 생성 |
| check_deck.py | 실제 Chrome에서 탐색·툴팁·히트맵·모바일 화면 검사 |
| collection_notes.md | 데이터 수집 방법과 재현 범위 |
| .env.example | Firecrawl 설정 예시. 실제 API 키는 포함하지 않음 |

## 사용

index.html을 브라우저로 열면 네트워크 라이브러리 없이 덱이 동작합니다. ← → 또는 Space로 이동하고 G는 목차, N은 발표자 노트, F는 전체 화면입니다. 모바일에서는 좌우 밀기로 이동하고 넓은 그래프는 가로로 스크롤할 수 있습니다. 브라우저 인쇄로 슬라이드별 PDF 저장이 가능하며 동작 줄이기 설정을 지원합니다.

## 재현

Python 3.14에서 실행했습니다. 저장소 루트에서 실행합니다.

```powershell
python -m pip install -r requirements.txt
python build_lotte_report.py
python build_deck.py
python check_deck.py
```

보고서 생성에는 Python 표준 라이브러리를 사용합니다. 이미지 변환에는 Pillow, 브라우저 검증에는 Playwright를 사용했습니다. check_deck.py는 Windows의 Chrome 경로를 지정하므로 다른 OS에서는 경로를 조정해야 합니다. build_deck.py는 index.html과 README.md 등 생성 파일을 다시 씁니다. CSS·JavaScript 및 이미지 에셋은 저장된 파일을 사용합니다. build_lotte_report.py와 build_deck.py는 저장된 데이터로 실행되며 API 호출이나 재수집을 수행하지 않습니다.

## 분석과 이미지의 한계

최신순 편의 표본 및 표현 사전 매칭으로 분석했습니다. 숫자 평점을 확보하지 못했으며 감성 표현 비율을 전체 관객 만족도로 해석할 수 없습니다. 영화별 표본 규모·작성 기간이 다르고 주제는 복수 매칭됩니다. 자세한 기준과 사전, 품질 표시는 보고서와 JSON·CSV에 기록했습니다. 원본에는 사이트에 공개된 작성자 표시와 리뷰 본문이 포함됩니다. 리뷰에 적힌 역사 주장·일정·직원 평가는 사실 검증 자료가 아닙니다.

GPT 이미지 에셋은 콘셉트 비주얼이며 실제 영화 장면·공식 시설 사진이 아닙니다. assets/prompts.md에 생성 프롬프트를 보존했습니다.

.env와 인증 정보는 저장하지 않습니다. 실제 Firecrawl 설정은 로컬 .env에 두세요.
