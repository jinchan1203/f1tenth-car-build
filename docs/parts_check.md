# 부품 확인 사항

## 배터리

보유: **DXF 2S LiPo 7.4V 8400 mAh 120C 하드케이스**, XT60 커넥터

| 연결 대상 | 2S (7.4V, 완충 8.4V) |
|---|---|
| 모터 (VESC 경유) | 돌긴 하지만 3S보다 느림 |
| VESC | ⚠️ 대부분 3S(약 8V) 이상 입력 → 조금만 방전돼도 전압 부족 가능. **우리 VESC 입력 범위 확인 필요** |
| Jetson Orin NX | ❌ 보통 9~20V 입력 → 승압 컨버터 없이는 부족 |
| LiDAR (Hokuyo) | ❌ 12V 필요 (공식 문서: 파워보드 12V 단자에서 공급) |

F1TENTH 차량은 보통 **3S LiPo (11.1V, 완충 12.6V)** 사용. 공식 BOM 페이지는 배터리 사양을 외부 스프레드시트로만 링크해서 직접 확인하지 못함.

**VESC가 Trampa VESC 6 MkVI라면 (같은 연구실 다른 팀 차 기준, 우리 부품도 같을 것으로 추정)**:
입력 **11.1V ~ 60V (3S ~ 12S)** 로 알려져 있음 ([fallman.tech 사양표](https://fallman.tech/vesc-6-controller), Trampa 공식 데이터시트는 미확인)
→ 2S(최대 8.4V)는 하한 미달 → **3S 이상 배터리 필요**. 2S 8400 mAh는 이 차에 쓰지 않는 것으로 정리.

VESC–배터리–모터 연결 참고: [UNICORN — How to Connect VESC to Battery and Motor](https://hmcl-unist.github.io/unicorn-racing/posts/vesc-battery-motor-connection-en/)

확인할 것:
- [ ] 우리 VESC가 실제로 VESC 6 MkVI인지 (라벨)
- [ ] 파워보드 입력 범위
- [ ] 연구실 3S 배터리 보유 여부
- [ ] 3S로 갈 경우: Slash 배터리 칸 크기, 커넥터(XT60/XT90/Traxxas)와 VESC 쪽 맞는지

## 스탠드오프·나사 (현재 미보유)

공식 레이저 컷 판 기준:

| 위치 | 규격 | 수량 |
|---|---|---|
| 아래 차체 → 상판 | M3 암-암(FF) 45 mm + M3 나사 | 3 |
| 와이파이 안테나 브래킷 | M3 FF 45 mm | 2 |
| 상판 → Jetson | M3 25 mm 스탠드오프 + M3 나사 | 4 |
| 상판 → 파워보드 | M3 25 mm 스탠드오프 + M3×8 | 3 |
| 상판 → 차체 스탠드오프 | M3×10 | 3 |
| VESC | M5 | 2 |
| LiDAR | M3 | 4 |
| 분할 상판 이음 | M3×10 볼트 + 너트 | 4 |

- UNICORN 판은 구멍 위치가 달라서 **판을 차체에 대보고 길이·개수 확정 후 구매**
- M3 황동 스탠드오프 세트(길이 혼합) 하나면 대부분 해결
- 급하면 3D 프린팅 임시 스탠드오프 가능 (진동에 약함 → 주행 전 금속으로 교체)

## 미정

- [ ] LiDAR 기종: 다른 팀 차는 Hokuyo 계열(검은 몸체·주황 뚜껑)로 보임 → 같은 부품이면 Hokuyo. 라벨로 UTM-30LX(USB) / UST-10LX(이더넷) 확인
- [ ] Jetson 캐리어보드 (상판 구멍과 맞는지)
- [ ] 와이파이 안테나·USB 허브·배럴잭 케이블·총알 어댑터(4→3.5 mm)·TRX↔XT90 어댑터 보유 여부
