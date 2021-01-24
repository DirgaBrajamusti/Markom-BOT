var mysql = require('mysql');
var db = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "",
    database: "pmbbot"
});
db.connect(function(err) {
    if (err) throw err;
    console.log("MySQL Connected!");
});

function updateStatusPesan(nomor_telepon, status){
    db.query(`SELECT status FROM pmb WHERE nomor_telepon = '${nomor_telepon}'`, function (err, result) {
        if (err){
            throw err
        }else{
            if(result[0].status == "Sudah Dibaca"){
                db.query(`UPDATE pmb SET status = 'Direspon' WHERE nomor_telepon = '${nomor_telepon}'`, function (err, result) {
                    if (err) throw err;
                    console.log(`${nomor_telepon}: Sudah Direspon`);
                  });
            }else{
                db.query(`UPDATE pmb SET status = '${status}' WHERE nomor_telepon = '${nomor_telepon}'`, function (err, result) {
                    if (err) throw err;
                    console.log(`${nomor_telepon}: ${status}`);
                  });
            }
        }
    });
}
updateStatusPesan("6281241668963", "Sudah Dibaca")