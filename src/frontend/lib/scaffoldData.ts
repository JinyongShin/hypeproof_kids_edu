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
    block: 1,
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
    block: 2,
    skill: "마스터 개발자",
    skillDesc: "본격적으로 게임을 만든다",
    prompts: [
      "이 캐릭터로 게임 만들어줘",
      "별 모으기 게임 만들어줘",
      "친구 찾기 게임 만들어줘",
      "구름 타는 게임 만들어줘",
    ],
  },
];

export function getScaffold(block: number): ScaffoldBlock | undefined {
  return SCAFFOLD_DATA.find((s) => s.block === block);
}
