# LUSH Clone Project

- 비건 프레쉬 코스메틱 브랜드 - 러쉬(LUSH) 사이트 클론.

## HHYYY - 훈훈한 연들

- 팀워크를 다지고자, 팀원들 이름을 바탕으로 팀명을 정했습니다.
- 팀원들 각자의 기술에 익숙해지는 것을 목표로 하여, 페이지 단위로 개발하였습니다.
- 팀원들 수준별로 적절한 역할 분담과 애자일한 스크럼 방식의 미팅, 그리고 활발한 의사소통으로 프로젝트를 성공적으로 마무리하였습니다.
- 기획 과정 없이 짧은 기간 안에 기술 습득 및 기본 기능 구현에 집중하기 위해 러쉬 사이트를 참고하였으며, 실제 서비스 개발 과정과 마찬가지로 무에서 유를 창조했습니다.

## 개발 기간 및 개발 인원

- 개발 기간 : 2021-10-04 ~ 2021-10-15 (공휴일 포함)
- 개발 인원
  ✔️ **Front-End** 3명 : 박미연, 박세연, 윤수연
  ✔️ **Back-End** 2명 : 김지훈, 박치훈

## 프로젝트 구현 영상

- 📎 [유튜브 영상 링크](https://youtu.be/dZ92JHGZodI)
- **Reference** : 이 프로젝트는 러쉬 사이트를 참조하여 학습 목적으로 만들었습니다. 실무수준의 프로젝트이지만 학습용으로 만들었기 때문에 이 코드를 활용하여 이득을 취하거나 무단 배포할 경우 법적으로 문제될 수 있습니다.

## 적용 기술
- ✔️ **Front-End** : React, SASS, JSX
- ✔️ **Back-End** : Django, Python, MySQL, jwt, bcypt, AWS RDS, AWS EC2
- ✔️ **Common** : Git, Github, Slack, Trello, Postman

## 구현 기능

#### 김지훈

- 회원가입 API
- 로그인 API
- 상품 리뷰 생성, 조회, 수정, 삭제, 좋아요 API
- 상품 리뷰 댓글 생성, 조회, 수정, 삭제 API

#### 박치훈

- 상품 목록 조회 API
- 상품 상세 조회 API
- 장바구니 상품 추가, 수정, 삭제 API

## EndPoint

- POST/users/signup (회원가입)
- POST/users/signin (로그인)
- GET/products (상품 목록/ 필터링, 솔팅)
- GET/products/{int:product_id} (상품 상세)
- GET/navigator/{int:category_id} (네비게이터)
- GET/category (카테고리 리스트)
- POST/carts (장바구니 생성)
- GET/carts (장바구니 조회)
- DEL/carts/{int:cart_id} (장바구니 삭제)
- PATCH/carts/{int:cart_id} (장바구니 수정)
- POST/products/reviews/{int:product_id} (리뷰 생성)
- GET/products/reviews/{int:product_id} (리뷰 목록 조회)
- DEL/reviews/{int:review_id} (리뷰 삭제)
- PATCH/reviews/{int:review_id} (리뷰 수정)
- GET/reviews/{int:review_id} (리뷰 개별 조회)
- GET/reviews/comments/{int:review_id} (리뷰 댓글 조회)
- POST/reviews/comments/{int:review_id} (리뷰 댓글 생성)
- PATCH/reviews/comment/{int:comment_id} (리뷰 댓글 수정)
- DEL/reviews/comment/{int:comment_id} (리뷰 댓글 삭제)
- POST/reviews/like/{int:review_id} (리뷰 좋아요)
