# SERVICE-PROOFREADING
lambda 에 코드를 복붙하여 배포하는 방식으로 배포.
(코드 변동이 자주 없음.)

배포 버전은 gateway에 연결되어있지 않고, invoke 를 통해서만 호출 가능.

# 스크립트 기록
[스크립트 기록 문서](https://topialive.atlassian.net/wiki/spaces/coding/pages/205717516/AI)에 스크립트 업데이트.
비개발 인원도 파악 가능하도록, 공통 구역 / 과목&레벨별 구역을 나누어 표기.

### 배포 준비물
1. archive/openai-lambda-package.zip : 람다 레이어로 추가되어야 함. (일부러 지우지 않는 이상 수정할 필요는 없음)
2. runtime 은 3.10 으로 지정.