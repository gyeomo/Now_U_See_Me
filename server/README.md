# Now_U_See_Me Server

## 1. 개발 환경 구축 및 설치  
 - JavaScript
 - Express
 - Node.js
 - Mysql 5.7
 - Ubuntu 18.0.1  
   
## 2. 사용법  
  
### mysql 5.7 설치 및 구동

#### 설치  
  
**설치 명령어**
`# apt-get install mysql-server -y`  
  
**확인**    
`mysql --version`    
    
**구동 확인**    
`# service mysqlId start`  
`mysql -u root -p`    
(default password는 `enter`키입력 이다.)  
  
**환경설정**  
`# service mysqlId start`  
`mysql_secure_installation`    

1. 비밀번호 복잡도 검사과정(n)  
2. 비밀번호 입력 & 확인(beyondme)  
3. 익명사용자 삭제(y)  
4. 원격접속허용(n)  
5. test DB삭제(n)  
6. previlege 테이블을 다시 로드할 것인지(n)  
7. 확인할 것이 더 있는지?(n)  
   
#### 비밀번호 변경(필요시)  
  
**mysql 구동 후**  
  
`alter user 'root'@'localhost' identified with beyondme by 'root';`  

**재실행**  
  
`# service mysqld restart`    
  
### Server 실행  
  
1. 터미널 열기  
2. server가 있는 폴더로 이동  
3. `npm start` 입력  
    
## 3. 특징  
  
- REST API Server 구축
    - SW 구조
        - app: 서버기능
            - api: api 로직 담당
                - `index.js`: request를 처리하기 위해 미들웨어들을 모아둔 곳
                - `controller.js`: 미들웨어에서 받은 내용을 처리해주는 곳
            - config: 서버가 구동하기 위한 환경변수 정의(상수)
            - models: 데이터베이스 모델링
        - bin: 서버 구동을 위한 코드
            - `www.js`: 서버 구동
            - `sync-database`: DB 싱크
    - 환경의 분리
        - 테스트때문에 서버가 실행되는 모드를 몇개 정의해야 한다. 테스트를 할 때 DB를 연결하게 되면 DB 테스트에서 사용한 데이터들이 쌓이게 된다. 따라서 테스트용 데이터베이스가 따로 있어야 하는데 이것을 위해 서버 환경을 분리한다.
        - 세가지 모드를 사용하였다
            - development
                - 개발모드로써 평소 개발할 때 쓰이는 환경이다.
            - test
                - test 환경으로 코드가 제대로 돌아가는지 mocha를 통해 TDD용으로 만들었다.
            - production
                - 운영모드로 실제로 코드가 서버로 배포되어 동작하는 환경을 의미한다.
                
            - 이러한 정보는 /app/config/environment.js에 구현되어 있다.
            ```c
            const environment = {
                development: {
                    mysql: {
                        username: 'root',
                        password: '',
                        database: 'now_u_see_me'
                    }
                },
                test: {
                    mysql: {
                        username: 'root',
                        password: '',
                        database: 'now_u_see_me_test'
                    }
                },
                production: {
                    mysql: {
                        username: 'root',
                        password: '',
                        database: 'NUSM'
                    }
                }
            }
            const nodeEnv = process.env.NODE_ENV || 'development';
            module.exports = environment[nodeEnv];
            ```  
            environments라는 변수를 두어 각 환경 이름에 해당하는 키를 만들었다. 그리고 nodeEnv라는 상수에 노드환경변수 값을 할당하였다. 노드를 실행하기 전에 "Node_ENV = test"라고 실행하면 이값에 "test"라는 문자열이 들어간다. 만약 아무것도 설정하지 않았으면 "development"문자열이 들어가게 될 것이다.
    - Mocha를 이용해 TDD 구현  
        describe()를 이용해 테스트 suite를 만들고, it()을 이용해 test를 실행하도록 했다.   
        test검증은 assert를 쓸 수도 있었지만 node.js 공식 홈페이지에서 다른 모듈을 사용하는 것을 권장하고 있기에 should 모듈을 이용해 서술식 검증 코드를 만들었다. 마지막으로 supertest 모듈을 이용해 express 프레임 워크 위에서 api 테스트를 가능하게 했다.
    - Sequelize를 이용한 ORM 사용
    - multer를 이용한 local storage 핸들링
    
- FCM을 이용해 notification 구현
    - FCM 사용 이유  
        어플리케이션의 알림기능을 구현하기 위해선 현재 서버에서 클라이언트로 알림을 전달할 방법이 있어야 한다. 
        그러나 본연의 서버의 기능을 수행하면서 또 하나의 복잡한 알림기능까지 포함하면 서버에 과부하가 걸린다고 판단하여 Google에서 무료로 제공하는 Firebase Cloud Messaging을 이용하였다.
    
	
       
## Revision history    
  
[now_u_see_me_server](https://github.com/kiryun/now_u_see_me_server)
