/**
 * 블록별 프롬프팅 스캐폴드 데이터.
 *
 * curriculum-wizard-v1: 타이틀 카드 생성 워크샵
 *
 * 이 파일만 보면 각 블록에서 아이들이 배우는 AI 프롬프팅 스킬과
 * 예시 문장을 파악할 수 있어야 한다.
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
    skill: "지휘관의 선언",
    skillDesc: "오프닝 — AI에게 만들 것을 선언한다",
    // 오프닝 블록 — 카드 없음
    prompts: [],
  },
  {
    block: 1,
    skill: "아바타 소환",
    skillDesc: "캐릭터를 묘사해서 소환한다",
    prompts: [
      "토끼처럼 생긴 캐릭터 만들어줘",
      "날개 달린 고양이",
      "반짝이는 별 요정",
      "귀여운 곰돌이 전사",
    ],
  },
  {
    block: 2,
    skill: "세계 구축",
    skillDesc: "캐릭터가 살 세계를 묘사한다",
    prompts: [
      "바다가 있는 세계 만들어줘",
      "우주 배경으로 해줘",
      "꽃이 가득한 숲으로 해줘",
      "구름 위의 성으로 해줘",
    ],
  },
  {
    block: 3,
    skill: "마스터 개발자",
    skillDesc: "카드를 꾸미고 효과를 추가한다",
    prompts: [
      "반짝이 효과 추가해줘",
      "무지개 배경으로 바꿔줘",
      "캐릭터에 왕관 씌워줘",
      "별가루 효과 넣어줘",
    ],
  },
  {
    block: 4,
    skill: "런칭쇼",
    skillDesc: "완성된 카드를 발표한다",
    // 발표 블록 — 카드 없음
    prompts: [],
  },
];

export function getScaffold(block: number): ScaffoldBlock | undefined {
  return SCAFFOLD_DATA.find((s) => s.block === block);
}
