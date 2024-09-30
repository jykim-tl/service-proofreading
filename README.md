# SERVICE-PROOFREADING
lambda 에 코드를 복붙하여 배포하는 방식으로 배포.
(코드 변동이 많지 않음.)

배포 버전은 gateway에 연결되어있지 않고, invoke 를 통해서만 호출 가능.

### 배포 준비물
1. archive/openai-lambda-package.zip : 람다 레이어로 추가되어야 함. (일부러 지우지 않는 이상 수정할 필요는 없음)
2. runtime 은 3.10 으로 지정.