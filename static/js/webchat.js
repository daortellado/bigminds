    $(document).ready(function() {
        var socket = io.connect();
        socket.on('connect', function() {
            socket.emit('connected');
            $('#myName').val('');
            $('#myMessage').val('');
            $('#mychanMessage').val('');
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
                socket.on('channel', function(json_chan) {
            var name = json_chan.name;
            var message = json_chan.content;
            var date = json_chan.date;
            if (name == '') {
                name = 'Anonymous';
            }
            if (message == '') {
                message = 'I forgot to add a message.';
            }

            $("#channelContainer").prepend("<div class=\"card mb-2\">\n" +
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
        socket.on('apptnoti', function(json_data_apptnoti) {
            var apptlinkcont = json_data_apptnoti.linkcont;
            var apptnow = json_data_apptnoti.now;
            var apptteacher = json_data_apptnoti.teacher;
            $("#apptnotificationsContainer").prepend("<div class=\"card mb-2\">\n" +
                "<div class=\"card-header\">\n" +
                "<h5 class=\"card-title\">Appointment with "+apptteacher+"</h5><h6 class=\"card-subtitle mb-2 text-muted\">"+apptnow+"</h6>\n" +
                "</div>\n" +
                "<div class=\"card-body\">\n" +
                ""+apptlinkcont+"\n" +
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
        $('#calendly-button').on('click', function() {
            document.getElementById("calendlyContainer").className = "";
            document.getElementById("formContainer").className = "d-none";
        });
        $('#form-button').on('click', function() {
            document.getElementById("calendlyContainer").className = "d-none";
            document.getElementById("formContainer").className = "";
        });
        $('#sendchanButton').on('click', function() {
            var message = $('#mychanMessage').val();
            console.log('Clicked!');
            console.log(uName)
            var chn = {name : uName, message : message}
            socket.emit('channel', chn);
            return $('#mychanMessage').val('');
            // $("#toggleFieldset").children().attr("disabled", "disabled");
            // $('#myMessage').attr('disabled', 'disabled');
            // $('#myName').attr('disabled', 'disabled');
        });
        $('#switchButton').on('click', function() {
            console.log('clicked');
            document.getElementById("messagesContainer").className = "d-none container mt-5";
            document.getElementById("channelContainer").className = "container mt-5";
            document.getElementById("submitForm").className = "d-none container mt-5";
            document.getElementById("submitchanForm").className = "container mt-5";
        });
        $('#switchbackButton').on('click', function() {
            console.log('clickedback');
            document.getElementById("messagesContainer").className = "container mt-5";
            document.getElementById("channelContainer").className = "d-none container mt-5";
            document.getElementById("submitForm").className = "container mt-5";
            document.getElementById("submitchanForm").className = "d-none container mt-5";
        });
    });