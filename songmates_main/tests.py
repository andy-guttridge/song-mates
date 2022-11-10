from django.test import TestCase
from django.contrib.auth.models import User
from .models import Profile, CollabRequest, Message
from .views import (ProfileAccount, UpdateProfile, UserDelete, RequestCollab,
                    CollabRequests, DeleteCollab, SendMsg, DeleteMsg)
from .forms import ProfileForm


class TestViewModelInteraction(TestCase):
    """
    Test suite to test key interactions between views and models
    """
    def setUp(self):
        """
        Create two test users who are logged in for unit tests
        """
        self.user = User.objects.create_user(username='testuser',
                                             password='test')
        login = self.client.login(username='testuser', password='test')
        self.user_2 = User.objects.create_user(username='testuser_2',
                                               password='test')

    def tearDown(self):
        """
        Make sure any profiles, collab requests and messages created by tests
        are deleted
        """
        Profile.objects.all().delete()
        CollabRequest.objects.all().delete()
        Message.objects.all().delete()

    def test_profile_creation(self):
        """
        Test new profile is created when account is registered
        """
        response = self.client.get('/edit-profile/')
        self.assertTrue(Profile.objects.filter(user=self.user).exists())
        profile = Profile.objects.get(user=self.user)
        self.assertEquals(self.user.pk, profile.user.pk)

    def test_profile_deletion(self):
        """
        Test profile is deleted when requested
        """
        # Create a profile for the user and check it exists
        profile = Profile.objects.create(user=self.user)
        self.assertTrue(Profile.objects.filter(user=self.user).exists())

        # Call the user-delete post method and check if profile no longer
        # exists
        response = self.client.post('/user-delete/')
        self.assertFalse(Profile.objects.filter(user=self.user).exists())

    def test_user_becomes_inactive(self):
        """
        Test user is made inactive when profile deleted
        """
        # Technique to ensure the latest state of the user is loaded from the
        # database:
        # https://stackoverflow.com/questions/64741329/why-is-my-test-function-not-activating-the-user
        self.user.refresh_from_db()

        # Check user is currently set to active
        self.assertTrue(self.user.is_active)

        # Request user-delete and check if user is now set to not active
        response = self.client.post('/user-delete/')
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_collab_request_is_created(self):
        """
        Create collaboration request is added correctly
        """
        # Call view to create new collab request to user_2
        response = self.client.post(f'/request-collab/{self.user_2.pk}')

        # Test the collab request exists and that it was sent to user_2
        self.assertTrue(CollabRequest.objects.filter(from_user=self.user)
                        .exists())
        self.assertEquals(CollabRequest.objects.filter(from_user=self.user).
                          first().to_user.pk, self.user_2.pk)

    def test_collab_request_approval(self):
        """
        Test collaboration request is added to correct profiles and deleted
        when approved
        """
        # Create profiles for the two test users
        user_profile = Profile.objects.create(user=self.user)
        user2_profile = Profile.objects.create(user=self.user_2)

        # Create collab request
        collab_request = CollabRequest.objects.create(from_user=self.user,
                                                      to_user=self.user_2)
        # Log user, login user_2 so they can approve the request
        logout = self.client.logout()
        login = self.client.login(username='testuser_2', password='test')

        # Check the collab request currently exists
        self.assertTrue(
            CollabRequest.objects.filter(from_user=self.user).exists()
            )

        # Call view for user_2 to approve the collab request
        response = self.client.post(f'/collab-requests/{self.user.pk}',
                                    {'collab-approve': 'True'})

        # Check the collab request has been deleted
        self.assertFalse(
            CollabRequest.objects.filter(from_user=self.user).exists()
            )

        # Check that user and user 2 are now 'friends'
        user_profile.refresh_from_db()
        self.assertTrue(user_profile.friends.filter(user=self.user_2).exists())

    def test_collab_request_rejection(self):
        """
        Test if collab request is deleted and not added
        to profiles when collab request is rejected
        """
        # Create profiles for the two test users
        user_profile = Profile.objects.create(user=self.user)
        user2_profile = Profile.objects.create(user=self.user_2)

        # Create collab request
        collab_request = CollabRequest.objects.create(from_user=self.user,
                                                      to_user=self.user_2)

        # Log user, login user_2 so they can reject the request
        logout = self.client.logout()
        login = self.client.login(username='testuser_2', password='test')

        # Call view for user_2 to reject the collab request
        response = self.client.post(f'/collab-requests/{self.user.pk}',
                                    {'collab-reject': 'True'})

        # Check the collab request has been deleted
        self.assertFalse(
            CollabRequest.objects.filter(from_user=self.user).exists()
            )

        # Check that user and user 2 are not now 'friends'
        user_profile.refresh_from_db()
        self.assertFalse(
            user_profile.friends.filter(user=self.user_2).exists()
            )

    def test_uncollab(self):
        """
        Test if request to end a collaboration correctly removes
        relationship between users
        """
        # Create profiles for the two test users
        user_profile = Profile.objects.create(user=self.user)
        user2_profile = Profile.objects.create(user=self.user_2)

        # Create relationship between the two users and check it exists
        user_profile.friends.add(user2_profile)
        user_profile.save()
        self.assertTrue(
            user_profile.friends.filter(user=self.user_2).exists()
            )

        # Call the view to request the deletion of the collaboration
        # relationship and check the relationship has been deleted
        response = self.client.post(f'/delete-collab/{self.user_2.pk}')
        self.assertFalse(
            user_profile.friends.filter(user=self.user_2).exists()
            )

    def test_message_send(self):
        """
        Test if message is sent correctly
        """
        # Create profiles for the two test users
        user_profile = Profile.objects.create(user=self.user)
        user2_profile = Profile.objects.create(user=self.user_2)

        # Create relationship between the two users and check it exists
        user_profile.friends.add(user2_profile)
        user_profile.save()
        self.assertTrue(
            user_profile.friends.filter(user=self.user_2).exists()
            )

        # Call view to send a message from user to user_2
        response = self.client.post(
                                        f'/send-msg/{self.user_2.pk}',
                                        {
                                            'msg-subject': 'This is a test',
                                            'msg-body': 'Hello, this is a test'
                                        }
                                    )

        # Test if message was created with correct values
        self.assertTrue(Message.objects.filter(
            from_user=self.user,
            to_user=self.user_2,
            subject='This is a test',
            message='Hello, this is a test'
        ).exists())

    def test_message_deletion(self):
        """
        Test if message is correctly deleted only when both users have
        requested deletion
        """
        # Create profiles for the two test users
        user_profile = Profile.objects.create(user=self.user)
        user2_profile = Profile.objects.create(user=self.user_2)

        # Create relationship between the two users and check it exists
        user_profile.friends.add(user2_profile)
        user_profile.save()
        self.assertTrue(
            user_profile.friends.filter(user=self.user_2).exists()
            )

        # Create a message between the two users
        message = Message.objects.create(
            pk=1,
            from_user=self.user,
            to_user=self.user_2,
            subject='Test',
            message='This is a test',
            from_deleted=False,
            to_deleted=False
        )

        # Call the view to request the message is deleted by the first user
        response = self.client.post(
                f'/delete-msg/{message.pk}',
                {
                    'confirm-msg-out-delete': 'True'
                }
            )

        # Test the message still exits
        self.assertTrue(
            Message.objects.filter(pk=message.pk).exists()
        )

        # Test the message is marked as deleted by first user
        self.assertTrue(
            Message.objects.filter(pk=message.pk).first().from_deleted is True
        )

        # Logout first user, login second user and request the message is
        # deleted
        logout = self.client.logout()
        login = self.client.login(username='testuser_2',
                                  password='test')
        response = self.client.post(
                f'/delete-msg/{message.pk}',
                {
                    'confirm-msg-in-delete': 'True'
                }
            )

        # Test the message has now been deleted
        self.assertFalse(
            Message.objects.filter(pk=message.pk).exists()
        )
