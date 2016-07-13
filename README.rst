=====
Adarnauth-WHSales
=====

Adarnauth-WHSales is a simple Django project to list wormhole
systems for sale. It was built as a tech demo for the apps
being built for Adarnauth.

Quick start
-----------

1. Create a virtualenv for running the project::

    virtualenv whsales/env

2. Activate the virtualenv::

    source whsales/env/bin/activate

3. Install requirements::

    pip install -r requirements.txt

4. Register an application with the EVE Developers site at
   https://developers.eveonline.com/applications
  - Select "CREST Access" and select "characterLocationRead"
  - Set the "Callback URL" to "https://yourdomain.com/eve_sso/callback"

5. Add SSO client settings to whsales/settings.py like this::

    EVE_SSO_CLIENT_ID = "my client id"
    EVE_SSO_CLIENT_SECRET = "my client secret"
    EVE_SSO_CALLBACK_URL = "my client callback url"

6. Run `python manage.py migrate` to create the populate tables.

7. Create a superuser account::

    python manage.py createsuperuser

8. Start the server and navigate to your site::

    python manage.py runserver 0.0.0.0:8000
