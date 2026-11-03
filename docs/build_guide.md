# RoboRacer 공식 조립 가이드 요약

원문: <https://f1tenth.readthedocs.io/en/main/getting_started/build_car> (난이도 중급, 약 1.5시간)
`roboracer.ai/build` 페이지는 이 문서로 연결된다. RoboRacer는 F1TENTH의 새 이름.

## 기본 구성 (공식 사이트 3D 모델 기준)

| 부품 | 공식 구성 | 비고 |
|---|---|---|
| 차체 | Traxxas Slash 4x4 (Premium) | 기존 전장은 빼고 **조향 서보만 남김** |
| 컴퓨터 | NVIDIA Jetson Orin (문서 사진은 Xavier NX) | LiDAR·VESC를 USB로 연결 |
| 모터 제어 | VESC | 모터와 조향 서보(PPM 선)를 함께 구동, Jetson과 USB |
| 전원 | 파워보드 | 배터리 → Jetson, LiDAR에 12V |
| LiDAR | Hokuyo UTM-30LX (USB) / UST-10LX (이더넷) | 두 모델은 장착 구멍이 조금 다름 |
| 상판 | 레이저 컷 Platform Deck (.dxf) | 이 저장소는 UNICORN 3D 프린팅 판으로 대체 |

## 1. 아래층 차체 (Lower Level Chassis)

준비: Traxxas 기본 육각렌치 3개, 뺀 나사 담을 통, 드라이버/펜치, **M3 나사 3개 + M3 FF 45 mm 스탠드오프 3개**, 나사 고정제, LiPo 배터리, 내화 충전백

1. 차 껍데기 클립 4개 제거
2. 기존 ESC(XL5) 제거: 나사 2개, 모터로 가는 총알 커넥터 분리
3. 리시버 박스 제거: 뚜껑 열고 ESC 선·서보 선을 리시버에서 분리 → 리시버를 양면테이프에서 떼기 → 박스 나사 2개 → **안테나 튜브**는 필요하면 드라이버/펜치로 뽑기
4. 기존 브러시드 모터 제거 (나사 1개, 보관)
5. 서보 반대쪽의 플라스틱 배터리 고정 포크 제거
6. **조향 서보(작은 파란 박스)만 남기고** 나머지 전장 전부 제거
7. 사이드 바(nerf bar) 2개 제거 (각 나사 4개, 아래쪽에서)
8. 바닥에서 M3 나사로 **45 mm 스탠드오프 3개** 고정: 모터 쪽 2, 배터리 쪽 1 (나사 고정제 권장)
9. 배터리를 모터 반대쪽 칸에 넣기

## 2. 자율주행 부품 준비 (Autonomy Elements)

- Jetson: 개발 보드 윗면 나사 4개 풀고, 안테나 선 분리 후 모듈 분리
- 와이파이 안테나: L자 브래킷에서 분리 → 보관한 나사에 **M3 FF 45 mm 스탠드오프 2개** → 안테나 재조립

## 3. 위층 판 (Upper Level Chassis)

1. **VESC**: 전원선이 바깥, A/B/C 선이 안쪽 → 판 뒤집어 **M5 나사 2개(대각선)**
2. **안테나**: VESC 뒤쪽에 M3 나사로, 선은 파워보드 아래로 돌려 Jetson까지
3. **Jetson**: 안테나 선 먼저 연결 → 판 아래에서 **M3 25 mm 스탠드오프** → M3 나사 4개
4. **파워보드**: 25 mm 스탠드오프 3개, **M3×8 나사**, 녹색 단자가 차 앞쪽, VESC와 간격 두기
5. **LiDAR**: 기종에 맞는 구멍, 아래에서 M3 나사 4개

> 공식 판은 비대칭(VESC 구멍이 한쪽으로 치우침). 방향 확인 후 장착.
> UNICORN Traxxas 판은 판 아래에 VESC 공간이 없어 **VESC를 판 위에** 고정하고, 케이블은 판 아래로 정리하되 **중심 구동축과 닿지 않게**.

## 4. 합체와 배선 (All Together)

1. 위층 판을 스탠드오프 위에 (VESC가 뒤쪽), PPM 선은 판 구멍으로 빼기, **M3×10 나사 3개**로 고정
2. 배선 순서
   - **모터 → VESC**: 4 mm→3.5 mm 총알 어댑터, **A=흰색, B=노란색, C=파란색**. VESC 펌웨어 후 거꾸로 돌면 흰↔파 교체
   - **배터리 → VESC**: 빨강=+, 검정=- 확인
   - **파워보드 12V → Jetson**: 배럴잭 **가운데 핀이 +**, 연결 전 극성 확인
   - **LiDAR**: 데이터는 USB(UTM-30LX) 또는 이더넷(UST-10LX), 전원은 12V 단자 (**갈색=+, 파란색=GND**)
   - **서보 PPM → VESC PPM 슬롯** (갈색 GND ↔ 서보 검정선)
   - **VESC micro USB → Jetson USB 허브**
   - 안테나 장착
3. 모든 케이블은 구동축·회전부와 떨어지게, LiDAR USB는 케이블 타이로 고정

## ⚠️ LiPo 안전

- **배터리를 거꾸로 꽂으면 VESC, 파워보드, Jetson이 손상되고 단락될 수 있음**
- 충전은 내화백에 넣고 불연성 바닥에서 지켜보면서
- 안 쓸 때는 배터리 분리 (과방전되면 충전 불가)
- 부풀거나 타는 냄새·연기 → 즉시 분리
- 배터리 단자끼리 절대 단락 금지

## 이후 (문서 조립 페이지에 링크 없음, 따로 정리 예정)

- VESC 펌웨어·모터 감지·서보 설정 (참고: UNICORN [서보 파라미터](https://hmcl-unist.github.io/unicorn-racing/posts/servo-parameter/), [ERPM 게인](https://hmcl-unist.github.io/unicorn-racing/posts/erpm-gain-calibration/))
- Jetson: Ubuntu + ROS 2 Humble, [`f1tenth_system` (humble-devel)](https://github.com/f1tenth/f1tenth_system/tree/humble-devel)
- 조이스틱 수동 주행 → LiDAR 확인 → Gap-follow 저속 자율주행 → Cartographer 맵/위치추정 → 레이싱라인 + Pure Pursuit/MAP
