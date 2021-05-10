# Hedwig pushgateway server role

[Hedwig](https://gitlab.com/famedly/services/hedwig) is a
pushgateway for matrix notifications, it implements the
[Matrix Push Notification API r0.1.1](https://matrix.org/docs/spec/push_gateway/r0.1.1)
and only supports [Firebase Cloud Messaging](https://firebase.google.com/docs/cloud-messaging/).

## Usage

You need to configure atleast `hedwig_fcm_admin_key` for the
FCM pushgateway to be able to talk to FCM, and the `hedwig_app_id`
and `hedwig_fcm_notification_click_action` values to the app you're pushing to.

You can override the configuration using `hedwig_extra_config`,
a dict in which you can use the same structure as in the
config file.
