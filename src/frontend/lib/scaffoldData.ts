/**
 * 블록별 프롬프팅 스캐폴드 데이터.
 *
 * 이 파일만 보면 각 블록에서 아이들이 배우는 AI 프롬프팅 스킬과
 * 예시 문장을 파악할 수 있어야 한다.
 *
 * 교육 목표 참조: wiki/specs/ai-prompting-literacy-input.md
 */

export interface ScaffoldBlock {
  block: number;
  /** 이 블록에서 연습하는 프롬프팅 스킬 이름 */
  skill: string;
  /** 스킬 설명 (퍼실리테이터 가이드용) */
  skillDesc: string;
  /** 아이에게 보여줄 예시 문장 카드. 빈 배열이면 카드 미표시 (자유 입력) */
  prompts: string[];
}

export const SCAFFOLD_DATA: ScaffoldBlock[] = [
  {
    block: 0,
    skill: "묘사하기",
    skillDesc: "원하는 것을 말로 그리듯 표현한다",
    prompts: [
      "토끼처럼 생긴 캐릭터 만들어줘",
      "날개 달린 고양이 캐릭터 만들어줘",
      "반짝이는 별 캐릭터 만들어줘",
      "귀여운 곰돌이 캐릭터 만들어줘",
    ],
  },
  {
    block: 1,
    skill: "구체화",
    skillDesc: "막연한 요청 → 구체적인 요청으로 바꾼다",
    prompts: [
      "왼쪽 오른쪽 화살표로 움직이게 해줘",
      "스페이스바 누르면 점프하게 해줘",
      "캐릭터가 빠르게 움직이게 해줘",
      "위아래 화살표로도 움직이게 해줘",
    ],
  },
  {
    block: 2,
    skill: "추가 요청",
    skillDesc: "기존 게임에 새 요소를 덧붙인다",
    prompts: [
      "거기다 친구 캐릭터도 추가해줘",
      "배경에 구름도 넣어줘",
      "화면에 별도 떠다니게 해줘",
      "꽃이 피어나는 효과도 추가해줘",
    ],
  },
  {
    block: 3,
    skill: "수정 요청",
    skillDesc: "특정 부분을 지목해서 바꾼다",
    prompts: [
      "별 대신 하트로 바꿔줘",
      "배경색을 하늘색으로 바꿔줘",
      "캐릭터를 더 크게 만들어줘",
      "점수를 화면 위쪽에 크게 표시해줘",
    ],
  },
  {
    block: 4,
    skill: "자유 조합",
    skillDesc: "배운 4가지 패턴을 자유롭게 조합한다",
    // 카드 없음 — 아이 스스로 입력
    prompts: [],
  },
  {
    block: 5,
    skill: "언어화",
    skillDesc: "어떻게 말했는지 설명한다",
    // 발표 블록 — 카드 없음
    prompts: [],
  },
];

export function getScaffold(block: number): ScaffoldBlock | undefined {
  return SCAFFOLD_DATA.find((s) => s.block === block);
}
