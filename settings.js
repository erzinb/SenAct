// JScript source code

// stores the reference to the XMLHttpRequest object
var N = 6;	// number of activators
var xmlHttp = createXmlHttpRequestObject();
var table;
var para;
var t;
var curstates = Array(N);

for (var i = 0; i < curstates.length; i++)
    curstates[i] = 2;

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
        // execute the quickstart.php page from the server
        xmlHttp.open("GET", "activators.php?id=settings", true);
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
            // extract the XML retrieved from the server
            //            xmlResponse = xmlHttp.responseXML;
            // obtain the document element (the root element) of the XML structure
            //            xmlDocumentElement = xmlResponse.documentElement;
            // get the text message, which is in the first child of
            // the the document element
            //            response = xmlDocumentElement.firstChild.data;
            // update the client display using the data received from the server

            x = xmlHttp.responseXML.documentElement.getElementsByTagName("settings");

            populateTable(x);

/*            x = xmlHttp.responseXML.documentElement.getElementsByTagName("sensors");

            populateTable1(x);

            x = xmlHttp.responseXML.documentElement.getElementsByTagName("programs");

            populateTable2(x);
*/
//            if (!para)
//                para = document.createElement("P");                       // Create a <p> element
//            if (!t) {
//                t = document.createTextNode("activators");      // Create a text node
//                para.appendChild(t);                        // Append the text to <p>
//            }
//            document.getElementById("myDivElement").appendChild(para);           // Append <p> to <div> with id="myDivElement"
//            if (t)
//                t.data = "Refresh transaction done: " + xmlHttp.readyState;

            // restart sequence
            setTimeout('process()', 1000);
        }
        // a HTTP status different than 200 signals an error
        else {
//            alert("There was a problem accessing the server: " + xmlHttp.statusText);
        }
    }
//    else {
//        if(t)
//            t.data = "Refresh transaction in progress: " + xmlHttp.readyState;
//    }
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
        tmp = document.getElementById("senactprog_active");
        tmp.value = row.cells[0].innerHTML;
        tmp = document.getElementById("senactsen_active");
        tmp.value = row.cells[1].innerHTML;
        tmp = document.getElementById("sampletime");
        tmp.value = row.cells[2].innerHTML;
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
    x = x[0].getElementsByTagName("setting");
    if (x && (x.length > 0) && (!table)) {
        table = document.createElement("table");
        var caption = table.createCaption();
        table.className = "Table1";
        caption.className = "TableCaption1";
        table.id = "settings";
        caption.innerHTML = "<b>Sistemske nastavitve</b>";

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
    if (!document.getElementById("settings"))
        if (table) {
            divelem.appendChild(table);
            divelem.appendChild(document.createElement("BR"));
        }
    }

    function Expand(obj) {
        if (!obj.savesize) obj.savesize = obj.size;
        obj.size = Math.max(obj.savesize, obj.value.length);
    }
