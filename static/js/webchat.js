    $(document).ready(function() {
        var socket = io.connect();
        socket.on('connect', function() {
            socket.emit('connected');
            $('#myName').val('');
            $('#myMessage').val('');
        });

        socket.on('message', function(msg) {
            var name = msg.json_data.name;
            var message = msg.json_data.content;
            var date = msg.json_data.date;
            if (name == '') {
                name = 'Anonymous';
            }
            if (message == '') {
                message = 'I forgot to add a message.';
            }

            $("#messagesContainer").prepend("<div class=\"card mb-2\">\n" +
                "<div class=\"card-header\">\n" +
                "<h5 class=\"card-title\">"+name+"</h5><h6 class=\"card-subtitle mb-2 text-muted\">"+date+"</h6>\n" +
                "</div>\n" +
                "<div class=\"card-body\">\n" +
                ""+message+"\n" +
                "</div>\n" +
                "</div>");
            console.log('Received message');
        });

  //       socket.on('page_view_increase', function(count) {
  //       	console.log('ping');
		// 	var total_count = count.page_views;
		// 	console.log(total_count + ' views');
  //       	$("#pageViews").text(total_count);
		// })
        window.onload =function getUser() {socket.emit('username');
                console.log('waddup boi');  
            };
                socket.on('username', function(usernametosend) {
        console.log('listen');         
         window.uName = usernametosend;
         console.log('uName')
        });
        socket.on('noti', function(json_data_noti) {
            var linkcont = json_data_noti.linkcont;
            var now = json_data_noti.now;
            var nameclass = json_data_noti.nameclass;
            $("#notificationsContainer").prepend("<div class=\"card mb-2\">\n" +
                "<div class=\"card-header\">\n" +
                "<h5 class=\"card-title\">"+nameclass+"</h5><h6 class=\"card-subtitle mb-2 text-muted\">"+now+"</h6>\n" +
                "</div>\n" +
                "<div class=\"card-body\">\n" +
                ""+linkcont+"\n" +
                "</div>\n" +
                "</div>");
            console.log('Received noti');
        });
        $('#sendButton').on('click', function() {
            var message = $('#myMessage').val();
            console.log('Clicked!');
            console.log(uName);
            socket.send({name : uName, message : message});
            return $('#myMessage').val('');
            // $("#toggleFieldset").children().attr("disabled", "disabled");
            // $('#myMessage').attr('disabled', 'disabled');
            // $('#myName').attr('disabled', 'disabled');
        });
    });