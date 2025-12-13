Classes
-------
Chat 3 6 -> Message  
GroupChat 4 10 -> Message  
Message 6 2 ->  
PrivateChat 5 4 -> Message  
Channel 9 13 -> Feed Post ChannelProfile  
ChannelProfile 13 4 ->  
Group 9 15 -> GroupProfile Feed Post  
GroupProfile 15 6 ->  
PrivateChannel 9 13 -> Feed Post ChannelProfile  
PrivateChannelProfile 13 4 ->  
Comment 9 8 -> Like  
ContentItem 3 2 ->  
Feed 2 10 -> Post ContentItem  
Hashtag 2 6 ->  
Like 5 5 ->  
MusicTrack 8 8 ->  
Post 8 7 -> Comment Like MediaFile Hashtag  
PrivateStory 6 8 -> Feed  
Reels 8 11 -> Feed MusicTrack  
Story 6 8 -> Feed  
Database 1 6 ->  
FriendDatabase 1 7 -> Friend  
MusicDatabase 1 11 -> MusicTrack  
PostDatabase 1 7 -> Post  
ReelsDatabase 1 10 -> Reels  
StoryDatabase 1 9 -> Story  
SubscriptionDatabase 1 9 -> Subscription  
UserDatabase 1 11 -> User  
MediaFile 8 8 ->  
MusicRecommendation 3 5 -> MusicTrack MusicDatabase  
PostRecommendations 3 5 -> Post PostDatabase  
ReelsRecommendation 3 5 -> Reels ReelsDatabase  
StoryRecommendations 3 5 -> Story StoryDatabase  
FriendSearch 1 2 -> FriendDatabase  
MusicSearch 1 2 -> MusicDatabase  
PostSearch 1 2 -> PostDatabase  
ReelsSearch 1 2 -> ReelsDatabase
Search 0 3 ->  
SearchQuery 7 4 -> Search  
StorySearch 1 2 -> StoryDatabase  
SubscriptionSearch 1 2 -> SubscriptionDatabase  
UserSearch 1 2 -> UserDatabase  
AuthenticationManager 1 7 -> UserDatabase User Session TwoFactorAuth  
PasswordHasher 0 2 ->  
TwoFactorAuth 1 3 ->  
Session 6 0 ->  
Friend 2 5 ->  
Subscription 4 3 ->  
Profile 9 7 ->  
User 15 10 -> PasswordHasher UserProfile Post Subscription Session  
UserProfile 9 6 -> Feed  

Exceptions (12)
---------------
AccountBannedException
EmptySearchQueryError
EmptyUsernameError
EntityAlreadyExistsException
InsufficientPermissionsException
InvalidCredentialsException
NegativeIDError
PasswordTooWeakException
SearchQueryException
TwoFactorRequiredException
UserAlreadyExistsException
UserNotFoundException

Summary
-------
Classes: 51  
Fields: 232  
Behaviors: 312  
Associations: 56  
Exceptions: 12
