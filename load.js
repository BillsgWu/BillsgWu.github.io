var cont = document.getElementsByClassName("container")[0]
var title = document.getElementsByTagName("title")[0]
var ver = document.getElementById("footerversion")
var hea = document.getElementById("headerusera")
var recart = document.getElementById("recommendarticles")
var hotart = document.getElementById("hotarticles")
var newart = document.getElementById("newarticles")
var authlg = document.getElementById("authlg")
fetch("https://553o7g9239.oicp.vip",{method: "get",mode: "cors"}).then(
    (response)=>{
        if(!response.ok){
            cont.innerHTML = "Network Error:" + response.status;
        }
        else
        {
            return response.json();
        }
    }
).then((json)=>{
    for(var i=0;i<json["recommendarticles"].length;++i){
        recart.innerHTML += '\
        <div class="col-sm-3">\
            <div class="card mb-3">\
                <img class="card-img-top" src="' + json["recommendarticles"][i]["jumimg"] + '" style="height: 120px;">\
                <div class="card-body">\
                    <a class="card-title h5" href="/?id=' + json["recommendarticles"][i]["id"] + '">' + json["recommendarticles"][i]["title"] + '</a><br>\
                    <span class="text-muted float-right">作者：' + json["recommendarticles"][i]["author"] + '</span>\
                </div>\
            </div>\
        </div>'
    }
    for(var i=0;i<json["hotarticles"].length;++i){
        hotart.innerHTML += '\
        <div class="col-sm-3">\
            <div class="card mb-3">\
                <img class="card-img-top" src="' + json["hotarticles"][i]["jumimg"] + '" style="height: 120px;">\
                <div class="card-body">\
                    <a class="card-title h5" href="/?id=' + json["hotarticles"][i]["id"] + '">' + json["hotarticles"][i]["title"] + '</a><br>\
                    <span class="text-muted float-right">作者：' + json["hotarticles"][i]["author"] + '</span>\
                </div>\
            </div>\
        </div>'
    }
    for(var i=0;i<json["newarticles"].length;++i){
        newart.innerHTML += '\
        <div class="col-sm-3">\
            <div class="card mb-3">\
                <img class="card-img-top" src="' + json["newarticles"][i]["jumimg"] + '" style="height: 120px;">\
                <div class="card-body">\
                    <a class="card-title h5" href="/?id=' + json["newarticles"][i]["id"] + '">' + json["newarticles"][i]["title"] + '</a><br>\
                    <span class="text-muted float-right">作者：' + json["newarticles"][i]["author"] + '</span>\
                </div>\
            </div>\
        </div>'
    }
    for(var i=0;i<json["authors"].length;++i){
        authlg.innerHTML += '<li class="list-group-item"><a href="/author/?id=' + json["authors"][i]["realname"] + '">' + json["authors"][i]["realname"] + '</a><span class="float-right">' + json["authors"][i]["count"] + '篇</span></li>'
    }
    ver.innerHTML = json["version"]
    if(json["title"]){
        title.textContent = json["title"] + " - 青中人文站"
    }
    if(json["user"]){
        hea.href = "/author/?id=" + json["uid"]
        hea.textContent = json["user"]
    }
}).catch(
    (error)=>{
        cont.innerHTML = error;
    }
);
//cont.innerHTML="<h1>Hello,world!</h1>"