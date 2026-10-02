# 수집 기록

- 기준일: 2026-10-02, Asia/Seoul.
- 인증: 로컬 .env의 FIRECRAWL_API_KEY. API 키는 이 저장소에 포함하지 않음.
- API: POST https://api.firecrawl.dev/v2/scrape.
- 인기 기준: https://www.lottecinema.co.kr/NLCHS/Movie/List?flag=1 의 현재 상영작 예매순 1~10위. 광고 제외.
- 상세 페이지: https://www.lottecinema.co.kr/NLCHS/Movie/MovieDetailView?movie={movie_id}.
- 포맷: markdown, html. 상세 페이지 수집 시 maxAge=0. 목록 최초 호출은 캐시 허용.
- 첫 화면에서 영화 정보 및 최신순 관람평 확보. 추가 요청은 button.tab_tit:last-of-type 클릭, 1초 대기 후 #btn_review_more 클릭과 1.2초 대기를 최대 3회 반복. VR 콘서트는 추가 버튼 1회 클릭.
- JavaScript 액션을 이용한 초기 추가 수집은 HTTP 500으로 실패했으며, 일반 click 액션으로 성공. 실패한 호출의 전체 응답·실행 스크립트는 당시 저장되지 않았으므로 이 문서는 그 방법을 요약한 기록임.
- 최종 541개: 일반 영화 8편은 60개씩, 암살자(들) 45개, VR 콘서트 16개. 실제 응답 중 리뷰 수가 많은 정상 파일을 영화별로 선택.
- lotte_raw/*.json: 응답 메타데이터·HTML·Markdown·수집 완료 시각 보존. list.json 및 retry_actions.json은 별도 수집 시각 필드를 추가하지 않았음.
- 중복 기준: 영화·작성시각·작성자 표시·본문이 동일한 경우만 제거. 원문 같은 다른 작성자의 리뷰는 유지.
- 재수집용 영구 스크립트는 최초 작업 당시 작성되지 않음. 저장된 build_lotte_report.py는 분석·보고서 재현용, build_deck.py는 덱 재현용.
