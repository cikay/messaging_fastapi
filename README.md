
In order to using the application the following steps need to be followed

Create multiple user by `users/create` endpoint, grab users id, they are needed to create conversation group

In order to use the following rest endpoint it is needed to be authenticated

Hit the Authorize button and enter the one of created users password and username and hit the
Authorize button if the credentials that are entered are correct it is logged in correctly.

To create conversation group, put created users id to users list in the request of
`conversationgroup/create` endpoint and fill the other fields, grab the created conversation group 
id from response, it is needed to send a message

In order to send a message, enter one of the users id that added to the created conversation group 
and set sender id and set created conversation group id to conversation group id field in the request
of `conversationgroups/message/create`

To see if a user that are not included to a conversation group is allowed to send
message or not, create a new user and pass the newly created user id to request of 
message without changing conversation group id and try to send. The following error 
will be occurred 

```json
{
  "detail": "User must be member of group"
}
```
