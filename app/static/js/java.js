const hrefs = document.querySelectorAll("a");
for (const el of hrefs) {
  el.addEventListener("click", function() {
    el.preventDefault();
    f_submit_loading();
    let url = this.href;
    window.location.href = url;
  });
}

function f_submit_loading(){
  try{
      var e = document.getElementById("submit_loader");
      e.classList.toggle("d-none");
  }catch{
      console.error('No existe el elemento loading submit for page');
  }
}

String.prototype.format = function(){
    var args = arguments
    return this.replace(/\{\{|\}\}|\{(\d+)\}/g, function (m, i) {
      if (m == "{{") return "{"
      if (m == "}}") return "}"
      return args[i]
    })
  }

function f_loading(){
    try{
        var e = document.getElementById("loading");
        e.classList.toggle("waviy");
    }catch{
        console.error('No existe el elemento loading');
    }
}

function f_show__detail(e){
  let name_tag = e.getAttribute("for");
  let div = document.getElementById(name_tag);
  div.classList.toggle("d-block");
}

function f_delete__parent(e, msg){
  console.error(msg);
  e.parentNode.parentNode.removeChild(e.parentNode)
}

function f_activate__check(e){
  let name_tag = e.getAttribute("for");
  let input = document.getElementById(name_tag);
  if (e.checked){
    input.disabled = false;
  }else{
    input.disabled = true;
  }
}

function f_check(checkbox) {
  checkbox.value = checkbox.checked ? 1 : 0;
}

function f_verArchivo(p_cCodigo){
  ruta = window.origin+"/verArchivo";
  console.info(ruta)
  fetch(ruta, {
    method: "GET",
    credentials: "include",
    cache: "no-cache",
    body:JSON.stringify(p_cCodigo)
  })
    .then(async response => {
      const isJson = response.headers.get('content-type')?.includes('application/json');
      const loBlob = isJson ? await response.json() : null;

      if (!response.ok || !data.OK) {
          const error = data.DATA || response.status;
          return Promise.reject(error);
      }
      const objUrl = window.URL.createObjectURL(data.DATA);
      //window.open(objUrl);
      var link = document.createElement('a');
      link.href = objUrl;
      link.download = lcPDfName;
      link.click();
    })
    .catch(error => {
        console.error('ERROR!', error);
    });

}