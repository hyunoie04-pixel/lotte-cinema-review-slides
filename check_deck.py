from pathlib import Path
from playwright.sync_api import sync_playwright
import json,sys
sys.stdout.reconfigure(encoding='utf-8')
out=Path('deck_qa');out.mkdir(exist_ok=True)
errors=[];layout=[]
with sync_playwright() as p:
 browser=p.chromium.launch(executable_path='C:/Program Files/Google/Chrome/Application/chrome.exe',headless=True)
 page=browser.new_page(viewport={'width':1600,'height':1030},device_scale_factor=1)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto((Path('index.html').resolve()).as_uri());page.wait_for_timeout(1600)
 assert page.locator('.slide').count()==18
 assert page.locator('.chart svg').count()==10
 for i in range(18):
  page.evaluate('(i)=>go(i)',i);page.wait_for_timeout(750)
  issues=page.evaluate('''()=>{const s=document.querySelector('.slide.active'),footer=s.querySelector('.slide-footer').getBoundingClientRect(),bounds=s.getBoundingClientRect();return [...s.querySelectorAll('h1,h2,h3,.lead,.chart,.chart-note,.metric-grid,.film-grid,.method-grid,.source-footer')].map(el=>({tag:el.tagName,cls:el.className,b:el.getBoundingClientRect()})).filter(o=>o.b.bottom>footer.top-8||o.b.right>bounds.right+2||o.b.left<bounds.left-2).map(o=>({tag:o.tag,cls:o.cls,bottom:Math.round(o.b.bottom),footer:Math.round(footer.top)}))}''')
  layout.append({'slide':i+1,'issues':issues})
  if i in [0,2,4,7,11,13,14,15]:page.screenshot(path=str(out/f'slide-{i+1:02}.png'))
 page.evaluate('go(7)');page.locator('[data-heat="count"]').click();assert page.locator('[data-heat="count"]').get_attribute('class')=='mode active'
 page.locator('#overviewBtn').click();assert page.locator('#overviewGrid button').count()==18
 page.locator('#overviewGrid button').nth(11).click();assert page.locator('#position').inner_text()=='12'
 page.keyboard.press('ArrowRight');assert page.locator('#position').inner_text()=='13'
 page.keyboard.press('n');assert page.locator('#notes').is_visible();page.keyboard.press('Escape')
 page.evaluate('go(11)');page.wait_for_timeout(1000);page.locator('#vr [data-tip]').first.hover();assert page.locator('#tooltip').is_visible()
 mobile=browser.new_page(viewport={'width':390,'height':844},is_mobile=True,has_touch=True)
 mobile.goto((Path('index.html').resolve()).as_uri());mobile.wait_for_timeout(900)
 for i in [0,1,7,11,13,15,17]:
  mobile.evaluate('(i)=>go(i)',i);mobile.wait_for_timeout(800)
  assert mobile.evaluate('document.documentElement.scrollWidth<=innerWidth+1'),f'mobile overflow {i+1}'
  if i in [0,7,11]:mobile.screenshot(path=str(out/f'mobile-{i+1:02}.png'),full_page=True)
 browser.close()
print(json.dumps({'javascript_errors':errors,'layout':layout,'checks':'18 slides; 10 SVG charts; heatmap switch; overview; keyboard; notes; tooltip; mobile width'},ensure_ascii=False,indent=2))
(out/'checks.json').write_text(json.dumps({'javascript_errors':errors,'layout':layout},ensure_ascii=False,indent=2),encoding='utf-8')
assert not errors
