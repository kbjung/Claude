#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_doc.py — 창업 프로젝트 공용 md → html 변환 도구

사용법
    python3 build_doc.py 문서.md                 # 같은 폴더에 문서.html 생성
    python3 build_doc.py 문서.md 다른이름.html    # 출력 파일명 지정

설계 원칙
    · md를 원본으로 작성하고 html은 이 스크립트로 생성한다.
    · html을 직접 편집하지 않는다 (수정은 항상 md에서).
    · 창업 CLAUDE.md의 「HTML 문서 작성 시 체크리스트」를 CSS에 내장했다.

md 확장 문법
    1) 복사 버튼 블록
        ```copy 카톡 문안
        여기 내용이 복사됨
        ```
        → 제목줄 + [복사] 버튼이 붙은 블록으로 렌더링

    2) 담당자 자동 채움 필드
        <!-- fields -->
        → 성명·연락처·이메일 입력칸 생성.
          복사 블록 안의 [[NAME]] [[PHONE]] [[EMAIL]] 이 실시간 치환됨

    3) 배지
        {{ok:확인됨}} {{warn:미확인}} {{red:불가}} {{info:진행 중}}
        → 색상 배지 (inline-block · nowrap 적용됨)

    4) 강조 박스
        :::ok
        초록 박스 (좋은 소식·결론)
        :::

        :::note
        주황 박스 (주의·경고)
        :::

        > 일반 인용문도 주황 박스로 렌더링됨 (기존 문서와 동일)

    5) 표 첫 칸을 좁게 고정
        | {{tight}}항목 | 내용 |
        → 해당 셀에 white-space:nowrap; width:1% 적용

    6) 원문 발췌 박스 (RFP·지원서 등 원문 인용 문서용)
        :::source (1) 원문 발췌: 소제목  {{new:신규 작성}}
        ㅇ 항목 제목
        - 세부 내용 1
        - 세부 내용 2
        :figure images/img01.png | 대체텍스트 | 캡션(출처 포함)
        (라벨 없이 남은 줄은 그대로 문단으로 출력됨)
        :::
        → source-box(좌측 녹색 테두리) + source-label 로 렌더링.
          ㅇ로 시작하는 줄은 o-item(굵게), -로 시작하는 줄은 dash-item으로 변환.
          :figure 줄은 figure-box(이미지+캡션)로 변환. <, </u> 등 원문 raw HTML도 그대로 통과됨.
          라벨(:::source 뒤 문구)이 없으면 라벨 span 없이 내용만 렌더링.

        박스 밖 단독 이미지는  @figure images/img09.png | 대체텍스트 | 캡션  한 줄로 삽입.

    7) 출처/근거 각주
        @cite 출처: 문서명, PDF p.n 「...」 인용 근거 설명
        → cite(회색 각주)로 렌더링. 보통 박스 바로 다음 줄에 사용.

    8) 서식 안내·작성요령·확인필요 박스
        :::guide [서식 안내문]
        맑은고딕 12 / 줄간격 160
        :::

        :::instruction
        ※ 작성요령: ...
        :::

        :::todo [확인 필요]
        내용
        :::

        :::meta
        **작성 방식:** 내용
        **신청사업비:** 내용
        :::
        → guide=파란 점선 박스, instruction=회색 안내 박스, todo=노란 확인 박스,
          meta=옅은 파란 안내 박스. [ ] 라벨은 선택. meta/여러 줄은 줄바꿈(<br>)으로 표시됨.

    9) 신규작성·제이콥확인·원문그대로 태그  (배지의 확장판, 어디서나 사용 가능)
        {{new:신규 작성}}  {{hold:제이콥 확인}}  {{verbatim:원문 그대로}}

    10) 삭제 후보(취소선)
        ~~삭제를 고려 중인 문장~~
        → 취소선 + 회색(strike-remove)으로 표시(완전히 지우지 않고 표시만 할 때 사용)

의존성
    pip install markdown --break-system-packages
    (없으면 스크립트가 자동 설치를 시도한다)
"""

import sys, os, re, subprocess, html as htmllib

# ---------------------------------------------------------------- 의존성
try:
    import markdown
except ImportError:
    print('[build_doc] markdown 패키지 설치 중...', file=sys.stderr)
    subprocess.run([sys.executable, '-m', 'pip', 'install', 'markdown',
                    '--break-system-packages', '-q'], check=False)
    import markdown

# ---------------------------------------------------------------- 스타일
CSS = """
:root{
  --bg:#f7f8fa; --card:#fff; --line:#e2e6ec; --text:#1f2937; --muted:#6b7280;
  --accent:#2563eb; --accent-soft:#eff6ff; --warn:#b45309; --warn-soft:#fffbeb;
  --green:#047857; --green-soft:#ecfdf5; --red:#b91c1c; --red-soft:#fef2f2;
}
*{box-sizing:border-box;}
body{margin:0;padding:32px 20px 64px;background:var(--bg);color:var(--text);
     font-family:'Pretendard','Malgun Gothic','Apple SD Gothic Neo',sans-serif;line-height:1.7;}
.wrap{max-width:960px;margin:0 auto;background:var(--card);border:1px solid var(--line);
      border-radius:14px;padding:36px 40px 48px;}
h1{font-size:24px;margin:0 0 18px;letter-spacing:-0.5px;padding-bottom:14px;
   border-bottom:3px solid var(--accent);}
h2{font-size:18px;margin:34px 0 12px;padding-bottom:7px;border-bottom:2px solid var(--accent);
   display:inline-block;}
h3{font-size:15.5px;margin:24px 0 8px;color:#111827;padding-left:9px;border-left:3px solid var(--accent);}
h4{font-size:14.5px;margin:18px 0 6px;color:#374151;}

/* 표 — CLAUDE.md 체크리스트 반영 */
table{width:100%;border-collapse:collapse;margin:12px 0;font-size:13.5px;}
th,td{border:1px solid var(--line);padding:8px 11px;text-align:left;vertical-align:top;}
th{background:#f3f5f8;font-weight:600;white-space:nowrap;}
td.tight{white-space:nowrap;width:1%;}

/* 인라인 배지 — 한국어 4자 이상도 잘리지 않게 */
.badge{display:inline-block;border-radius:999px;padding:2px 10px;font-size:12px;
       font-weight:700;white-space:nowrap;}
.b-ok{background:var(--green-soft);color:var(--green);border:1px solid #b8e6cf;}
.b-warn{background:var(--warn-soft);color:var(--warn);border:1px solid #f0d9a8;}
.b-red{background:var(--red-soft);color:var(--red);border:1px solid #f3c2c2;}
.b-info{background:var(--accent-soft);color:var(--accent);border:1px solid #bfd6fb;}

/* 강조 박스 */
blockquote,.box-note{margin:14px 0;padding:12px 18px;background:var(--warn-soft);
       border-left:3px solid var(--warn);border-radius:6px;font-size:13.5px;}
.box-ok{margin:14px 0;padding:12px 18px;background:var(--green-soft);
       border-left:3px solid var(--green);border-radius:6px;font-size:13.5px;}
blockquote p,.box-note p,.box-ok p{margin:5px 0;}
blockquote table,.box-note table,.box-ok table{font-size:12.5px;}

code{background:#f3f5f8;padding:2px 6px;border-radius:4px;font-size:12.8px;
     font-family:'D2Coding','Consolas','Malgun Gothic',monospace;}
pre{background:#1f2937;color:#e5e7eb;padding:16px 18px;border-radius:9px;overflow:auto;
    font-size:13px;line-height:1.7;}
pre code{background:none;color:inherit;padding:0;}
hr{border:none;border-top:1px solid var(--line);margin:30px 0;}
p,li{font-size:14px;}
a{color:var(--accent);text-decoration:none;font-weight:600;}
a:hover{text-decoration:underline;}
del,s{color:var(--muted);}
img{max-width:100%;height:auto;}
figure.figure-keep{margin:16px 0;}
figure.figure-keep img{display:block;width:100%;}

/* 복사 버튼 블록 */
.block{border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:16px 0;background:#fcfcfd;}
.bhead{display:flex;align-items:center;justify-content:space-between;gap:12px;flex-wrap:wrap;
       padding:10px 14px;background:#f3f5f8;border-bottom:1px solid var(--line);}
.btitle{font-size:13.5px;font-weight:700;}
.copybtn{border:1px solid var(--accent);background:var(--accent);color:#fff;border-radius:7px;
         padding:7px 18px;font-size:13px;font-weight:700;cursor:pointer;font-family:inherit;
         white-space:nowrap;transition:.15s;}
.copybtn:hover{filter:brightness(1.08);}
.copybtn.done{background:var(--green);border-color:var(--green);}
.copybtn.fail{background:var(--red);border-color:var(--red);}
pre.copytext{margin:0;padding:16px 18px;background:#fff;color:var(--text);font-size:13px;
     line-height:1.8;white-space:pre-wrap;word-break:break-word;font-family:inherit;}

/* 담당자 입력 필드 */
.fields{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:16px 0 6px;}
.fld label{display:block;font-size:12.5px;color:var(--muted);margin-bottom:4px;font-weight:600;}
.fld input{width:100%;padding:8px 11px;border:1px solid var(--line);border-radius:7px;
           font-size:14px;font-family:inherit;}
.fld input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft);}

/* 펩타이드 작업용액 계산기 */
.calc{margin:16px 0;padding:20px;border:1px solid #bfd6fb;background:#f8fbff;border-radius:12px;}
.calc h4{margin:0 0 5px;padding:0;border:0;color:#17324d;font-size:16px;}
.calc .hint{margin:0 0 15px;color:var(--muted);font-size:13px;}
.calc-grid{display:grid;grid-template-columns:repeat(3,minmax(150px,1fr));gap:12px;}
.calc-field label{display:block;margin-bottom:4px;color:var(--muted);font-size:12.5px;font-weight:700;}
.calc-field input{width:100%;padding:8px 10px;border:1px solid var(--line);border-radius:7px;background:#fff;font:14px inherit;}
.calc-field input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px var(--accent-soft);}
.field-reset{margin-top:4px;border:1px solid #c7d2e0;background:#fff;color:#526579;border-radius:5px;padding:3px 7px;font:11.5px inherit;cursor:pointer;}
.field-reset:hover{background:#f3f7fb;color:var(--accent);}
.calc-results{margin:18px 0 0;border-collapse:separate;border-spacing:0;border:1px solid #c8d8ec;border-radius:9px;overflow:hidden;}
.calc-results th{background:#eaf2fc;white-space:normal;}
.calc-results td{background:#fff;font-variant-numeric:tabular-nums;}
.calc .formula{margin:14px 0 0;color:#4b5563;font-size:12.5px;}
.calc .error{margin-top:10px;color:var(--red);font-size:13px;font-weight:700;}
.calc .default{display:block;margin-top:3px;color:#64748b;font-size:11.5px;font-weight:500;}
.calc-actions{display:flex;align-items:center;gap:10px;flex-wrap:wrap;margin:14px 0 4px;}
.calc-reset{border:1px solid var(--accent);background:#fff;color:var(--accent);border-radius:7px;padding:7px 12px;font:700 13px inherit;cursor:pointer;}
.calc-reset:hover{background:var(--accent-soft);}
.calc-action-note{color:var(--muted);font-size:12.5px;}
.prep-summary{margin:16px 0 8px;border:1px solid #8fb0d3;border-radius:9px;overflow:hidden;}
.prep-summary th{background:#173f6a;color:#fff;white-space:normal;}
.prep-summary td{background:#fff;font-variant-numeric:tabular-nums;}
.prep-summary tr.highlight td{background:#f0f7ff;}
.prep-summary .mix{font-weight:700;color:#173f6a;}
.calc .status{margin:12px 0 0;padding:10px 12px;border-radius:7px;background:#eef7ef;color:#176b2b;font-size:13px;}
.calc .status.warn{background:var(--warn-soft);color:var(--warn);border-left:3px solid var(--warn);}

footer{max-width:960px;margin:14px auto 0;color:var(--muted);font-size:12.5px;text-align:center;}

/* 원문 발췌 박스 (RFP·지원서 등 원문 인용 문서용) */
.meta{background:#eef2f8;border:1px solid #c9d6ea;padding:12px 16px;border-radius:6px;font-size:14px;margin:12px 0;}
.blue-guide{color:#1550c9;background:#eef4ff;border:1px dashed #a9c2ec;padding:8px 12px;margin:8px 0;font-size:13.5px;border-radius:4px;}
.guide-label{font-weight:700;color:#1550c9;font-size:12px;}
.instruction{color:#333;font-size:13.5px;background:#f4f4f4;padding:8px 12px;margin:8px 0;border-radius:4px;}
.source-box{background:#fff;border:1px solid #d8d8d8;border-left:4px solid #6b8f1a;padding:10px 14px;margin:8px 0;font-size:14px;border-radius:4px;}
.source-box p{margin:4px 0;}
.source-label{font-weight:700;color:#6b8f1a;font-size:12px;}
.cite{color:#888;font-size:12px;margin:6px 0 10px;}
.todo{background:#fff6db;border:1px solid #ecd583;padding:10px 14px;margin:8px 0;border-radius:4px;font-size:14px;}
.todo-label{font-weight:700;color:#a67c00;font-size:12px;}
.o-item{font-weight:700;margin:12px 0 4px;}
.dash-item{margin:3px 0;padding-left:14px;text-indent:-14px;}
.strike-remove{text-decoration:line-through;color:#999;}
.figure-box{text-align:center;margin:14px 0;padding:10px;background:#fff;border:1px solid #e0e0e0;border-radius:6px;}
.figure-box img{max-width:100%;height:auto;border-radius:4px;}
.figure-caption{font-size:12.5px;color:#666;margin-top:6px;}
.tag-new,.tag-hold,.tag-verbatim{display:inline-block;font-size:11px;padding:2px 6px;border-radius:10px;margin-left:6px;font-weight:700;white-space:nowrap;}
.tag-new{background:#ffe3e3;color:#a33;}
.tag-hold{background:#fff0c2;color:#8a6300;}
.tag-verbatim{background:#e8f0e0;color:#4a6b1a;}

@media (max-width:768px){
  body{padding:18px 10px 40px;}
  .wrap{padding:20px 16px 30px;}
  table{font-size:12px;} th,td{padding:6px 7px;}
  .bhead{flex-direction:column;align-items:stretch;} .copybtn{width:100%;}
  .calc-grid{grid-template-columns:repeat(2,minmax(130px,1fr));}
  .prep-summary{font-size:11.5px;} .prep-summary th,.prep-summary td{padding:6px 7px;}
}
@media print{
  figure.figure-keep{break-inside:avoid-page;page-break-inside:avoid;}
}
"""

JS = r"""
var FIELDS=[['f_name','[[NAME]]','[  성명  ]'],
            ['f_phone','[[PHONE]]','[  전화  ]'],
            ['f_email','[[EMAIL]]','[  이메일  ]']];
function fillAll(){
  document.querySelectorAll('pre.copytext[data-tpl]').forEach(function(el){
    var t=el.getAttribute('data-tpl');
    FIELDS.forEach(function(a){
      var i=document.getElementById(a[0]);
      var v=(i&&i.value.trim())?i.value.trim():a[2];
      t=t.split(a[1]).join(v);
    });
    el.textContent=t;
  });
}
FIELDS.forEach(function(a){
  var i=document.getElementById(a[0]);
  if(i) i.addEventListener('input',fillAll);
});
fillAll();

function flash(b,ok){
  var o=b.getAttribute('data-label')||b.textContent;
  b.setAttribute('data-label',o);
  b.classList.add(ok?'done':'fail');
  b.textContent=ok?'✔ 복사됨':'✕ 복사 실패';
  setTimeout(function(){b.classList.remove('done','fail');b.textContent=o;},1700);
}
function copyText(text,btn){
  var ta=document.createElement('textarea');
  ta.value=text; ta.setAttribute('readonly','');
  ta.style.position='fixed'; ta.style.top='-2000px'; ta.style.left='0';
  document.body.appendChild(ta);
  ta.select(); ta.setSelectionRange(0,ta.value.length);
  var ok=false; try{ok=document.execCommand('copy');}catch(e){ok=false;}
  document.body.removeChild(ta);
  if(ok){flash(btn,true);return;}
  if(navigator.clipboard&&navigator.clipboard.writeText){
    navigator.clipboard.writeText(text).then(function(){flash(btn,true);},function(){flash(btn,false);});
  } else {flash(btn,false);}
}
document.querySelectorAll('.copybtn').forEach(function(b){
  b.addEventListener('click',function(){
    var el=document.getElementById(b.dataset.target);
    if(el) copyText(el.textContent,b);
  });
});

function fmtCalc(value, digits){
  if(!isFinite(value)) return '—';
  return Number(value.toFixed(digits === undefined ? 1 : digits)).toLocaleString('ko-KR');
}
function readCalc(id){
  var el=document.getElementById(id);
  return el ? Number(el.value) : NaN;
}
function updatePeptideCalc(){
  if(!document.getElementById('pc_animals')) return;
  var n=readCalc('pc_animals'), dose=readCalc('pc_dose'), active=readCalc('pc_active'),
      stock=readCalc('pc_stock'), glycerol=readCalc('pc_glycerol'), over=readCalc('pc_over'),
      aliquot=readCalc('pc_aliquot');
  var err='', status='', corrected=false;
  var working=active/dose*1000;
  var nominal=n*dose;
  var prep=nominal*(1+over/100);
  var activeTotal=working*prep/1000;
  var minStock=working/(1-glycerol/100);
  var effectiveStock=Math.max(stock,minStock);
  var stockVol=activeTotal/effectiveStock*1000;
  var glycerolVol=prep*glycerol/100;
  var dpbsVol=prep-stockVol-glycerolVol;
  var reconstitution=aliquot/effectiveStock*1000;
  var reconstitutionInput=aliquot/stock*1000;
  var minoxPrep=n*dose*(1+over/100);
  var maxGlycerol=Math.max(0,100*(1-working/stock));
  if([n,dose,active,stock,glycerol,over,aliquot].some(function(v){return !isFinite(v) || v < 0;})) err='0 이상의 숫자를 입력하세요.';
  else if(dose===0 || stock===0) err='도포부피와 보관용액 농도는 0보다 커야 합니다.';
  else if(glycerol>=100) err='glycerol 비율은 100% 미만으로 입력하세요.';
  else if(stock < minStock - 0.0001){
    corrected=true;
    status='입력한 보관용액 '+fmtCalc(stock,2)+' μM은 작업용액 '+fmtCalc(working,2)+' μM와 glycerol '+fmtCalc(glycerol,1)+'%를 함께 유지하기에 부족합니다. 아래 합성량은 필요한 최소 '+fmtCalc(minStock,2)+' μM 보관용액으로 자동 보정했습니다. 입력 농도를 그대로 사용하려면 glycerol은 최대 '+fmtCalc(maxGlycerol,1)+'%까지로 낮춰야 합니다.';
  } else {
    status='입력한 보관용액 농도로 glycerol '+fmtCalc(glycerol,1)+'% 작업용액을 제조할 수 있습니다.';
  }
  var out={
    pc_working:fmtCalc(working,2)+' μM', pc_nominal:fmtCalc(nominal,1)+' μL',
    pc_prep:fmtCalc(prep,1)+' μL', pc_active_total:fmtCalc(activeTotal,2)+' nmol',
    pc_stock_vol:fmtCalc(stockVol,1)+' μL', pc_glycerol_vol:fmtCalc(glycerolVol,1)+' μL',
    pc_dpbs_vol:fmtCalc(Math.max(0,dpbsVol),1)+' μL',
    pc_reconstitution:fmtCalc(reconstitution,1)+' μL', pc_reconstitution_input:fmtCalc(reconstitutionInput,1)+' μL', pc_min_stock:fmtCalc(minStock,2)+' μM',
    pc_effective_stock:fmtCalc(effectiveStock,2)+' μM', pc_minox_prep:fmtCalc(minoxPrep,1)+' μL',
    pc_minox_nominal:fmtCalc(n*dose,1)+' μL', pc_sum_n:n+'마리', pc_sample_sum_n:n+'마리',
    pc_sum_dose:fmtCalc(dose,1)+' μL', pc_sample_sum_dose:fmtCalc(dose,1)+' μL', pc_sum_prep:fmtCalc(prep,1)+' μL',
    pc_sum_mix:fmtCalc(stockVol,1)+' μL 보관용액 + '+fmtCalc(glycerolVol,1)+' μL glycerol + '+fmtCalc(Math.max(0,dpbsVol),1)+' μL DPBS',
    pc_minox_sum_n:n+'마리', pc_minox_sum_dose:fmtCalc(dose,1)+' μL',
    pc_minox_sum_mix:'5% 원액 '+fmtCalc(minoxPrep,1)+' μL', pc_aliquot_sum:fmtCalc(aliquot,1)+' nmol',
    pc_stock_sum:fmtCalc(stock,1)+' μM', pc_reconstitution_input_summary:fmtCalc(reconstitutionInput,1)+' μL DPBS'
  };
  Object.keys(out).forEach(function(id){var el=document.getElementById(id);if(el)el.textContent=err?'—':out[id];});
  var error=document.getElementById('pc_error'); if(error) error.textContent=err;
  var st=document.getElementById('pc_status'); if(st){st.textContent=err?'':status;st.className='status'+(corrected?' warn':'');}
}
document.querySelectorAll('.peptide-calc input').forEach(function(i){i.addEventListener('input',updatePeptideCalc);});
var resetCalc=document.getElementById('pc_reset');
if(resetCalc) resetCalc.addEventListener('click',function(){
  document.querySelectorAll('.peptide-calc input[data-default]').forEach(function(i){i.value=i.dataset.default;});
  updatePeptideCalc();
});
document.querySelectorAll('.field-reset').forEach(function(b){b.addEventListener('click',function(){
  var i=document.getElementById(b.getAttribute('data-reset-target'));
  if(i){i.value=i.dataset.default;updatePeptideCalc();}
});});
updatePeptideCalc();
"""

# ---------------------------------------------------------------- 변환
def build(md_path, out_path=None):
    src = open(md_path, encoding='utf-8').read()
    stem = os.path.splitext(os.path.basename(md_path))[0]
    if out_path is None:
        out_path = os.path.join(os.path.dirname(os.path.abspath(md_path)), stem + '.html')

    # 1) 복사 버튼 블록 추출  ```copy 제목
    blocks = []
    def grab_copy(m):
        title = (m.group(1) or '복사').strip()
        body = m.group(2)
        blocks.append((title, body))
        return '\n@@COPYBLOCK%d@@\n' % (len(blocks) - 1)
    src = re.sub(r'```copy[ \t]*([^\n]*)\n(.*?)\n```', grab_copy, src, flags=re.S)

    # 2) 강조 박스 :::ok / :::note / :::source / :::meta / :::guide / :::instruction / :::todo
    boxes = []
    def grab_box(m):
        boxes.append((m.group(1), (m.group(2) or '').strip(), m.group(3)))
        return '\n@@BOX%d@@\n' % (len(boxes) - 1)
    src = re.sub(r':::(ok|note|source|meta|guide|instruction|todo)([ \t]+[^\n]*)?[ \t]*\n(.*?)\n:::',
                 grab_box, src, flags=re.S)

    # 2b) 출처/근거 각주  @cite 텍스트   /   박스 밖 단독 이미지  @figure 경로|대체텍스트|캡션
    cites = []
    def grab_cite(m):
        cites.append(m.group(1).strip())
        return '\n@@CITE%d@@\n' % (len(cites) - 1)
    src = re.sub(r'^@cite[ \t]+(.+)$', grab_cite, src, flags=re.M)

    figures = []
    def grab_figure(m):
        figures.append(m.group(1).strip())
        return '\n@@FIGURE%d@@\n' % (len(figures) - 1)
    src = re.sub(r'^@figure[ \t]+(.+)$', grab_figure, src, flags=re.M)

    has_fields = '<!-- fields -->' in src or '<!--fields-->' in src
    src = src.replace('<!-- fields -->', '@@FIELDS@@').replace('<!--fields-->', '@@FIELDS@@')
    has_peptide_calc = '<!-- peptide-calculator -->' in src or '<!--peptide-calculator-->' in src
    src = src.replace('<!-- peptide-calculator -->', '@@PEPTIDECALC@@').replace('<!--peptide-calculator-->', '@@PEPTIDECALC@@')

    # 3) 마크다운 변환
    body = markdown.markdown(src, extensions=['tables', 'fenced_code', 'nl2br', 'attr_list'])

    # 4~5) 인라인 확장 문법 치환 — 본문과 강조 박스 내부에 동일하게 적용
    kind = {'ok': 'b-ok', 'warn': 'b-warn', 'red': 'b-red', 'info': 'b-info'}
    tag_kind = {'new': 'tag-new', 'hold': 'tag-hold', 'verbatim': 'tag-verbatim'}

    def apply_inline(h):
        # 배지  {{ok:텍스트}}
        h = re.sub(r'\{\{(ok|warn|red|info):([^}]*)\}\}',
                   lambda m: '<span class="badge %s">%s</span>' % (kind[m.group(1)], m.group(2)), h)
        # 원문 표시 태그  {{new:텍스트}} {{hold:텍스트}} {{verbatim:텍스트}}
        h = re.sub(r'\{\{(new|hold|verbatim):([^}]*)\}\}',
                   lambda m: '<span class="%s">%s</span>' % (tag_kind[m.group(1)], m.group(2)), h)
        # 표 첫 칸 좁게  {{tight}}
        h = h.replace('<td>{{tight}}', '<td class="tight">')
        h = h.replace('<th>{{tight}}', '<th class="tight">')
        h = re.sub(r'\{\{tight\}\}', '', h)
        # 삭제 후보(취소선)  ~~텍스트~~
        h = re.sub(r'~~(.+?)~~', r'<span class="strike-remove">\1</span>', h, flags=re.S)
        return h

    body = apply_inline(body)

    def inline_md(text):
        """한 줄짜리 텍스트에 굵게·기울임·링크 등 인라인 마크다운만 적용 (블록 <p> 래핑은 제거)."""
        h = markdown.markdown(text, extensions=['nl2br'])
        if h.startswith('<p>') and h.endswith('</p>') and h.count('<p>') == 1:
            h = h[3:-4]
        return h

    def render_figure(spec):
        """'경로 | 대체텍스트 | 캡션' → figure-box(이미지+캡션) HTML"""
        parts = spec.split('|')
        path = parts[0].strip()
        alt = parts[1].strip() if len(parts) > 1 else ''
        cap = inline_md(parts[2].strip()) if len(parts) > 2 else ''
        return ('<div class="figure-box">\n<img src="%s" alt="%s">\n'
                '<div class="figure-caption">%s</div>\n</div>'
                % (path, htmllib.escape(alt, quote=True), cap))

    def render_source_content(text):
        """원문 발췌 박스 내부를 줄 단위로 처리: ㅇ→o-item, -→dash-item, :figure→그림,
        <로 시작하는 줄(raw HTML)은 그대로 통과, 그 외는 일반 문단으로 출력."""
        out = []
        for raw in text.split('\n'):
            line = raw.strip()
            if not line:
                continue
            if line.startswith('@cite '):
                out.append('<div class="cite">%s</div>' % inline_md(line[len('@cite '):]))
            elif line.startswith('<'):
                out.append(line)
            elif line.startswith(':figure '):
                out.append(render_figure(line[len(':figure '):]))
            elif line.startswith('ㅇ '):
                out.append('<div class="o-item">ㅇ %s</div>' % inline_md(line[2:]))
            elif line.startswith('- '):
                out.append('<div class="dash-item">- %s</div>' % inline_md(line[2:]))
            else:
                out.append(inline_md(line))
        return '\n'.join(out)

    # 6) 강조/안내 박스 복원 (내부도 apply_inline 통과시킬 것)
    box_meta = {
        'ok':          {'wrap': 'box-ok'},
        'note':        {'wrap': 'box-note'},
        'meta':        {'wrap': 'meta'},
        'guide':       {'wrap': 'blue-guide',   'label_class': 'guide-label'},
        'instruction': {'wrap': 'instruction'},
        'todo':        {'wrap': 'todo',         'label_class': 'todo-label'},
    }
    for i, (k, label, inner) in enumerate(boxes):
        if k == 'source':
            content_html = render_source_content(inner)
            has_block = content_html.lstrip().startswith(('<div', '<table'))
            if label:
                sep = '<br><br>\n' if has_block else ' '
                rep = '<div class="source-box"><span class="source-label">%s</span>%s%s</div>' % (label, sep, content_html)
            else:
                rep = '<div class="source-box">%s</div>' % content_html
        else:
            conf = box_meta[k]
            inner_html = markdown.markdown(inner.strip('\n'), extensions=['tables', 'fenced_code', 'nl2br'])
            if inner_html.startswith('<p>') and inner_html.endswith('</p>') and inner_html.count('<p>') == 1:
                inner_html = inner_html[3:-4]
            label_html = ''
            if conf.get('label_class') and label:
                label_html = '<span class="%s">%s</span> ' % (conf['label_class'], label)
            rep = '<div class="%s">%s%s</div>' % (conf['wrap'], label_html, inner_html)
        rep = apply_inline(rep)
        body = body.replace('<p>@@BOX%d@@</p>' % i, rep).replace('@@BOX%d@@' % i, rep)

    # 6b) 출처 각주 / 단독 이미지 복원
    for i, text in enumerate(cites):
        rep = apply_inline('<div class="cite">%s</div>' % inline_md(text))
        body = body.replace('<p>@@CITE%d@@</p>' % i, rep).replace('@@CITE%d@@' % i, rep)
    for i, spec in enumerate(figures):
        rep = apply_inline(render_figure(spec))
        body = body.replace('<p>@@FIGURE%d@@</p>' % i, rep).replace('@@FIGURE%d@@' % i, rep)

    # 7) 복사 블록 복원
    for i, (title, text) in enumerate(blocks):
        esc = htmllib.escape(text)
        pre = ('<pre class="copytext" id="cp%d" data-tpl="%s">%s</pre>'
               % (i, htmllib.escape(text, quote=True), esc))
        rep = ('<div class="block"><div class="bhead"><div class="btitle">%s</div>'
               '<button class="copybtn" data-target="cp%d">복사</button></div>%s</div>'
               % (htmllib.escape(title), i, pre))
        body = body.replace('<p>@@COPYBLOCK%d@@</p>' % i, rep).replace('@@COPYBLOCK%d@@' % i, rep)

    # 8) 담당자 필드 복원
    fields_html = ('<div class="fields">'
                   '<div class="fld"><label>성명</label><input id="f_name" placeholder="예: 김범중"></div>'
                   '<div class="fld"><label>연락처</label><input id="f_phone" placeholder="예: 010-0000-0000"></div>'
                   '<div class="fld"><label>이메일</label><input id="f_email" placeholder="예: name@inha.edu"></div>'
                   '</div>')
    body = body.replace('<p>@@FIELDS@@</p>', fields_html).replace('@@FIELDS@@', fields_html)

    peptide_calc_html = ('<div class="calc peptide-calc">'
                         '<h4>1일 합성·준비 계산기</h4>'
                         '<p class="hint">신규 샘플은 동결건조 소분액 → DPBS 보관용액 → 실험 직전 작업용액 순서로 계산합니다. 각 입력값은 기본값을 함께 표시하며, 변경 즉시 아래 실험 당일용 합성표가 갱신됩니다.</p>'
                         '<div class="calc-grid">'
                         '<div class="calc-field"><label>동결건조 소분량 (nmol)<span class="default">기본값: 100 nmol</span></label><input id="pc_aliquot" data-default="100" type="number" min="0" step="1" value="100"><button type="button" class="field-reset" data-reset-target="pc_aliquot">기본값</button></div>'
                         '<div class="calc-field"><label>보관용액 농도 (μM)<span class="default">기본값: 80 μM</span></label><input id="pc_stock" data-default="80" type="number" min="0" step="1" value="80"><button type="button" class="field-reset" data-reset-target="pc_stock">기본값</button></div>'
                         '<div class="calc-field"><label>신규 샘플 1회 투여량 (nmol)<span class="default">기본값: 4 nmol</span></label><input id="pc_active" data-default="4" type="number" min="0" step="0.1" value="4"><button type="button" class="field-reset" data-reset-target="pc_active">기본값</button></div>'
                         '<div class="calc-field"><label>각 군 마리 수<span class="default">기본값: 3마리</span></label><input id="pc_animals" data-default="3" type="number" min="0" step="1" value="3"><button type="button" class="field-reset" data-reset-target="pc_animals">기본값</button></div>'
                         '<div class="calc-field"><label>모든 군 공통 1회 도포부피 (μL)<span class="default">기본값: 100 μL</span></label><input id="pc_dose" data-default="100" type="number" min="0" step="1" value="100"><button type="button" class="field-reset" data-reset-target="pc_dose">기본값</button></div>'
                         '<div class="calc-field"><label>작업용액 내 glycerol 비율 (%)<span class="default">기본값: 25%</span></label><input id="pc_glycerol" data-default="25" type="number" min="0" max="99" step="1" value="25"><button type="button" class="field-reset" data-reset-target="pc_glycerol">기본값</button></div>'
                         '<div class="calc-field"><label>피펫·튜브 손실 여유율 (%)<span class="default">기본값: 20%</span></label><input id="pc_over" data-default="20" type="number" min="0" step="1" value="20"><button type="button" class="field-reset" data-reset-target="pc_over">기본값</button></div>'
                         '</div>'
                         '<div class="calc-actions"><button id="pc_reset" type="button" class="calc-reset">↺ 기본값으로 되돌리기</button><span class="calc-action-note">기본값: 각 군 3마리, 공통 100 μL/마리, 신규 샘플 4 nmol/회</span></div>'
                         '<h4>신규 샘플 보관용액 제조</h4>'
                         '<table class="prep-summary"><thead><tr><th>동결건조 소분량</th><th>목표 보관용액 농도</th><th>녹일 DPBS 양</th><th>제조 단계</th></tr></thead><tbody>'
                         '<tr><td id="pc_aliquot_sum"></td><td id="pc_stock_sum"></td><td class="mix" id="pc_reconstitution_input_summary"></td><td>동결건조 소분액 + DPBS</td></tr>'
                         '</tbody></table>'
                         '<h4>군별 1일 도포 준비량</h4>'
                         '<table class="prep-summary"><thead><tr><th>실험군</th><th>마리 수</th><th>실제 1회 도포</th><th>1일 준비량<br>(20% 여유)</th><th>실험 직전 준비할 물질</th></tr></thead><tbody>'
                         '<tr><td><b>무처치</b></td><td id="pc_sum_n"></td><td id="pc_sum_dose"></td><td>—</td><td>도포하지 않음</td></tr>'
                         '<tr><td><b>미녹시딜 5% 원액</b></td><td id="pc_minox_sum_n"></td><td id="pc_minox_sum_dose"></td><td><b id="pc_minox_prep"></b><br><span class="default">명목: <span id="pc_minox_nominal"></span></span></td><td class="mix" id="pc_minox_sum_mix"></td></tr>'
                         '<tr class="highlight"><td><b>신규 샘플</b></td><td id="pc_sample_sum_n"></td><td id="pc_sample_sum_dose"></td><td><b id="pc_sum_prep"></b><br><span class="default">활성물질: <span id="pc_active_total"></span></span></td><td class="mix" id="pc_sum_mix"></td></tr>'
                         '</tbody></table>'
                         '<table class="calc-results"><thead><tr><th>신규 샘플 보관용액·작업용액 검산</th><th>결과</th><th>실제 수행 시 확인사항</th></tr></thead><tbody>'
                         '<tr><td>작업용액 농도</td><td id="pc_working"></td><td>실제 도포액의 농도</td></tr>'
                         '<tr><td>25% glycerol 유지를 위한 최소 보관용액 농도</td><td id="pc_min_stock"></td><td>이보다 낮으면 입력 농도 그대로는 제조 불가</td></tr>'
                         '<tr><td>계산에 적용한 보관용액 농도</td><td id="pc_effective_stock"></td><td>입력이 낮으면 자동 보정값</td></tr>'
                         '<tr><td>보관용액 1회 취량</td><td id="pc_stock_vol"></td><td>실험 직전에 취할 보관용액</td></tr>'
                         '<tr><td>glycerol 첨가량</td><td id="pc_glycerol_vol"></td><td>최종 작업용액의 입력 비율</td></tr>'
                         '<tr><td>DPBS 첨가량</td><td id="pc_dpbs_vol"></td><td>최종 작업용액 부피까지 보정</td></tr>'
                         '<tr><td>입력 보관용액 농도로 소분액 1개 재용해 시 DPBS</td><td id="pc_reconstitution_input"></td><td>위 요약표의 보관용액 제조량</td></tr>'
                         '<tr><td>계산 적용 농도로 소분액 1개 재용해 시 DPBS</td><td id="pc_reconstitution"></td><td>입력 농도가 낮아 자동 보정되면 이 값을 사용</td></tr>'
                         '</tbody></table>'
                         '<p id="pc_status" class="status" role="status"></p>'
                         '<p class="formula">계산식: 작업농도(μM) = 1회 투여량(nmol) ÷ 도포부피(μL) × 1,000. 보관용액 취량(μL) = 필요 총량(nmol) ÷ 적용 보관용액 농도(μM) × 1,000.</p>'
                         '<p id="pc_error" class="error" role="alert"></p></div>')
    body = body.replace('<p>@@PEPTIDECALC@@</p>', peptide_calc_html).replace('@@PEPTIDECALC@@', peptide_calc_html)

    # 9) 제목
    m = re.search(r'<h1>(.*?)</h1>', body, re.S)
    title = re.sub(r'<[^>]+>', '', m.group(1)).strip() if m else stem

    out = ('<!DOCTYPE html>\n<html lang="ko">\n<head>\n<meta charset="UTF-8">\n'
           '<meta name="viewport" content="width=device-width, initial-scale=1.0">\n'
           '<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n'
           '<div class="wrap">\n%s\n</div>\n'
           '<footer>%s</footer>\n<script>%s</script>\n</body>\n</html>\n'
           % (htmllib.escape(title), CSS, body, htmllib.escape(stem), JS))

    open(out_path, 'w', encoding='utf-8').write(out)

    # 검수 리포트
    warn = []
    if '@@' in out:
        warn.append('치환되지 않은 자리표시자(@@)가 남아 있음')
    # 복사 블록 안의 {{ }}는 의도된 원문일 수 있으므로 블록 밖만 검사
    outside = re.sub(r'<pre class="copytext".*?</pre>', '', out, flags=re.S)
    leftover = re.findall(r'\{\{[^}\n]{0,40}\}\}', outside)
    if leftover:
        warn.append('치환되지 않은 확장 문법이 남아 있음: %s' % ', '.join(sorted(set(leftover))[:5]))
    if has_fields and 'f_name' not in out:
        warn.append('fields 지시자가 있으나 입력칸이 생성되지 않음')
    if has_peptide_calc and 'pc_animals' not in out:
        warn.append('peptide-calculator 지시자가 있으나 계산기가 생성되지 않음')
    n_source = sum(1 for k, _, _ in boxes if k == 'source')
    print('[build_doc] %s → %s' % (os.path.basename(md_path), os.path.basename(out_path)))
    print('           표 %d · 복사블록 %d · 강조/안내박스 %d(원문발췌 %d) · 각주 %d · 이미지 %d · 배지 %d · %d bytes'
          % (out.count('<table>'), len(blocks), len(boxes), n_source, len(cites),
             out.count('<img '), out.count('class="badge'), len(out)))
    for w in warn:
        print('  [경고] ' + w)
    return out_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    build(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
