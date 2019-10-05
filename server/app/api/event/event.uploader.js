const multer = require("multer");

exports.uploader = multer({
    storage: multer.diskStorage({
        destination: function (req, file, cb){
            cb(null, '../fresh/');
        },
        filename: function (req, file, cb){
            cb(null, file.originalname);
        }
    })
});


