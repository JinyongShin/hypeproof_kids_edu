"""LLM이 생성한 SVG를 저장/렌더 전에 소독하는 단일 진입점.

프런트엔드 (GamePreview.tsx의 sanitizeSvg)와 동일한 정책을 서버에서도
적용하여 defense-in-depth. 게임 HTML의 svgToImage는 data URL → Image()
경로라 스크립트 실행 위험은 낮지만, 카드 JSON은 다른 곳(어드민/디버그
뷰, /cards 엔드포인트)에서 그대로 인라인될 수 있어 입구에서 차단.
"""

import json
import re

_MAX_SVG_LEN = 8000  # 200x200 일러스트 기준 충분, 그 이상은 거부
_SCRIPT_RE = re.compile(r"<script[\s\S]*?</script>", re.IGNORECASE)
_FOREIGN_RE = re.compile(r"<foreignObject[\s\S]*?</foreignObject>", re.IGNORECASE)
_ON_ATTR_RE = re.compile(r"""\son\w+\s*=\s*(?:"[^"]*"|'[^']*'|[^\s>]+)""", re.IGNORECASE)
_JS_URL_RE = re.compile(
    r"""(?:href|xlink:href)\s*=\s*(?:"javascript:[^"]*"|'javascript:[^']*'|javascript:[^\s>]+)""",
    re.IGNORECASE,
)


def sanitize_svg(raw: str | None) -> str:
    """SVG 문자열을 sanitize. 빈 문자열·비-SVG·과대 입력은 빈 문자열로 거부."""
    if not raw or not isinstance(raw, str):
        return ""
    trimmed = raw.strip()
    if not trimmed.lower().startswith("<svg"):
        return ""
    if len(trimmed) > _MAX_SVG_LEN:
        return ""
    cleaned = _SCRIPT_RE.sub("", trimmed)
    cleaned = _FOREIGN_RE.sub("", cleaned)
    cleaned = _ON_ATTR_RE.sub("", cleaned)
    cleaned = _JS_URL_RE.sub("", cleaned)
    return cleaned


def sanitize_card_json(card_json_str: str) -> str:
    """카드 JSON 문자열에서 image_svg 필드를 소독. 파싱 실패 시 원본 반환."""
    try:
        data = json.loads(card_json_str)
    except (json.JSONDecodeError, TypeError):
        return card_json_str
    if isinstance(data, dict) and "image_svg" in data:
        data["image_svg"] = sanitize_svg(data.get("image_svg"))
        return json.dumps(data, ensure_ascii=False)
    return card_json_str
