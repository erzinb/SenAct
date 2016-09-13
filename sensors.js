// JScript source code

// stores the reference to the XMLHttpRequest object
var N = 6;	// number of activators
var xmlHttp = createXmlHttpRequestObject();
var table;

// retrieves the XMLHttpRequest object
function createXmlHttpRequestObject() {
    // will store the reference to the XMLHttpRequest object
    var xmlHttp;
    // if running Internet Explorer
    if (window.ActiveXObject) {
        try {
            xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        catch (e) {
            xmlHttp = false;
        }
    }
    // if running Mozilla or other browsers
    else {
        try {
            xmlHttp = new XMLHttpRequest();
        }
        catch (e) {
            xmlHttp = false;
        }
    }
    // return the created object or display an error message
    if (!xmlHttp)
        alert("Error creating the XMLHttpRequest object.");
    else
        return xmlHttp;
}

// make asynchronous HTTP request using the XMLHttpRequest object - get activators status
function process() {
    // proceed only if the xmlHttp object isn't busy
    if (xmlHttp.readyState == 4 || xmlHttp.readyState == 0) {
        // retrieve the name typed by the user on the form
//        name = encodeURIComponent(document.getElementById("myName").value);
        xmlHttp.open("GET", "activators.php?id=all", true);
        // define the method to handle server responses
        xmlHttp.onreadystatechange = handleServerResponse;
        // make the server request
        xmlHttp.send(null);
    }
    else
    // if the connection is busy, try again after one second
        setTimeout('process()', 1000);
}

// executed automatically when a message is received from the server
function handleServerResponse() {
    var x, xx, i;
    // move forward only if the transaction has completed
    if (xmlHttp.readyState == 4) {
        // status of 200 indicates the transaction completed successfully
        if (xmlHttp.status == 200) {
            x = xmlHttp.responseXML.documentElement.getElementsByTagName("sensors");
            populateTable(x);

            // restart sequence
            setTimeout('process()', 1000);
        }
        // a HTTP status different than 200 signals an error
        else {
//            alert("There was a problem accessing the server: " + xmlHttp.statusText);
        }
    }
}

function myClickHandler(event) {
    var target;
    event = event || window.event;
    if (event.target)
        target = event.target;
    else
        target = event.srcElement;
    if (table) {
        row = target.parentElement;
        tmp = document.getElementById("id");
        tmp.value = row.cells[0].innerHTML;
        Expand(tmp);
        tmp = document.getElementById("name");
        tmp.value = row.cells[1].innerHTML;
        Expand(tmp);
        tmp = document.getElementById("type");
        tmp.value = row.cells[2].innerHTML;
//        Expand(tmp);
        tmp = document.getElementById("tl");
        tmp.value = row.cells[3].innerHTML;
        Expand(tmp);
        tmp = document.getElementById("th");
        tmp.value = row.cells[4].innerHTML;
        Expand(tmp);
        tmp = document.getElementById("k");
        tmp.value = row.cells[6].innerHTML;
        Expand(tmp);
        tmp = document.getElementById("n");
        tmp.value = row.cells[7].innerHTML;
        Expand(tmp);
    }
}

function myMouseOver(event) {
    var target;
    event = event || window.event;
    if (event.target)
        target = event.target;
    else
        target = event.srcElement;

    target.parentElement.focus();
    target.parentElement.className = "TableContentMouseOver1";
}

function myMouseOut(event) {
    var target;
    event = event || window.event;
    if (event.target)
        target = event.target;
    else
        target = event.srcElement;
    target.parentElement.className = "TableContent1";
}

function populateTable(x) {
    x = x[0].getElementsByTagName("sensor");
    if (x && (x.length > 0) && (!table)) {
        table = document.createElement("table");
        var caption = table.createCaption();
        table.className = "Table1";
        caption.className = "TableCaption1";
        table.id = "sensors";
        caption.innerHTML = "<b>Senzorji</b>";

        var header = table.createTHead();
        var row = header.insertRow(0);
        for (i = x[0].children.length-1; i >= 0; i--) {
            var cell = row.insertCell(0);
            cell.className = "TableHead1";
            cell.innerHTML = x[0].children[i].nodeName;
        }
    }
    for (i = 0; i < x.length; i++) {
        var row;
        var cell;
        if (!(table.rows[i + 1]))
            row = table.insertRow(i + 1);
        else
            row = table.rows[i + 1];

        for (j = 0; j < x[i].children.length; j++) {
            if (!(row.cells[j])) {
                cell = row.insertCell(j);
                cell.className = "TableContent1";
                cell.onclick = myClickHandler;
                cell.onmouseover = myMouseOver;
                cell.onmouseout = myMouseOut;
            }
            else
                cell = row.cells[j];
            cell.innerHTML = x[i].children[j].innerHTML;
        }
    }

    var divelem = document.getElementById("myDivElement");
    if (!document.getElementById("sensors"))
        if (table) {
            divelem.appendChild(table);
            divelem.appendChild(document.createElement("BR"));
        }
    }

    function Expand(obj) {
        if (!obj.savesize) obj.savesize = obj.size;
        obj.size = Math.max(obj.savesize, obj.value.length);
    }
