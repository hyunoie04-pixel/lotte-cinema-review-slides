from pathlib import Path
import json,re,html,csv,collections,datetime
ROOT=Path(__file__).resolve().parent
RAW=ROOT/'lotte_raw'
OUT=ROOT/'lotte_report';OUT.mkdir(exist_ok=True)
IDS=['24708','24623','24724','24654','24128','24751','24725','24971','24868','24982']
POS=['재밌','재미있','재미있었','재미있게','재밋','재미씀','재미지','잼있','잼나','잼씀','꿀잼','즐겁','즐거','즐감','잘 봤','잘봤','잘 보았','잘보았','좋았','좋아','좋다','좋네','좋은','좋고','좋음','좋게','좋아요','최고','명작','추천','감동','귀엽','귀여','귀요','기여','웅장','흥미','볼만','굿','만족','훌륭','사랑스','케미','캐미','통쾌','짜릿','명연기','몰입감','몰입도 높','노련']
NEG=['지루','노잼','재미없','재미가 없','잼없','별로','아쉽','아쉬','최악','아까','불친절','불쾌','실패','납득이 안','이해가 안','이해가 안된','이해가 안되','난해','조잡','구리','구려','구린','엉성','어색','부족','밍밍','시끄럽','졸려','안맞','안 맞','후회','왜곡','날조','선동물','안볼','실망','더러','심드렁','안좋','안 좋','안맞','힘들','집중이 깨','떨어져서','한숨쉬','뭘까','모르겠다','답답','올드']
THEMES={
'연기·배우':['연기','배우','구교환','신승호','강기영','최민식','한소희','설경구','전도연','변요한','노재원','캐미','케미'],
'서사·연출':['스토리','서사','연출','개연성','결말','엔딩','전개','캐릭터','캐릭','감독','여운','내용'],
'몰입·속도':['몰입','긴장','박진감','속도','순삭','지루','졸려','후딱'],
'영상·음향·기기':['cg','그래픽','음향','음량','소리','시끄럽','웅장','스케일','화질','초점','기기','광음','인피니티','스크린'],
'원작·시리즈 비교':['원작','웹툰','리메이크','1편','1탄','타짜1','시리즈','마녀','첫 브이알','작년 브이알','처음했던'],
'역사·사회 해석':['역사','왜곡','언론','진실','고증','시대','논란','자유','평등','계층'],
'공포·강도':['공포','무섭','무서','기괴','섬뜩','소름','충격','다크','심연','전체관람가','미드소마'],
'굿즈·특전':['굿즈','경품','특전'],
'극장 서비스·매너':['직원','불친절','관람매너','잡담','시끄러웠','핸드폰','리클라이너','응대'],
'재관람·추천 의향':['다시 보','다시보','또 보','또보','한번더','한 번 더','n차','3번째','두번','2번','추천','꼭 보','꼭보','보러가','보세요']}
NOTES={
'24708':('캐릭터의 귀여움과 후반부 반전에 관심이 모인다. 밝은 그림체와 어두운 이야기의 대비가 반복적으로 언급된다.','지루한 초반, 예상보다 강한 분위기, 굿즈·특전 품절에 대한 불만이 보인다. 무섭다는 표현은 장르 묘사일 수 있어 부정으로 자동 처리하지 않았다.','어린이 동반 관객에게 이야기 분위기를 안내하고, 특전의 지점별 재고·소진 안내를 개선할 여지가 있다.'),
'24623':('긴장감, 몰입, 배우들의 연기와 시대 재현에 대한 긍정 의견이 나온다.','역사 해석과 표현 방식에 대한 상반된 반응이 섞인다. 리뷰의 사실 주장과 역사 왜곡·평점 공격 주장은 검증된 사실로 취급하지 않았다.','작품의 긴장감·연기와 역사 해석 논쟁을 분리해 읽는 편이 유용하다. 관람평으로 사건의 진위를 판단할 수 없다.'),
'24724':('배우의 코믹 연기와 빠른 흐름, 가벼운 오락물로서의 재미가 강점으로 언급된다.','CG의 어색함, 개연성 부족, 다른 초능력 영화와의 유사성을 지적하는 의견이 함께 보인다.','관객의 기대를 배우 중심의 액션·코미디 경험에 맞추는 것이 적절하다. CG·설정 완성도에 민감한 관객의 반응은 다를 수 있다.'),
'24654':('배우들의 연기와 오락성이 긍정적으로 언급된다. 일부는 앞선 후속작보다 낫다고 평가한다.','첫 작품과의 비교, 익숙한 구성, 포커 지식에 따른 이해 차이가 드러난다.','포커 용어를 간단히 안내하고, 첫 작품과의 비교 기대를 고려할 수 있다.'),
'24128':('큰 화면, 웅장한 음향·스케일, 연출과 재관람 경험이 주요 강점으로 나타난다.','긴 러닝타임과 중반의 지루함, 사전 지식과 이해 난도에 대한 의견이 보인다.','극장 관람의 화면·음향 가치를 설명하고 긴 상영시간을 사전에 안내할 수 있다.'),
'24751':('배우들의 호흡과 연기, 따뜻하고 편안한 분위기, 한국식 리메이크를 좋게 보는 의견이 나타난다.','원작에서 바뀐 캐릭터의 성격과 악역의 동기를 납득하기 어렵다는 의견도 나온다.','배우들의 호흡과 편안한 정서를 주요 관람 포인트로 소개하되 원작과의 차이를 염두에 둘 수 있다.'),
'24725':('배우들의 연기와 깊은 몰입, 여운, 관계와 사회적 차이에 대한 해석이 보인다.','난해함, 이해의 어려움, 답답함과 극장 내 잡담에 관한 의견이 섞인다.','스포일러 없는 주제·인물 안내가 이해에 도움이 될 수 있다. 리뷰에 적힌 상영 종료일은 공식 일정으로 검증되지 않았다.'),
'24971':('멤버를 가까이 보는 1인칭 경험과 재관람 의향이 긍정적인 요소다.','곡 선정·구성, 작은 음량, 기기 초점·무게·화질, 직원 응대가 불만으로 언급된다. 지점별 경험은 상반되며 사실 확인이 필요하다.','음량·초점 설정과 기기 착용 안내, 직원 응대를 우선 점검할 수 있다. 작은 표본으로 지점 간 우열을 판단할 수 없다.'),
'24868':('공포의 강도, 잔상, 몰입과 장르적 재미를 좋게 보는 반응이 나타난다.','자극·소음에 대한 불편과 인물 행동에 대한 답답함이 나온다. 무서움·소름 자체는 장르 만족과 함께 나타날 수 있다.','공포·자극 강도를 사전에 안내하는 것이 관객 기대를 맞추는 데 도움이 된다.'),
'24982':('재관람의 감동과 향수, 특별관 음향, 추가 영상에 대한 관심이 나타난다.','멀티버스 이해의 어려움, 지루함, 좌석에 대한 불만도 보인다.','특별관 경험과 추가 영상의 범위를 정확히 안내할 수 있다. 일반 앙코르 상영과 별도의 영화 코드로 집계했다. 이벤트 포스터 소진·재고 안내에 대한 불만도 보여 특전 안내를 함께 점검할 수 있다.')}
def clean(t):return re.sub(r'[\t\r\n ]+',' ',html.unescape(re.sub('<[^>]+>',' ',t))).strip()
def matches(t,terms):
 t=t.lower();return sorted(set(w for w in terms if w in t))
def sentiment_cues(t):
 normalized=t.lower().replace('굿즈','특전')
 for phrase in ['지루하지','지루할 틈 없이','후회가 없','후회가없','후회안','후회하지 않을','안 아까','안아까','재미가 없는건 아닌','나쁘지','나쁘진','나쁘지도']:
  normalized=normalized.replace(phrase,' ')
 for phrase in ['좋지않','좋지 않','좋아하지 않','안좋아','안 좋아','안 좋','별로 안좋','별로 안 좋','재미있지는 않','추천하고 싶진 않']:
  normalized=normalized.replace(phrase,' 부정표현 ')
 return matches(normalized,POS), matches(normalized,NEG)+(['부정표현'] if '부정표현' in normalized else [])
movies=[];reviews=[]
for rank,mid in enumerate(IDS,1):
 candidates=[RAW/(mid+'.json'),RAW/(mid+'_expanded.json')]
 docs=[(p,json.loads(p.read_text(encoding='utf-8'))) for p in candidates if p.exists()]
 docs=[(p,d) for p,d in docs if d.get('success') and d.get('data',{}).get('html')]
 p,d=max(docs,key=lambda pd:pd[1]['data']['html'].count('class="review_info"'))
 md=d['data']['markdown'];h=d['data']['html'];name=re.search(r'^\*\*(.+?)\*\*',md,re.M).group(1)
 count=re.search(r'관람평 \(([\d,]+)\)',md);total=int(count.group(1).replace(',','')) if count else None
 url='https://www.lottecinema.co.kr/NLCHS/Movie/MovieDetailView?movie='+mid
 chunks=[x for x in re.findall(r'<li\b[^>]*>(.*?)</li>',h,re.S) if 'class="review_info"' in x]
 seen=set();local=[];dups=0
 for chunk in chunks:
  tx=clean(re.search(r'<div class="review_info">(.*?)</div>',chunk,re.S).group(1))
  dt=re.search(r'<span class="date">(.*?)</span>',chunk,re.S);date=clean(dt.group(1)) if dt else ''
  author=re.search(r'<span class="name">(.*?)</span>',chunk,re.S);author=clean(author.group(1)) if author else ''
  ident=(date,author,tx)
  if ident in seen:dups+=1;continue
  seen.add(ident)
  po,ne=sentiment_cues(tx)
  sentiment='혼합 단서' if po and ne else '긍정 단서' if po else '부정 단서' if ne else '단서 없음'
  tags=[k for k,v in THEMES.items() if matches(tx,v)]
  good=re.search(r'class="btn_ic_good"[^>]*>.*?</em>\s*(\d+)',chunk,re.S)
  row={'review_id':mid+'-'+str(len(local)+1).zfill(3),'rank':rank,'movie_id':mid,'movie':name,'date':date,'text':tx,'quality_flag':('다른 영화 중심 리뷰' if mid=='24128' and '암살자' in tx else '짧거나 제목만 있는 리뷰' if len(tx)<4 or tx.replace(' ','')==name.replace(' ','') else ''),'likes':int(good.group(1)) if good else 0,'sentiment':sentiment,'positive_terms':'|'.join(po),'negative_terms':'|'.join(ne),'themes':'|'.join(tags),'source_url':url,'collected_at':d.get('collected_at',''),'raw_file':p.name}
  local.append(row)
 reviews+=local
 m={'rank':rank,'movie_id':mid,'movie':name,'release':re.search(r'(\d{4}\.\d{2}\.\d{2}) 개봉',md).group(1),'runtime':int(re.search(r'- (\d+)분',md).group(1)),'total_reviews':total,'sample_reviews':len(local),'coverage_pct':round(len(local)/total*100,2) if total else None,'duplicates_removed':dups,'oldest_review':min((r['date'] for r in local),default=''),'latest_review':max((r['date'] for r in local),default=''),'source_url':url,'collected_at':d.get('collected_at',''),'raw_file':p.name,'sentiment_counts':dict(collections.Counter(r['sentiment'] for r in local)),'theme_counts':{t:sum(t in r['themes'].split('|') for r in local) for t in THEMES}}
 movies.append(m)
assert len(movies)==10 and all(m['sample_reviews']>0 for m in movies)
assert len({r['review_id'] for r in reviews})==len(reviews)
for filename,rows in [('movies.csv',movies),('reviews.csv',reviews)]:
 with (OUT/filename).open('w',encoding='utf-8-sig',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows([{k:json.dumps(v,ensure_ascii=False) if isinstance(v,dict) else v for k,v in r.items()} for r in rows])
(OUT/'analysis_data.json').write_text(json.dumps({'movies':movies,'reviews':reviews,'method':{'positive_terms':POS,'negative_terms':NEG,'theme_terms':THEMES,'classification':'substring matching; mixed if both positive and negative cues; no cues is unclassified'}},ensure_ascii=False,indent=2),encoding='utf-8')
n=len(reviews);t=sum(m['total_reviews'] or 0 for m in movies);sent=collections.Counter(r['sentiment'] for r in reviews)
start=min(m['collected_at'] for m in movies);end=max(m['collected_at'] for m in movies)
intro=f'2026년 10월 2일 롯데시네마 현재 상영작의 예매순 상위 10개를 대상으로 공개 관람평 {n:,}개를 수집했다. 선택한 상세 페이지의 전체 관람평 표시 합계는 {t:,}개이며 수집 표본은 {n/t*100:.2f}%다. 이는 최신순 편의 표본으로 전체 관객의 만족도를 대표하지 않는다.'
method=['인기 기준: 현재 상영작 목록의 예매순 표시 순서. 광고는 제외하고 1~10위 영화 코드를 추출했다. 예매율 수치는 페이지에서 확보되지 않아 계산하지 않았다.',f'수집: .env의 FIRECRAWL_API_KEY로 Firecrawl v2 scrape 호출. 원본 HTML·Markdown·메타데이터 보존. 상세 페이지 수집 완료 시각(KST): {start} ~ {end}. 목록 최초 응답은 Firecrawl 캐시를 허용했으므로 완전히 같은 순간의 실시간 순위임을 보장하지 않는다.', '표본: 최신순 첫 화면과 관람평 펼쳐보기 클릭으로 영화별 최대 60개를 목표로 수집했다. 동적 로딩 및 전체 리뷰 규모에 따라 실제 수집 건수는 다르다. 숫자 평점·평균 평점은 HTML에서 확보되지 않아 미제공이며 리뷰 캐릭터 이미지에서 추정하지 않았다.', '중복: 같은 영화에서 작성시각·작성자 표시·본문이 모두 같은 항목만 제거한다. 같은 문장의 다른 작성자 리뷰는 유지한다. 작성자는 정제 CSV에서 제외하고 영화별 리뷰 ID로 표시한다. 원본 HTML에는 사이트의 공개 작성자 표시가 남아 있다.', '감성: 긍정·부정 표현 사전의 부분 문자열 일치로 네 범주를 집계한다. 긍정과 부정 표현이 모두 있으면 혼합 단서, 모두 없으면 단서 없음이다. 굿즈를 긍정 표현 굿으로 잘못 세지 않도록 보정하고 일부 명시적인 부정·부정어의 부정 표현을 보정했으나 반어와 문맥은 놓칠 수 있다. 정확도를 검증한 감성 모델이 아니며 긍정 단서 비율을 만족도나 긍정률로 해석하지 않는다. 사전과 리뷰별 매칭 표현은 JSON·CSV에 공개했다.', '주제: 지정된 표현이 있는 리뷰 수를 주제별로 집계한다. 복수 주제에 포함될 수 있으므로 합계가 표본 수를 넘을 수 있다. 키워드가 없으면 실제 주제를 놓칠 수 있다. 정성 해석은 리뷰 본문을 읽어 작성했으며 키워드 빈도만으로 인과관계를 주장하지 않는다.', '한계: 최신순·소표본·포인트 적립에 따른 작성 동기·팬덤과 특별관 관객의 차이가 반영된다. 관람평 안의 일정, 역사 주장, 직원 및 지점 평가는 작성자의 경험·주장이고 별도로 검증하지 않았다. 리뷰가 관람 전 표현처럼 보이더라도 임의 삭제하지 않았다. 오디세이 페이지의 암살자(들) 중심 리뷰 1건과 짧은·제목만 있는 리뷰는 품질 표시를 남기고 전체 표현 집계에 유지했다. 따라서 표현 집계를 작품 만족도로 사용할 수 없다.']
findings=['관람 동기는 서로 다르다. 치이카와의 캐릭터·굿즈, 엔하이픈의 근접 VR 경험, 오디세이·어벤져스의 극장 화면·음향 가치가 구분된다. 단일 만족도 지표만으로 이들을 비교하기 어렵다.', '연기에 대한 칭찬과 서사·CG에 대한 불만은 같은 리뷰에서도 공존한다. 부활남·타짜·인턴에서 강점과 불만을 분리해 보는 것이 유용하다.', '공포의 강도는 장르 기대에 따라 가치가 달라진다. 치이카와는 귀여운 외형과 내용의 간극, 옵세션은 공포의 잔상이 반복적으로 논의된다. 무섭다는 말 자체를 불만으로 계산하지 않았다.', '작품 외 경험은 별도 관리가 필요하다. VR의 초점·기기 무게·음량·직원 응대, 특전 품절, 관람 매너와 좌석에 대한 의견은 영화의 작품성과 구분해 점검할 수 있다.', '역사·사회적 해석과 이해 난도는 독립적인 축이다. 암살자(들)의 역사 해석 논쟁, 가능한 사랑의 난해함과 여운이 이를 보여준다. 리뷰에 담긴 주장을 사실 판단의 근거로 삼을 수 없다.']
mdlines=['# 롯데시네마 인기 영화 10편 관람평 분석', '',intro,'','## 수집·분석 방법','']+['- '+x for x in method]+['','## 영화별 수집 현황','','| 예매순 | 영화 | 전체 관람평 표시 | 수집 | 수집 비중 |','|---:|---|---:|---:|---:|']
for m in movies:mdlines.append(f"| {m['rank']} | [{m['movie']}]({m['source_url']}) | {m['total_reviews']:,} | {m['sample_reviews']} | {m['coverage_pct']:.2f}% |")
mdlines+=['','## 주요 발견','']+['- '+x for x in findings]+['','## 감성 표현 단서 집계','','전체 표본: '+', '.join(f'{k} {sent[k]}개' for k in ['긍정 단서','부정 단서','혼합 단서','단서 없음'])+'. 이는 표현 사전의 매칭 결과이며 전체 관객의 만족도 추정이 아니다.','','| 영화 | 긍정 단서 | 부정 단서 | 혼합 단서 | 단서 없음 |','|---|---:|---:|---:|---:|']
for m in movies:mdlines.append('| '+m['movie']+' | '+' | '.join(str(m['sentiment_counts'].get(k,0)) for k in ['긍정 단서','부정 단서','혼합 단서','단서 없음'])+' |')
mdlines+=['','## 영화별 해석','']
for m in movies:
 a,b,c=NOTES[m['movie_id']];top=sorted(m['theme_counts'].items(),key=lambda x:-x[1])[:4]
 mdlines += [f"### {m['rank']}. {m['movie']}",'',f"표본 {m['sample_reviews']}개 / 전체 표시 {m['total_reviews']:,}개. 작성 기간 {m['oldest_review']} ~ {m['latest_review']}.",'','자주 매칭된 주제: '+', '.join(f'{k} {v}개' for k,v in top)+'.','',f'강점: {a}',f'불만·해석 차이: {b}',f'시사점: {c}','',f"[원문 상세 페이지]({m['source_url']}) · 근거: reviews.csv의 {m['movie_id']}- 접두사 리뷰 및 lotte_raw/{m['raw_file']}",'']
mdlines+=['## 활용 제안','','- 관객 안내: 공포·자극의 정도, 긴 상영시간, 원작·시리즈와의 차이, 특별관·VR 체험 요소를 구체적으로 안내한다.','- 운영 점검: 특전 재고 안내와 VR 음량·초점·착용 지원을 검토하고, 직원 응대·관람 매너·좌석 불만은 지점 확인 후 조치한다.','- 후속 조사: 영화별 동일 기간에 최신순과 공감순 표본을 함께 확보하고 실제 평점을 별도로 수집해야 장기 추세 및 관객 만족도를 더 신뢰성 있게 비교할 수 있다.','','## 파일 안내','','- report.html: 차트와 영화·감성·검색 필터를 포함한 오프라인 보고서.','- movies.csv / reviews.csv: UTF-8 BOM을 사용한 Excel용 정제 데이터.','- analysis_data.json: 분석 결과와 공개된 표현 사전.','- ../lotte_raw/: Firecrawl 응답 원본.','- ../build_lotte_report.py: 원본에서 보고서를 다시 만드는 스크립트.','','출처: [롯데시네마 현재 상영작·예매순](https://www.lottecinema.co.kr/NLCHS/Movie/List?flag=1). 영화별 관람평 출처는 각 영화 링크와 정제 데이터에 기록했다.']
(OUT/'report.md').write_text('\n'.join(mdlines),encoding='utf-8')
def esc(v):return html.escape(str(v),quote=True)
cards=[]
colors={'긍정 단서':'#16836d','부정 단서':'#c95763','혼합 단서':'#d29b34','단서 없음':'#929eaf'}
for m in movies:
 a,b,c=NOTES[m['movie_id']];bars=''.join(f'<span style="background:{color};width:{m["sentiment_counts"].get(k,0)/m["sample_reviews"]*100:.3f}%" title="{k}: {m["sentiment_counts"].get(k,0)}"></span>' for k,color in colors.items())
 themes=''.join(f'<div class="theme"><span>{esc(k)}</span><meter value="{v}" max="{m["sample_reviews"]}"></meter><b>{v}</b></div>' for k,v in sorted(m['theme_counts'].items(),key=lambda x:-x[1])[:5])
 cards.append(f'<article><div class="rank">예매 {m["rank"]}위 · {m["runtime"]}분</div><h3><a href="{m["source_url"]}" target="_blank" rel="noopener">{esc(m["movie"])}</a></h3><p class="muted">전체 표시 {m["total_reviews"]:,}개 · 수집 {m["sample_reviews"]}개 ({m["coverage_pct"]:.2f}%)</p><div class="bar">{bars}</div><p class="small">'+ ' / '.join(k+': '+str(m['sentiment_counts'].get(k,0)) for k in colors)+f'</p>{themes}<p><strong>강점</strong> {esc(a)}</p><p><strong>불만·해석 차이</strong> {esc(b)}</p><p><strong>시사점</strong> {esc(c)}</p><p class="small">리뷰 작성 기간 {esc(m["oldest_review"])} ~ {esc(m["latest_review"])}</p></article>')
options=''.join(f'<option value="{m["movie_id"]}">{esc(m["movie"])}</option>' for m in movies)
summary=''.join(f'<p>{esc(x)}</p>' for x in findings)
methodhtml=''.join(f'<li>{esc(x)}</li>' for x in method)
jsdata=json.dumps(reviews,ensure_ascii=False).replace('<','\\u003c')
page='''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>롯데시네마 관람평 분석</title><style>
:root{font-family:Malgun Gothic,Arial,sans-serif;color:#182d42;background:#f3f6fa;line-height:1.75}body{margin:0}header{background:#132b41;color:white;padding:46px max(6vw,22px)}main{max-width:1220px;margin:auto;padding:28px 22px}h1{font-size:clamp(26px,3vw,40px);line-height:1.4;margin:8px 0}h2{margin-top:36px}h3{line-height:1.45;font-size:20px}a{color:inherit}article,.panel{background:white;border:1px solid #dfe5ed;border-radius:14px;padding:24px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:20px}.rank{color:#16836d;font-weight:bold}.muted,.small{color:#617184}.small{font-size:12px}.bar{display:flex;height:16px;overflow:hidden;border-radius:8px;background:#eee}.theme{display:grid;grid-template-columns:145px 1fr 30px;gap:12px;align-items:center;font-size:13px}meter{width:100%;height:14px}select,input{padding:10px;border:1px solid #bcc7d5;border-radius:6px;max-width:100%;font:inherit}input{width:250px}.filters{display:flex;flex-wrap:wrap;gap:12px}.review{padding:16px 0;border-bottom:1px solid #e4eaf1}.review p{margin:7px 0;white-space:pre-wrap;overflow-wrap:anywhere}button{padding:10px 18px;background:#132b41;color:white;border:0;border-radius:6px;cursor:pointer}.tag{font-size:12px;background:#e8f1f4;padding:3px 7px;border-radius:4px}.stats{display:flex;gap:30px;flex-wrap:wrap;margin:22px 0}.stats b{font-size:28px;display:block}.notice{border-left:4px solid #d29b34;padding-left:16px}.files{display:flex;gap:16px;flex-wrap:wrap}@media(max-width:760px){.grid{grid-template-columns:1fr}.theme{grid-template-columns:130px 1fr 25px}}@media print{header{background:white;color:black}.filters,button,.reviewpanel{display:none}.grid{display:block}article{break-inside:avoid;margin-bottom:20px}main{padding:0}}
</style><header><div>LOTTE CINEMA · 2026.10.02 · 예매순 TOP 10</div><h1>관람평으로 본 영화의 강점과 불만</h1><p>작품의 재미, 기대의 차이, 극장 경험을 함께 살펴본 공개 리뷰 분석</p></header><main>'''
page+=f'<div class="stats"><div><b>10</b>영화</div><div><b>{n:,}</b>수집 리뷰</div><div><b>{t:,}</b>전체 관람평 표시 합계</div><div><b>{n/t*100:.2f}%</b>수집 비중</div></div><div class="panel"><p>{esc(intro)}</p><p class="notice">감성 차트는 표현 사전의 매칭 결과입니다. 만족도·평점·전체 관객의 긍정률을 뜻하지 않습니다. 최신순 표본이며 영화별 표본 규모와 시점이 다릅니다.</p></div><h2>주요 발견</h2><div class="panel">{summary}</div><h2>영화별 분석</h2><p>초록: 긍정 단서 · 빨강: 부정 단서 · 노랑: 혼합 단서 · 회색: 단서 없음. 주제는 복수 집계입니다.</p><div class="grid">'+''.join(cards)+'</div>'
page+=f'<h2>수집 방법과 한계</h2><div class="panel"><ol>{methodhtml}</ol></div><h2>수집 리뷰 탐색</h2><div class="panel reviewpanel"><div class="filters"><label>영화 <select id="movie"><option value="">전체 영화</option>{options}</select></label><label>표현 단서 <select id="sent"><option value="">전체</option>'+''.join(f'<option>{k}</option>' for k in colors)+'</select></label><label>본문 검색 <input id="query" placeholder="예: CG, 굿즈, 음향"></label></div><p id="count"></p><div id="list"></div><button id="more">다음 40개 보기</button></div><h2>자료 다운로드</h2><div class="files"><a href="movies.csv">영화 정보 CSV</a><a href="reviews.csv">관람평 CSV</a><a href="analysis_data.json">분석 JSON</a><a href="report.md">Markdown 보고서</a><a href="../lotte_raw/">Firecrawl 원본</a></div><p class="small">출처: <a href="https://www.lottecinema.co.kr/NLCHS/Movie/List?flag=1">롯데시네마 현재 상영작·예매순</a>. 영화별 원문 출처는 각 카드의 제목과 리뷰 출처 링크에 연결되어 있습니다.</p></main>'
page+='<script id="data" type="application/json">'+jsdata+'</script><script>const rows=JSON.parse(document.getElementById("data").textContent);const $=id=>document.getElementById(id);let limit=40;const esc=s=>String(s).replace(/[&<>"\x27]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;","\\\"":"&quot;","\x27":"&#39;"}[c]||"&quot;"));function draw(){const filtered=rows.filter(r=>(!$("movie").value||r.movie_id===$("movie").value)&&(!$("sent").value||r.sentiment===$("sent").value)&&r.text.toLowerCase().includes($("query").value.toLowerCase()));$("count").textContent=`검색 결과 ${filtered.length}개 / 표시 ${Math.min(limit,filtered.length)}개`;$("list").innerHTML=filtered.slice(0,limit).map(r=>`<div class="review"><b>${esc(r.movie)}</b> <span class="tag">${esc(r.sentiment)}</span><p>${esc(r.text)}</p><div class="small">${esc(r.review_id)} · ${esc(r.date)} · 공감 ${r.likes} · 품질 표시: ${esc(r.quality_flag||"없음")} · 주제: ${esc(r.themes||"미분류")}<br>긍정 매칭: ${esc(r.positive_terms||"없음")} / 부정 매칭: ${esc(r.negative_terms||"없음")} · <a href="${r.source_url}" target="_blank" rel="noopener">출처</a></div></div>`).join("");$("more").hidden=limit>=filtered.length}for(const id of ["movie","sent","query"])$(id).addEventListener("input",()=>{limit=40;draw()});$("more").addEventListener("click",()=>{limit+=40;draw()});draw();</script></html>'
(OUT/'report.html').write_text(page,encoding='utf-8')
print(json.dumps({'movies':len(movies),'reviews':n,'total_displayed_reviews':t,'sentiment':dict(sent),'sample_counts':[(m['movie'],m['sample_reviews']) for m in movies]},ensure_ascii=False,indent=2))
