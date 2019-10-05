const fs = require('fs');

exports.unknown = (req, res) => {
    console.log("/image/unknown/:"+req.params.filename);
    console.log("/image/unknown/:"+req.params.eventTime);
    
    let filename = req.params.filename;
    let eventTime = req.params.eventTime;
    var path = '../learn/un/'+eventTime+'/'+filename;

    var fileStream = fs.createReadStream(path);

    fileStream.on('open', function () {
        res.writeHead(200, {"Content-Type": "image/jpeg"});
        fileStream.pipe(res);
    });
    fileStream.on('error', function () {
        res.writeHead(404, {"Content-Type": "text/html"});
        res.end("Page not found");
    });

}