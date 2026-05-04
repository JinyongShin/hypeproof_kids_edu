"""게임 엔진 — Spec composition 방식.

LLM은 작은 JSON spec을 emit한다. 이 파일의 단일 universal renderer가
spec을 받아 동일한 HTML 템플릿 안에서 분기 실행한다.

장점 vs 4 enumerated 템플릿:
- 메카닉 enumeration 없음. 부품 조합으로 수백 가지 게임 표현 가능.
- 파일 1개, 함수 1개로 추가 메카닉 = spec field 추가 + JS 분기 추가.
- LLM 출력은 여전히 짧은 JSON (Cloudflare 100s 안전, R4 보장).

Spec schema (모든 필드 optional, default로 채움):
{
  "player": {
    "movement": "free" | "x_fixed" | "jump" | "swim",
    "x": 200, "y": 500, "speed": 5,
    "gravity": 0.7, "jump_v": -13   // jump 일 때만
  },
  "spawns": [
    {
      "role": "item" | "hazard" | "friend",
      "sprite": "이모지 1개",
      "from": "top" | "bottom" | "left" | "right" | "alternating_lr"
            | "static_grid_bottom" | "wandering",
      "motion": "fall" | "rise" | "horizontal" | "sine" | "static" | "wandering",
      "rate": 0.03,            // 분당 spawn 빈도 (0~0.1). static_*은 무시.
      "speed": 2,              // 이동 속도 multiplier
      "score_delta": 1,        // collide 시 점수 변화 (item=+1, hazard=-1 default)
      "respawn_on_collect": true   // friend는 보통 true
    }
  ],
  "world": {
    "scroll": "none" | "horizontal" | "parallax",
    "bg_svg": "..."             // optional, world card SVG
  },
  "goal": {
    "time_limit": 45,           // seconds, 0이면 시간 제한 없음 (target만으로 종료)
    "target_score": 0           // 0이면 목표 없음 (시간만으로 종료)
  },
  "char_sprite": "...",         // character SVG
  "title_msg": "캐릭터의 모험!"
}
"""
import json
from string import Template


UNIVERSAL_TMPL = Template('''<!DOCTYPE html>
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
<div id="ui"><div id="score">⭐ 0</div><div id="msg">$title_msg</div></div>
<div id="toast"></div>
<canvas id="c" width="400" height="600"></canvas>
<button id="restart" onclick="resetGame()">다시 하기! &#x1f504;</button>
<script>
const SPEC = $spec_json;
const canvas = document.getElementById("c"), ctx = canvas.getContext("2d");
const W = 400, H = 600, GROUND = H - 90;

// --- player init ---
const PLAYER_DEF = SPEC.player || {};
const movement = PLAYER_DEF.movement || "free";
const player = {
  x: PLAYER_DEF.x !== undefined ? PLAYER_DEF.x : (movement === "jump" ? 100 : 200),
  y: PLAYER_DEF.y !== undefined ? PLAYER_DEF.y : (movement === "jump" ? GROUND - 48 : 500),
  vy: 0,
  w: 48, h: 48,
  speed: PLAYER_DEF.speed || 5,
  gravity: PLAYER_DEF.gravity !== undefined ? PLAYER_DEF.gravity : 0.7,
  jump_v: PLAYER_DEF.jump_v !== undefined ? PLAYER_DEF.jump_v : -13,
  onGround: true,
};

// --- world / goal ---
const WORLD = SPEC.world || {};
const SCROLL_MODE = WORLD.scroll || "none";
const WORLD_SVG = WORLD.bg_svg || "";
const TIME_LIMIT = (SPEC.goal && SPEC.goal.time_limit !== undefined) ? SPEC.goal.time_limit : 45;
const TARGET_SCORE = (SPEC.goal && SPEC.goal.target_score) || 0;
const CHAR_SVG = SPEC.char_sprite || "";

let score = 0, timeLeft = TIME_LIMIT, gameOver = false;
let scrollX = 0;
const SPAWNS = SPEC.spawns || [];
let entities = [];           // {x,y,vx,vy,size,role,sprite,score_delta,respawn,motion,phase}
let particles = [];

// --- assets ---
let charImg = null, worldImg = null;
function svgToImage(svg, cb){
  if (!svg) return;
  const img = new Image();
  img.onload = () => cb(img);
  img.onerror = () => {};
  img.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(svg);
}
svgToImage(CHAR_SVG, i => charImg = i);
svgToImage(WORLD_SVG, i => worldImg = i);

// --- input ---
const keys = {};
document.addEventListener("keydown", e => keys[e.key] = true);
document.addEventListener("keyup", e => keys[e.key] = false);
document.addEventListener("keydown", e => {
  if (movement === "jump" && (e.key === " " || e.key === "ArrowUp" || e.key === "w" || e.key === "W")) {
    if (player.onGround) { player.vy = player.jump_v; player.onGround = false; }
  }
});
let touchX = null;
canvas.addEventListener("touchstart", e => {
  if (movement === "jump") {
    if (player.onGround) { player.vy = player.jump_v; player.onGround = false; }
  } else {
    touchX = e.touches[0].clientX;
  }
  e.preventDefault();
}, {passive: false});
canvas.addEventListener("touchmove", e => {
  if (movement !== "jump") touchX = e.touches[0].clientX;
  e.preventDefault();
}, {passive: false});
canvas.addEventListener("touchend", () => touchX = null);

// --- spawn entity ---
function spawnFromSpec(specIdx) {
  const sp = SPAWNS[specIdx];
  if (!sp) return;
  let x, y, vx = 0, vy = 0;
  const speedMult = (sp.speed || 2);
  switch (sp.from) {
    case "top":
      x = Math.random() * (W - 30) + 15; y = -20;
      vy = (1 + Math.random() * 2) * speedMult; break;
    case "bottom":
      x = Math.random() * (W - 30) + 15; y = H + 20;
      vy = -(1 + Math.random() * 2) * speedMult; break;
    case "left":
      x = -20; y = Math.random() * (GROUND - 80) + 40;
      vx = (1 + Math.random() * 2) * speedMult; break;
    case "right":
      x = W + 20; y = Math.random() * (GROUND - 80) + 40;
      vx = -(1 + Math.random() * 2) * speedMult; break;
    case "alternating_lr":
      const fromLeft = Math.random() < 0.5;
      x = fromLeft ? -20 : W + 20;
      y = Math.random() * (GROUND - 80) + 40;
      vx = (fromLeft ? 1 : -1) * (1 + Math.random() * 2) * speedMult; break;
    case "wandering":
      x = Math.random() * (W - 60) + 30;
      y = Math.random() * (GROUND - 80) + 40;
      const ang = Math.random() * Math.PI * 2;
      vx = Math.cos(ang) * speedMult; vy = Math.sin(ang) * speedMult; break;
    case "static_grid_bottom":
      // handled in initial population
      return;
    default:
      x = Math.random() * (W - 30) + 15; y = -20;
      vy = (1 + Math.random() * 2) * speedMult;
  }
  // motion overrides initial velocity
  if (sp.motion === "static") { vx = 0; vy = 0; }
  if (sp.motion === "rise" && vy >= 0) vy = -Math.abs(vy || speedMult);
  entities.push({
    x, y, vx, vy,
    size: 24 + Math.random() * 8,
    rot: 0,
    role: sp.role || "item",
    sprite: sp.sprite || "⭐",
    score_delta: sp.score_delta !== undefined ? sp.score_delta : (sp.role === "hazard" ? -1 : 1),
    respawn: !!sp.respawn_on_collect,
    motion: sp.motion || "fall",
    phase: Math.random() * Math.PI * 2,  // for sine
    specIdx: specIdx,
  });
}

// initial population for static_grid_bottom roles
SPAWNS.forEach((sp, idx) => {
  if (sp.from === "static_grid_bottom") {
    const count = 8;
    for (let i = 0; i < count; i++) {
      entities.push({
        x: 30 + (i * (W - 60) / (count - 1)),
        y: GROUND - 30,
        vx: 0, vy: 0,
        size: 26,
        rot: 0,
        role: sp.role || "item",
        sprite: sp.sprite || "⭐",
        score_delta: sp.score_delta !== undefined ? sp.score_delta : 1,
        respawn: !!sp.respawn_on_collect,
        motion: "static",
        phase: 0,
        specIdx: idx,
      });
    }
  }
});

function addParticle(x, y, color) {
  for (let i = 0; i < 6; i++) particles.push({
    x, y,
    vx: (Math.random() - 0.5) * 5,
    vy: (Math.random() - 0.5) * 5,
    life: 30, color, size: 3 + Math.random() * 3
  });
}
function showToast(msg, color) {
  const t = document.getElementById("toast");
  t.textContent = msg; t.style.color = color || "#ffd166";
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 700);
}

function update() {
  if (gameOver) return;

  // player movement
  if (movement === "free" || movement === "swim") {
    if (keys.ArrowLeft || keys.a) player.x -= player.speed;
    if (keys.ArrowRight || keys.d) player.x += player.speed;
    if (keys.ArrowUp || keys.w) player.y -= player.speed;
    if (keys.ArrowDown || keys.s) player.y += player.speed;
    if (touchX !== null) player.x += (touchX - canvas.getBoundingClientRect().left - player.w/2 - player.x) * 0.1;
  } else if (movement === "jump") {
    if (keys.ArrowLeft || keys.a) player.x -= player.speed;
    if (keys.ArrowRight || keys.d) player.x += player.speed;
    player.vy += player.gravity;
    player.y += player.vy;
    if (player.y >= GROUND - player.h) {
      player.y = GROUND - player.h;
      player.vy = 0;
      player.onGround = true;
    }
  } else if (movement === "x_fixed") {
    if (keys.ArrowUp || keys.w) player.y -= player.speed;
    if (keys.ArrowDown || keys.s) player.y += player.speed;
  }
  player.x = Math.max(0, Math.min(W - player.w, player.x));
  if (movement !== "jump") player.y = Math.max(0, Math.min(H - player.h, player.y));

  // scroll
  if (SCROLL_MODE === "horizontal" || SCROLL_MODE === "parallax") {
    scrollX += 3;
  }

  // spawn from rate-based specs
  SPAWNS.forEach((sp, idx) => {
    if (sp.from === "static_grid_bottom") return;
    if (Math.random() < (sp.rate || 0.03)) spawnFromSpec(idx);
  });

  // entity update
  for (let i = entities.length - 1; i >= 0; i--) {
    const e = entities[i];
    if (e.motion === "sine") {
      e.phase += 0.05;
      e.x += Math.sin(e.phase) * 1.5;
      e.y += e.vy || 1;
    } else if (e.motion === "wandering") {
      e.x += e.vx; e.y += e.vy;
      if (e.x <= 0 || e.x >= W - e.size) e.vx *= -1;
      if (e.y <= 0 || e.y >= GROUND - e.size) e.vy *= -1;
    } else {
      e.x += e.vx; e.y += e.vy;
    }
    e.rot += 0.05;

    // collide with player
    const dx = (e.x) - (player.x + player.w/2);
    const dy = (e.y) - (player.y + player.h/2);
    if (Math.abs(dx) < 32 && Math.abs(dy) < 32) {
      score = Math.max(0, score + e.score_delta);
      if (e.score_delta < 0) {
        addParticle(e.x, e.y, "#ff5566");
        showToast("앗 조심!", "#ff8899");
      } else if (e.role === "friend") {
        addParticle(e.x, e.y, "#a0e7e5");
        showToast("친구 +1!", "#a0e7e5");
      } else {
        addParticle(e.x, e.y, "#ffd166");
        if (e.score_delta > 1) showToast("+" + e.score_delta, "#ffd166");
      }
      if (e.respawn) {
        // respawn at new location (for friend/wandering pattern)
        spawnFromSpec(e.specIdx);
      }
      entities.splice(i, 1);
      // early-win check
      if (TARGET_SCORE > 0 && score >= TARGET_SCORE) {
        gameOver = true;
        document.getElementById("restart").style.display = "block";
      }
      continue;
    }
    // off-screen cleanup (static items don't expire)
    if (e.motion !== "static") {
      if (e.x < -50 || e.x > W + 50 || e.y > H + 30 || e.y < -50) {
        entities.splice(i, 1);
      }
    }
  }

  // particles
  for (let i = particles.length - 1; i >= 0; i--) {
    particles[i].x += particles[i].vx;
    particles[i].y += particles[i].vy;
    particles[i].life--;
    if (particles[i].life <= 0) particles.splice(i, 1);
  }

  // time
  if (TIME_LIMIT > 0) {
    timeLeft -= 1/60;
    if (timeLeft <= 0) {
      gameOver = true;
      document.getElementById("restart").style.display = "block";
    }
  }
  document.getElementById("score").textContent =
    "⭐ " + score + (TARGET_SCORE > 0 ? "/" + TARGET_SCORE : "");
}

function draw() {
  // bg
  if (worldImg) {
    if (SCROLL_MODE === "horizontal" || SCROLL_MODE === "parallax") {
      const sf = SCROLL_MODE === "parallax" ? 0.3 : 1;
      const ox = ((-scrollX * sf) % W + W) % W;
      ctx.drawImage(worldImg, -ox, 0, W, H);
      ctx.drawImage(worldImg, W - ox, 0, W, H);
    } else {
      ctx.drawImage(worldImg, 0, 0, W, H);
    }
    ctx.fillStyle = "rgba(0,0,0,0.15)";
    ctx.fillRect(0, 0, W, H);
  } else {
    const grd = ctx.createLinearGradient(0, 0, 0, H);
    grd.addColorStop(0, "#1e1b4b");
    grd.addColorStop(1, "#0f172a");
    ctx.fillStyle = grd;
    ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = "rgba(255,255,255,0.25)";
    for (let i = 0; i < 40; i++) {
      const sx = (i * 137 + 50) % W, sy = (i * 97 + 30) % H;
      ctx.beginPath(); ctx.arc(sx, sy, (i % 3) + 1, 0, Math.PI * 2); ctx.fill();
    }
  }
  // ground (jump mode visual)
  if (movement === "jump") {
    ctx.fillStyle = "rgba(80,60,120,0.7)";
    ctx.fillRect(0, GROUND, W, H - GROUND);
  }
  // entities
  entities.forEach(e => {
    ctx.save();
    ctx.translate(e.x, e.y);
    if (e.motion !== "static") ctx.rotate(e.rot);
    ctx.font = e.size + "px serif";
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    if (e.role === "hazard") { ctx.shadowColor = "#ff5566"; ctx.shadowBlur = 12; }
    else if (e.role === "friend") { ctx.shadowColor = "#a0e7e5"; ctx.shadowBlur = 12; }
    ctx.fillText(e.sprite, 0, 0);
    ctx.restore();
  });
  // particles
  particles.forEach(p => {
    ctx.globalAlpha = p.life / 30;
    ctx.fillStyle = p.color;
    ctx.beginPath(); ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2); ctx.fill();
  });
  ctx.globalAlpha = 1;
  // player
  if (charImg) {
    ctx.save();
    ctx.shadowColor = "#a78bfa"; ctx.shadowBlur = 18;
    ctx.drawImage(charImg, player.x, player.y, player.w, player.h);
    ctx.restore();
  } else {
    ctx.font = "40px serif";
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.fillText("✨", player.x + player.w/2, player.y + player.h/2);
  }
  // game over
  if (gameOver) {
    ctx.fillStyle = "rgba(0,0,0,0.5)"; ctx.fillRect(0, 0, W, H);
    ctx.fillStyle = "white";
    ctx.font = "bold 36px sans-serif"; ctx.textAlign = "center";
    const won = TARGET_SCORE > 0 && score >= TARGET_SCORE;
    ctx.fillText(won ? "성공! 🎉" : "시간 끝!", W/2, H/2 - 30);
    ctx.font = "24px sans-serif";
    ctx.fillText("⭐ " + score + " 점!", W/2, H/2 + 20);
  }
}

function resetGame() {
  score = 0; timeLeft = TIME_LIMIT; gameOver = false;
  entities = []; particles = [];
  if (movement === "jump") {
    player.y = GROUND - player.h; player.vy = 0; player.onGround = true; player.x = 100;
  } else {
    player.x = PLAYER_DEF.x !== undefined ? PLAYER_DEF.x : 200;
    player.y = PLAYER_DEF.y !== undefined ? PLAYER_DEF.y : 500;
  }
  // re-populate static grid items
  SPAWNS.forEach((sp, idx) => {
    if (sp.from === "static_grid_bottom") {
      const count = 8;
      for (let i = 0; i < count; i++) {
        entities.push({
          x: 30 + (i * (W - 60) / (count - 1)),
          y: GROUND - 30, vx: 0, vy: 0,
          size: 26, rot: 0,
          role: sp.role || "item",
          sprite: sp.sprite || "⭐",
          score_delta: sp.score_delta !== undefined ? sp.score_delta : 1,
          respawn: !!sp.respawn_on_collect,
          motion: "static", phase: 0, specIdx: idx,
        });
      }
    }
  });
  document.getElementById("restart").style.display = "none";
}

function loop() { update(); draw(); requestAnimationFrame(loop); }
loop();
</script></body></html>''')


# ---------------------------------------------------------------------------
# Spec validation + defaults
# ---------------------------------------------------------------------------

ALLOWED_MOVEMENT = {"free", "x_fixed", "jump", "swim"}
ALLOWED_FROM = {"top", "bottom", "left", "right", "alternating_lr",
                "static_grid_bottom", "wandering"}
ALLOWED_MOTION = {"fall", "rise", "horizontal", "sine", "static", "wandering"}
ALLOWED_ROLE = {"item", "hazard", "friend"}
ALLOWED_SCROLL = {"none", "horizontal", "parallax"}


def _clamp(v, lo, hi, default):
    try:
        x = float(v)
    except (TypeError, ValueError):
        return default
    return max(lo, min(hi, x))


def _validate_spawn(s):
    """Spawn 한 개의 필드 정규화. 모든 필드 default 보장. 잘못된 입력이면 None."""
    if not isinstance(s, dict):
        return None
    role = s.get("role")
    if role not in ALLOWED_ROLE:
        role = "item"
    from_ = s.get("from")
    if from_ not in ALLOWED_FROM:
        from_ = "top"
    motion = s.get("motion")
    if motion not in ALLOWED_MOTION:
        motion = "fall"
    sprite = s.get("sprite") or ""
    if not isinstance(sprite, str) or len(sprite) > 8:
        sprite = "⭐" if role == "item" else ("💧" if role == "hazard" else "🐰")
    rate = _clamp(s.get("rate"), 0.001, 0.15, 0.03)
    speed = _clamp(s.get("speed"), 0.2, 6.0, 2.0)
    score_delta_default = -1 if role == "hazard" else 1
    score_delta = int(_clamp(s.get("score_delta"), -5, 5, score_delta_default))
    respawn = bool(s.get("respawn_on_collect", role == "friend"))
    return {
        "role": role,
        "from": from_,
        "motion": motion,
        "sprite": sprite,
        "rate": rate,
        "speed": speed,
        "score_delta": score_delta,
        "respawn_on_collect": respawn,
    }


def validate_spec(raw: dict, char_svg: str = "", world_svg: str = "",
                  char_name: str = "모험가") -> dict:
    """LLM이 emit한 spec을 검증·기본값 채움. 항상 작동 가능한 spec 반환."""
    if not isinstance(raw, dict):
        raw = {}

    # player
    p = raw.get("player") or {}
    if not isinstance(p, dict):
        p = {}
    movement = p.get("movement")
    if movement not in ALLOWED_MOVEMENT:
        movement = "free"
    player = {
        "movement": movement,
        "x": int(_clamp(p.get("x"), 0, 360, 200 if movement != "jump" else 100)),
        "y": int(_clamp(p.get("y"), 0, 540, 500)),
        "speed": _clamp(p.get("speed"), 1, 12, 5),
    }
    if movement == "jump":
        player["gravity"] = _clamp(p.get("gravity"), 0.2, 1.5, 0.7)
        player["jump_v"] = _clamp(p.get("jump_v"), -20, -6, -13)

    # spawns
    raw_spawns_in = raw.get("spawns")
    raw_spawns = raw_spawns_in if isinstance(raw_spawns_in, list) else []
    spawns = []
    for s in raw_spawns[:6]:  # 최대 6개로 제한 (성능)
        v = _validate_spawn(s)
        if v is not None:
            spawns.append(v)
    if not spawns:
        # fallback: 위에서 떨어지는 아이템 1개
        fallback = _validate_spawn({"role": "item", "from": "top", "motion": "fall"})
        if fallback:
            spawns.append(fallback)

    # world
    w = raw.get("world") or {}
    if not isinstance(w, dict):
        w = {}
    scroll = w.get("scroll")
    if scroll not in ALLOWED_SCROLL:
        scroll = "none"
    world = {
        "scroll": scroll,
        "bg_svg": w.get("bg_svg") or world_svg,
    }

    # goal
    g = raw.get("goal") or {}
    if not isinstance(g, dict):
        g = {}
    goal = {
        "time_limit": int(_clamp(g.get("time_limit"), 0, 180, 45)),
        "target_score": int(_clamp(g.get("target_score"), 0, 50, 0)),
    }

    char_sprite = raw.get("char_sprite") or char_svg
    title_msg = raw.get("title_msg") or f"{char_name}의 모험!"

    return {
        "player": player,
        "spawns": spawns,
        "world": world,
        "goal": goal,
        "char_sprite": char_sprite,
        "title_msg": title_msg,
    }


# ---------------------------------------------------------------------------
# Builder
# ---------------------------------------------------------------------------

def build_game_with_spec(spec_raw: dict, char_card=None, world_card=None) -> str:
    """검증된 spec → HTML 문자열."""
    char_card = char_card or {}
    world_card = world_card or {}
    char_svg = char_card.get("image_svg", "") or ""
    world_svg = world_card.get("image_svg", "") or ""
    char_name = char_card.get("name", "모험가") or "모험가"
    spec = validate_spec(spec_raw, char_svg=char_svg, world_svg=world_svg,
                         char_name=char_name)
    spec_json = json.dumps(spec, ensure_ascii=False)
    title_msg = spec["title_msg"].replace('"', "'")
    return UNIVERSAL_TMPL.safe_substitute(
        spec_json=spec_json,
        title_msg=title_msg,
    )


# ---------------------------------------------------------------------------
# Helpers — equivalent specs for the 4 legacy mechanics (등가성 검증용)
# ---------------------------------------------------------------------------

def spec_for_collect(item_emoji: str = "⭐") -> dict:
    return {
        "player": {"movement": "free"},
        "spawns": [{"role": "item", "from": "top", "motion": "fall",
                    "sprite": item_emoji, "rate": 0.03, "speed": 2}],
        "world": {"scroll": "none"},
        "goal": {"time_limit": 45, "target_score": 0},
    }


def spec_for_dodge(item_emoji: str = "⭐", hazard_emoji: str = "💧") -> dict:
    return {
        "player": {"movement": "free"},
        "spawns": [
            {"role": "item", "from": "top", "motion": "fall",
             "sprite": item_emoji, "rate": 0.025, "speed": 2.5},
            {"role": "hazard", "from": "top", "motion": "fall",
             "sprite": hazard_emoji, "rate": 0.02, "speed": 2.5},
        ],
        "world": {"scroll": "none"},
        "goal": {"time_limit": 45, "target_score": 0},
    }


def spec_for_chase(friend_emoji: str = "🐰") -> dict:
    return {
        "player": {"movement": "free"},
        "spawns": [{"role": "friend", "from": "wandering", "motion": "wandering",
                    "sprite": friend_emoji, "rate": 0.001, "speed": 1.8,
                    "score_delta": 1, "respawn_on_collect": True}],
        "world": {"scroll": "none"},
        "goal": {"time_limit": 45, "target_score": 5},
    }


def spec_for_jump(item_emoji: str = "⭐", hazard_emoji: str = "🌵") -> dict:
    return {
        "player": {"movement": "jump"},
        "spawns": [
            {"role": "hazard", "from": "right", "motion": "horizontal",
             "sprite": hazard_emoji, "rate": 0.018, "speed": 4},
            {"role": "item", "from": "right", "motion": "horizontal",
             "sprite": item_emoji, "rate": 0.022, "speed": 4, "score_delta": 2},
        ],
        "world": {"scroll": "horizontal"},
        "goal": {"time_limit": 45, "target_score": 0},
    }
