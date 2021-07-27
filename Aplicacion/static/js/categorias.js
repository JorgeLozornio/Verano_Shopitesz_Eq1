function getCategorias(){
    console.log('Hola1.5');
    var ajax=new XMLHttpRequest();
    
    var url='/Categorias/ajax';
    ajax.open('get',url,true);
   
    ajax.onreadystatechange=function(){
        if(this.readyState==4 && this.status==200){
            console.log('Hola2')
           llenarDrop(this.responseText);

        }
    };
    ajax.send();
}
let cate

function llenarDrop(datos){
    console.log('Hola3')
    var drop=document.getElementById("categorias");
    var categorias=JSON.parse(datos);
    for(i=0;i<categorias.length;i++){
        var cat=categorias[i];
        console.log('Päso por aqui')
        var li=document.createElement("li");
        li.innerHTML= `<a class="dropdown-item">${cat.nombre}</a>`
        drop.appendChild(li);
        
    }
}

function llenarTabla(datos){
    var tabla=document.getElementById("datos");
    var productos=JSON.parse(datos);
    eliminarTabla();
    for(i=0;i<productos.length;i++){
        var li=document.createElement("li");
        var prod=productos[i];
        for (propiedad in prod){
            //alert(propiedad);
            //alert(prod[propiedad]);
            var td=document.createElement("td");
            var texto=document.createTextNode(prod[propiedad]);
            td.appendChild(texto);
            tr.appendChild(td);
        }
        var link=crearLink(prod.idProducto);
        td=document.createElement("td");
        td.appendChild(link);
        tr.appendChild(td);
        tabla.appendChild(tr);
        
        
    }
}