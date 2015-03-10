// JScript File

// Base functionality class;

var ITBase =
{
    // Just simplify returning of DHTML element.
    // @element - id of element to return.
    $: function (element)
    {
        return document.getElementById(element);
    },

    // Attaching to event.
    // @eventName - name of event.
    // @listener - method, that will be called to proccess event.
    // @target - element, on which event will be fired.
    AddEvent: function (eventName, listener, target)
    {
        if (!target) { target = window; }
        eventName == "unload" ? "beforeunload" : eventName;

        if (target.addEventListener)
        {
            target.addEventListener(eventName, listener, false);
        }
        else if (target.attachEvent)
        {
            if (target == window && !(eventName == "unload" || eventName == "load" || eventName == "beforeunload"))
            {
                target = window.document;
            }
            target.attachEvent("on" + eventName, listener);
        }
    },

    Pointer: function (event)
    {
        return { x: ITBase.PointerX(event), y: ITBase.PointerY(event) };
    },

    PointerX: function (event)
    {
        return event.pageX || (event.clientX + (document.documentElement.scrollLeft || document.body.scrollLeft));
    },

    PointerY: function (event)
    {
        return event.pageY || (event.clientY + (document.documentElement.scrollTop || document.body.scrollTop));
    },

    DocumentSize: function ()
    {
        return { width: this.DocumentWidth(), height: this.DocumentHeight() };
    },

    DocumentWidth: function ()
    {
        return this.isOpera ? 0 : parseInt(document.body.scrollWidth < 400 ? 400 : document.body.scrollWidth);
    },

    DocumentHeight: function ()
    {
        return this.isOpera ? 0 : parseInt(document.body.scrollHeight < 300 ? 300 : document.body.scrollHeight);
    },

    GetUrl: function ()
    {
        //return escape(window.location.hostname + window.location.pathname + window.location.search);
        return escape(window.location.href);
    },

    GetResolution: function ()
    {
        if (screen) { return "" + screen.width + "&" + screen.height; }
        else { return "0&0"; }
    },

    GetElementName: function (event)
    {
        source = event.srcElement || event.target;
        return findElementAnchor(source).tagName;
    },

    GetElementClickedUrl: function (event)
    {
        source = event.srcElement || event.target;
        source = findElementAnchor(source);

        if (source.tagName == "A")
        {
            return escape(source.href);
        }
        else
        {
            return "%20";
        }
    }

}

ITBase.isDOM = document.getElementById ? true : false; //DOM1 browser (MSIE 5+, Netscape 6, Opera 5+)
ITBase.isOpera = ITBase.isOpera5 = (window.opera && ITBase.isDOM) ? true : false; //Opera 5+
ITBase.isOpera6 = (ITBase.isOpera && window.print) ? true : false; //Opera 6+
ITBase.isOpera7 = (ITBase.isOpera && document.readyState) ? true : false; //Opera 7+
ITBase.isMSIE = (document.all && document.all.item && !ITBase.isOpera) ? true : false; //Microsoft Internet Explorer 4+
ITBase.isMSIE5 = (ITBase.isDOM && ITBase.isMSIE) ? true : false; //MSIE 5+
ITBase.isNetscape4 = document.layers ? true : false; //Netscape 4.*
ITBase.isMozilla = (ITBase.isDOM && navigator.appName=="Netscape") ? true : false; //Mozilla или Netscape 6.*	


// Collector class;
function Collector(){}

Collector.Init          = CC_Init;
Collector.ProccessClick = CC_ProccessClick;
Collector.LoadedAt      = (new Date()).getTime();
Collector.Data = 
    {
        clickX: 0,
        clickY: 0,
        percentX: 0,
        deltaTime: 0,
        counter: 0,
        url: "",
        elementName: "",
        resolution: 0,
        documentWidth: 0,
        documentHeight: 0,
        clientId: 0,
        clickedUrl: ""
    }

function CC_ProccessClick(e)
{
    ev = e ? e : window.event;
    
    try
    {    
		Collector.Data.counter++;
		Collector.Data.clickX = ITBase.Pointer(ev).x;
		Collector.Data.clickY = ITBase.Pointer(ev).y;
		Collector.Data.deltaTime = ((new Date()).getTime() - Collector.LoadedAt) / 1000;
		Collector.Data.url = ITBase.GetUrl();
		Collector.Data.resolution = ITBase.GetResolution();
		Collector.Data.documentWidth = ITBase.DocumentSize().width;
		Collector.Data.documentHeight = ITBase.DocumentSize().height;
		Collector.Data.elementName = ITBase.GetElementName(ev);	
		Collector.Data.clickedUrl = ITBase.GetElementClickedUrl(ev);
		
		// vs: check the correct itrMId value
		if (itrMId && parseInt(itrMId)>0)
		{  
		    Collector.Data.clientId = itrMId ? parseInt(itrMId) : 0;
		}
		else
		{
		    return;
		}
		
		if (Collector.Data.documentWidth != 0 && Collector.Data.documentHeight != 0)
		{
			Collector.Data.clickX = Collector.Data.clickX < Collector.Data.documentWidth ? Collector.Data.clickX : Collector.Data.documentWidth - 10;
			Collector.Data.clickY = Collector.Data.clickY < Collector.Data.documentHeight ? Collector.Data.clickY : Collector.Data.documentHeight - 10;
		}
		Collector.Data.clickX = Collector.Data.clickX < 0 ? 1 : Collector.Data.clickX;
		Collector.Data.clickY = Collector.Data.clickY < 0 ? 1 : Collector.Data.clickY;
	     
		if ( (Collector.Data.clickX != (Collector.Data.documentWidth - 10))) // TODO!
		{
			XmlHttp.Send();       
			//alert ("ok");
			//alert (Collector.Data.clickX + " : " + Collector.Data.documentWidth);
		}
	}
	catch(e){}
}

function CC_Init()
{
	try
	{
		Collector.Data.deltaTime = (new Date()).getTime();
	    
		ITBase.AddEvent("mousedown", Collector.ProccessClick, document)    
	    
		CreateTransportBox();
    }
    catch(e){}
}

function findElementAnchor(element)
{
    var parent = element.parentNode;	
	
	while (parent.tagName != 'A')
	{
	    parent = parent.parentNode;
	    if (parent == null)
	    {
	        return element;
	    }
	}	
	return parent;
}


// * XMLHTTP OBJECT *//

var XmlHttp = function(){}

XmlHttp.htmlhttp = null;
XmlHttp.Send = XH_Send;
XmlHttp.FormatPostString = XH_FormatPostString;
//XmlHttp.RequestHost = "http://kvc13/IntelClick/Default.aspx?";
XmlHttp.RequestHost = window.location.protocol + "//" + itrRqstH + "/e/clk.dll?";
XmlHttp.RequestUrl = null;


function XH_Send()
{
	try
	{
		transportBox.src = XmlHttp.FormatPostString();
		transportBox.onload = function() { return; }
	}
	catch(e){}
}

function XH_FormatPostString()
{
 
       fstr   = "" + Collector.Data.clientId;     
       fstr   += "&" + Collector.Data.clickX;
       fstr   += "&" + Collector.Data.clickY;
       fstr   += "&" + Collector.Data.url;
       fstr   += "&" + Collector.Data.resolution;
       fstr   += "&" + Collector.Data.documentWidth;
       fstr   += "&" + Collector.Data.documentHeight;
       fstr   += "&" + Collector.Data.elementName;    
       fstr   += "&" + Collector.Data.clickedUrl;
//     fstr   += "&=" + Collector.Data.deltaTime;
//     fstr   += "&" + Collector.Data.counter;
     
       return XmlHttp.RequestHost + fstr;
}

var transportBox;
function CreateTransportBox()
{
	try
	{
		transportBox = new Image(1,1);
	}catch(e){}
}
Collector.Init();