
In order to using the application the following steps need to be followed

Create multiple user by `users/create` endpoint, grab users id, they are needed to create conversation group

In order to use the following rest endpoint it is needed to be authenticated

Hit the Authorize button and enter the one of created users password and username and hit the
Authorize button if the credentials that are entered are correct it is logged in correctly.

To create conversation group, put created users id to users list in the request of
`conversationgroup/create` endpoint and fill the other fields, grab the created conversation group 
id from response, it is needed to send a message

