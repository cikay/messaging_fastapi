
In order to using the application the following steps need to be followed

Create multiple user by `users/create` endpoint, grab users id, they are needed to create conversation group

In order to use the following rest endpoint it is needed to be authenticated

Hit the Authorize button and enter the one of created users password and username and hit the
Authorize button if the credentials that are entered are correct it is logged in correctly.

To create conversation group, put created users id to users list in the request of
`conversationgroup/create` endpoint and fill the other fields, grab the created conversation group 
id from response, it is needed to send a message

Websocket added but it is not related with the above endpoints. There is no authentication feature
in to send a message by websocket endpoint.

In order to use sending message go to `/` endpoint and enter the conversation group id and hit the
connect button to have a connection

Then fill the text input and hit the send button. To see whether the message is sent to all clients
open the same endpoint in a different browser and send another message. The conversation group id should
the same to see the message that are sent by the other clients

