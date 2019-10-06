const express = require('express');
const router = express.Router();
const bodyParser = require('body-parser');

router.use(bodyParser.json());
router.use(bodyParser.urlencoded({extended: true}));

const controller = require('./event.controller');
const uploader = require('./event.uploader');


//1. event에 대한 image 들을 받는다.
//2. storage에 data 저장 
//3. db에 path, type = fresh(0), eventname(time) 저장 
router.post('/upload', uploader.uploader.array('file', 5), controller.upload);

//만약 받은 내용이 unknown이라면(learning 에서 unknown이라면)
//1. {eventTime}, {path}, type = unknown 을 받는다.
//2. db에 저장
//3. mobile에 notification 보내기
// 각각의 data field는 이미 learning에서 판단되서 오는 값들임
router.post('/unknown', controller.unknown);

// 모바일에서
// fcm을 사용하기 위한 token 생성 시 server로 보내야 함
router.post('/token', controller.token);

// 모바일에서
// 문제가 되는 사진(unknown)을 받는다.
router.get('/images/:eventTime', controller.images);

// 모바일에서 
// 각 인물들에 대해서 변경된 type을 서버에게 알려준다.
router.post('/update', controller.update);

module.exports = router;