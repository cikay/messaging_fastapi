
HTML_AS_STRING = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <button id="connect">Connect</button>
        <br /><br /><br /><br />
        <h2>Conversation group id</h2>
        <input type="text" id="conversationgroup" autocomplete="off"/>
        <br /><br /><br /><br />
        <form action="" onsubmit="sendMessage(event)">
            <h2>Text message</h2>
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            let WEBSOCKET
            let connect_btn = document.getElementById("connect")

            connect_btn.addEventListener('click', (e) => {
                e.preventDefault()
                const conversationgroup = document.getElementById("conversationgroup")
                const conversationgroup_id = conversationgroup.value
                WEBSOCKET = new WebSocket(
                    `ws://localhost:8000/ws/${conversationgroup_id}`
                );
                console.log("websocket", WEBSOCKET)
                conversationgroup.addEventListener('change', (e) => {
                    conversationgroup_id = e.target.value
                })
                WEBSOCKET.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
            })
            const isOpen = (ws) => ws.readyState === ws.OPEN
            function sendMessage(event) {
                event.preventDefault()
                if (!isOpen(WEBSOCKET)){
                    console.log("Not open")
                    return
                }
                var input = document.getElementById("messageText")
                WEBSOCKET.send(input.value)
                input.value = ''
            }
        
        </script>
    </body>
</html>
"""