//JScript source code

//stores the reference to the XMLHttpRequest object
var N = 6;	// number of activators
var xmlHttp = createXmlHttpRequestObject();
var xmlHttp1 = createXmlHttpRequestObject();
var table, table1, table2;
var para,para1;
var t,t1;
var responseDone = true;
var responseDone1 = true;
var curstates = Array(N);

for(var i=0;i<curstates.length;i++)
	curstates[i] = 2;

//retrieves the XMLHttpRequest object
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

//make asynchronous HTTP request using the XMLHttpRequest object - get activators status
function process() {
	// proceed only if the xmlHttp object isn't busy
	if (responseDone1 && (xmlHttp.readyState == 4 || xmlHttp.readyState == 0)) {
		// retrieve the name typed by the user on the form
//		name = encodeURIComponent(document.getElementById("myName").value);
		// execute the quickstart.php page from the server
		responseDone = false;
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

//make asynchronous HTTP request using the XMLHttpRequest object - get activators status
function activate(command) {
	// proceed only if the xmlHttp object isn't busy
	if (responseDone && (xmlHttp1.readyState == 4 || xmlHttp1.readyState == 0)) {
		responseDone1 = false;
		xmlHttp1.open("GET", "activators.php?" + command, true);
		// define the method to handle server responses
		xmlHttp1.onreadystatechange = handleServerResponse1;
		// make the server request
		xmlHttp1.send(null);
	}
	else
		// if the connection is busy, try again after 0.7 second
		setTimeout('activate("'+command+'")', 700);
}

//executed automatically when a message is received from the server
function handleServerResponse1() {
	var x, xx, i;
	// move forward only if the transaction has completed
	if (xmlHttp1.readyState == 4) {
		// status of 200 indicates the transaction completed successfully
		if (xmlHttp1.status == 200) {
			// extract the XML retrieved from the server
			xmlResponse = xmlHttp1.responseXML;
			// obtain the document element (the root element) of the XML structure
			xmlDocumentElement = xmlResponse.documentElement;
			// get the text message, which is in the first child of
			// the the document element
			responseMessage = xmlDocumentElement.outerHTML;
			// update the client display using the data received from the server

//			if(!para1)
//			para1 = document.createElement("P");                       // Create a <p> element
//			if (!t1) {
//			t1 = document.createTextNode(responseMessage);      // Create a text node
//			para1.appendChild(t1);                        // Append the text to <p>
//			}
//			else
//			t1.data = responseMessage;
//			document.getElementById("myDivElement").appendChild(para1);           // Append <p> to <div> with id="myDivElement"

			responseDone1 = true;
//			if (t1)
//			t1.data = "Transaction done: " + xmlHttp1.readyState;
		}
		// a HTTP status different than 200 signals an error
		else {
//			alert("There was a problem accessing the server: " + xmlHttp1.statusText);
		}
	}
//	else {
//	if (t1)
//	t1.data = "Transaction in progress: " + xmlHttp1.readyState;
//	}
}

//executed automatically when a message is received from the server
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

			x = xmlHttp.responseXML.documentElement.getElementsByTagName("activators");

			populateTable(x);

			x = xmlHttp.responseXML.documentElement.getElementsByTagName("sensors");

			populateTable1(x);

			x = xmlHttp.responseXML.documentElement.getElementsByTagName("programs");

			populateTable2(x);

			responseDone = true;
//			if (!para)
//			para = document.createElement("P");                       // Create a <p> element
//			if (!t) {
//			t = document.createTextNode("activators");      // Create a text node
//			para.appendChild(t);                        // Append the text to <p>
//			}
//			document.getElementById("myDivElement").appendChild(para);           // Append <p> to <div> with id="myDivElement"
//			if (t)
//			t.data = "Refresh transaction done: " + xmlHttp.readyState;

			// restart sequence
			setTimeout('process()', 1000);
		}
		// a HTTP status different than 200 signals an error
		else {
//			alert("There was a problem accessing the server: " + xmlHttp.statusText);
		}
	}
//	else {
//	if(t)
//	t.data = "Refresh transaction in progress: " + xmlHttp.readyState;
//	}
}

function myClickHandler(event) {
	var target;
	event = event || window.event;
	if (event.target)
		target = event.target;
	else
		target = event.srcElement;

	var curText = target.innerHTML;
	target.innerHTML = "Wait...";
	var state = 1;
	if (curText == "ON") {
		state = 0;
	}
	activate("id=" + target.id + "&action=write&value=" + state + "&block=2");
	//        alert("Reley" + target.id + " switched to " + target.innerHTML);  //"Cell: " + "(" + i + ", " + j + ")");
	//        target.innerHTML = curText;
}

function myMouseOver(event) {
	var target;
	event = event || window.event;
	if (event.target)
		target = event.target;
	else
		target = event.srcElement;

	target.focus();
	if (target.innerHTML == "ON") {
		target.className = "TableContentStateMouseOverON";
	}
	else
		target.className = "TableContentStateMouseOverOFF";
}

function myMouseOut(event) {
	var target;
	event = event || window.event;
	if (event.target)
		target = event.target;
	else
		target = event.srcElement;
	if (target.innerHTML == "ON")
		target.className = "TableContentStateON";
	else
		target.className = "TableContentStateOFF";
}

function myClickHandler1(event) {
	window.location = "activators.html"
}

function myClickHandler2(event) {
	window.location = "sensors.html"
}

function myClickHandler3(event) {
	window.location = "programs.html"
}

function populateTable(x) {
	x = x[0].getElementsByTagName("activator");
	if (x && (x.length > 0) && (!table)) {
		table = document.createElement("table");
		var caption = table.createCaption();
		table.className = "Table1";
		caption.className = "TableCaption1";
		table.id = "activators";
		caption.innerHTML = "<b>Aktivatorji</b>";
		caption.onclick = myClickHandler1;

//		var c = document.createElement("INPUT");
//		c.setAttribute("type", "checkbox");
//		c.value = true;
//		c.setAttribute("id", "cbManual");
//		pelem = document.createElement("P");
//		tx = document.createTextNode("	Rocno:");
//		tx.className = "Rocno";
//		pelem.appendChild(tx);
//		caption.appendChild(tx);
//		caption.appendChild(c);

		var header = table.createTHead();
		var row = header.insertRow(0);
		/*
        var cell = row.insertCell(0);
        cell.className = "TableHead1";
        cell.innerHTML = "Id";
		 */
		var cell = row.insertCell(0);
		cell.className = "TableHead1";
		cell.innerHTML = "Ime";
		cell = row.insertCell(1);
		cell.innerHTML = "Stanje";
		cell.className = "TableHead1";
	}
	for (i = 0; i < x.length; i++) {
		var row;
		var cell;
		if (!(table.rows[i + 1]))
			row = table.insertRow(i + 1);
		else
			row = table.rows[i + 1];

		xx = x[i].getElementsByTagName("id");
		ACTIVATOR = xx[0].firstChild.nodeValue;
		/*        try {
            if (!(row.cells[0])) {
                cell = row.insertCell(0);
            }
            else
                cell = row.cells[0];
            cell.className = "TableContent1";
            cell.innerHTML = xx[0].firstChild.nodeValue;
        }
        catch (er) {
            cell.innerHTML = "&nbsp;";
        }
		 */
		xx = x[i].getElementsByTagName("name");
		try {
			if (!(row.cells[0])) {
				cell = row.insertCell(0);
			}
			else
				cell = row.cells[0];
			cell.className = "TableContent1";
			cell.innerHTML = xx[0].firstChild.nodeValue;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}

		xx = x[i].getElementsByTagName("state");
		if (!(row.cells[1])) {
			cell = row.insertCell(1);
			cell.onclick = myClickHandler;
			cell.onmouseover = myMouseOver;
			cell.onmouseout = myMouseOut;
		}
		else
			cell = row.cells[1];
		//	        cell.className = "TableContent1";
		try {
			curstates[ACTIVATOR-1] = xx[0].firstChild.nodeValue;
			if(curstates[ACTIVATOR-1] == 2)	//prižiganje
				curstates[ACTIVATOR-1] = 1;
			else if(curstates[ACTIVATOR-1] == 3)	//gašenje
				curstates[ACTIVATOR-1] = 0;

			if (xx[0].firstChild.nodeValue == 1) {
				state = "ON";
				if ((cell.className == "TableContentStateMouseOverON") || (cell.className == "TableContentStateMouseOverOFF"))
					cell.className = "TableContentStateMouseOverON";
				else
					cell.className = "TableContentStateON";
			}
			else if (xx[0].firstChild.nodeValue == 2) {
				state = "Vzig";
				if ((cell.className == "TableContentStateMouseOverON") || (cell.className == "TableContentStateMouseOverOFF"))
					cell.className = "TableContentStateMouseOverON";
				else
					cell.className = "TableContentStateON";
			}
			else if (xx[0].firstChild.nodeValue == 3) {
				state = "Gasenje";
				if ((cell.className == "TableContentStateMouseOverON") || (cell.className == "TableContentStateMouseOverOFF"))
					cell.className = "TableContentStateMouseOverOFF";
				else
					cell.className = "TableContentStateOFF";
			}
			else {
				state = "OFF";
				if ((cell.className == "TableContentStateMouseOverON") || (cell.className == "TableContentStateMouseOverOFF"))
					cell.className = "TableContentStateMouseOverOFF";
				else
					cell.className = "TableContentStateOFF";
			}
			cell.innerHTML = state;
			cell.id = i + 1;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}
	}

	var divelem = document.getElementById("myDivElement");
	if (!document.getElementById("activators"))
		if (table) {
			divelem.appendChild(table);
			divelem.appendChild(document.createElement("BR"));
		}
}

function populateTable1(x) {
	x = x[0].getElementsByTagName("sensor");
	if (x && (x.length > 0) && (!table1)) {
		table1 = document.createElement("table");
		var caption = table1.createCaption();
		table1.className = "Table1";
		caption.className = "TableCaption1";
		table1.id = "sensors";
		caption.innerHTML = "<b>Senzorji</b>";
		var header = table1.createTHead();
		var row = header.insertRow(0);
		var cell = row.insertCell(0);
		caption.onclick = myClickHandler2;
		/*
        cell.className = "TableHead1";
        cell.innerHTML = "Id";
        cell = row.insertCell(1);
		 */
		cell.className = "TableHead1";
		cell.innerHTML = "Ime";


		cell = row.insertCell(1);
		cell.innerHTML = "T";
		cell.className = "TableHead1";
		cell = row.insertCell(2);
		cell.innerHTML = "Izmerjeno";
		cell.className = "TableHead1";
	}
	for (i = 0; i < x.length; i++) {
		var row;
		var cell;
		if (!(table1.rows[i + 1]))
			row = table1.insertRow(i + 1);
		else
			row = table1.rows[i + 1];

		/*
        xx = x[i].getElementsByTagName("id");
        try {
            if (!(row.cells[0])) {
                cell = row.insertCell(0);
            }
            else
                cell = row.cells[0];
            cell.className = "TableContent1";
            cell.innerHTML = xx[0].firstChild.nodeValue;
        }
        catch (er) {
            cell.innerHTML = "&nbsp;";
        }
		 */
		xx = x[i].getElementsByTagName("name");
		try {
			if (!(row.cells[0])) {
				cell = row.insertCell(0);
			}
			else
				cell = row.cells[0];
			cell.className = "TableContent1";
			cell.innerHTML = xx[0].firstChild.nodeValue;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}

		xx = x[i].getElementsByTagName("T");
		try {
			if (!(row.cells[1])) {
				cell = row.insertCell(1);
			}
			else
				cell = row.cells[1];
			cell.className = "TableContent1";
			cell.innerHTML = xx[0].firstChild.nodeValue;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}

		xx = x[i].getElementsByTagName("last_change");
		try {
			if (!(row.cells[2])) {
				cell = row.insertCell(2);
			}
			else
				cell = row.cells[2];
			cell.className = "TableContent1";
			cell.innerHTML = xx[0].firstChild.nodeValue;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}

	}

	var divelem = document.getElementById("myDivElement");
	if (!document.getElementById("sensors"))
		if (table1) {
			document.getElementById("myDivElement").appendChild(table1);
			divelem.appendChild(document.createElement("BR"));
		}
}

function populateTable2(x) {
	var len = 0;
//	var states = Array(N);
//	for(var i=0;i<states.length;i++)
//	states[i] = 2;
	x = x[0].getElementsByTagName("program");

	if(x)
		len = x.length;

//	if (x && (x.length > 0) && (!table2)) {
	if (!table2) {
		table2 = document.createElement("table");
		var caption = table2.createCaption();
		table2.className = "Table1";
		caption.className = "TableCaption1";
		table2.id = "programs";
		caption.innerHTML = "<b>Aktivni programi</b>";
		caption.onclick = myClickHandler3;
		var header = table2.createTHead();

		var row = header.insertRow(0);

		var cell = row.insertCell(0);
		cell.className = "TableHead1";
		cell.innerHTML = "Aktivator";

		cell = row.insertCell(1);
		cell.innerHTML = "Senzor";
		cell.className = "TableHead1";

		cell = row.insertCell(2);
		cell.innerHTML = "TON";
		cell.className = "TableHead1";

		cell = row.insertCell(3);
		cell.innerHTML = "TOFF";
		cell.className = "TableHead1";

		cell = row.insertCell(4);
		cell.innerHTML = "Start";
		cell.className = "TableHead1";

		cell = row.insertCell(5);
		cell.innerHTML = "Stop";
		cell.className = "TableHead1";

		cell = row.insertCell(6);
		cell.innerHTML = "Mesec";
		cell.className = "TableHead1";

		cell = row.insertCell(7);
		cell.innerHTML = "Dan";
		cell.className = "TableHead1";

		cell = row.insertCell(8);
		cell.innerHTML = "Teden";
		cell.className = "TableHead1";

		cell = row.insertCell(9);
		cell.innerHTML = "DanTedna";
		cell.className = "TableHead1";

	}
	else if(table2) if(table2.rows.length >1)
		if(((!x) || (x && (x.length < table2.rows.length-1))) && table2)
		{
			for(var i = table2.rows.length; i > 1;i--)
			{
				table2.deleteRow(i-1);
			}
		}


	for (i = 0; i < len; i++) {
		var row;
		var cell;
		if (!(table2.rows[i + 1]))
			row = table2.insertRow(i + 1);
		else
			row = table2.rows[i + 1];


		xx = x[i].getElementsByTagName("ID");
		ACTIVATOR = parseInt(xx[0].firstChild.nodeValue);
		xx = x[i].getElementsByTagName("ACTIVATOR");
		try {
			if (!(row.cells[0])) {
				cell = row.insertCell(0);
			}
			else
				cell = row.cells[0];
			cell.className = "TableContent1";
			cell.innerHTML = xx[0].firstChild.nodeValue;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}

		xx = x[i].getElementsByTagName("SENSOR");
		try {
			if (!(row.cells[1])) {
				cell = row.insertCell(1);
			}
			else
				cell = row.cells[1];
			cell.className = "TableContent1";
			cell.innerHTML = xx[0].firstChild.nodeValue;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}

		xx = x[i].getElementsByTagName("TON");
		try {
			if (!(row.cells[2])) {
				cell = row.insertCell(2);
			}
			else
				cell = row.cells[2];
			cell.className = "TableContent1";
			cell.innerHTML = xx[0].firstChild.nodeValue;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}

		xx = x[i].getElementsByTagName("TOFF");
		try {
			if (!(row.cells[3])) {
				cell = row.insertCell(3);
			}
			else
				cell = row.cells[3];
			cell.className = "TableContent1";
			cell.innerHTML = xx[0].firstChild.nodeValue;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}

		xx = x[i].getElementsByTagName("START");
		try {
			if (!(row.cells[4])) {
				cell = row.insertCell(4);
			}
			else
				cell = row.cells[4];
			cell.className = "TableContent1";
			cell.innerHTML = xx[0].firstChild.nodeValue;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}

		xx = x[i].getElementsByTagName("STOP");
		try {
			if (!(row.cells[5])) {
				cell = row.insertCell(5);
			}
			else
				cell = row.cells[5];
			cell.className = "TableContent1";
			cell.innerHTML = xx[0].firstChild.nodeValue;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}

		xx = x[i].getElementsByTagName("MESEC");
		try {
			if (!(row.cells[6])) {
				cell = row.insertCell(6);
			}
			else
				cell = row.cells[6];
			cell.className = "TableContent1";
			cell.innerHTML = xx[0].firstChild.nodeValue;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}

		xx = x[i].getElementsByTagName("DAN");
		try {
			if (!(row.cells[7])) {
				cell = row.insertCell(7);
			}
			else
				cell = row.cells[7];
			cell.className = "TableContent1";
			cell.innerHTML = xx[0].firstChild.nodeValue;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}

		xx = x[i].getElementsByTagName("TEDEN");
		try {
			if (!(row.cells[8])) {
				cell = row.insertCell(8);
			}
			else
				cell = row.cells[8];
			cell.className = "TableContent1";
			cell.innerHTML = xx[0].firstChild.nodeValue;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}

		xx = x[i].getElementsByTagName("DANTEDNA");
		try {
			if (!(row.cells[9])) {
				cell = row.insertCell(9);
			}
			else
				cell = row.cells[9];
			cell.className = "TableContent1";
			cell.innerHTML = xx[0].firstChild.nodeValue;
		}
		catch (er) {
			cell.innerHTML = "&nbsp;";
		}

/*		xx = x[i].getElementsByTagName("T");
		var T=null;
		if(xx)
			if(xx[0].firstChild)
				T = parseFloat(xx[0].firstChild.nodeValue);
		xx = x[i].getElementsByTagName("TON");
		if(xx)
			if(xx[0].firstChild)
				TL = parseFloat(xx[0].firstChild.nodeValue);
		xx = x[i].getElementsByTagName("TOFF");
		if(xx)
			if(xx[0].firstChild)
				TOFF = parseFloat(xx[0].firstChild.nodeValue);
		xx = x[i].getElementsByTagName("STATE");
		if(xx[0].firstChild) {
			STATE = parseInt(xx[0].firstChild.nodeValue);
			if(STATE == 2)	//prižiganje
				STATE = 1;
			else if(STATE == 3)	//gašenje
				STATE = 0;
		}
*/
/*		if(T) {
			if(T > TOFF) {
				if(states[ACTIVATOR-1]==2)
					states[ACTIVATOR-1]=0;
			}
			else if(T < TL) {
				states[ACTIVATOR-1]=1;
			}
		}
		else
			states[ACTIVATOR-1]=1;
*/
	}
	
	var divelem = document.getElementById("myDivElement");
	if (!document.getElementById("programs"))
		if (table2) {
			document.getElementById("myDivElement").appendChild(table2);
			divelem.appendChild(document.createElement("BR"));
			/*            var chkIdInput = document.createElement("input");
            chkIdInput.setAttribute("type","button");
            chkIdInput.id = "Add";
            chkIdInput.value = "Button";
            divelem.appendChild(chkIdInput);
			 */
		}
}