const qrcode = require('qrcode-terminal');
const fs = require('fs');
const { Client } = require('whatsapp-web.js');
const fetch = require('node-fetch');
const { MessageMedia } = require('whatsapp-web.js');
const { Contact } = require('whatsapp-web.js');
var express = require('express');
var app = express();
var mime = require('mime-types')
var redis = require('redis'),
rd = redis.createClient();

// Redis Connection
rd.on('error', function(err){
    console.log('Error ' + err);
});
rd.on('ready', function(){
    console.log('// Redis Ready');
});

// Path where the session data will be stored
const SESSION_FILE_PATH = './config/session.json';
// Load the session data if it has been previously saved
let sessionData;
if(fs.existsSync(SESSION_FILE_PATH)) {
    sessionData = require(SESSION_FILE_PATH);
}

// Use the saved values
const client = new Client({ puppeteer: {headless: true, executablePath: 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',args: ['--no-sandbox', '--disable-setuid-sandbox']}, session: sessionData });

// Generating the QR Code
client.on('qr', qr => {
    qrcode.generate(qr, {small: true});
});

// When connected to Whatsapp!
client.on('ready', () => {
    console.log('// Whatsapp Bot online');
    console.log('// API Server online At http://localhost:5002');
    // client.sendMessage("6281241668963@c.us","Whatsapp BOT Online + Server API is Running");
});

// Save session values to the file upon successful auth
client.on('authenticated', (session) => {
    sessionData = session;
    fs.writeFile(SESSION_FILE_PATH, JSON.stringify(session), function (err) {
        if (err) {
            console.error(err);
        }
    });
});

// Web
app.get('/', function(req, res) {
    res.send("Whatsapp Chatbot API");
});
app.listen(5002);


app.get('/api/v1/send/:phone_number/message/:message', async function(req, res) {
    if(req.params['phone_number'].startsWith("62") == true){
        var phone_number = req.params['phone_number'] + "@c.us"
        const chat = await client.sendMessage(phone_number,req.params['message']);
        res.send('{"status":"200", "ID":"' + chat.id._serialized + '","phone_number":"' + phone_number + '"}');
    }else{
        res.send('{"status:404","message":"error"}');
    }
});
app.get('/api/v1/sendsurat/:phone_number/file/:file', async function(req, res) {
    if(req.params['phone_number'].startsWith("62") == true){
        var phone_number = req.params['phone_number'] + "@c.us"
        const attachment = MessageMedia.fromFilePath("./assets/template/" + req.params['file'])
        const chat = await client.sendMessage(phone_number, attachment);
        res.send('{"status":"200", "ID":"' + chat.id._serialized + '","phone_number":"' + phone_number + '"}');
    }else{
        res.send('{"status:404","message":"error"}');
    }
});

var terkirim = [];
client.on('message_ack', (message, ack)=>{
    if(ack == 1){
        console.log(message.id._serialized +": Server Send");
        rd.set("msg:"+ message.to.slice(0, -5), "Pending");
    }else if(ack == 2){
        console.log(message.id._serialized +": Message Received");
        rd.set("msg:"+message.to.slice(0, -5), "Terkirim");
    }else if(ack == 3){
        console.log(message.id._serialized +": Message Readed");
        rd.set("msg:"+message.to.slice(0, -5), "Sudah Dibaca");
    }
});

app.get('/api/v1/cekterkirim', async function(req, res) {
    res.send(terkirim["status"]);
});

client.on('message', async message => {
    if(message.isStatus == false){
        // Untuk yang berfile
        if (message.hasMedia == true) {
            const attachmentData = await message.downloadMedia();
            let file = new Buffer.from(attachmentData.data,'base64');
            let ext = mime.extension(attachmentData.mimetype);
            fs.writeFileSync('assets/userfile/' + message.from.slice(0, -5) + message.body, file);
            console.log(message.from + " send: " + attachmentData.mimetype);
            const contact = await message.getContact();
            console.log(message.from + " send: " + message.body + attachmentData.mimetype);
            bot_api = 'http://127.0.0.1:5000/api/v1/message?message_from=' + message.from.slice(0, -5) + '&' + 'message_name=' + contact.pushname + '&' + 'message_body=' + message.body + '&' + 'attachment=true';
            fetch(bot_api).then(response => response.json()).then(json => {
                if (json['type'] == "message"){
                    client.sendMessage(message.from, json['data']);
                    console.log("Pesan Terkirim: " + json['data']);
                }else{
                    const attachment = MessageMedia.fromFilePath(json['data'])
                    client.sendMessage(message.from, attachment, {caption: json['caption']});
                    console.log("Attachment Terkirim")
                }
            });
        // Untuk yang tidak berfile
        }else{
            const contact = await message.getContact();
            console.log(message.from + " send: " + message.body + "| Message ID: " + message.id);
            bot_api = 'http://127.0.0.1:5000/api/v1/message?message_from=' + message.from.slice(0, -5) + '&' + 'message_name=' + contact.pushname + '&' + 'message_body=' + message.body + '&' + 'attachment=false';
            fetch(bot_api).then(response => response.json())
            .then(json => {
                if (json['type'] == "message"){
                    client.sendMessage(message.from, json['data']);
                    console.log("Pesan Terkirim: " + json['data']);
                }else{
                    if (json['data'].slice(-3) == "mp3"){
                        const mp3 = MessageMedia.fromFilePath(json['data'])
                        client.sendMessage(message.from, mp3, {sendAudioAsVoice: true});
                        console.log("Voice Note Terkirim")
                    }else{
                        const gambar = MessageMedia.fromFilePath(json['data'])
                        client.sendMessage(message.from, gambar, {caption: json['caption']});
                        console.log("File Terkirim")
                    }
                }
            });
        }
    }
});

client.initialize();
