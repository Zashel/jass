var locale = {}

// Messages parser
function parse_data(data) {
    console.log(data)
    if (data.signal === "ping") {
        console.log("pong");
        send_pong();
    } else if (data.signal === "message") {
        console.log(data.text);
    } else if (data.signal === "bye") {
        console.log("Connection close as requested by server");
        webSocket.close();
    } else if (data.signal == "drawnewinterface") {
        if (data.type_parent == "TagName") {
            document.getElementsByTagName(data.parent_name)[0].innerHTML = data.interface;
        } else if (data.type_parent == "Id") {
            document.getElementById(data.parent_name).innerHTML = data.interface;
        };
    } else if (data.signal == "locale") {
        console.log("locale recibido");
        locale = data.locale;
    } else if (data.signal == "openinterface") {
        OpenInterface(data.interface, data.data)
    };
};

// Initialize WebSocket
function initWebSocket(direction, port, secure_connection, protocols=[], parser=parse_data) {
    // Getting the connection String for WebSocket
    connString = "://"+direction+":"+port;
    if (secure_connection === true) {
        connString = "wss"+connString
    }
    else {
        connString = "ws"+connString
    };

    // Test compatibility
    if ("WebSocket" in window) {
        // Set the WebSocket
        webSocket = new WebSocket(connString);  // No Protocols by now. TODO

        // Set the main handlers
        webSocket.onopen = function() {
            console.log("Connected")
            send_hi()
        };
        webSocket.onmessage = function(event) {
            var received = JSON.parse(event.data);
            parser(received)
        };
        webSocket.onclose = function() {
            send_bye()
        };
    }
    else {
        alert("Browser Not Supported");
    };
};

function get_now() {
    var now = new Date()
    var nowStr = now.getFullYear()+"-"+
             now.getMonth()+"-"+
             now.getDate()+" "+
             now.getHours()+":"+
             now.getMinutes()+":"+
             now.getSeconds();
    return nowStr
};

function signal(signal, datos={}) {
    result = {
            "signal": signal,
            "date": get_now()
    }
    for (dato in datos) {
        result[dato] = datos[dato]
    }
    return JSON.stringify(result)
};

function send_pong() {
    webSocket.send(signal("pong"));
};

function send_bye() {
    webSocket.send(signal("bye"));
};

function send_message(to, text) {
    webSocket.send(signal(
        "message", {
            "to": to,
            "text": text
        }
        ));
};

function send_open_interface(interface) {
    webSocket.send(signal(
        "openinterface", {
            "interface": interface,
            "data": []
            }
        ));
};

function send_hi() {
    webSocket.send(signal("hi"))
};


//Hour Mask
function hour_mask(field) {
    var hour = field.value;
          if (hour.match(/^\d{2}$/) !== null) {
                field.value = hour + ':';
          };
    }

//Editors:

function HourEditor(args) {
    var $hour;
    var scope = this;
    this.init = function () {
      $hour = $("<INPUT type='text' onkeyup='hour_mask(this)' maxlength='5' placeholder='hh:mm' />")
          .appendTo(args.container)
          .bind("keydown", scope.handleKeyDown);
      scope.focus();
    };
    this.handleKeyDown = function (e) {
      if (e.keyCode == $.ui.keyCode.LEFT || e.keyCode == $.ui.keyCode.RIGHT || e.keyCode == $.ui.keyCode.TAB) {
        e.stopImmediatePropagation();
      }
    };
    this.destroy = function () {
      $(args.container).empty();
    };
    this.focus = function () {
      $hour.focus();
    };
    this.serializeValue = function () {
      return {hour: $hour.val()};
    };
    this.applyValue = function (item, state) {
      item.hour = state.hour;
    };
    this.loadValue = function (item) {
      $hour.val(item.hour);
    };
    this.isValueChanged = function () {
      return args.item.hour != $hour.val();
    };
    this.validate = function () {
      return {valid: true, msg: null};
    };
    this.init();
  }

function SelectorFormatter(row, cell, value, columnDef, dataContext) {
    return locale[value];
}

function SelectorEditor(items) {
    function Editor(args) {
        var $selection;
        var scope = this;
        this.init = function () {
          $(args.container).empty();
          var select = "<SELECT>"
          for (var item in items) {
            item = items[item]
            select = select.concat(
              "<OPTION value='"+item+"'>"+locale[item]+"</OPTION>"
            )
          };
          select = select.concat("</SELECT>")
          $selection = $(select)
              .appendTo(args.container)
              .bind("keydown", scope.handleKeyDown);
          scope.focus();
        };
        this.handleKeyDown = function (e) {
          if (e.keyCode == $.ui.keyCode.LEFT || e.keyCode == $.ui.keyCode.RIGHT || e.keyCode == $.ui.keyCode.TAB) {
            e.stopImmediatePropagation();
          }
        };
        this.destroy = function () {
          $(args.container).empty();
        };
        this.focus = function () {
          $selection.focus();
        };
        this.serializeValue = function () {
          return {selection: $selection.val()};
        };
        this.applyValue = function (item, state) {
          item.selection = state.selection;
          item[args.column.field] = state.selection;
        };
        this.loadValue = function (item) {
          $selection.val(item.selection);
        };
        this.isValueChanged = function () {
          return args.item.selection != $selection.val();
        };
        this.validate = function () {
          return {valid: true, msg: null};
        };
        this.init();
    }
    return Editor
}

//Selectors:

var commitment_type_selections = ["tc", "tr"]

function Locate(field) {
    data = locale[field];
    if (data == undefined) {
        return field;
    } else {
        return data;
    }
}

//Grids
var grid_options = {
    editable: true,
    enableCellNavigation: true,
    enableColumnReorder: true,
    enableAddRow: true,
    asyncEditorLoading: false,
    autoEdit: true,
    rowHeight: 30
    };

function initiate_grid(columns, data) {
    grid = new Slick.Grid("#main", data, columns, grid_options);
    }

//Interfaces

function OpenInterface(interface, data) {
    if (interface == "commitments_grid") {
        document.getElementById("main").InnerHTML = "";
        initiate_grid(commitments_columns(Locate), data);
    }
}

function clean() {
    document.getElementById('main').InnerHTML = "";
}