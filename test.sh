srv=http://127.0.0.1:9000
phone=1231
curl -d '{"phone":'$phone'}' $srv/api/account/reg_verify
echo ""

curl -d '{"phone":'$phone',"verify_code":"94d03b599a7b59c0534835de1cc2be27","passwd":"ddd"}' $srv/api/account/reg
echo ""

curl -d '{"phone":'$phone'}' $srv/api/account/passwd_verify
echo ""

curl -d '{"phone":'$phone',"verify_code":"94d03b599a7b59c0534835de1cc2be27","passwd":"eee"}' $srv/api/account/passwd
echo ""

curl -d '{"mid":1,"ts":12221,"passwd":"d2f2297d6e829cd3493aa7de4416a18f","sign":"ds"}' $srv/api/account/login
echo ""

curl -d '{"name":"糖城1","ver":"1.0.1","desc":"糖城app，下载方式挖矿","icon":"http://bpic.588ku.com/element_origin_min_pic/18/01/11/c2b53e883f3a5d62badca6b10cb3838b.jpg", "url":"http://p.gdown.baidu.com/b94fee84e5efd1089a5afee51453ee7bb903f8de7abb942ad910843f56b9135d3763fb6133c3878150b66e586d59ef1e141cf0cf4368df61fe69b7fbdd1916517e2f9311be979e641bc25cb3999eb0d56357d68a17412979630725651eee73fa13188f2535927d32ed025eaeddcafd0dd610de6d09d66244f861e2448b58f939","size":19129231,"rate":6.0,"down_time":1922,"down_user":812,"rec_rank":70,"hot_rank":50,"block_rank":90,"new_rank":10}' http://127.0.0.1:9000/api/appstore/add_app
echo ""
curl -d '{"name":"糖城2","ver":"1.0.1","desc":"糖城app，下载方式挖矿","icon":"http://bpic.588ku.com/element_origin_min_pic/18/01/11/c2b53e883f3a5d62badca6b10cb3838b.jpg", "url":"http://p.gdown.baidu.com/b94fee84e5efd1089a5afee51453ee7bb903f8de7abb942ad910843f56b9135d3763fb6133c3878150b66e586d59ef1e141cf0cf4368df61fe69b7fbdd1916517e2f9311be979e641bc25cb3999eb0d56357d68a17412979630725651eee73fa13188f2535927d32ed025eaeddcafd0dd610de6d09d66244f861e2448b58f939","size":19129231,"rate":6.0,"down_time":1922,"down_user":812,"rec_rank":70,"hot_rank":50,"block_rank":90,"new_rank":10}' http://127.0.0.1:9000/api/appstore/add_app
echo ""
curl -d '{"name":"糖城3","ver":"1.0.1","desc":"糖城app，下载方式挖矿","icon":"http://bpic.588ku.com/element_origin_min_pic/18/01/11/c2b53e883f3a5d62badca6b10cb3838b.jpg", "url":"http://p.gdown.baidu.com/b94fee84e5efd1089a5afee51453ee7bb903f8de7abb942ad910843f56b9135d3763fb6133c3878150b66e586d59ef1e141cf0cf4368df61fe69b7fbdd1916517e2f9311be979e641bc25cb3999eb0d56357d68a17412979630725651eee73fa13188f2535927d32ed025eaeddcafd0dd610de6d09d66244f861e2448b58f939","size":19129231,"rate":6.0,"down_time":1922,"down_user":812,"rec_rank":70,"hot_rank":50,"block_rank":90,"new_rank":10}' http://127.0.0.1:9000/api/appstore/add_app
echo ""
curl -d '{"name":"糖城4","ver":"1.0.1","desc":"糖城app，下载方式挖矿","icon":"http://bpic.588ku.com/element_origin_min_pic/18/01/11/c2b53e883f3a5d62badca6b10cb3838b.jpg", "url":"http://p.gdown.baidu.com/b94fee84e5efd1089a5afee51453ee7bb903f8de7abb942ad910843f56b9135d3763fb6133c3878150b66e586d59ef1e141cf0cf4368df61fe69b7fbdd1916517e2f9311be979e641bc25cb3999eb0d56357d68a17412979630725651eee73fa13188f2535927d32ed025eaeddcafd0dd610de6d09d66244f861e2448b58f939","size":19129231,"rate":6.0,"down_time":1922,"down_user":812,"rec_rank":70,"hot_rank":50,"block_rank":90,"new_rank":10}' http://127.0.0.1:9000/api/appstore/add_app
echo ""
curl -d '{"name":"糖城5","ver":"1.0.1","desc":"糖城app，下载方式挖矿","icon":"http://bpic.588ku.com/element_origin_min_pic/18/01/11/c2b53e883f3a5d62badca6b10cb3838b.jpg", "url":"http://p.gdown.baidu.com/b94fee84e5efd1089a5afee51453ee7bb903f8de7abb942ad910843f56b9135d3763fb6133c3878150b66e586d59ef1e141cf0cf4368df61fe69b7fbdd1916517e2f9311be979e641bc25cb3999eb0d56357d68a17412979630725651eee73fa13188f2535927d32ed025eaeddcafd0dd610de6d09d66244f861e2448b58f939","size":19129231,"rate":6.0,"down_time":1922,"down_user":812,"rec_rank":70,"hot_rank":50,"block_rank":90,"new_rank":10}' http://127.0.0.1:9000/api/appstore/add_app
echo ""
curl -d '{"name":"糖城6","ver":"1.0.1","desc":"糖城app，下载方式挖矿","icon":"http://bpic.588ku.com/element_origin_min_pic/18/01/11/c2b53e883f3a5d62badca6b10cb3838b.jpg", "url":"http://p.gdown.baidu.com/b94fee84e5efd1089a5afee51453ee7bb903f8de7abb942ad910843f56b9135d3763fb6133c3878150b66e586d59ef1e141cf0cf4368df61fe69b7fbdd1916517e2f9311be979e641bc25cb3999eb0d56357d68a17412979630725651eee73fa13188f2535927d32ed025eaeddcafd0dd610de6d09d66244f861e2448b58f939","size":19129231,"rate":6.0,"down_time":1922,"down_user":812,"rec_rank":70,"hot_rank":50,"block_rank":90,"new_rank":10}' http://127.0.0.1:9000/api/appstore/add_app
echo ""
curl -d '{"name":"糖城7","ver":"1.0.1","desc":"糖城app，下载方式挖矿","icon":"http://bpic.588ku.com/element_origin_min_pic/18/01/11/c2b53e883f3a5d62badca6b10cb3838b.jpg", "url":"http://p.gdown.baidu.com/b94fee84e5efd1089a5afee51453ee7bb903f8de7abb942ad910843f56b9135d3763fb6133c3878150b66e586d59ef1e141cf0cf4368df61fe69b7fbdd1916517e2f9311be979e641bc25cb3999eb0d56357d68a17412979630725651eee73fa13188f2535927d32ed025eaeddcafd0dd610de6d09d66244f861e2448b58f939","size":19129231,"rate":6.0,"down_time":1922,"down_user":812,"rec_rank":70,"hot_rank":50,"block_rank":90,"new_rank":10}' http://127.0.0.1:9000/api/appstore/add_app
echo ""
curl -d '{"name":"糖城8","ver":"1.0.1","desc":"糖城app，下载方式挖矿","icon":"http://bpic.588ku.com/element_origin_min_pic/18/01/11/c2b53e883f3a5d62badca6b10cb3838b.jpg", "url":"http://p.gdown.baidu.com/b94fee84e5efd1089a5afee51453ee7bb903f8de7abb942ad910843f56b9135d3763fb6133c3878150b66e586d59ef1e141cf0cf4368df61fe69b7fbdd1916517e2f9311be979e641bc25cb3999eb0d56357d68a17412979630725651eee73fa13188f2535927d32ed025eaeddcafd0dd610de6d09d66244f861e2448b58f939","size":19129231,"rate":6.0,"down_time":1922,"down_user":812,"rec_rank":70,"hot_rank":50,"block_rank":90,"new_rank":10}' http://127.0.0.1:9000/api/appstore/add_app
echo ""
curl -d '{"name":"糖城9","ver":"1.0.1","desc":"糖城app，下载方式挖矿","icon":"http://bpic.588ku.com/element_origin_min_pic/18/01/11/c2b53e883f3a5d62badca6b10cb3838b.jpg", "url":"http://p.gdown.baidu.com/b94fee84e5efd1089a5afee51453ee7bb903f8de7abb942ad910843f56b9135d3763fb6133c3878150b66e586d59ef1e141cf0cf4368df61fe69b7fbdd1916517e2f9311be979e641bc25cb3999eb0d56357d68a17412979630725651eee73fa13188f2535927d32ed025eaeddcafd0dd610de6d09d66244f861e2448b58f939","size":19129231,"rate":6.0,"down_time":1922,"down_user":812,"rec_rank":70,"hot_rank":50,"block_rank":90,"new_rank":10}' http://127.0.0.1:9000/api/appstore/add_app
echo ""
curl -d '{"name":"糖城10","ver":"1.0.1","desc":"糖城app，下载方式挖矿","icon":"http://bpic.588ku.com/element_origin_min_pic/18/01/11/c2b53e883f3a5d62badca6b10cb3838b.jpg", "url":"http://p.gdown.baidu.com/b94fee84e5efd1089a5afee51453ee7bb903f8de7abb942ad910843f56b9135d3763fb6133c3878150b66e586d59ef1e141cf0cf4368df61fe69b7fbdd1916517e2f9311be979e641bc25cb3999eb0d56357d68a17412979630725651eee73fa13188f2535927d32ed025eaeddcafd0dd610de6d09d66244f861e2448b58f939","size":19129231,"rate":6.0,"down_time":1922,"down_user":812,"rec_rank":70,"hot_rank":50,"block_rank":90,"new_rank":10}' http://127.0.0.1:9000/api/appstore/add_app
echo ""
curl -d '{"name":"糖城11","ver":"1.0.1","desc":"糖城app，下载方式挖矿","icon":"http://bpic.588ku.com/element_origin_min_pic/18/01/11/c2b53e883f3a5d62badca6b10cb3838b.jpg", "url":"http://p.gdown.baidu.com/b94fee84e5efd1089a5afee51453ee7bb903f8de7abb942ad910843f56b9135d3763fb6133c3878150b66e586d59ef1e141cf0cf4368df61fe69b7fbdd1916517e2f9311be979e641bc25cb3999eb0d56357d68a17412979630725651eee73fa13188f2535927d32ed025eaeddcafd0dd610de6d09d66244f861e2448b58f939","size":19129231,"rate":6.0,"down_time":1922,"down_user":812,"rec_rank":70,"hot_rank":50,"block_rank":90,"new_rank":10}' http://127.0.0.1:9000/api/appstore/add_app
echo ""