var local_strings = {};
var commitment_type_selections = [];
var commitment_status_selections = [];
var complaint_reason_selections = [];

var commitment_grid;
var commitment_grid;
var complaint_grid;

var last_sent;

// Messages parser
function parse_data(data) {
    console.log(data)
    switch (data.signal) {
        case "ping":
            console.log("pong");
            send_pong();
            break;
        case "message":
            console.log(data.text);
            break;
        case "bye":
            console.log("Connection close as requested by server");
            webSocket.close();
            break;
        case "drawnewinterface":
            if (data.type_parent == "TagName") {
                document.getElementsByTagName(data.parent_name)[0].innerHTML = data.interface;
            } else if (data.type_parent == "Id") {
                document.getElementById(data.parent_name).innerHTML = data.interface;
            };
            break;
        case "openinterface":
            OpenInterface(data.interface, data.data)
            break;
        case "setvariable":
            window[data.variable] = data.json
            break;
        case "setdivvisible":
            set_div_visible(data.div_id)
            break;
        case "setdataset":
            console.log(data)
            window[data.interface].setData(data.data, false)
            window[data.interface].invalidateAllRows();
            window[data.interface].render();
            break;
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
    final = JSON.stringify(result)
    console.log(final)
    return final
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

function send_action_interface(action, interface, variables={}) {
    var final_vars;
    for (name in variables) {
        final_vars = final_vars+"|"+variables[name];
    };
    to_send = signal(
        "actioninterface", {
            "please_do": action,
            "interface": interface,
            "variables": variables
            }
        );
    console.log(to_send)
    webSocket.send(to_send);
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

function DateEditor(args) {
    var $date;
    var scope = this;
    this.init = function () {
      $date = $("<INPUT type='date'/>")
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
      $date.focus();
    };
    this.serializeValue = function () {
      return {date: $date.val()};
    };
    this.applyValue = function (item, state) {
      item.date = state.date;
      item[args.column.field] = state.date;
    };
    this.loadValue = function (item) {
      $date.val(item.date);
    };
    this.isValueChanged = function () {
      return args.item.date != $date.val();
    };
    this.validate = function () {
      return {valid: true, msg: null};
    };
    this.init();
  }

function DateFormatter(row, cell, value, columnDef, dataContext) {
    return new Date(value).toLocaleDateString();
}


function HourEditor(args) {
    var $hour;
    var scope = this;
    this.init = function () {
      //$hour = $("<INPUT type='text' onkeyup='hour_mask(this)' maxlength='5' placeholder='hh:mm' />")
      $hour = $("<INPUT type='time'/>")
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
      item[args.column.field] = state.hour;
      console.log(state.hour)
      console.log(args.column.field)
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
    return local_strings[value];
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
              "<OPTION value='"+item+"'>"+local_strings[item]+"</OPTION>"
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

function Locate(field) {
    data = local_strings[field];
    if (data == undefined) {
        return field;
    } else {
        return data;
    }
}

//Grids
var isAsc = true;

var grid_options = {
    editable: true,
    enableCellNavigation: true,
    enableColumnReorder: true,
    enableAddRow: true,
    asyncEditorLoading: false,
    autoEdit: true,
    rowHeight: 30
    };

function initiate_grid(name, columns, data) {
    window[name] = new Slick.Grid("#"+name, data, columns, grid_options);
    window[name].onAddNewRow.subscribe(function (e, args) {
        var item = args.item;
        window[name].invalidateRow(data.length);
        data.push(item);
        window[name].updateRowCount();
        window[name].render();
    });
    window[name].onSort.subscribe(function (e, args) {
        var sorting;
        switch (args.sortAsc) {
            case false:
                sorting = "Desc";
                break;
            default:
                sorting = "Asc";
                break;
        };
        send_action_interface("sort_grid", name, {"field":args.sortCol.field, "sorting": sorting})
    });
};

//Interfaces

function set_div_visible(div_id) {
     document.getElementById("main").style.display="none";
     document.getElementById("commitments_grid").style.display="none";
     document.getElementById("complaints_grid").style.display="none";
     document.getElementById(div_id).style.display="block";

};

function OpenInterface(interface, data) {
    switch (interface) {
        case "commitments_grid":
            initiate_grid(interface, commitments_columns(Locate), data);
            break;
        case "complaints_grid":
            initiate_grid(interface, complaints_columns(Locate), data);
            break;
    };
    set_div_visible(interface);
};

function clean() {
    grid = "";
    document.getElementById('main').InnerHTML = "";
};