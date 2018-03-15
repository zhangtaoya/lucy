phone=1231
curl -d '{"phone":'$phone'}' http://127.0.0.1:9000/api/account/reg_verify
echo ""
curl -d '{"phone":'$phone',"verify_code":"94d03b599a7b59c0534835de1cc2be27","passwd":"ddd"}' http://127.0.0.1:9000/api/account/reg
echo ""
curl -d '{"phone":'$phone'}' http://127.0.0.1:9000/api/account/passwd_verify
echo ""
curl -d '{"phone":'$phone',"verify_code":"94d03b599a7b59c0534835de1cc2be27","passwd":"eee"}' http://127.0.0.1:9000/api/account/passwd
