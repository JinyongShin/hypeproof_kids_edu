"""게임 템플릿 — 템플릿 기반 HTML5 게임 생성. AI 호출 없이 즉시.

캐릭터·세계 카드의 SVG를 게임 캔버스에 그대로 그려 넣는다.
AI 파라미터(이모지·테마)는 SVG가 없을 때의 폴백.
"""
import json
from string import Template

GAME_TMPL = Template('''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;min-height:100vh;font-family:sans-serif}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(100,100,255,0.3)}
#ui{position:fixed;top:20px;left:50%;transform:translateX(-50%);color:white;text-align:center;z-index:10}
#score{font-size:24px;font-weight:bold;text-shadow:0 0 10px rgba(255,255,255,0.5)}
#msg{font-size:16px;margin-top:5px;opacity:0.8}
#restart{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(255,255,255,0.2);color:white;border:2px solid white;padding:15px 30px;font-size:20px;border-radius:10px;cursor:pointer;backdrop-filter:blur(5px)}
</style></head><body>
<div id="ui"><div id="score">$item_emoji 0</div><div id="msg">$char_name의 모험!</div></div>
<canvas id="c" width="400" height="600"></canvas>
<button id="restart" onclick="resetGame()">다시 하기! &#x1f504;</button>
<script>
const canvas=document.getElementById("c"),ctx=canvas.getContext("2d");
const W=400,H=600;
let score=0,timeLeft=45,gameOver=false,player={x:200,y:500,w:48,h:48,speed:5};
let items=[],particles=[],keys={};
const CHAR_COLOR="$char_color";
const CHAR_EMOJI="$char_emoji";
const ITEM_EMOJI="$item_emoji";
const BG_TOP="$bg_top";
const BG_BOT="$bg_bot";
const CHAR_SVG=$char_svg_json;
const WORLD_SVG=$world_svg_json;
let charImg=null, worldImg=null;
function svgToImage(svg, cb){
  if(!svg) return;
  const img=new Image();
  img.onload=()=>cb(img);
  img.onerror=()=>{};
  img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg);
}
svgToImage(CHAR_SVG, i=>charImg=i);
svgToImage(WORLD_SVG, i=>worldImg=i);
document.addEventListener("keydown",e=>keys[e.key]=true);
document.addEventListener("keyup",e=>keys[e.key]=false);
let touchX=null;
canvas.addEventListener("touchstart",e=>{touchX=e.touches[0].clientX;e.preventDefault()},{passive:false});
canvas.addEventListener("touchmove",e=>{touchX=e.touches[0].clientX;e.preventDefault()},{passive:false});
canvas.addEventListener("touchend",()=>touchX=null);
function spawnItem(){items.push({x:Math.random()*(W-30)+15,y:-20,speed:1+Math.random()*2,size:18+Math.random()*10,rot:0})}
function addParticle(x,y,color){for(let i=0;i<5;i++)particles.push({x,y,vx:(Math.random()-0.5)*4,vy:(Math.random()-0.5)*4,life:30,color,size:3+Math.random()*3})}
function update(){
if(gameOver)return;
if(keys.ArrowLeft||keys.a)player.x-=player.speed;
if(keys.ArrowRight||keys.d)player.x+=player.speed;
if(keys.ArrowUp||keys.w)player.y-=player.speed;
if(keys.ArrowDown||keys.s)player.y+=player.speed;
if(touchX!==null)player.x+=(touchX-canvas.getBoundingClientRect().left-player.w/2-player.x)*0.1;
player.x=Math.max(0,Math.min(W-player.w,player.x));
player.y=Math.max(0,Math.min(H-player.h,player.y));
if(Math.random()<0.03)spawnItem();
for(let i=items.length-1;i>=0;i--){items[i].y+=items[i].speed;items[i].rot+=0.05;
if(Math.abs(items[i].x-player.x-player.w/2)<32&&Math.abs(items[i].y-player.y-player.h/2)<32){score++;addParticle(items[i].x,items[i].y,"#FFD700");items.splice(i,1)}
else if(items[i].y>H+20)items.splice(i,1)}
for(let i=particles.length-1;i>=0;i--){particles[i].x+=particles[i].vx;particles[i].y+=particles[i].vy;particles[i].life--;if(particles[i].life<=0)particles.splice(i,1)}
timeLeft-=1/60;if(timeLeft<=0){gameOver=true;document.getElementById("restart").style.display="block"}
document.getElementById("score").textContent=ITEM_EMOJI+" "+score;
}
function draw(){
if(worldImg){ctx.drawImage(worldImg,0,0,W,H);ctx.fillStyle="rgba(0,0,0,0.15)";ctx.fillRect(0,0,W,H)}
else{let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,BG_TOP);grd.addColorStop(1,BG_BOT);ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
ctx.fillStyle="rgba(255,255,255,0.3)";for(let i=0;i<50;i++){let sx=(i*137+50)%W,sy=(i*97+30)%H;ctx.beginPath();ctx.arc(sx,sy,(i%3)+1,0,Math.PI*2);ctx.fill()}}
items.forEach(it=>{ctx.save();ctx.translate(it.x,it.y);ctx.rotate(it.rot);ctx.font=it.size+"px serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ITEM_EMOJI,0,0);ctx.restore()});
particles.forEach(p=>{ctx.globalAlpha=p.life/30;ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
if(charImg){ctx.save();ctx.shadowColor=CHAR_COLOR;ctx.shadowBlur=18;ctx.drawImage(charImg,player.x,player.y,player.w,player.h);ctx.restore()}
else{ctx.font="40px serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(CHAR_EMOJI,player.x+player.w/2,player.y+player.h/2);ctx.shadowColor=CHAR_COLOR;ctx.shadowBlur=20;ctx.strokeStyle=CHAR_COLOR;ctx.lineWidth=2;ctx.strokeRect(player.x-2,player.y-2,player.w+4,player.h+4);ctx.shadowBlur=0}
if(gameOver){ctx.fillStyle="rgba(0,0,0,0.5)";ctx.fillRect(0,0,W,H);ctx.fillStyle="white";ctx.font="bold 36px sans-serif";ctx.textAlign="center";ctx.fillText("시간 끝!",W/2,H/2-30);ctx.font="24px sans-serif";ctx.fillText(ITEM_EMOJI+" "+score+"개 모음!",W/2,H/2+20)}
}
function resetGame(){score=0;timeLeft=45;gameOver=false;items=[];particles=[];player.x=200;player.y=500;document.getElementById("restart").style.display="none"}
function loop(){update();draw();requestAnimationFrame(loop)}loop();
</script></body></html>''')


# 캐릭터 이름 키워드 → 이모지 폴백 (SVG 없을 때만 사용)
EMOJI_MAP = {
    "아이언맨": "🤖", "아이언": "🤖", "iron": "🤖", "로봇": "🤖",
    "히어로": "🦸", "영웅": "🦸", "hero": "🦸", "수호자": "🛡️",
    "마법사": "🧙", "마녀": "🧙", "wizard": "🧙",
    "요정": "🧚", "fairy": "🧚",
    "전사": "⚔️", "warrior": "⚔️", "기사": "🤺",
    "공룡": "🦕", "용": "🐉", "dragon": "🐉",
    "고양이": "🐱", "cat": "🐱",
    "토끼": "🐰", "rabbit": "🐰",
    "강아지": "🐶", "dog": "🐶",
    "곰": "🐻", "여우": "🦊", "사자": "🦁", "판다": "🐼", "호랑이": "🐯",
    "펭귄": "🐧", "돌고래": "🐬", "물고기": "🐟", "fish": "🐟",
    "별": "⭐", "star": "⭐",
}

# 세계 키워드 → 배경 그라데이션 (SVG 없을 때만 사용)
BG_THEMES = {
    "우주": ("#0a0a2e", "#1a1a4e"), "별": ("#0a0a2e", "#1a1a4e"),
    "밤하늘": ("#0a0a2e", "#1a1a4e"), "은하": ("#0a0a2e", "#1a1a4e"),
    "바다": ("#0077b6", "#023e8a"), "물": ("#0077b6", "#023e8a"),
    "해양": ("#0077b6", "#023e8a"),
    "숲": ("#2d6a4f", "#1b4332"), "나무": ("#2d6a4f", "#1b4332"),
    "초원": ("#2d6a4f", "#1b4332"), "꽃": ("#86a96f", "#5d8a4e"),
    "불": ("#6a040f", "#370617"), "화산": ("#6a040f", "#370617"),
    "마을": ("#4a6fa5", "#2c3e50"),
    "하늘": ("#87CEEB", "#4682B4"), "구름": ("#87CEEB", "#4682B4"),
}


def _parse_card(raw):
    """문자열 또는 dict 카드를 dict로 정규화."""
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return {}
    return {}


def _find_latest_by_type(cards, card_type):
    """리스트(시간순 ASC)에서 해당 타입의 최신 카드 1장. 없으면 {}.
    cards 항목은 JSON 문자열이거나 dict."""
    for raw in reversed(cards or []):
        c = _parse_card(raw)
        if c.get("card_type") == card_type:
            return c
    return {}


def build_game_with_params(card_jsons: list, params: dict, user_prompt: str = "") -> str:
    """카드 리스트(시간순) + AI 파라미터로 게임 빌드.
    - character 카드의 image_svg → 플레이어 스프라이트
    - world 카드의 image_svg → 게임 배경
    - SVG가 없으면 emoji + 그라데이션으로 폴백.
    """
    char_card = _find_latest_by_type(card_jsons, "character")
    world_card = _find_latest_by_type(card_jsons, "world")

    char_name = char_card.get("name", "모험가") or "모험가"
    char_svg = char_card.get("image_svg", "") or ""
    world_name = world_card.get("name", "") or ""
    world_desc = (world_card.get("world", "") or "") + " " + (world_card.get("description", "") or "")
    world_combined = (world_name + " " + world_desc).strip()
    world_svg = world_card.get("image_svg", "") or ""

    # 캐릭터 이모지 폴백 (SVG 없을 때 표시)
    ai_emoji = (params or {}).get("char_emoji", "")
    emoji = ai_emoji.strip() if isinstance(ai_emoji, str) else ""
    if not emoji:
        for k, v in EMOJI_MAP.items():
            if k.lower() in char_name.lower():
                emoji = v
                break
    if not emoji:
        emoji = "✨"

    # 배경 그라데이션 폴백 (SVG 없을 때 표시)
    ai_bg = (params or {}).get("bg_theme", "")
    bg_top, bg_bot = "#2a1a4e", "#1a1a2e"
    if isinstance(ai_bg, str) and ai_bg in BG_THEMES:
        bg_top, bg_bot = BG_THEMES[ai_bg]
    else:
        for k, v in BG_THEMES.items():
            if k in world_combined:
                bg_top, bg_bot = v
                break

    # 아이템 이모지: AI 우선, 그 다음 세계 키워드, 그 다음 기본
    ai_item = (params or {}).get("item_emoji", "")
    item_emoji = ai_item.strip() if isinstance(ai_item, str) else ""
    if not item_emoji:
        if any(w in world_combined for w in ["바다", "물", "해양"]):
            item_emoji = "🐚"
        elif any(w in world_combined for w in ["숲", "꽃", "나무"]):
            item_emoji = "🌸"
        elif any(w in world_combined for w in ["불", "화산"]):
            item_emoji = "🔥"
        elif any(w in world_combined for w in ["우주", "별", "은하", "밤하늘"]):
            item_emoji = "⭐"
        else:
            item_emoji = "⭐"

    return GAME_TMPL.safe_substitute(
        char_name=char_name,
        char_emoji=emoji,
        char_color="#a78bfa",
        char_svg_json=json.dumps(char_svg),
        world_svg_json=json.dumps(world_svg),
        item_emoji=item_emoji,
        bg_top=bg_top,
        bg_bot=bg_bot,
    )


# 하위 호환: 일부 코드가 build_game을 호출할 수 있어 유지.
def build_game(character_cards: list, world_cards: "list | None" = None) -> str:
    _ = world_cards  # 시그니처 호환을 위해 유지
    return build_game_with_params(character_cards or [], {}, "")
