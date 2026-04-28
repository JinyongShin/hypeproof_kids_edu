"""게임 템플릿 — 템플릿 기반 HTML5 게임 생성. AI 호출 없이 즉시.

캐릭터·세계 카드의 SVG를 게임 캔버스에 그대로 그려 넣는다.
AI 파라미터(이모지·테마)는 SVG가 없을 때의 폴백.

게임 타입별 함수를 register 데코레이터로 TEMPLATES dict에 등록.
새 게임 추가 = 함수 1개 + 템플릿 문자열 1개. 다른 인프라 없음.
"""
import json
from string import Template

from svg_sanitizer import sanitize_svg

# ----------------------------------------------------------------------------
# 게임 1 — collect: 떨어지는 아이템 모으기 (기본, 평화로운)
# ----------------------------------------------------------------------------
COLLECT_TMPL = Template('''<!DOCTYPE html>
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
const PACE=$pace_scale, TARGET=$target_score;
let score=0,timeLeft=$time_limit,gameOver=false,player={x:200,y:500,w:48,h:48,speed:5};
let items=[],particles=[],keys={};
const CHAR_COLOR="$char_color";
const CHAR_EMOJI="$char_emoji";
const ITEM_EMOJI="$item_emoji";
const BG_TOP="$bg_top";
const BG_BOT="$bg_bot";
const CHAR_SVG=$char_svg_json;
const WORLD_SVG=$world_svg_json;
let charImg=null, worldImg=null;
function svgToImage(svg, cb){if(!svg) return;const img=new Image();img.onload=()=>cb(img);img.onerror=()=>{};img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg)}
svgToImage(CHAR_SVG, i=>charImg=i);
svgToImage(WORLD_SVG, i=>worldImg=i);
document.addEventListener("keydown",e=>keys[e.key]=true);
document.addEventListener("keyup",e=>keys[e.key]=false);
let touchX=null;
canvas.addEventListener("touchstart",e=>{touchX=e.touches[0].clientX;e.preventDefault()},{passive:false});
canvas.addEventListener("touchmove",e=>{touchX=e.touches[0].clientX;e.preventDefault()},{passive:false});
canvas.addEventListener("touchend",()=>touchX=null);
function spawnItem(){items.push({x:Math.random()*(W-30)+15,y:-20,speed:(1+Math.random()*2)*PACE,size:18+Math.random()*10,rot:0})}
function addParticle(x,y,color){for(let i=0;i<5;i++)particles.push({x,y,vx:(Math.random()-0.5)*4,vy:(Math.random()-0.5)*4,life:30,color,size:3+Math.random()*3})}
function update(){
if(gameOver)return;
if(keys.ArrowLeft||keys.a)player.x-=player.speed;
if(keys.ArrowRight||keys.d)player.x+=player.speed;
if(keys.ArrowUp||keys.w)player.y-=player.speed;
if(keys.ArrowDown||keys.s)player.y+=player.speed;
if(touchX!==null)player.x+=(touchX-canvas.getBoundingClientRect().left-player.w/2-player.x)*0.1;
player.x=Math.max(0,Math.min(W-player.w,player.x));player.y=Math.max(0,Math.min(H-player.h,player.y));
if(Math.random()<0.03*PACE)spawnItem();
for(let i=items.length-1;i>=0;i--){items[i].y+=items[i].speed;items[i].rot+=0.05;
if(Math.abs(items[i].x-player.x-player.w/2)<32&&Math.abs(items[i].y-player.y-player.h/2)<32){score++;addParticle(items[i].x,items[i].y,"#FFD700");items.splice(i,1);
if(TARGET>0&&score>=TARGET){gameOver=true;document.getElementById("restart").style.display="block"}}
else if(items[i].y>H+20)items.splice(i,1)}
for(let i=particles.length-1;i>=0;i--){particles[i].x+=particles[i].vx;particles[i].y+=particles[i].vy;particles[i].life--;if(particles[i].life<=0)particles.splice(i,1)}
timeLeft-=1/60;if(timeLeft<=0){gameOver=true;document.getElementById("restart").style.display="block"}
document.getElementById("score").textContent=ITEM_EMOJI+" "+score+(TARGET>0?"/"+TARGET:"");
}
function draw(){
if(worldImg){ctx.drawImage(worldImg,0,0,W,H);ctx.fillStyle="rgba(0,0,0,0.15)";ctx.fillRect(0,0,W,H)}
else{let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,BG_TOP);grd.addColorStop(1,BG_BOT);ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
ctx.fillStyle="rgba(255,255,255,0.3)";for(let i=0;i<50;i++){let sx=(i*137+50)%W,sy=(i*97+30)%H;ctx.beginPath();ctx.arc(sx,sy,(i%3)+1,0,Math.PI*2);ctx.fill()}}
items.forEach(it=>{ctx.save();ctx.translate(it.x,it.y);ctx.rotate(it.rot);ctx.font=it.size+"px serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ITEM_EMOJI,0,0);ctx.restore()});
particles.forEach(p=>{ctx.globalAlpha=p.life/30;ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
if(charImg){ctx.save();ctx.shadowColor=CHAR_COLOR;ctx.shadowBlur=18;ctx.drawImage(charImg,player.x,player.y,player.w,player.h);ctx.restore()}
else{ctx.font="40px serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(CHAR_EMOJI,player.x+player.w/2,player.y+player.h/2);ctx.shadowColor=CHAR_COLOR;ctx.shadowBlur=20;ctx.strokeStyle=CHAR_COLOR;ctx.lineWidth=2;ctx.strokeRect(player.x-2,player.y-2,player.w+4,player.h+4);ctx.shadowBlur=0}
if(gameOver){ctx.fillStyle="rgba(0,0,0,0.5)";ctx.fillRect(0,0,W,H);ctx.fillStyle="white";ctx.font="bold 36px sans-serif";ctx.textAlign="center";var label=(TARGET>0&&score>=TARGET)?"성공! 🎉":"시간 끝!";ctx.fillText(label,W/2,H/2-30);ctx.font="24px sans-serif";ctx.fillText(ITEM_EMOJI+" "+score+"개 모음!",W/2,H/2+20)}
}
function resetGame(){score=0;timeLeft=$time_limit;gameOver=false;items=[];particles=[];player.x=200;player.y=500;document.getElementById("restart").style.display="none"}
function loop(){update();draw();requestAnimationFrame(loop)}loop();
</script></body></html>''')


# ----------------------------------------------------------------------------
# 게임 2 — dodge: 위험은 피하고 안전한 것만 모으기 (스릴, 협력적)
# 위험에 닿으면 점수만 -1 (최소 0). 죽지 않음.
# ----------------------------------------------------------------------------
DODGE_TMPL = Template('''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;min-height:100vh;font-family:sans-serif}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(100,100,255,0.3)}
#ui{position:fixed;top:20px;left:50%;transform:translateX(-50%);color:white;text-align:center;z-index:10}
#score{font-size:24px;font-weight:bold;text-shadow:0 0 10px rgba(255,255,255,0.5)}
#msg{font-size:16px;margin-top:5px;opacity:0.8}
#toast{position:fixed;top:90px;left:50%;transform:translateX(-50%);color:#ffd166;font-weight:bold;font-size:22px;text-shadow:0 0 8px rgba(0,0,0,0.7);opacity:0;transition:opacity 0.18s;pointer-events:none;z-index:11}
#toast.show{opacity:1}
#restart{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(255,255,255,0.2);color:white;border:2px solid white;padding:15px 30px;font-size:20px;border-radius:10px;cursor:pointer;backdrop-filter:blur(5px)}
</style></head><body>
<div id="ui"><div id="score">$item_emoji 0</div><div id="msg">$char_name이 위험을 피한다!</div></div>
<div id="toast"></div>
<canvas id="c" width="400" height="600"></canvas>
<button id="restart" onclick="resetGame()">다시 하기! &#x1f504;</button>
<script>
const canvas=document.getElementById("c"),ctx=canvas.getContext("2d");
const W=400,H=600;
const PACE=$pace_scale, TARGET=$target_score;
let score=0,timeLeft=$time_limit,gameOver=false,player={x:200,y:500,w:48,h:48,speed:5};
let items=[],particles=[],keys={};
const CHAR_COLOR="$char_color";
const CHAR_EMOJI="$char_emoji";
const ITEM_EMOJI="$item_emoji";
const HAZARD_EMOJI="$hazard_emoji";
const BG_TOP="$bg_top";
const BG_BOT="$bg_bot";
const CHAR_SVG=$char_svg_json;
const WORLD_SVG=$world_svg_json;
let charImg=null, worldImg=null;
function svgToImage(svg, cb){if(!svg) return;const img=new Image();img.onload=()=>cb(img);img.onerror=()=>{};img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg)}
svgToImage(CHAR_SVG, i=>charImg=i);
svgToImage(WORLD_SVG, i=>worldImg=i);
document.addEventListener("keydown",e=>keys[e.key]=true);
document.addEventListener("keyup",e=>keys[e.key]=false);
let touchX=null;
canvas.addEventListener("touchstart",e=>{touchX=e.touches[0].clientX;e.preventDefault()},{passive:false});
canvas.addEventListener("touchmove",e=>{touchX=e.touches[0].clientX;e.preventDefault()},{passive:false});
canvas.addEventListener("touchend",()=>touchX=null);
function spawnItem(){var hazard=Math.random()<0.45;items.push({x:Math.random()*(W-30)+15,y:-20,speed:(1.5+Math.random()*2.5)*PACE,size:hazard?28:20,rot:0,hazard:hazard})}
function addParticle(x,y,color){for(let i=0;i<6;i++)particles.push({x,y,vx:(Math.random()-0.5)*5,vy:(Math.random()-0.5)*5,life:32,color,size:3+Math.random()*3})}
function showToast(msg,color){var t=document.getElementById("toast");t.textContent=msg;t.style.color=color||"#ffd166";t.classList.add("show");setTimeout(()=>t.classList.remove("show"),700)}
function update(){
if(gameOver)return;
if(keys.ArrowLeft||keys.a)player.x-=player.speed;
if(keys.ArrowRight||keys.d)player.x+=player.speed;
if(keys.ArrowUp||keys.w)player.y-=player.speed;
if(keys.ArrowDown||keys.s)player.y+=player.speed;
if(touchX!==null)player.x+=(touchX-canvas.getBoundingClientRect().left-player.w/2-player.x)*0.1;
player.x=Math.max(0,Math.min(W-player.w,player.x));player.y=Math.max(0,Math.min(H-player.h,player.y));
if(Math.random()<0.04*PACE)spawnItem();
for(let i=items.length-1;i>=0;i--){items[i].y+=items[i].speed;items[i].rot+=0.05;
if(Math.abs(items[i].x-player.x-player.w/2)<32&&Math.abs(items[i].y-player.y-player.h/2)<32){
  if(items[i].hazard){score=Math.max(0,score-1);addParticle(items[i].x,items[i].y,"#ff5566");showToast("앗 조심!","#ff8899")}
  else{score++;addParticle(items[i].x,items[i].y,"#ffd166");showToast("+1","#ffd166");
    if(TARGET>0&&score>=TARGET){gameOver=true;document.getElementById("restart").style.display="block"}}
  items.splice(i,1)}
else if(items[i].y>H+20)items.splice(i,1)}
for(let i=particles.length-1;i>=0;i--){particles[i].x+=particles[i].vx;particles[i].y+=particles[i].vy;particles[i].life--;if(particles[i].life<=0)particles.splice(i,1)}
timeLeft-=1/60;if(timeLeft<=0){gameOver=true;document.getElementById("restart").style.display="block"}
document.getElementById("score").textContent=ITEM_EMOJI+" "+score+(TARGET>0?"/"+TARGET:"");
}
function draw(){
if(worldImg){ctx.drawImage(worldImg,0,0,W,H);ctx.fillStyle="rgba(0,0,0,0.2)";ctx.fillRect(0,0,W,H)}
else{let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,BG_TOP);grd.addColorStop(1,BG_BOT);ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
ctx.fillStyle="rgba(255,255,255,0.25)";for(let i=0;i<40;i++){let sx=(i*137+50)%W,sy=(i*97+30)%H;ctx.beginPath();ctx.arc(sx,sy,(i%3)+1,0,Math.PI*2);ctx.fill()}}
items.forEach(it=>{ctx.save();ctx.translate(it.x,it.y);ctx.rotate(it.rot);ctx.font=it.size+"px serif";ctx.textAlign="center";ctx.textBaseline="middle";
if(it.hazard){ctx.shadowColor="#ff5566";ctx.shadowBlur=14}ctx.fillText(it.hazard?HAZARD_EMOJI:ITEM_EMOJI,0,0);ctx.restore()});
particles.forEach(p=>{ctx.globalAlpha=p.life/32;ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
if(charImg){ctx.save();ctx.shadowColor=CHAR_COLOR;ctx.shadowBlur=18;ctx.drawImage(charImg,player.x,player.y,player.w,player.h);ctx.restore()}
else{ctx.font="40px serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(CHAR_EMOJI,player.x+player.w/2,player.y+player.h/2);ctx.shadowColor=CHAR_COLOR;ctx.shadowBlur=20;ctx.strokeStyle=CHAR_COLOR;ctx.lineWidth=2;ctx.strokeRect(player.x-2,player.y-2,player.w+4,player.h+4);ctx.shadowBlur=0}
if(gameOver){ctx.fillStyle="rgba(0,0,0,0.5)";ctx.fillRect(0,0,W,H);ctx.fillStyle="white";ctx.font="bold 36px sans-serif";ctx.textAlign="center";var label=(TARGET>0&&score>=TARGET)?"성공! 🎉":"잘 피했어!";ctx.fillText(label,W/2,H/2-30);ctx.font="24px sans-serif";ctx.fillText(ITEM_EMOJI+" "+score+"개 모음!",W/2,H/2+20)}
}
function resetGame(){score=0;timeLeft=$time_limit;gameOver=false;items=[];particles=[];player.x=200;player.y=500;document.getElementById("restart").style.display="none"}
function loop(){update();draw();requestAnimationFrame(loop)}loop();
</script></body></html>''')


# ----------------------------------------------------------------------------
# 게임 3 — chase: 떠다니는 친구 따라잡아 손잡기
# 5명 친구 모으면 일찍 끝, 협력적 서사
# ----------------------------------------------------------------------------
CHASE_TMPL = Template('''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;min-height:100vh;font-family:sans-serif}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(100,100,255,0.3)}
#ui{position:fixed;top:20px;left:50%;transform:translateX(-50%);color:white;text-align:center;z-index:10}
#score{font-size:24px;font-weight:bold;text-shadow:0 0 10px rgba(255,255,255,0.5)}
#msg{font-size:16px;margin-top:5px;opacity:0.8}
#toast{position:fixed;top:90px;left:50%;transform:translateX(-50%);color:#a0e7e5;font-weight:bold;font-size:22px;text-shadow:0 0 8px rgba(0,0,0,0.7);opacity:0;transition:opacity 0.18s;pointer-events:none;z-index:11}
#toast.show{opacity:1}
#restart{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(255,255,255,0.2);color:white;border:2px solid white;padding:15px 30px;font-size:20px;border-radius:10px;cursor:pointer;backdrop-filter:blur(5px)}
</style></head><body>
<div id="ui"><div id="score">$friend_emoji 0/5</div><div id="msg">$char_name이 친구를 찾아간다!</div></div>
<div id="toast"></div>
<canvas id="c" width="400" height="600"></canvas>
<button id="restart" onclick="resetGame()">다시 하기! &#x1f504;</button>
<script>
const canvas=document.getElementById("c"),ctx=canvas.getContext("2d");
const W=400,H=600;
const PACE=$pace_scale;
let score=0,timeLeft=$time_limit,gameOver=false,player={x:200,y:500,w:48,h:48,speed:5};
let particles=[],keys={},npc={x:100,y:100,w:42,h:42,vx:1.6*PACE,vy:1.2*PACE};
const CHAR_COLOR="$char_color";
const CHAR_EMOJI="$char_emoji";
const FRIEND_EMOJI="$friend_emoji";
const BG_TOP="$bg_top";
const BG_BOT="$bg_bot";
const CHAR_SVG=$char_svg_json;
const WORLD_SVG=$world_svg_json;
const TARGET=$target_score;
let charImg=null, worldImg=null;
function svgToImage(svg, cb){if(!svg) return;const img=new Image();img.onload=()=>cb(img);img.onerror=()=>{};img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg)}
svgToImage(CHAR_SVG, i=>charImg=i);
svgToImage(WORLD_SVG, i=>worldImg=i);
document.addEventListener("keydown",e=>keys[e.key]=true);
document.addEventListener("keyup",e=>keys[e.key]=false);
let touchX=null;
canvas.addEventListener("touchstart",e=>{touchX=e.touches[0].clientX;e.preventDefault()},{passive:false});
canvas.addEventListener("touchmove",e=>{touchX=e.touches[0].clientX;e.preventDefault()},{passive:false});
canvas.addEventListener("touchend",()=>touchX=null);
function respawnNpc(){npc.x=Math.random()*(W-100)+50;npc.y=Math.random()*(H-200)+50;var ang=Math.random()*Math.PI*2;var sp=(1.5+Math.random()*0.8)*PACE;npc.vx=Math.cos(ang)*sp;npc.vy=Math.sin(ang)*sp}
function addParticle(x,y,color){for(let i=0;i<8;i++)particles.push({x,y,vx:(Math.random()-0.5)*5,vy:(Math.random()-0.5)*5,life:36,color,size:3+Math.random()*3})}
function showToast(msg){var t=document.getElementById("toast");t.textContent=msg;t.classList.add("show");setTimeout(()=>t.classList.remove("show"),800)}
function update(){
if(gameOver)return;
if(keys.ArrowLeft||keys.a)player.x-=player.speed;
if(keys.ArrowRight||keys.d)player.x+=player.speed;
if(keys.ArrowUp||keys.w)player.y-=player.speed;
if(keys.ArrowDown||keys.s)player.y+=player.speed;
if(touchX!==null)player.x+=(touchX-canvas.getBoundingClientRect().left-player.w/2-player.x)*0.1;
player.x=Math.max(0,Math.min(W-player.w,player.x));player.y=Math.max(0,Math.min(H-player.h,player.y));
npc.x+=npc.vx;npc.y+=npc.vy;
if(npc.x<=0||npc.x>=W-npc.w)npc.vx*=-1;if(npc.y<=0||npc.y>=H-npc.h)npc.vy*=-1;
npc.x=Math.max(0,Math.min(W-npc.w,npc.x));npc.y=Math.max(0,Math.min(H-npc.h,npc.y));
var dx=(npc.x+npc.w/2)-(player.x+player.w/2),dy=(npc.y+npc.h/2)-(player.y+player.h/2);
if(Math.sqrt(dx*dx+dy*dy)<40){score++;addParticle(npc.x+npc.w/2,npc.y+npc.h/2,"#a0e7e5");showToast("친구 +1!");
  if(TARGET>0&&score>=TARGET){gameOver=true;document.getElementById("restart").style.display="block"}
  else{respawnNpc()}}
for(let i=particles.length-1;i>=0;i--){particles[i].x+=particles[i].vx;particles[i].y+=particles[i].vy;particles[i].life--;if(particles[i].life<=0)particles.splice(i,1)}
timeLeft-=1/60;if(timeLeft<=0){gameOver=true;document.getElementById("restart").style.display="block"}
document.getElementById("score").textContent=FRIEND_EMOJI+" "+score+(TARGET>0?"/"+TARGET:"");
}
function draw(){
if(worldImg){ctx.drawImage(worldImg,0,0,W,H);ctx.fillStyle="rgba(0,0,0,0.15)";ctx.fillRect(0,0,W,H)}
else{let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,BG_TOP);grd.addColorStop(1,BG_BOT);ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
ctx.fillStyle="rgba(255,255,255,0.25)";for(let i=0;i<40;i++){let sx=(i*137+50)%W,sy=(i*97+30)%H;ctx.beginPath();ctx.arc(sx,sy,(i%3)+1,0,Math.PI*2);ctx.fill()}}
ctx.font="36px serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.shadowColor="#a0e7e5";ctx.shadowBlur=12;
ctx.fillText(FRIEND_EMOJI,npc.x+npc.w/2,npc.y+npc.h/2);ctx.shadowBlur=0;
particles.forEach(p=>{ctx.globalAlpha=p.life/36;ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
if(charImg){ctx.save();ctx.shadowColor=CHAR_COLOR;ctx.shadowBlur=18;ctx.drawImage(charImg,player.x,player.y,player.w,player.h);ctx.restore()}
else{ctx.font="40px serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(CHAR_EMOJI,player.x+player.w/2,player.y+player.h/2);ctx.shadowColor=CHAR_COLOR;ctx.shadowBlur=20;ctx.strokeStyle=CHAR_COLOR;ctx.lineWidth=2;ctx.strokeRect(player.x-2,player.y-2,player.w+4,player.h+4);ctx.shadowBlur=0}
if(gameOver){ctx.fillStyle="rgba(0,0,0,0.5)";ctx.fillRect(0,0,W,H);ctx.fillStyle="white";ctx.font="bold 36px sans-serif";ctx.textAlign="center";
var label=(TARGET>0&&score>=TARGET)?"모두 만났어! 🎉":"시간 끝!";ctx.fillText(label,W/2,H/2-30);
ctx.font="24px sans-serif";ctx.fillText(FRIEND_EMOJI+" "+score+"명 친구",W/2,H/2+20)}
}
function resetGame(){score=0;timeLeft=$time_limit;gameOver=false;particles=[];player.x=200;player.y=500;respawnNpc();document.getElementById("restart").style.display="none"}
function loop(){update();draw();requestAnimationFrame(loop)}loop();
</script></body></html>''')


# ----------------------------------------------------------------------------
# 게임 4 — jump: 횡스크롤. 장애물 점프 + 공중 아이템 줍기
# 캐릭터는 x 고정, 좌우에서 다가오는 장애물을 점프로 넘기. 공중 아이템 = 점프 보상.
# 부딪혀도 점수만 -1 (최소 0). 협력형 — 죽지 않음.
# ----------------------------------------------------------------------------
JUMP_TMPL = Template('''<!DOCTYPE html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<style>*{margin:0;padding:0;box-sizing:border-box}body{background:#1a1a2e;display:flex;justify-content:center;align-items:center;min-height:100vh;font-family:sans-serif}
canvas{border-radius:12px;box-shadow:0 0 30px rgba(100,100,255,0.3)}
#ui{position:fixed;top:20px;left:50%;transform:translateX(-50%);color:white;text-align:center;z-index:10}
#score{font-size:24px;font-weight:bold;text-shadow:0 0 10px rgba(255,255,255,0.5)}
#msg{font-size:16px;margin-top:5px;opacity:0.8}
#toast{position:fixed;top:90px;left:50%;transform:translateX(-50%);color:#ffd166;font-weight:bold;font-size:22px;text-shadow:0 0 8px rgba(0,0,0,0.7);opacity:0;transition:opacity 0.18s;pointer-events:none;z-index:11}
#toast.show{opacity:1}
#restart{display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);background:rgba(255,255,255,0.2);color:white;border:2px solid white;padding:15px 30px;font-size:20px;border-radius:10px;cursor:pointer;backdrop-filter:blur(5px)}
</style></head><body>
<div id="ui"><div id="score">$item_emoji 0</div><div id="msg">$char_name이 점프! (스페이스/↑/탭)</div></div>
<div id="toast"></div>
<canvas id="c" width="400" height="600"></canvas>
<button id="restart" onclick="resetGame()">다시 하기! &#x1f504;</button>
<script>
const canvas=document.getElementById("c"),ctx=canvas.getContext("2d");
const W=400,H=600,GROUND=H-90;
const PACE=$pace_scale, TARGET=$target_score;
let score=0,timeLeft=$time_limit,gameOver=false;
let player={x:100,y:GROUND-48,vy:0,w:48,h:48,onGround:true};
let obstacles=[],items=[],particles=[],scrollX=0;
const GRAVITY=0.7,JUMP_V=-13,SCROLL_SPEED=4*PACE;
const CHAR_COLOR="$char_color";
const CHAR_EMOJI="$char_emoji";
const ITEM_EMOJI="$item_emoji";
const HAZARD_EMOJI="$hazard_emoji";
const BG_TOP="$bg_top";
const BG_BOT="$bg_bot";
const CHAR_SVG=$char_svg_json;
const WORLD_SVG=$world_svg_json;
let charImg=null, worldImg=null;
function svgToImage(svg, cb){if(!svg) return;const img=new Image();img.onload=()=>cb(img);img.onerror=()=>{};img.src='data:image/svg+xml;charset=utf-8,'+encodeURIComponent(svg)}
svgToImage(CHAR_SVG, i=>charImg=i);
svgToImage(WORLD_SVG, i=>worldImg=i);
function jump(){if(player.onGround){player.vy=JUMP_V;player.onGround=false}}
document.addEventListener("keydown",e=>{if(e.key===" "||e.key==="ArrowUp"||e.key==="w"||e.key==="W")jump()});
canvas.addEventListener("touchstart",e=>{jump();e.preventDefault()},{passive:false});
canvas.addEventListener("mousedown",e=>{jump()});
function spawnObstacle(){obstacles.push({x:W+30,y:GROUND-32,w:34,h:38,passed:false})}
function spawnItem(){items.push({x:W+20,y:GROUND-110-Math.random()*60,w:30,h:30,rot:0})}
function addParticle(x,y,color){for(let i=0;i<6;i++)particles.push({x,y,vx:(Math.random()-0.5)*5,vy:(Math.random()-0.5)*5,life:30,color,size:3+Math.random()*3})}
function showToast(msg,color){var t=document.getElementById("toast");t.textContent=msg;t.style.color=color||"#ffd166";t.classList.add("show");setTimeout(()=>t.classList.remove("show"),700)}
function update(){
if(gameOver)return;
player.vy+=GRAVITY;player.y+=player.vy;
if(player.y>=GROUND-player.h){player.y=GROUND-player.h;player.vy=0;player.onGround=true}
scrollX+=SCROLL_SPEED*0.75;
if(Math.random()<0.018*PACE)spawnObstacle();
if(Math.random()<0.022*PACE)spawnItem();
for(let i=obstacles.length-1;i>=0;i--){var o=obstacles[i];o.x-=SCROLL_SPEED;
if(!o.passed&&o.x+o.w<player.x){o.passed=true;score++;addParticle(o.x,GROUND-20,"#a0e7e5");
  if(TARGET>0&&score>=TARGET){gameOver=true;document.getElementById("restart").style.display="block"}}
if(player.x<o.x+o.w&&player.x+player.w>o.x&&player.y<o.y+o.h&&player.y+player.h>o.y){
  score=Math.max(0,score-1);addParticle(o.x,o.y,"#ff5566");showToast("앗 조심!","#ff8899");obstacles.splice(i,1);continue}
if(o.x<-50)obstacles.splice(i,1)}
for(let i=items.length-1;i>=0;i--){var it=items[i];it.x-=SCROLL_SPEED;it.rot+=0.07;
if(player.x<it.x+it.w&&player.x+player.w>it.x&&player.y<it.y+it.h&&player.y+player.h>it.y){
  score+=2;addParticle(it.x,it.y,"#ffd166");showToast("+2","#ffd166");items.splice(i,1);
  if(TARGET>0&&score>=TARGET){gameOver=true;document.getElementById("restart").style.display="block"}continue}
if(it.x<-50)items.splice(i,1)}
for(let i=particles.length-1;i>=0;i--){var p=particles[i];p.x+=p.vx;p.y+=p.vy;p.life--;if(p.life<=0)particles.splice(i,1)}
timeLeft-=1/60;if(timeLeft<=0){gameOver=true;document.getElementById("restart").style.display="block"}
document.getElementById("score").textContent=ITEM_EMOJI+" "+score+(TARGET>0?"/"+TARGET:"");
}
function draw(){
if(worldImg){ctx.drawImage(worldImg,(-scrollX*0.3)%W,0,W,H);ctx.drawImage(worldImg,(-scrollX*0.3)%W+W,0,W,H);ctx.fillStyle="rgba(0,0,0,0.18)";ctx.fillRect(0,0,W,H)}
else{let grd=ctx.createLinearGradient(0,0,0,H);grd.addColorStop(0,BG_TOP);grd.addColorStop(1,BG_BOT);ctx.fillStyle=grd;ctx.fillRect(0,0,W,H);
ctx.fillStyle="rgba(255,255,255,0.25)";for(let i=0;i<35;i++){let sx=((i*173-scrollX*0.5)%W+W)%W,sy=(i*97+30)%(H-150);ctx.beginPath();ctx.arc(sx,sy,(i%3)+1,0,Math.PI*2);ctx.fill()}}
ctx.fillStyle="rgba(80,60,120,0.7)";ctx.fillRect(0,GROUND,W,H-GROUND);
ctx.fillStyle="rgba(255,255,255,0.15)";for(let i=0;i<8;i++){let gx=((i*73-scrollX)%W+W)%W;ctx.fillRect(gx,GROUND+10,40,4)}
obstacles.forEach(o=>{ctx.save();ctx.translate(o.x+o.w/2,o.y+o.h/2);ctx.font="32px serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.shadowColor="#ff5566";ctx.shadowBlur=12;ctx.fillText(HAZARD_EMOJI,0,0);ctx.restore()});
items.forEach(it=>{ctx.save();ctx.translate(it.x+it.w/2,it.y+it.h/2);ctx.rotate(it.rot);ctx.font="28px serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ITEM_EMOJI,0,0);ctx.restore()});
particles.forEach(p=>{ctx.globalAlpha=p.life/30;ctx.fillStyle=p.color;ctx.beginPath();ctx.arc(p.x,p.y,p.size,0,Math.PI*2);ctx.fill()});ctx.globalAlpha=1;
if(charImg){ctx.save();ctx.shadowColor=CHAR_COLOR;ctx.shadowBlur=18;ctx.drawImage(charImg,player.x,player.y,player.w,player.h);ctx.restore()}
else{ctx.font="40px serif";ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(CHAR_EMOJI,player.x+player.w/2,player.y+player.h/2);ctx.shadowColor=CHAR_COLOR;ctx.shadowBlur=20;ctx.strokeStyle=CHAR_COLOR;ctx.lineWidth=2;ctx.strokeRect(player.x-2,player.y-2,player.w+4,player.h+4);ctx.shadowBlur=0}
if(gameOver){ctx.fillStyle="rgba(0,0,0,0.5)";ctx.fillRect(0,0,W,H);ctx.fillStyle="white";ctx.font="bold 36px sans-serif";ctx.textAlign="center";var label=(TARGET>0&&score>=TARGET)?"성공! 🎉":"잘 달렸어!";ctx.fillText(label,W/2,H/2-30);ctx.font="24px sans-serif";ctx.fillText(ITEM_EMOJI+" "+score+"점!",W/2,H/2+20)}
}
function resetGame(){score=0;timeLeft=$time_limit;gameOver=false;obstacles=[];items=[];particles=[];player.y=GROUND-48;player.vy=0;player.onGround=true;document.getElementById("restart").style.display="none"}
function loop(){update();draw();requestAnimationFrame(loop)}loop();
</script></body></html>''')


# ----------------------------------------------------------------------------
# Registry — game_type → builder 함수
# ----------------------------------------------------------------------------
TEMPLATES = {}


def register(name):
    def deco(fn):
        TEMPLATES[name] = fn
        return fn
    return deco


@register("collect")
def _collect_html(**ctx):
    return COLLECT_TMPL.safe_substitute(**ctx)


@register("dodge")
def _dodge_html(**ctx):
    ctx.setdefault("hazard_emoji", "💧")
    return DODGE_TMPL.safe_substitute(**ctx)


@register("chase")
def _chase_html(**ctx):
    ctx.setdefault("friend_emoji", "🐰")
    return CHASE_TMPL.safe_substitute(**ctx)


@register("jump")
def _jump_html(**ctx):
    ctx.setdefault("hazard_emoji", "🌵")
    return JUMP_TMPL.safe_substitute(**ctx)


# ----------------------------------------------------------------------------
# 폴백 매핑
# ----------------------------------------------------------------------------
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
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return {}
    return {}


def _find_latest_by_type(cards, card_type):
    for raw in reversed(cards or []):
        c = _parse_card(raw)
        if c.get("card_type") == card_type:
            return c
    return {}


def build_game_with_params(card_jsons: list, params: dict, user_prompt: str = "") -> str:
    """카드 리스트(시간순) + AI 파라미터로 게임 빌드.
    params['game_type'] in {collect, dodge, chase}. 없거나 모르는 값이면 collect 폴백.
    """
    char_card = _find_latest_by_type(card_jsons, "character")
    world_card = _find_latest_by_type(card_jsons, "world")

    char_name = char_card.get("name", "모험가") or "모험가"
    char_svg = sanitize_svg(char_card.get("image_svg", "") or "")
    world_name = world_card.get("name", "") or ""
    world_desc = (world_card.get("world", "") or "") + " " + (world_card.get("description", "") or "")
    world_combined = (world_name + " " + world_desc).strip()
    world_svg = sanitize_svg(world_card.get("image_svg", "") or "")

    ai_emoji = (params or {}).get("char_emoji", "")
    emoji = ai_emoji.strip() if isinstance(ai_emoji, str) else ""
    if not emoji:
        for k, v in EMOJI_MAP.items():
            if k.lower() in char_name.lower():
                emoji = v
                break
    if not emoji:
        emoji = "✨"

    ai_bg = (params or {}).get("bg_theme", "")
    bg_top, bg_bot = "#2a1a4e", "#1a1a2e"
    if isinstance(ai_bg, str) and ai_bg in BG_THEMES:
        bg_top, bg_bot = BG_THEMES[ai_bg]
    else:
        for k, v in BG_THEMES.items():
            if k in world_combined:
                bg_top, bg_bot = v
                break

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

    # 3축 difficulty 파라미터 — 안전 범위로 클램프
    def _clamp(v, lo, hi, default):
        try:
            x = float(v)
        except (TypeError, ValueError):
            return default
        return max(lo, min(hi, x))

    pace_scale = _clamp((params or {}).get("pace_scale"), 0.5, 1.8, 1.0)
    time_limit = int(_clamp((params or {}).get("time_limit"), 20, 90, 45))

    game_type = (params or {}).get("game_type", "collect")
    # chase는 기본 목표 5, 다른 게임은 0(무제한 시간만)
    default_target = 5 if game_type == "chase" else 0
    target_score = int(_clamp((params or {}).get("target_score"), 0, 30, default_target))
    # chase는 target_score=0이면 영원히 안 끝나므로 항상 ≥1로 보정
    if game_type == "chase" and target_score <= 0:
        target_score = 5

    ctx = dict(
        char_name=char_name,
        char_emoji=emoji,
        char_color="#a78bfa",
        char_svg_json=json.dumps(char_svg),
        world_svg_json=json.dumps(world_svg),
        item_emoji=item_emoji,
        bg_top=bg_top,
        bg_bot=bg_bot,
        pace_scale=pace_scale,
        time_limit=time_limit,
        target_score=target_score,
    )

    # AI가 hazard / friend emoji 직접 지정 가능
    ai_hazard = (params or {}).get("hazard_emoji", "")
    if isinstance(ai_hazard, str) and ai_hazard.strip():
        ctx["hazard_emoji"] = ai_hazard.strip()
    ai_friend = (params or {}).get("friend_emoji", "")
    if isinstance(ai_friend, str) and ai_friend.strip():
        ctx["friend_emoji"] = ai_friend.strip()

    fn = TEMPLATES.get(game_type, TEMPLATES["collect"])
    return fn(**ctx)


def build_game(character_cards: list, world_cards: "list | None" = None) -> str:
    _ = world_cards
    return build_game_with_params(character_cards or [], {}, "")
