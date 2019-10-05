const models = require('../../models/models');
// const fcm = require('./event.fcm');
var FCM = require('fcm-node');
var fs = require('fs');

var serverKey = 'AAAAUPlFQ-I:APA91bGISszRb6F6tFSKCM6qkP_hDlDVhUBdCIMiKED5wtsNI06pt28RxYnn78igZwld5Zf6fz5e3eDMPCyn8uvyNIlyOJKc2KFd3APE84p9c52cxLK9x-p84iW7bkY1m2ON8r9ijWKC';
var fcm = new FCM(serverKey);
var client_token;

var rimraf = require("rimraf");

// CAM에서 찍은 사용자 image를 보낼때 호출된다.
exports.upload = (req, res) => {
    console.log("/event/upload");
    // console.log(req);
    let files = req.files;

    if(files == null){
        console.log("file not transfer!");
        res.status(404).json({error: 'File not transfer!'});
    }

    // 1. image file의 이름을 오름차순으로 정렬해서 mg_addrs에 저장.
    let img_addrs = [];
    files.forEach(element => {
        img_addrs.push(element['originalname']);
    });
    img_addrs.sort();

    // 2. event 이름(eventTime), image 저장 경로를 DB에 event Table을 만들어 저장한다.
    var str_types = '';
    var str_addrs = '';

    for(i = 0; i<img_addrs.length; i++){
        if( i == img_addrs.length - 1){
            str_types += 'fresh';
            str_addrs += "../learn/fr/"+img_addrs[i];//img_addrs[i];//"../fresh/"+img_addrs[i];
        }else{
            str_types += 'fresh,';
            str_addrs += "../learn/fr/"+img_addrs[i]+',';//img_addrs[i]+',';//"../fresh/"+img_addrs[i]+',';
        }
    }

    let eventTime =img_addrs[0].replace(".jpg","");
    models.Event.create({
        eventTime: eventTime,
        types: str_types,
        img_addrs: str_addrs
    })
    // 성공했다면 201 응답
    .then(function(event){
        return res.status(201).json({res: 'success: create tbale '+eventTime})
    })
    // 실패라면 404 응답
    .catch(function(err){
        console.log(err);
        return res.status(404).json({err:'error: Do not create table '+img_addrs[0]});
    });
}

// learning에서 unknown이 검출되면 호출된다.
exports.unknown = (req, res) => {
    console.log("event/unknown")

    // {
    //  eventTime: string,
    //  types: string,
    //  img_addrs: [string, string]
    // }
    // console.log(req.body);
    // console.log(typeof req.body.eventTime);
    // console.log(typeof req.body.types);
    // console.log(typeof req.body.img_addrs);
    var eventTime = req.body.eventTime; // event timell
    var types = [];
    var img_addrs=[];
    types.push(req.body.types);
    img_addrs.push(req.body.img_addrs);
    // if(typeof req.body.types == "string"){
    //     types.push(req.body.types)
    // }else{

    //     types = req.body.types; // unknown, friends, family
    // }
    // if(typeof req.body.img_addrs == "string"){
    //     img_addrs.push(req.body.img_addrs)
    // }else{
    //     img_addrs = req.body.img_addrs; // image address   
    // }
    
    console.log(eventTime);
    console.log(types);
    console.log(img_addrs);
    
    var str_types = '';
    var str_addrs = '';

    // 1. type과 img_addr를 table 형식에 맡게 바꿔준다.
    for(i = 0; i<img_addrs.length; i++){
        if( i == img_addrs.length - 1){
            str_types += types[i];
            str_addrs += "../learn/un/"+eventTime+"/"+img_addrs[i];//img_addrs[i];//"../unknown/"+eventTime+img_addrs[i];
        }else{
            str_types += types[i]+',';
            str_addrs += "../learn/un/"+eventTime+"/"+img_addrs[i]+',';//img_addrs[i]+',';//"../unknown/"+eventTime+img_addrs[i]+',';
        }
    }
    console.log(str_types);
    console.log(str_addrs);
    if(eventTime == null){
        return res.status(404).json({err: 'eventTime is null!'});
    }

    // 2. eventTime을 이용해 table을 찾고 types와 img_addrs를 update 해준다.
    models.Event.update(
        {
            types: str_types,
            img_addrs: str_addrs
        },
        {where: {eventTime: eventTime}, returning: true}
    ).then(function(event){
        // res.json(result[1][0]);

        // 3. update 성공이면 notification 보낼 자료구조(push_data)를 만든다.
        // console.log(eventTime)
        var push_data = {
            to: client_token,
            // app이 실행중이지 않을 때 상태바 알림으로 등록할 내용
            notification: {
                title: "Warnning",
                body: "An unknown person broke into our house!",
                sound: "default",
                client_token: "FCM_PLUGIN_ACTIVITY",
                icon: "fcm_push_icon"
            },
            // message 중요도
            priority: "high",
            // app package name
            restricted_package_name: "com.dev.kih.nusm",
            // app에게 전달할 데이터 notification identity를 보내줘야 함
            data: {
                eventTime: eventTime
            }
        };
        // 4. fcm을 이용해 notification을 보낸다.
        fcm.send(push_data, function(err, response){
            if(err){
                console.error("Failed notification!");
                console.log(err);
                // return res.status(404).json({err: "Failed notification!"});
            }else{
                console.log('Success notification');
                // return res.status(201).json({res: "Success notification"});
            }
        });

    })
    // 만약 db에 update하는 것이 실패한다면
    .catch(function(err){
        return res.status(404).json({err:'error: Do not update table '+eventTime});
    });

    res.status(201).json({res: 'Successfully sent notification and update table '+eventTime});
}

// 모바일에서 fcm을 보낼 때 호출
exports.token = (req, res) => {
    console.log('/event/token');

    client_token = req.body.token;
    if(client_token == null){
        return res.status(404).json({err: 'Token post error!'});
    }

    // token 받았으면 db에 저장
    // but 지금은 어플에서 계속 새로 생성하고 있으니 상관 없음
    res.status(201).json({res: 'Token post success!'});
}

// 모바일에서 unknown event에 대한 image요청할 때 호출
exports.images = (req, res) => {
    console.log("/event/images/: "+req.params.eventTime);

    // 1. 모바일에서 보낸 eventTime 받기
    let eventTime = req.params.eventTime;

    if(eventTime = null){
        return res.status(404).json({err: 'eventTime is null! check for URL(/event/images/:eventTime)'});
    }
    // 2. eventTime을 이용해 해당 table 검출
    models.Event.findAll({
        attributes: ['img_addrs'],
        where: {
            eventTime: req.params.eventTime//'2019-9-30-0-6-54-797042'
        }
    }).then(function(event){
        // console.log(event[0].toJSON().img_addrs)
        // 3. 검출된 table(event)에서 img_addrs를 img_addrs에 저장
        var img_addrs = event[0].toJSON().img_addrs; // event table의 image address
        console.log(img_addrs)
        // 4. img_addrs에 , 기준으로 img_addrs를 split해서 list형태로 저장
        var list_addrs = img_addrs.split(','); // comma 기준으로 자른다.

        // 5. image name과 실제 이미지가 있는 url을 보낸다. ../image/image.controller.js 참고
        console.log(list_addrs)
        // console.log("eventTime:"+req.params.eventTime);

        var response = {};
        var results = [];
        for(var i = 0; i<list_addrs.length; i++){
            var replace_str = '../learn/un/'+req.params.eventTime+'/';
            var name = list_addrs[i].replace(replace_str, "");
            var url = '/image/unknown/'+req.params.eventTime;
            
            var image = {};
            image['name'] = name;
            image['url'] = url;

            results.push(image);

        }
        response['images'] = results;
        return res.status(201).json(response);
    }).catch(function(err){
        console.log(err);
        return res.status(404).json({err: 'No such incoreect table: '+eventTime});
    })

}

// 모바일에서 선택한 사진 type update
exports.update = (req, res) => {
    console.log("event/update");

    // 1. 사용자(모바일)에게 받은 제대로된 type을 받는다.
    let eventTime = req.body.eventTime; // event time
    let types = req.body.types; // unknown, friends, family
    let imageName = req.body.imageName; // image address

    console.log(eventTime);
    console.log(types);
    console.log(imageName);

    // 2. 받은 데이터를 table형식으로 맞춰준다.
    // str_types = '';
    // str_names = '';

    // for(i = 0; i<img_addrs.length; i++){
    //     if( i == img_addrs.length - 1){
    //         str_types += types[i];
    //         str_addrs += "../unknown/"+eventTime+img_addrs[i];
    //     }else{
    //         str_types += types[i]+',';
    //         str_addrs += "../unknown/"+eventTime+img_addrs[i]+',';
    //     }
    // }

    if(eventTime == null){
        res.status(404).json({err: 'eventTime is null!'});
    }

    // 3. 분류된 사진을 폴더에 재배치 해준다.
    var path = '../learn/un/'+eventTime+"/";
    for(i=0; i<imageName.length; i++){
        if(types[i] == 'Family'){ // family
            let new_path = '../learn/fa/'+eventTime+imageName[i];
            fs.rename(path+imageName[i], new_path, function(err){
                if(err){
                    console.log("Family 이동 실패");
                    return res.status(404).json({err: 'Failed to move '+imageName[i]+'to fmaily directory'});
                }else{
                    // 5. 그리고 제대로 이동이 되었다면 eventTime: req.body.eventTime을 받는 table은 삭제해준다.
                    console.log("Family 이동 성공");
                    // res.json({res: 'Failed to move '+img_addrs[i]+'to fmaily directory'});
                }
            })
        }else if(types[i] == 'Friends'){ // friends
            let new_path = '../learn/fd/'+eventTime+imageName[i];
            fs.rename(path+imageName[i], new_path, function(err){
                if(err){
                    console.log("Friends 이동 실패");
                    return res.status(404).json({err: 'Failed to move '+imageName[i]+'to friends directory'});
                }else{
                    console.log("Friends 이동 성공");
                }
            })
        }
    }

    rimraf.sync("../learn/un/"+eventTime);
    // 4. row 삭제
    models.Event.destroy(
        {
            where: {
                eventTime: eventTime
            }
        }
    ).then(function(result) {
        console.log(eventTime+"삭제 성공");
        // res.json({});
    }).catch(function(err) {
        console.log(err);
        // return res.status(404).json({err: eventTime+": Failed delete row!"});
    });

    // 3. eventTime을 이용해 types, img_addrs를 update해준다.
    // models.Event.update(
    //     {
    //         types: str_types,
    //         img_addrs: str_addrs
    //     },
    //     {where: {eventTime: eventTime}, returning: true}
    // ).then(function(event){
    //     var img_addrs =event.img_addrs;
    //     var types = event.types;

    //     // 4. img_addrs의 idx와 types의 idx는 서로 1:1 대응된다.
    //     // 따라서 types[i]가 1이면 family, 2이면 friends으로 분류하고
    //     // 그에 맞는 directory에 파일을 이동시켜 준다.
    //     for(i=0; i<img_addrs.length; i++){
    //         if(types[i] == 'family'){ // family
    //             let new_path = '../family/';
    //             fs.rename(img_addrs[i], new_path, function(err){
    //                 if(err){
    //                     console.log("Family 이동 실패");
    //                     return res.status(404).json({err: 'Failed to move '+img_addrs[i]+'to fmaily directory'});
    //                 }else{
    //                     // 5. 그리고 제대로 이동이 되었다면 eventTime: req.body.eventTime을 받는 table은 삭제해준다.
    //                     console.log("Family 이동 성공");
    //                     // res.json({res: 'Failed to move '+img_addrs[i]+'to fmaily directory'});
    //                 }
    //             })
    //         }else if(types[i] == 'friends'){ // friends
    //             let new_path = '../friends/';
    //             fs.rename(img_addrs[i], new_path, function(err){
    //                 if(err){
    //                     console.log("Friends 이동 실패");
    //                     return res.status(404).json({err: 'Failed to move '+img_addrs[i]+'to friends directory'});
    //                 }else{
    //                     console.log("Friends 이동 성공");
    //                 }
    //             })
    //         }
    //     }
    // }).catch(function(err){
    //     return res.status(404).json({err:'No such incoreect table:  '+eventTime});
    // });

    res.status(201).json({res: eventTime});

}